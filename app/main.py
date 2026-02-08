"""
Lead Quiz Bot — main entry point.
Collects leads through Telegram quiz.
"""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Support both running modes: python app/main.py and python -m app.main
try:
    from handlers.feature import router as feature_router
    from database import init_db
except ImportError:
    from app.handlers.feature import router as feature_router
    from app.database import init_db

# Load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Create main router for start/echo handlers
main_router = Router(name="main")


@main_router.message(CommandStart())
async def on_start(message: Message) -> None:
    """Handle /start command."""
    await message.answer(
        "👋 *Привет!*\n\n"
        "Я бот Lead Quiz под брендом *Вячеслав Ветошкин*.\n\n"
        "📝 Напишите /quiz или просто «квиз» чтобы начать.\n"
        "❓ Напишите /help для списка команд.",
        parse_mode="Markdown"
    )


# Include routers in correct order:
# 1. feature_router first (handles /quiz, /help, /cancel, quiz states)
# 2. main_router last (handles /start and fallback echo)
dp.include_router(feature_router)
dp.include_router(main_router)


@main_router.message()
async def echo(message: Message) -> None:
    """Handle unknown messages (fallback)."""
    await message.answer(
        "❌ Команда не распознана.\n"
        "Напишите /help для списка команд."
    )


async def main() -> None:
    """Main entry point."""
    logger.info("Starting Lead Quiz Bot...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
