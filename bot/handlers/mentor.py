from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ChatAction

from mentor import ask_mentor
from bot.storage import get_history, add_turn, clear_history
from bot.formatters import build_sources_block
from bot.html_sanitizer import sanitize_telegram_html
from aiogram.filters import CommandStart, Command
import logging
import asyncio

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "<b>Привіт!</b> Я ментор з Django. Сповісти мене про свою задачу — "
        "підкажу напрямок, а не готовий код 😉",
        parse_mode="HTML",
    )

@router.message(Command("new"))
async def handle_new_chat(message: Message):
    clear_history(message.from_user.id)
    await message.answer("🆕 Починаємо нову розмову. Історію попередніх повідомлень очищено.")


@router.message(F.text)
async def handle_question(message: Message):
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    history = get_history(message.from_user.id)

    try:
        result = asyncio.to_thread(ask_mentor, message.text, history)
    except Exception:
        logging.exception("ask_mentor failed for user %s", message.from_user.id)
        await message.answer("Вибач, зараз виникла технічна помилка. Спробуй, будь ласка, ще раз за хвилину.")
        return
    add_turn(message.from_user.id, message.text, result["answer"])

    safe_answer = sanitize_telegram_html(result["answer"])
    try:
        await message.answer(safe_answer, parse_mode="HTML")
    except TelegramBadRequest:
        await message.answer(safe_answer)

    sources_block = build_sources_block(result["sources"])
    if sources_block is not None:
        await message.answer(**sources_block.as_kwargs())