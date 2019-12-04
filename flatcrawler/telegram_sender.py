from typing import List
from .wg_result import WGResult
import requests as req

class SenderTelegram(object):

    def __init__(self, bot_token: str, receiver_id: List[str]):
        self.bot_token = bot_token
        self.receiver_ids = receiver_id


    def sendWGMessage(self, wg_message: WGResult):
        bot_message = wg_message.as_string()
        for chat_id in self.receiver_ids:
            send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
            response = req.get(send_text)
