import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from pytesseract import pytesseract

from PIL import Image
import pyocr


def get_menu_image():

    urlName = "http://tus-dining.co.jp/menu/"
    url = requests.get(urlName)
    soup = BeautifulSoup(url.content, "html.parser")

    katsushika = soup.body.find_all("div", class_="grid-box isotope-item katsushika")[0]

    # pprint(katsushika.find_all("img"))
    imgs = [ _["src"] for _ in katsushika.find_all("img")]
    pprint(imgs)

    for i, img in enumerate(imgs):
        r = requests.get(img)
        with open(os.path.join("..", str(i)+".jpg"),'wb') as file:
                file.write(r.content)

def ocr(img_path):
    path_tesseract = "/usr/bin/tesseract"
    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract
    
    tools = pyocr.get_available_tools()
    tool = tools[0]
    img_org = Image.open(img_path)

    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img_org, lang="jpn", builder=builder)

    return result

    
def main():
    # get_menu_image()
    print(ocr("/opt/1.jpg"))

if __name__ == "__main__":
    main()
