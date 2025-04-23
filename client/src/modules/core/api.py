import httpx
from typing import Optional, List

BASE_URL = "https://zerotrace-production.up.railway.app"

class API:
    @staticmethod
    def register(
        username: str, kem_public_key: str, signature_public_key: str
    ) -> Optional[bool]:
        try:
            r = httpx.post(
                f"{BASE_URL}/register",
                json={
                    "username": username,
                    "kem_public_key": kem_public_key,
                    "signature_public_key": signature_public_key,
                },
            )
            if r.status_code == 200:
                return True
            elif r.status_code == 409:
                return False
            r.raise_for_status()
        except httpx.HTTPStatusError:
            raise

    @staticmethod
    def get_user_public_key(username: str) -> Optional[dict]:
        try:
            r = httpx.get(f"{BASE_URL}/user/{username}")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError:
            return None

    @staticmethod
    def get_user(public_key: str) -> Optional[dict]:
        try:
            r = httpx.get(f"{BASE_URL}/lookup/{public_key}")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError:
            return None

    @staticmethod
    def send_message(
        sender_public_key: str,
        recv_public_key: str,
        shared_secret_aes_ciphertext: str,
        shared_secret_kem_ciphertext: str,
        crypted_msg: str,
        nonce_msg: str,
        nonce_secret: str,
        signature: str,
        hash_pub: str,
        msg_type: int,
        dialog_hash: str,
        timestamp:float
    ) -> bool:

        try:
            r = httpx.post(
                f"{BASE_URL}/send",
                json={
                    "sender_public_key": sender_public_key,
                    "recipient_public_key": recv_public_key,
                    "shared_secret_aes_ciphertext": shared_secret_aes_ciphertext,
                    "shared_secret_kem_ciphertext": shared_secret_kem_ciphertext,
                    "ciphertext": crypted_msg,
                    "nonce": nonce_msg,
                    "shared_secret_aes_nonce": nonce_secret,
                    "signature": signature,
                    "hash_public": hash_pub,
                    "msg_type": msg_type,
                    "dialog_hash": dialog_hash,
                    "timestamp":timestamp
                },
            )
            r.raise_for_status()
            return True
        except httpx.HTTPError as e:
            print(f"[ERROR] Failed to send message: {e}")
            return False

    @staticmethod
    def get_messages(public_key: str, last_timestamp: int) -> List[dict]:
        try:
            r = httpx.get(
                f"{BASE_URL}/messages/{public_key}", params={"last": last_timestamp}
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            print(f"[ERROR] Failed to fetch messages: {e}")
            return []
    
    @staticmethod
    def get_dialog_messages(dialog_hash: str, last_timestamp: float) -> List[dict]:
        try:
            r = httpx.get(
                f"{BASE_URL}/dialog/{dialog_hash}", params={"last": last_timestamp}
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            print(f"[ERROR] Failed to fetch messages: {e}")
            return []
    
    @staticmethod
    def get_dialogs(public_key) -> List[dict]:
        try:
            r = httpx.get(
                f"{BASE_URL}/dialogs/{public_key}"
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            print(f"[ERROR] Failed to fetch messages: {e}")
            return []
    def search_user(self, query: str) -> List[dict]:
        try:
            r = httpx.get(
                f"{BASE_URL}/users/{query}"
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            print(f"[ERROR] Failed to fetch messages: {e}")
            return []