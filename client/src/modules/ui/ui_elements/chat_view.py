import flet as ft
from time import time, sleep

from modules.core.messenger_core import SecureMessenger
from modules.ui.services.message_service import MessageService
from modules.ui.services.chat_service import ChatService
from modules.ui.models.message import TextMessage, LoadAnim
from modules.database import MessageDatabase


class ChatView:
    def __init__(
        self,
        page: ft.Page,
        messenger: SecureMessenger,
        chat_service: ChatService,
        database: MessageDatabase,
    ):
        self.page = page
        self.database = database
        self.messages_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        self.input_field = ft.TextField(hint_text="Type a message...", expand=True, on_submit=self.send_message)
        self.send_button = ft.IconButton(icon=ft.Icons.SEND, on_click=self.send_message)
        self.message_service = MessageService(messenger)
        self.__chat_service = chat_service
        self.current_chat_id = None
        self.messages = []
        self.displayed_timestamps = set()  # Для отслеживания отображенных сообщений

    def build(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(content=self.messages_column, expand=True),
                    ft.Row(controls=[self.input_field, self.send_button]),
                ],
                expand=True,
            ),
        )

    def load_messages(self, messages):
        """Загружает только новые сообщения в чат."""
        new_controls = []
        for msg in messages:
            if msg.timestamp not in self.displayed_timestamps:
                self.messages.append(msg)
                self.displayed_timestamps.add(msg.timestamp)
                if isinstance(msg, LoadAnim):
                    new_controls.append(ft.ProgressRing())
                elif isinstance(msg, TextMessage):
                    new_controls.append(ft.Text(f"{msg.sender}: {msg.text}"))
        self.messages_column.controls.extend(new_controls)
        self.page.update()

    def set_chat(self, chat_id):
        """Устанавливает текущий чат и загружает его сообщения."""
        self.current_chat_id = chat_id
        self.messages_column.controls.clear()
        self.messages.clear()
        self.displayed_timestamps.clear()
        messages = self.message_service.get_messages(chat_id)
        self.load_messages(messages)

    def send_message(self, e):
        """Отправляет сообщение и сразу отображает его в чате."""
        if self.input_field.value and self.current_chat_id:
            msg = TextMessage(text=self.input_field.value, sender="You", timestamp=round(time(),2))
            self.database.add_message(
                "You", msg.text.encode(), 0, msg.timestamp, self.current_chat_id
            )
            # Добавляем сообщение в список и интерфейс с индикатором загрузки
            self.messages.append(msg)
            self.displayed_timestamps.add(msg.timestamp)
            temp_control = ft.Row(
                [
                    ft.ProgressRing(scale=0.4),
                    ft.Text(f"{msg.sender}: {msg.text}"),
                ]
            )
            self.messages_column.controls.append(temp_control)
            self.input_field.value = ""
            self.page.update()
            # Отправка сообщения (в реальном приложении это асинхронно)
            self.message_service.send_message(
                self.__chat_service.mock_chats[self.current_chat_id]["public_key"],
                msg,
            )
            # Заменяем индикатор загрузки на текст сообщения
            index = self.messages_column.controls.index(temp_control)
            self.messages_column.controls[index] = ft.Text(f"{msg.sender}: {msg.text}")
            self.page.update()
    @staticmethod
    def remove_type(lst, type_to_remove):
        return [item for item in lst if not isinstance(item, type_to_remove)]

    def update_chat_view(chat_view_instance):
        """Обновляет чат, подгружая новые сообщения из базы данных."""
        while True:
            if not chat_view_instance.current_chat_id:
                sleep(2)
                continue
            sleep(2)
            # Получаем временную метку последнего сообщения
            if chat_view_instance.messages:
                timestamp = max(chat_view_instance.messages, key=lambda x: x.timestamp).timestamp
            else:
                timestamp = 0
            # Загружаем новые сообщения из базы данных
            tuple_messages = chat_view_instance.database.get_messages(
                chat_view_instance.current_chat_id, timestamp
            )
            messages = []
            if tuple_messages:
                chat_view_instance.messages_column.controls = ChatView.remove_type(chat_view_instance.messages_column.controls, ft.ProgressRing)
            for message in tuple_messages:
                if message[2] == 0:  # Обычное текстовое сообщение
                    messages.append(TextMessage(message[1].decode(), message[0], message[3]))
                elif message[2] == 5:  # Анимация загрузки
                    messages.append(LoadAnim(0))
            if messages:
                chat_view_instance.load_messages(messages)  # Загружаем без реверса