import glob
import os
import sys
from datetime import datetime, timedelta, timezone

import requests
from slackbot.bot import default_reply, listen_to, respond_to
from slacker import Slacker

import slackbot_settings

JST = timezone(timedelta(hours=+9), 'JST')

def get_today_date():
    dt_today = datetime.now(JST)
    return dt_today

def get_weekly_menu(dt):
    # メニューを取得したい日付をintで保持
    # dt[0]: 日付の数字 e.g) 20200713
    # dt[1]: 曜日 e.g) Mon
    dt = dt.split(" ")
    dt[0] = int(dt[0].replace("-",''))

    # 画像名から月曜日の日付を取得
    mondays = []
    files = sorted(glob.glob("./result/*"))
    for f in files:
        monday = int(os.path.splitext(os.path.basename(f))[0].split("_")[1])
        mondays.append(monday)
    
    if mondays[0] <= dt[0] and dt[0] < mondays[1]:
        # 1週目
        return "/opt/imgs/1.jpg"

    else:
        # 2週目
        return "/opt/imgs/2.jpg"

@listen_to("!week")
def send_weekly_menu(message):

    message.send("Here's Weekly Menu!")

    dt_today = get_today_date()
    dt_today = datetime.strftime(dt_today, "%Y-%m-%d %a")

    img_path = get_weekly_menu(dt_today)

    slacker = Slacker(slackbot_settings.API_TOKEN)
    channel = "lunch"
    file = img_path

    slacker.files.upload(file_=file, channels=channel)
