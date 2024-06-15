from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class AddMessageCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id

        if not self.bot_started_dict.get(chat_id) or not self.current_topic_dict.get(chat_id):
            await update.message.reply_text('The bot is not started or no topic is set. Use /start and /settopic to begin.')
            return

        user_message = " ".join(context.args)
        if not user_message:
            await update.message.reply_text('Please provide a message to add after /add.')
            return

        self.message_dict[chat_id].append(user_message)
        await self.update_message_list(update, context)

    async def update_message_list(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        all_messages = f"Topic: {self.current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(self.message_dict[chat_id]))
        
        if self.last_message_id_dict.get(chat_id):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=self.last_message_id_dict[chat_id])
            except Exception as e:
                print(f"Failed to delete message: {e}")

        sent_message = await context.bot.send_message(chat_id=chat_id, text=f'{all_messages}')
        self.last_message_id_dict[chat_id] = sent_message.message_id
