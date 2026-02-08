"""
Tests for quiz handlers.
"""
import pytest
import os
import sys
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Set test environment
os.environ["DB_PATH"] = "test_data/test_database.sqlite3"
os.environ["ADMIN_IDS"] = "123456789"


class MockMessage:
    """Mock Telegram message."""
    
    def __init__(self, text: str, user_id: int = 12345, username: str = "testuser"):
        self.text = text
        self.from_user = MagicMock()
        self.from_user.id = user_id
        self.from_user.username = username
        self.bot = AsyncMock()
        self.answer = AsyncMock()


class MockFSMContext:
    """Mock FSM context."""
    
    def __init__(self):
        self._state = None
        self._data = {}
    
    async def get_state(self):
        return self._state
    
    async def set_state(self, state):
        self._state = state
    
    async def get_data(self):
        return self._data.copy()
    
    async def update_data(self, **kwargs):
        self._data.update(kwargs)
    
    async def clear(self):
        self._state = None
        self._data = {}


def test_questions_defined():
    """Test that QUESTIONS list is properly defined."""
    from handlers.feature import QUESTIONS
    
    assert len(QUESTIONS) == 7
    assert all(isinstance(q, str) for q in QUESTIONS)


def test_states_defined():
    """Test that FSM states are properly defined."""
    from handlers.feature import QuizStates, STATES_LIST
    
    assert len(STATES_LIST) == 7
    assert QuizStates.q1 in STATES_LIST
    assert QuizStates.q7 in STATES_LIST


def test_help_command():
    """Test /help command handler."""
    from handlers.feature import help_cmd
    
    message = MockMessage("/help")
    asyncio.run(help_cmd(message))
    
    message.answer.assert_called_once()
    call_args = message.answer.call_args
    assert "Lead Quiz Bot" in call_args[0][0]


def test_start_quiz():
    """Test quiz start."""
    from handlers.feature import start_quiz, QuizStates
    
    async def run_test():
        message = MockMessage("квиз")
        state = MockFSMContext()
        await start_quiz(message, state)
        return message, state
    
    message, state = asyncio.run(run_test())
    
    message.answer.assert_called_once()
    assert asyncio.run(state.get_state()) == QuizStates.q1
    data = asyncio.run(state.get_data())
    assert data["answers"] == []


def test_cancel_quiz_no_active():
    """Test /cancel when no quiz is active."""
    from handlers.feature import cancel_quiz
    
    async def run_test():
        message = MockMessage("/cancel")
        state = MockFSMContext()
        await cancel_quiz(message, state)
        return message
    
    message = asyncio.run(run_test())
    
    message.answer.assert_called_once()
    assert "Нет активного" in message.answer.call_args[0][0]


def test_cancel_quiz_active():
    """Test /cancel when quiz is active."""
    from handlers.feature import cancel_quiz, QuizStates
    
    async def run_test():
        message = MockMessage("/cancel")
        state = MockFSMContext()
        await state.set_state(QuizStates.q3)
        await cancel_quiz(message, state)
        return message, state
    
    message, state = asyncio.run(run_test())
    
    message.answer.assert_called_once()
    assert "отменён" in message.answer.call_args[0][0]
    assert asyncio.run(state.get_state()) is None


def test_process_answer_next_question():
    """Test answering moves to next question."""
    from handlers.feature import process_answer, QUESTIONS
    
    async def run_test():
        message = MockMessage("Иван")
        state = MockFSMContext()
        await state.update_data(answers=[])
        await process_answer(message, state, 0)
        return message
    
    message = asyncio.run(run_test())
    
    message.answer.assert_called_once()
    # Should show question 2
    assert QUESTIONS[1] in message.answer.call_args[0][0]


def test_process_answer_final():
    """Test completing all questions."""
    from handlers.feature import process_answer
    
    async def run_test():
        message = MockMessage("@testcontact")
        state = MockFSMContext()
        await state.update_data(answers=["A1", "A2", "A3", "A4", "A5", "A6"])
        
        with patch('handlers.feature.save_lead', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = 1
            await process_answer(message, state, 6)
        
        return message, state
    
    message, state = asyncio.run(run_test())
    
    # Should thank user
    assert "Спасибо" in message.answer.call_args[0][0]
    # Should clear state
    assert asyncio.run(state.get_state()) is None
