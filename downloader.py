import json
import subprocess

courses = json.load(open("courses_m3u8.json"))
download_path = r"C:\Users\lakee\Desktop\IIA\3F1\Recordings"

for title, url in courses["3F1"].items():
    if (url):
        title = title.replace(" ", "_")
        title = title.replace("/", "_")
        title = title.replace("\\", "_")
        title = title.replace(":", "_")
        title = title.replace(".", "_")
        title = title.replace(",", "_")
        hm = f"{download_path}\{title}.mp4"
        print(
            f"downloadm3u8  -o {hm} {url[0]}\n-----------------------------------------------")
        subprocess.run(
            f"downloadm3u8  -o {hm} {url[0]}")
