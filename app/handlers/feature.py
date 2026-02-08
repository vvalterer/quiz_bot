"""
Quiz handlers with FSM state management.
Collects leads through 7 questions and notifies admin.
"""
import os
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

try:
    from database import save_lead
except ImportError:
    from app.database import save_lead

logger = logging.getLogger(__name__)
router = Router(name=__name__)

# Load admin IDs from environment
ADMIN_IDS = [
    int(x.strip()) 
    for x in os.getenv("ADMIN_IDS", "").split(",") 
    if x.strip().isdigit()
]

QUESTIONS = [
    "1️⃣ Как вас зовут?",
    "2️⃣ Какая ниша/сфера?",
    "3️⃣ Главная цель?",
    "4️⃣ Бюджет (примерно)?",
    "5️⃣ Сроки запуска?",
    "6️⃣ Есть сайт? (да/нет + ссылка)",
    "7️⃣ Как связаться? (телеграм/почта)",
]


class QuizStates(StatesGroup):
    """FSM states for quiz flow."""
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()


STATES_LIST = [
    QuizStates.q1, QuizStates.q2, QuizStates.q3, QuizStates.q4,
    QuizStates.q5, QuizStates.q6, QuizStates.q7
]


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    """Handle /help command."""
    await message.answer(
        "🤖 *Lead Quiz Bot — Вячеслав Ветошкин*\n\n"
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/quiz — начать квиз\n"
        "/cancel — отменить квиз",
        parse_mode="Markdown"
    )


@router.message(Command("quiz"))
@router.message(F.text.lower().contains("квиз"))
async def start_quiz(message: Message, state: FSMContext) -> None:
    """Start the quiz flow."""
    await state.clear()
    await state.update_data(answers=[])
    await state.set_state(QuizStates.q1)
    await message.answer(
        "📝 *Начинаем квиз из 7 вопросов!*\n\n"
        "Вы можете отменить в любой момент командой /cancel\n\n"
        f"{QUESTIONS[0]}",
        parse_mode="Markdown"
    )


@router.message(Command("cancel"))
async def cancel_quiz(message: Message, state: FSMContext) -> None:
    """Cancel the quiz."""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нет активного квиза для отмены.")
        return
    
    await state.clear()
    await message.answer(
        "✅ Квиз отменён. Напишите /quiz чтобы начать заново."
    )


async def process_answer(
    message: Message, 
    state: FSMContext, 
    question_index: int
) -> None:
    """Process quiz answer and move to next question or finish."""
    data = await state.get_data()
    answers = data.get("answers", [])
    answers.append(message.text)
    
    if question_index < len(QUESTIONS) - 1:
        # Move to next question
        await state.update_data(answers=answers)
        await state.set_state(STATES_LIST[question_index + 1])
        await message.answer(QUESTIONS[question_index + 1])
    else:
        # Quiz completed
        await state.clear()
        
        # Format summary
        summary_lines = []
        for i, (q, a) in enumerate(zip(QUESTIONS, answers)):
            summary_lines.append(f"{q}\n   ↳ {a}")
        summary = "\n\n".join(summary_lines)
        
        # Send to user
        await message.answer(
            f"✅ *Спасибо за ответы!*\n\n"
            f"Ваши ответы:\n\n{summary}\n\n"
            f"Мы свяжемся с вами в ближайшее время! 🚀",
            parse_mode="Markdown"
        )
        
        # Save to database
        try:
            lead_id = await save_lead(
                user_id=message.from_user.id,
                username=message.from_user.username,
                answers=answers
            )
            logger.info(f"Lead saved: id={lead_id}, user_id={message.from_user.id}")
        except Exception as e:
            logger.error(f"Failed to save lead: {e}")
        
        # Notify admins
        if ADMIN_IDS:
            admin_text = (
                f"🆕 *Новый лид!*\n\n"
                f"👤 User ID: `{message.from_user.id}`\n"
                f"📛 Username: @{message.from_user.username or 'не указан'}\n\n"
                f"📋 *Ответы:*\n\n{summary}"
            )
            bot: Bot = message.bot
            for admin_id in ADMIN_IDS:
                try:
                    await bot.send_message(
                        admin_id, 
                        admin_text, 
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin {admin_id}: {e}")


# Handler for each question state
@router.message(QuizStates.q1)
async def handle_q1(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 0)


@router.message(QuizStates.q2)
async def handle_q2(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 1)


@router.message(QuizStates.q3)
async def handle_q3(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 2)


@router.message(QuizStates.q4)
async def handle_q4(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 3)


@router.message(QuizStates.q5)
async def handle_q5(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 4)


@router.message(QuizStates.q6)
async def handle_q6(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 5)


@router.message(QuizStates.q7)
async def handle_q7(message: Message, state: FSMContext) -> None:
    await process_answer(message, state, 6)
