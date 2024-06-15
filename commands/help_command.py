from commands.command import Command
from util.open_command_text import OpenCommandText
from telegram import Update
from telegram.ext import CallbackContext

class HelpCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        command_list_text_file= 'command_list_text.txt'
        
        command_list_text = OpenCommandText.get_text(command_list_text_file)

        await update.message.reply_text(command_list_text)