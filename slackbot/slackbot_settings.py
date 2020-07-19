import os

# 「Bot User OAuth Access Token」をコピーして貼り付ける
API_TOKEN = os.environ["BOT_API_TOKEN"]

# 対応するメッセージがなかった場合に反応するメッセージ
DEFAULT_REPLY = "何言ってんだこいつ"

# Botが実行するスクリプトを配置するディレクトリパスのリスト
PLUGINS = [
    'slackbot.plugins',
    'botmodules.conversation',
    'botmodules.get_menu'
]
