from typing import List
import telegram

class ReceiverTelegram(object):

    def __init__(self, bot_token: str, receiver_ids: List[str]):
        self.bot_token = bot_token
        self.receiver_ids = receiver_ids
        self.bot = telegram.Bot(token=self.bot_token)
        # Check how many message there when created.
        # Is used so that only the new messages are read
        # Get last message with -1
        self.chat_offset = 0
        last_message = self.bot.get_updates(offset=-1)
        if len(last_message) > 0:
            self.chat_offset = last_message[0].update_id + 1
        # self.chat_offset = 0


    def get_new_messages(self):
        messages = []
        new_updates = self.bot.get_updates(offset=self.chat_offset)
        # new_updates = self.bot.get_updates()
        for update in new_updates:
            messages.append(update.message.text)

        if len(new_updates) > 0:
            self.chat_offset = new_updates[-1].update_id + 1
        return messages
