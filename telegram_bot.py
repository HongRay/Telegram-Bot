import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Dictionary to store messages per chat_id
message_dict = {}

# Dictionary to store the message ID of the last sent message per chat_id
last_message_id_dict = {}

# Dictionary to store the bot started status per chat_id
bot_started_dict = {}

# Dictionary to store the current topic per chat_id
current_topic_dict = {}

set_topic = False

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    bot_started_dict[chat_id] = True
    current_topic_dict[chat_id] = None
    message_dict[chat_id] = []
    print("Start command received")  # Debugging line
    await update.message.reply_text('Hi! This is a bot that lists your messages, eliminating the need to copy and paste messages. ' +
        'The idea is thought by Alvis_SoHot and the bot is created by Hong Ray.\n\n' +
        'Here are the functions:\n\n' +
        '/start - Start the bot and set up the environment\n\n' +
        '/end - Stop the bot and get the final list of messages\n\n' +
        '/settopic [your topic] - Set the topic for the message list\n\n' +
        '/add [your message] - Add a message to the list\n\n' +
        '/list - List all messages under the current topic\n\n' +
        '/delete [message number] - Delete a message from the list\n\n')   
    await update.message.reply_text('Please set a topic for the list by typing /settopic [your topic].')

async def end(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    bot_started_dict[chat_id] = False
    print("End command received")  # Debugging line
    await update.message.reply_text('The bot has stopped updating messages.')
    all_messages = f"Topic: {current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(message_dict[chat_id]))
    await update.message.reply_text(f'{all_messages}')

async def set_topic(update: Update, context: CallbackContext) -> None:
    global set_topic  # Ensure we're modifying the global variable
    set_topic = True
    chat_id = update.effective_chat.id
    current_topic_dict[chat_id] = " ".join(context.args)
    if current_topic_dict[chat_id]:
        print(f"Topic set to: {current_topic_dict[chat_id]}")  # Debugging line
        await update.message.reply_text(f'Topic set to: {current_topic_dict[chat_id]}')
    else:
        await update.message.reply_text('Please provide a topic after /settopic prefix. e.g /settopic grab order')

async def add_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    if not bot_started_dict.get(chat_id) or not current_topic_dict.get(chat_id):
        await update.message.reply_text('The bot is not started or no topic is set. Use /start and /settopic to begin.')
        return

    user_message = " ".join(context.args)
    if not user_message:
        await update.message.reply_text('Please provide a message to add after /add.')
        return

    message_dict[chat_id].append(user_message)

    await update_message_list(update, context)

async def list_messages(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    if not bot_started_dict.get(chat_id):
        await update.message.reply_text('The bot is not started. Use /start to begin.')
        return

    if not current_topic_dict.get(chat_id):
        await update.message.reply_text('Please set a topic first using /settopic [your topic].')
        return

    if not message_dict.get(chat_id):
        await update.message.reply_text('No messages to display.')
        return

    # Compile the message list into a single string
    all_messages = f"Topic: {current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(message_dict[chat_id]))
    await update.message.reply_text(f'{all_messages}')

async def delete_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    if not bot_started_dict.get(chat_id) or not current_topic_dict.get(chat_id):
        await update.message.reply_text('The bot is not started or no topic is set. Use /start and /settopic to begin.')
        return

    try:
        position = int(context.args[0]) - 1
        if position < 0 or position >= len(message_dict[chat_id]):
            await update.message.reply_text('Invalid position. Please provide a valid message position to delete.')
            return

        del message_dict[chat_id][position]
        await update_message_list(update, context)

    except (IndexError, ValueError):
        await update.message.reply_text('Please provide a valid message position to delete after /delete.')

async def update_message_list(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    # Compile the message list into a single string
    all_messages = f"Topic: {current_topic_dict[chat_id]}\n" + "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(message_dict[chat_id]))

    # If a previous message exists, delete it
    if last_message_id_dict.get(chat_id):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=last_message_id_dict[chat_id])
        except Exception as e:
            print(f"Failed to delete message: {e}")

    # Send a new message with the updated list
    sent_message = await context.bot.send_message(chat_id=chat_id, text=f'{all_messages}')
    # Update the last message ID
    last_message_id_dict[chat_id] = sent_message.message_id

async def mention_response(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.name
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

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = Application.builder().token("7255373802:AAEV5UKJ2NIsCGAVBWs18Qnmw0IxmoCOWkk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("end", end))
    application.add_handler(CommandHandler("settopic", set_topic))
    application.add_handler(CommandHandler("add", add_message))
    application.add_handler(CommandHandler("list", list_messages))
    application.add_handler(CommandHandler("delete", delete_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mention_response))

    print("Bot started")  # Debugging line
    application.run_polling()

if __name__ == '__main__':
    main()
