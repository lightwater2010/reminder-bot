from aiogram import Bot



async def send_note(bot: Bot, note_desc: str, id):
    await bot.send_message(id, text=f"Вам нужно будет {note_desc} !!!")