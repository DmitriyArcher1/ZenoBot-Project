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
    <b>Команды бота:</b>
    
    <b>Добавить Задачу</b> - создать новую задачу
    <b>Мои Задачи</b> - посмотреть текущие задачи
    <b>Помощь</b> - непосредственно это сообщение
    
    <i>Бот создан командой ...</i>
    """
    await message.answer(help_text, parse_mode = "HTML")
    
@router.message(F.text == "Добавить задачу")
async def add_task_start(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task)
    await message.answer(
        "Отправь мне текст задачи, которую ты хочешь добавить:\n\n"
        "<i>Например: Сходить в магазин за молоком</i>",
        parse_mode = "HTML"
    )
    
@router.message(TaskStates.waiting_for_task)
async def add_task_finish(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task_text = message.text
    
    if user_tasks[user_id]:
        task_id = max(user_tasks[user_id].keys()) + 1
    else:
        task_id = 1
    
    user_tasks[user_id][task_id] = {
        "text": task_text,
        "done": False
    }
    
    await state.clear()
    await message.answer(
        f"Задача добавлена!\n\n"
        f"{task_text}",
        reply_markup = kb.get_main_menu_keyboard()
    )

@router.message(F.text == "Показать мои задачи")
async def show_tasks(message: Message):
    user_id = message.from_user.id
    
    if not user_tasks[user_id]:
        await message.answer(
            "У тебя пока нет задач.\n\n"
            "Нажми 'Добавить задачу' для создания новой!"
        )
        return
    
    total = len(user_tasks[user_id])
    done = sum(1 for t in user_tasks[user_id].values() if t["done"])
    
    await message.answer(
        f"<b>Твои задачи</b> ({done}/{total} выполнено):\n\n"
        "<i>Нажми на задачу для действий с ней</i>",
        reply_markup = kb.get_tasks_keyboard(user_tasks[user_id]),
        parse_mode = "HTML"
    )