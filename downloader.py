import json
import subprocess

courses = json.load(open("courses_m3u8.json"))
download_path = r"C:\Users\lakee\Desktop\IIA\3F7\Recordings"

for title, url in courses["3F7"].items():
    if (url):
        title = title.replace(" ", "_")
        title = title.replace("/", "_")
        title = title.replace("\\", "_")
        title = title.replace(":", "_")
        title = title.replace(".", "_")
        title = title.replace(",", "_")
        hm = f"{download_path}\{title}.mp4"
        print(
            f"downloadm3u8  -o {hm} {url}\n-----------------------------------------------")
        subprocess.run(
            f"downloadm3u8  -o {hm} {url}")
