# from dataclasses import dataclass
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


notify_text = "🔔 Напоминания"  # 📅 ⏰ 📝 🕒 ⏳
create_notify_text = "✨ Создать напоминание"  # ✨ ✏️ ⏱️
list_notify_text = "📋 Список напоминаний"  # 📜 📄
remove_notify_text = "🗑️ Удалить напоминание"  # ❌ 🚫 ✖️


back_text = "◀️ Назад"  # 🔙 ◀️ ↩️ 🚪 🏠


accept_text = "✅ Принять"
cancel_text = "❌ Отмена"

# @dataclass
# class Notify:
#     def __init__(self) -> None:
#         self.create = create_notify_text
#         self.list = list_notify_text
#         self.remove = remove_notify_text


main_menu_kbd = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=notify_text)],
        [KeyboardButton(text="Функция №2")],
        [KeyboardButton(text="Функция №3")],
    ],
)


notify_menu_kbd = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=create_notify_text)],
        [KeyboardButton(text=list_notify_text)],
        [KeyboardButton(text=remove_notify_text)],
        [KeyboardButton(text=back_text)],
    ],
)

notify_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=accept_text, callback_data="create_notify_confirm_accept"
            ),
            InlineKeyboardButton(
                text=cancel_text, callback_data="create_notify_confirm_cancel"
            ),
        ]
    ]
)
