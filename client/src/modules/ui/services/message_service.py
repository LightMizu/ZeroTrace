
from modules.ui.models.message import TextMessage
from modules.core.messenger_core import SecureMessenger
class MessageService:
    def __init__(self, messenger: SecureMessenger):
        self.__messenger = messenger

    def get_messages(self, chat_id: str) -> list[TextMessage]:
        return []

    def send_message(self, public_key: str, message: TextMessage):
        self.__messenger.send_message(public_key,message.text.encode(),0, message.timestamp)