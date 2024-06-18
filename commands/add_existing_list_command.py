from commands.command import Command
from telegram import Update
from telegram.ext import CallbackContext

class AddExistingListCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        print("addlist command recieved")
        chat_id = update.effective_chat.id
        text = update.message.text[len('/addlist '):].strip()
        
        if ':' not in text:
            await update.message.reply_text('Invalid format. Please use "topic: item1, item2, item3, ...". e.g. grab: item1, item2, ...')
            return
        
        try:
            topic, items = text.split(':', 1)
            topic = topic.strip()
            items = [item.strip() for item in items.split(',')]
            print("Check")

            if not self.bot_started_dict.get(chat_id, False):
                await update.message.reply_text('Please /start to start the bot')

            # Check if there is an existing topic and list
            if self.current_topic_dict.get(chat_id) and self.message_dict.get(chat_id):
                await update.message.reply_text('You already have an active topic. Please use /end to finish it before adding a new list.')
                return

            # Add the topic to the current_topic_dict
            self.current_topic_dict[chat_id] = topic

            # Initialize the message_dict for the chat_id if not already done
            if chat_id not in self.message_dict:
                self.message_dict[chat_id] = []

            # Add the items to the message_dict
            self.message_dict[chat_id].extend(items)

            await update.message.reply_text(f'Added items to topic "{topic}":\n' + "\n".join(items))
        except Exception as e:
            await update.message.reply_text('Error processing your list. Please ensure it is formatted as "topic: item1, item2, item3, ..."')
            print(f"Error: {e}")
