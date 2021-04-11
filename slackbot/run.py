from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings

from ..utils.get_menu_data import get_menu_image

def main():
    slack = Slacker(slackbot_settings.API_TOKEN)
    _ = get_menu_image()
    # slack.chat.post_message('lunch', 'こんにちは!', as_user=True)

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('starting slackbot')
    main()