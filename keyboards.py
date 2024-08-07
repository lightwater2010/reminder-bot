from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_inline_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать заметку"),KeyboardButton(text="Все заметки")],
    [KeyboardButton(text="Изменить заметку"),KeyboardButton(text="Удалить заметку")]
],resize_keyboard=True)

notes = {
    "Мусор":{"description":"Выбросить мусор", "date_to_receive_note":"8:00"}, 
    "ДЗ":{"description":"Сделать домашку по алгебре", "date_to_receive_note":"19:30"},
    "Душ":{"description":"Принять душ переде сном", "date_to_receive_note":"22:30"},
}

async def inline_all_notes():
    kb = InlineKeyboardBuilder()
    for note in notes:
        kb.add(InlineKeyboardButton(text=note, callback_data=note))
    return kb.adjust(2).as_markup()

async def inline_all_notes_to_update():
    kb = InlineKeyboardBuilder()
    for note in notes:
        kb.add(InlineKeyboardButton(text=note, callback_data="update_"+note))
    return kb.adjust(2).as_markup()

async def inline_all_notes_to_delete():
    kb = InlineKeyboardBuilder()
    for note in notes:
        kb.add(InlineKeyboardButton(text=note, callback_data="delete_"+note))
    return kb.adjust(2).as_markup()

#НАДО СДЕЛАТЬ НЕ ТРИ КЛАВИАТУРЫ А ОДНУ InlineKeyboardBuilder()

inline_notes_buttons_with_update = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Назад", callback_data="back_to_notes_update"),
    InlineKeyboardButton(text="Обновить заметку", callback_data="update_note")
]])
inline_notes_buttons_with_delete = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Назад", callback_data="back_to_notes_delete"),
    InlineKeyboardButton(text="Удалить заметку", callback_data="delete_note")
]])

inline_back_to_notes = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Назад", callback_data='back_to_notes')
]])



