from modules.core.messenger_core import SecureMessenger

from typing import Optional, Dict


class ChatService:
    def __init__(self, messenger: SecureMessenger):
        self.mock_chats: Dict[dict] = {}

        self.__messenger: SecureMessenger = messenger

    def get_chats(self, query: Optional[str] = None):
        chats = self.__messenger.get_dialogs()
        for chat in chats:
            user = self.__messenger.get_user(chat["public_key"])
            self.mock_chats[chat["dialog_hash"]] = {
                "name": user["username"],
                "public_key": chat["public_key"],
            }
        if query:
            finded = self.__messenger.search_users(query)
            for finded_user in finded:
                user = {
                    "name": finded_user["username"],
                    "public_key": finded_user["kem_public_key"],
                }
                dialog_hash = self.__messenger.generate_dialog_id(
                    finded_user["kem_public_key"], self.__messenger.kem_public_key
                )
                print(self.mock_chats)
                self.mock_chats[dialog_hash] = user
        return self.mock_chats
