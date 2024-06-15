from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class ListMessagesCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id

        if not self.bot_started_dict.get(chat_id):
            await update.message.reply_text('The bot is not started. Use /start to begin.')
            return

        if not self.current_topic_dict.get(chat_id):
            await update.message.reply_text('Please set a topic first using /settopic [your topic].')
            return

        if not self.message_dict.get(chat_id):
            await update.message.reply_text('No messages to display.')
            return

        all_messages = f"Topic: {self.current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(self.message_dict[chat_id]))
        await update.message.reply_text(f'{all_messages}')
