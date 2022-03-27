from time import sleep
from seleniumwire import webdriver


def update_links(panopto_folders):
    if not panopto_folders:
        return None
    query = "&maxResults=250"
    res = {}
    for key, value in panopto_folders.items():
        res[key] = value + query
    return res


class Driver:
    def __init__(self, panopto_folders=None, moodle_links=None) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.driver = webdriver.Chrome(options=self.options)
        self.panopto_folders = update_links(panopto_folders)
        self.moodle_links = moodle_links

    def get_m3u8_url(self):
        res = []
        sleep(0.5)
        multi_camera = self.driver.execute_script("""try {
  document.querySelector("[aria-pressed=false]").click();
} catch (error) {return false} return true;""")

        if multi_camera:
            sleep(0.1)
            for request in self.driver.requests:
                if "m3u8" in request.url and "index" not in request.url:
                    res.append(request.url)
            print(f"L={len(res)} {res}\n-----------------------------------------")
            del self.driver.requests
            return res
        del self.driver.requests
        return self.driver.execute_script("""const getArray = () => {
  let performance =
    window.performance ||
    window.msPerformance ||
    window.webkitPerformance ||
    {};
  let network = performance.getEntries() || {};

  let names = network.map((n) => n.name);
  return names.filter((n) => n.includes(".m3u8") && !n.includes("index"));
};

let a = getArray();
return a;
""")

    def get_lectures_dict(self):
        return self.driver.execute_script("""elements = document.querySelectorAll("a.detail-title");
        res = {};
        for (el of elements) {
          try {
            href = el.href;
            title = el.getElementsByTagName("span")[0].innerText;
            if (href && title) {
              res[title] = href;
            }
          } catch (error) {}
        }
        return res;
        """)

    def get_lectures_m3u8(self):
        lectures_dict = self.get_lectures_dict()
        res = {}
        for title, url in lectures_dict.items():
            self.driver.get(url)
            sleep(2)
            m3u8_url = self.get_m3u8_url()

            if not m3u8_url:
                print("Trying again x1")
                self.driver.get(url)
                sleep(1)
                m3u8_url = self.get_m3u8_url()
                if not m3u8_url:
                    self.driver.get(url)
                    sleep(1)
                    m3u8_url = self.get_m3u8_url()

            res[title] = m3u8_url
        return res

    def get_download_driver(self, name, basePath):
        profile = {
            'download.prompt_for_download': False,
            'download.default_directory': f'{basePath}/{name}/Notes',
            'download.directory_upgrade': True,
            'plugins.always_open_pdf_externally': True,
        }
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', profile)
        return webdriver.Chrome(options=options)

    def get_download_object(self, validSubstrings, invalidSubstrings=None):
        if invalidSubstrings:
            additonalJs = f"return getPDFObjects({validSubstrings},{invalidSubstrings})"
        else:
            additonalJs = f"return getPDFObjects({validSubstrings})"
        baseJs = """const getObject=(element)=>{try{const link=element.getElementsByClassName("aalink")[0].href;const splitText=element.getElementsByClassName("instancename")[0].innerText.split(/\\r?\\n/);const type=splitText[splitText.length-1];const text=splitText[0];if(type==="File"){return{link,text}}}catch(error){return null}};const filterBySubstrings=(data,validSubstrings,invalidSubstrings=undefined)=>data.filter(({text})=>{const condition1=validSubstrings.some((substring)=>text.includes(substring));if(invalidSubstrings){const condition2=!invalidSubstrings.some((substring)=>text.includes(substring));return condition1&&condition2}return condition1});const getPDFObjects=(validSubstrings,invalidSubstrings=undefined)=>{const elements=document.getElementsByClassName("activityinstance");const res=Array.from(elements).reduce((arr,element)=>{const object=getObject(element);if(object){arr.push(object)}return arr},[]);return filterBySubstrings(res,validSubstrings,invalidSubstrings)};"""

        return self.driver.execute_script(f"{baseJs}{additonalJs}")
