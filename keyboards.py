from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура главного меню для бота. Содержит кнопки для добавления задачи, просмотра задач и удаления задачи.

    Returns:
        ReplyKeyboardMarkup: Клавиатура главного меню с кнопками для добавления задачи, просмотра задач и удаления задачи
    """
    builder = ReplyKeyboardBuilder()
    
    builder.add(KeyboardButton(text = "Добавить задачу"))
    builder.add(KeyboardButton(text = "Показать мои задачи"))
    builder.add(KeyboardButton(text = "Удалить задачу"))
    builder.adjust(2, 1)
    
    return builder.as_markup(resize_keyboard = True)


def get_tasks_keyboard(tasks: dict) -> InlineKeyboardMarkup:
    """Клавиатура для отображения списка задач пользователя. Каждая задача отображается с иконкой статуса (выполнена или нет) и обрезанным текстом задачи.

    Args:
        tasks (dict): Словарь задач, где ключ - ID задачи, а значение - словарь с информацией о задаче (текст и статус выполнения)

    Returns:
        InlineKeyboardMarkup: Клавиатура с задачами
    """
    builder = InlineKeyboardBuilder()
    
    for task_id, task in tasks.items():
        status = "✅" if task['done'] else "❌"
        builder.button(
            text = f"{status} {task['text'][:30]}",
            callback_data = f"task_{task_id}"
        )
        
    builder.adjust(1)
    
    return builder.as_markup()

def get_task_actions(task_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для действий с задачей: отметить как выполненную, удалить, вернуться к списку задач

    Args:
        task_id (int): ID задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура с действиями для задачи
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(text = "Отметить как выполненную", callback_data = f"done_{task_id}")
    builder.button(text = "Удалить задачу", callback_data = f"delete_{task_id}")
    builder.button(text = "Назад к списку задач", callback_data = "back_to_tasks")
    
    builder.adjust(2, 1)
    
    return builder.as_markup()

def get_task_done(task_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для отображения статуса задачи после её выполнения. Содержит кнопку для возврата к списку задач.

    Args:
        task_id (int): ID задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой для возврата к списку задач
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(text = "Назад к списку задач", callback_data = "back_to_tasks")
    builder.button(text = "Удалить задачу", callback_data = f"delete_{task_id}")
    
    builder.adjust(1, 2)
    
    return builder.as_markup()