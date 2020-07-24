# Today-s_Lunch

Slack Bot to notify today's lunch menus TUS in Katsushika!

## Usage
This is deployed to Heroku and based on Hubot. I'll spare you the Hubot setup.
```sh
heroku login
git clone https://github.com/yaneura-no-gomi/Today-s_Lunch.git 
heroku create [your-app-name]
heroku git:remote -a [your-app-name]
heroku config:set BOT_API_TOKEN="xoxb_xxxxx..."
heroku config:set CHANNEL_ID="xxxxxx"
git push heroku master
```

**When you start the app, be sure to run the `!update` command first.**


## Commands
It works by mending the bot or sending the following commands on a specific channel.
- `!help`: Help for this app
- `!today`: View today's lunch
- `!tomorrow`: View tomorrow's lunch
- `!week`: View weekly menu by the image
- `!update`: Update database