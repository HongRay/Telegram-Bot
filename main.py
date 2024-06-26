# main.py
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes
from commands.start_command import StartCommand
from commands.end_command import EndCommand
from commands.set_topic_command import SetTopicCommand
from commands.add_message_command import AddMessageCommand
from commands.list_messages_command import ListMessagesCommand
from commands.delete_message_command import DeleteMessageCommand
from commands.mention_response_command import MentionResponseCommand
from commands.help_command import HelpCommand
from commands.clear_command import ClearCommand
from commands.command import Command
from commands.add_existing_list_command import AddExistingListCommand
from util.open_file import OpenCommandText

# Dictionaries to store state
message_dict = {}
last_message_id_dict = {}
bot_started_dict = {}
current_topic_dict = {}

class CommandInvoker:
    def __init__(self):
        self._commands = {}

    def register(self, command_name: str, command: Command):
        self._commands[command_name] = command

    async def execute(self, command_name: str, update: Update, context: CallbackContext):
        command = self._commands.get(command_name)
        if command:
            await command.execute(update, context)
            
invoker = CommandInvoker()

def main() -> None:
    token = OpenCommandText.get_token()
    application = Application.builder().token(token).build()

    # Register commands
    invoker.register("start", StartCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("end", EndCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("settopic", SetTopicCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("add", AddMessageCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("list", ListMessagesCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("delete", DeleteMessageCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("mention_response", MentionResponseCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("help", HelpCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("clear", ClearCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))
    invoker.register("addlist", AddExistingListCommand(bot_started_dict, current_topic_dict, message_dict, last_message_id_dict))

    
    async def handle_command(update: Update, context: CallbackContext) -> None:
        command_name = update.message.text.split()[0][1:]  # Get command without '/'
        await invoker.execute(command_name, update, context)
    
    async def handle_mention_response(update: Update, context: CallbackContext) -> None:
        await invoker.execute("mention_response", update, context)

    #adding command handlers 
    application.add_handler(CommandHandler("start", handle_command))
    application.add_handler(CommandHandler("end", handle_command))
    application.add_handler(CommandHandler("settopic", handle_command))
    application.add_handler(CommandHandler("add", handle_command))
    application.add_handler(CommandHandler("list", handle_command))
    application.add_handler(CommandHandler("delete", handle_command))
    application.add_handler(CommandHandler("help", handle_command))
    application.add_handler(CommandHandler("clear", handle_command))
    application.add_handler(CommandHandler("addlist", handle_command))
    
    # Works only with admin rights 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mention_response))

    print("Bot started")
    application.run_polling()

if __name__ == '__main__':
    main()
