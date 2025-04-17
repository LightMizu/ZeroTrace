from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    text: str
    sender: str
    timestamp: datetime = datetime.now()
