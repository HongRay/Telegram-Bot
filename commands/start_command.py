from commands.command import Command
from util.open_file import OpenCommandText
from telegram import Update
from telegram.ext import CallbackContext

class StartCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        self.bot_started_dict[chat_id] = True
        self.current_topic_dict[chat_id] = None
        self.message_dict[chat_id] = []
        command_list_text_file = 'command_list_text.txt'
        
        print("Start command received")

        command_list_text =  OpenCommandText.get_text(command_list_text_file)
        
        await update.message.reply_text(
            'Hi! This is a bot that lists your messages, eliminating the need to copy and paste messages. ' +
            'The idea is thought by Alvis_SoHot and the bot is created by Hong Ray.\n\n' +
            command_list_text + "\n\n" 
        )
        await update.message.reply_text('Please set a topic for the list by typing /settopic [your topic].')
