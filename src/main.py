import os
import re
from pprint import pprint

import pyocr
import requests
from bs4 import BeautifulSoup
from PIL import Image
from pytesseract import pytesseract

from image_croper import ImageCroper

ROOT_PATH = "/opt/"

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
        with open(os.path.join(ROOT_PATH, str(i)+"_2.jpg"),'wb') as file:
                file.write(r.content)

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    new_image = Image.fromarray(new_image)
    return new_image

def crop_img(img_path):
    croper = ImageCroper(img_path)
    croper.extract_lines()
    croped_imgs = croper.crop_by_frame()

    for k, v in croped_imgs.items():
        pil_imgs = []
        for cv_img in v:
            pil_imgs.append(cv2pil(cv_img))
        v = pil_imgs

    return croped_imgs

def ocr(img_path):
    path_tesseract = "/usr/bin/tesseract"
    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract
    
    tools = pyocr.get_available_tools()
    tool = tools[0]

    croped_imgs = crop_img(img_path)

    print(croped_imgs)

    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img_org, lang="jpn", builder=builder)

    return result

    
def main():
    get_menu_image()
    # print(ocr("/opt/1.jpg"))

if __name__ == "__main__":
    main()
