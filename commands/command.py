from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext

class Command(ABC):
    def __init__(self, bot_started_dict, current_topic_dict, message_dict, last_message_id_dict):
        self.bot_started_dict = bot_started_dict
        self.current_topic_dict = current_topic_dict
        self.message_dict = message_dict
        self.last_message_id_dict = last_message_id_dict

    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext) -> None:
        pass
