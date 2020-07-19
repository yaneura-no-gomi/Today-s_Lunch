from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import slackbot_settings


# メンションあり応答
@respond_to('こんにちは')
def greeting(message):
    # メンションして応答
    message.reply('こんにちは!')


# メンションなし応答
@listen_to('もうかりまっか')
def greeting(message):

    # メンションなしで応答
    message.send('ぼちぼちでんな')


@default_reply
def my_default_handler(message):
    # デフォルトリプライをsendに変更する
    message.send(slackbot_settings.DEFAULT_REPLY)