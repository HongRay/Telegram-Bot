from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class MentionResponseCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        bot_username = context.bot.username
        print(bot_username)
        print(update.message.text)
        if f"@{bot_username}" in update.message.text:
            await update.message.reply_text('Hi! This is a bot that lists your messages, eliminating the need to copy and paste messages.' +
            'The idea is thought by Alvis_SoHot and the bot is created by Hong Ray.\n\n' +
            'Here are the functions:\n\n' +
            '/start - Start the bot and set up the environment\n\n' +
            '/end - Stop the bot and get the final list of messages\n\n' +
            '/settopic [your topic] - Set the topic for the message list\n\n' +
            '/add [your message] - Add a message to the list\n\n' +
            '/list - List all messages under the current topic\n\n' +
            '/delete [message number] - Delete a message from the list')
