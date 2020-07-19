from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import slackbot_settings


@listen_to("!getmenu")
def greeting(message):

    message.send('メニューを表示します')

@listen_to("!update")
def greeting(message):

    message.send('データベースを更新します')
