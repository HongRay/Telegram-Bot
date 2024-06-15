from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class SetTopicCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        self.current_topic_dict[chat_id] = " ".join(context.args)
        if self.current_topic_dict[chat_id]:
            print(f"Topic set to: {self.current_topic_dict[chat_id]}") 
            await update.message.reply_text(f'Topic set to: {self.current_topic_dict[chat_id]}')
        else:
            await update.message.reply_text('Please provide a topic after /settopic prefix. e.g /settopic grab order')
