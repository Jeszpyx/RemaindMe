import asyncio
import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import BotCommand

from notify_router import notify_router
from keyboards import main_menu_kbd, notify_menu_kbd, notify_text
from constants import enviroment

TOKEN = enviroment.BOT_TOKEN


dp = Dispatcher()
dp.include_router(notify_router)

temp_folder = "temp"
temp_folder_path = os.path.join(os.getcwd(), temp_folder)

if not os.path.exists(temp_folder_path):
    os.makedirs(temp_folder_path)


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет. Я очень полезный бот. Выбери нужное действие из меню:",
        reply_markup=main_menu_kbd,
    )


@dp.message(F.text == notify_text)
async def handle_notify_button(message: Message):
    await message.delete()
    await message.answer(
        "Вы зашли в меню напоминаний:",
        reply_markup=notify_menu_kbd,
    )


# @dp.message(F.voice)
# async def handle_voice(message: Message, bot: Bot):
#     file_id = message.voice.file_id
#     file = await bot.get_file(file_id)
#     save_path = os.path.join(temp_folder_path, "voice.ogg")
#     await bot.download(file, destination=save_path)
#     # await message.reply("Голосовое сообщение сохранено! Распознаю...")

#     # await message.reply(f"Текст голосового сообщения:\n{text}")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить\перезапустить бота"),
            BotCommand(command="help", description="Помощь по использованию бота"),
            BotCommand(command="cancel", description="Отменить текущее действие"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
