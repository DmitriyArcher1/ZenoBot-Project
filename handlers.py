from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards as kb

router = Router()

user_tasks = {}

class TaskStates(StatesGroup):
    waiting_for_task = State()
    
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_tasks:
        user_tasks[user_id] = {}
    
    await message.answer(
        f" Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе управлять задачами.\n"
        "Выбери действие:",
        reply_markup = kb.get_main_menu_keyboard()
    )

@router.message(Command("help"))
@router.message(F.text == " Помощь")
async def cmd_help(message: Message):
    help_text = """
    
    """