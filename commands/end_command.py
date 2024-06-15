from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class EndCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        self.bot_started_dict[chat_id] = False
        print("End command received") 
        await update.message.reply_text('The bot has stopped updating messages.')
        all_messages = f"Topic: {self.current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(self.message_dict[chat_id]))
        await update.message.reply_text(f'{all_messages}')
