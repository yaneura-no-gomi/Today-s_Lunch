from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings

def main():
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('timeline', 'こんにちは!', as_user=True)

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('starting slackbot')
    main()