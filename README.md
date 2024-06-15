# telegram-list-bot
Telegram bot that allows multiple users to add messages in a consolidated area without copying and pasting previous messages. The bot can start and stop tracking messages, set a topic for the message list, add messages, list all messages under the current topic, delete messages, and clear all data.

This idea is credited to Alvis Soh, NUSC ambassador and enthusiast, future perm sec and ultimate sheng shiong runner. 

## Functions 
- Start the Bot: `/start`
- End the Bot: `/end`
- Set Topic: `/settopic [your topic]`
- Add Message: `/add [your message]`
- List Messages: `/list`
- Delete Message: `/delete [message number]`
- Clear All Data: `/clear`

## Getting Started 
### Prerequisites
- [Python](https://www.python.org/downloads/)
- [Python-telegram-bot API](https://pypi.org/project/python-telegram-bot/)
- [Bot token from BotFather](https://core.telegram.org/bots/tutorial)

### Running the bot 
1. Navigate to `data` folder and replace the token id with your own bot's token (Tutorial to obtain bot token in the link above). 
2. Navigate to the directory with `main.py` and run 
```python
python main.py
```