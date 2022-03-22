from time import sleep
from selenium import webdriver


def update_links(panopto_folders):
    query = "&maxResults=250"
    res = {}
    for key, value in panopto_folders.items():
        res[key] = value + query
    return res


class Driver:
    def __init__(self, panopto_folders) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.driver = webdriver.Chrome(options=self.options)
        self.panopto_folders = update_links(panopto_folders)

    def get_m3u8_url(self):
        JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
        network_requests = self.driver.execute_script(JS_get_network_requests)
        for n in network_requests:
            name = n["name"]
            if ".m3u8" in name and "index.m3u8" not in name:
                return name

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
            sleep(0.5)
            m3u8_url = self.get_m3u8_url()

            res[title] = m3u8_url
        return res
