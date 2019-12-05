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
        try:
            last_message = self.bot.get_updates(offset=-1)
        except telegram.error.TimedOut:
            print("Fatal Error while constructing Telegram Receiver. Get Updated timed out")
            #TODO raise exception
        if len(last_message) > 0:
            self.chat_offset = last_message[0].update_id + 1
        # self.chat_offset = 0


    def get_new_messages(self):
        """Get new messages"""
        messages = []
        try:
            new_updates = self.bot.get_updates(offset=self.chat_offset)
            for update in new_updates:
                messages.append(update.message.text)

            if len(new_updates) > 0:
                self.chat_offset = new_updates[-1].update_id + 1
            return messages
        except telegram.error.TimedOut:
            print("Error while getting Telegram updates: TimeOut")
            return []

    def get_new_msg_messages(self):
        """Get all messages that mean to send a text to a landlord in form of pair(hash, name, language)"""
        results = []
        new_messages = self.get_new_messages()
        for message in new_messages:
            msg_words = message.split()
            if len(msg_words) == 3:
                print(msg_words[0])
                if str.upper(msg_words[0]) == "MSG":
                    results.append((msg_words[1], msg_words[2]))
        return results
