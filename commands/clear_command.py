from commands.command import Command
from util.open_file import OpenCommandText
from telegram import Update
from telegram.ext import CallbackContext

class ClearCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        
        self.message_dict[chat_id] = []
        self.last_message_id_dict[chat_id] = None
        
        await update.message.reply_text('All data has been cleared. The bot has been reset.')