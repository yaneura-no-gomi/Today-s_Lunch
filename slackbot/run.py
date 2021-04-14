import sys
from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings

sys.path.append('./utils/')
from utils.get_menu_data import get_menu_image

def main():
    slack = Slacker(slackbot_settings.API_TOKEN)
    _ = get_menu_image()
    bot = Bot()
    bot.run()
    slack.chat.post_message('lunch', 'こんにちは!', as_user=True)

    

if __name__ == "__main__":
    print('starting slackbot')
    main()