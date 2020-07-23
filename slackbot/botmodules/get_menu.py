from datetime import datetime, timedelta, timezone
import sys
import os
import glob
from slackbot.bot import default_reply, listen_to, respond_to

import pandas as pd

import slackbot_settings

sys.path.append("./")
from utils.get_menu_data import crop_img, get_menu_image, ocr

JST = timezone(timedelta(hours=+9), 'JST')

def get_today_date():
    dt_today = datetime.now(JST)
    return dt_today


def series2text(d):
    """
        pd.Seriesをいいかんじの文字列に整形して返す
    """
    menu = ''
    for idx, m in zip(d.index, d):
        
        # 変な文字が入っていた場合は”なし”として返す
        if len(m) > 2:
            menu += str(idx) + ": " + m + "\n"

        else:
            menu += str(idx) + ": " + "なし" + "\n"

    return menu


def extract_menu(dt):
    # メニューを取得したい日付をintで保持
    # dt[0]: 日付の数字 e.g) 20200713
    # dt[1]: 曜日 e.g) Mon
    dt = dt.split(" ")
    dt[0] = int(dt[0].replace("-",''))
    dt[1] = dt[1].lower()

    if dt[1] == "sat" or dt[1] == "sun":
        return "休業日です"
    
    # 画像名から月曜日の日付を取得
    mondays = []
    files = sorted(glob.glob("./result/*"))
    for f in files:
        monday = int(os.path.splitext(os.path.basename(f))[0].split("_")[1])
        mondays.append(monday)
    
    if mondays[0] <= dt[0] and dt[0] < mondays[1]:
        # 1週目
        df = pd.read_csv(files[0], index_col=0).fillna("なし")
        menu = series2text(df.loc[:, dt[1]])
        return menu

    else:
        # 2週目
        df = pd.read_csv(files[1], index_col=0).fillna("なし")
        menu = series2text(df.loc[:, dt[1]])
        return menu
 

@listen_to("!help")
def send_help(message):

    how_to_use = "`!today`: 今日のメニューを表示\n `!tomorrow`: 明日のメニューを表示\n `!week`: 今週のメニューを表示\n `!update`: データベースを更新"
    message.send("How to use! \n" + how_to_use)

@listen_to("!test")
def test(message):
    menu = extract_menu("2020-07-20 Mon")
    message.send(menu)


@listen_to("!today")
def send_today_menu(message):
    dt_today = get_today_date()
    dt_today = datetime.strftime(dt_today, "%Y-%m-%d %a")

    menu = extract_menu(dt_today)

    message.send(f"Here's Today's Menu! ({dt_today})")
    message.send(menu)


@listen_to("!tomorrow")
def send_tommorow_menu(message):
    dt_today = get_today_date()
    dt_tomorrow = dt_today + timedelta(days=1)
    dt_tomorrow = datetime.strftime(dt_tomorrow, "%Y-%m-%d %a")

    menu = extract_menu(dt_tomorrow)

    message.send(f"Here's Tomorrow's Menu! ({dt_tomorrow})")
    message.send(menu)


@listen_to("!update")
def update_database(message):

    # message.send("データベースを更新しています...")

    # 既存のcsvを削除
    files = glob.glob("./result/*")
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

    # ２週間分のメニュー画像がとれるので、それぞれの月曜の日付を取得
    mondays = get_menu_image()
    print(mondays)

    dt_today = get_today_date()
    dt_today = datetime.strftime(dt_today, "%Y-%m-%d %a")

    croped_imgs = crop_img("./imgs/1.jpg")
    ocr(croped_imgs, mondays[0])
    croped_imgs = crop_img("./imgs/2.jpg")
    ocr(croped_imgs, mondays[1])

    message.send("更新が完了しました!")
