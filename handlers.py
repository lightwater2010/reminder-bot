from aiogram import F, Router, types, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import start_inline_kb, inline_all_notes, notes, inline_all_notes_to_update, inline_all_notes_to_delete, inline_notes_buttons_with_update, inline_notes_buttons_with_delete, inline_back_to_notes 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import apsched

class Note(StatesGroup):
    name = State()
    description = State()
    date_to_receive_note = State()

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(f"<b>Привет <u>{message.chat.username}</u>!\nСоздавай заметки в моём боте и ты ничего не забудешь!</b>", parse_mode="HTML", reply_markup=start_inline_kb)

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("<b><i>/start</i></b> - начало\n<b><i>/help</i></b> - список команд", parse_mode="HTML")

@router.message(F.text == "Создать заметку")
async def create_note1(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(Note.name)
    await message.answer("Напишите имя заметки:")

@router.message(Note.name)
async def create_note2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Note.description)
    await message.answer("Напишите описание вышей заметки:")

@router.message(Note.description)
async def create_note3(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Note.date_to_receive_note)
    await message.answer("Напишите дату и время когда вам напомнить о заметке (2024-05-20 20:00):")

@router.message(Note.date_to_receive_note)
async def create_note4(message: types.Message, state: FSMContext, apscheduler: AsyncIOScheduler, bot:Bot):
    await state.update_data(date_to_receive_note=message.text)
    data = await state.get_data()
    name = data['name']
    description = data['description']
    time = data['date_to_receive_note']
    time_to_scheduler = time.replace("-"," ").replace(":", " ")
    time_to_scheduler_list = list(map(int, time_to_scheduler.split()))
    year = time_to_scheduler_list[0]
    month = time_to_scheduler_list[1]
    day = time_to_scheduler_list[2]
    hour = time_to_scheduler_list[3]
    minutes = time_to_scheduler_list[4]
    date = datetime.datetime(year, month, day, hour, minutes)
    apscheduler.add_job(apsched.send_note, trigger="date", run_date=date, kwargs={"bot":bot, "note_desc":description, "id":message.from_user.id})
    await message.answer(f"Заметка '{name}' была создана создана!")    
    await state.clear()

@router.message(F.text == 'Все заметки')
async def all_notes(message: types.Message):
    await message.delete()
    await message.answer("Выберите одну из них:",reply_markup=await inline_all_notes())

@router.callback_query(F.data.count("back_to_notes"))
async def back_to_notes(callback: types.CallbackQuery):
    if "update" in callback.data:
        return await callback.message.edit_text("Выберите заметку, которую хотите изменить",reply_markup=await inline_all_notes_to_update())
    elif "delete" in callback.data:
        return await callback.message.edit_text("Выберите заметку, которую хотите удалить",reply_markup=await inline_all_notes_to_delete())
    else:
        return await callback.message.edit_text("Выберите одну из них:",reply_markup=await inline_all_notes())
@router.callback_query()
async def about_note(callback: types.CallbackQuery):
    notes_names = [note for note in notes.keys()]
    if callback.data in notes_names:
        description = notes[callback.data]['description']
        date = notes[callback.data]['date_to_receive_note']
        await callback.message.edit_text(f"Название: {callback.data} \nОписание: {description}\nВремя: {date}", reply_markup=inline_back_to_notes)
    elif "update_" in callback.data:
        note_name = callback.data.replace("update_","")
        description = notes[note_name]['description']
        date = notes[note_name]['date_to_receive_note']
        await callback.message.edit_text(f"Название: {note_name} \nОписание: {description}\nВремя: {date}", reply_markup=inline_notes_buttons_with_update)
    elif "delete_" in callback.data:
        note_name = callback.data.replace("delete_","")
        description = notes[note_name]['description']
        date = notes[note_name]['date_to_receive_note']
        await callback.message.edit_text(f"Название: {note_name} \nОписание: {description}\nВремя: {date}", reply_markup=inline_notes_buttons_with_delete)
@router.message(F.text == "Изменить заметку")
async def update_note(message: types.Message):
    await message.delete()
    await message.answer("Выберите заметку, которую хотите изменить", reply_markup=await inline_all_notes_to_update())
@router.message(F.text == "Удалить заметку")
async def delete_note(message: types.Message):
    await message.delete()
    await message.answer("Выбери заметку, которую хотите удалить", reply_markup=await inline_all_notes_to_delete())

