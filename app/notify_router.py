from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from assistant_service import assistant_service
from transcribe_service import transcribe_service
from file_service import file_service
from keyboards import (
    back_text,
    create_notify_text,
    list_notify_text,
    main_menu_kbd,
    notify_confirm_keyboard,
    notify_menu_kbd,
    remove_notify_text,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

notify_router = Router()


class Form(StatesGroup):
    notify_input = State()


@notify_router.message(Command("cancel"))
@notify_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "Действие отменено",
        reply_markup=notify_menu_kbd,
    )


@notify_router.message(F.text == create_notify_text)
async def handle_create_notify_button(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.notify_input)
    await message.answer(
        "📝 Отправьте мне описание напоминания с указанием даты и времени.\nВы можете написать текстовое сообщение или отправить голосовое.",
        reply_markup=ReplyKeyboardRemove(),
    )


@notify_router.message(Form.notify_input)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.voice:
        file_id = message.voice.file_id
        file = await message.bot.get_file(file_id)
        file_name = f"{file_id}.ogg"
        file_path = file_service.get_path_to_save(file_name=file_name)
        await message.bot.download_file(file.file_path, file_path)
        text = await transcribe_service.transcribe(file_path)
        print(text, "text")
        result = await assistant_service.get_notification_data(user_prompt=text)
        print(result, "result")
        if not result:
            await message.answer("Извините, не удалость расознать голосовое сообщение")
        else:
            await message.answer(result, reply_markup=notify_confirm_keyboard)
            await state.clear()
    elif message.text:
        text = message.text
        result = await assistant_service.get_notification_data(user_prompt=text)
        if not result:
            await message.answer("Извините, не удалость определить тему сообщения")
        else:
            await message.answer(result, reply_markup=notify_confirm_keyboard)
            await state.clear()
    else:
        await message.answer("Пожалуйста, отправьте текст или голосовое сообщение")


@notify_router.message(F.text == list_notify_text)
async def handle_list_notify_button(message: Message):
    await message.answer("Этот метод ещё не реализован")


@notify_router.message(F.text == remove_notify_text)
async def handle_remove_notify_button(message: Message):
    await message.answer("Этот метод ещё не реализован")


@notify_router.message(F.text == back_text)
async def handle_list_notify_button(message: Message):
    await message.answer("Вы в главном меню", reply_markup=main_menu_kbd)
