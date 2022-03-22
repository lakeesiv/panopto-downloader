from time import sleep
from Driver import Driver
import json

panopto_folders = json.load(open("panopto_folders.json"))

D = Driver(panopto_folders)

D.driver.get(
    "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Home.aspx")

print("""
YOU HAVE 15s TO LOG IN THROUGH RAVEN
""")

sleep(15)
courses_m3u8 = {}

for course, link in D.panopto_folders.items():
    print(f"Downloading {course}")
    D.driver.get(link)
    sleep(1)
    lectures_m3u8 = D.get_lectures_m3u8()
    courses_m3u8[course] = lectures_m3u8

with open('courses_m3u8.json', 'w') as fp:
    json.dump(courses_m3u8, fp,  indent=4)
