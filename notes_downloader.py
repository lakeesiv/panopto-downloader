from time import sleep
from Driver import Driver
import json
import os

course = "3F1"
moodle_links = json.load(open("moodle_links.json"))
moodle_links = {course: moodle_links[course]}

base_path = r"C:\Users\lakee\Desktop\IIA"
D = Driver(moodle_links=moodle_links, base_path=base_path)

D.driver.get(
    moodle_links[course]["link"])

print("""
YOU HAVE 15s TO LOG IN THROUGH RAVEN
""")

sleep(15)

# print(D.get_download_object(["filled", "annotated"]))
# D.get_download_driver("3F1", base_path)

for key, obj in moodle_links.items():
    D.driver.get(obj["link"])
    sleep(1)
    D.download_pdfs(key, base_path, obj.get(
        "validSubstrings"), obj.get("invalidSubstrings"))
