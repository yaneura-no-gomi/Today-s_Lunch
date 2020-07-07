import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def main():

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
    


if __name__ == "__main__":
    main()
