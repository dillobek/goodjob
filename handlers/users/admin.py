import asyncio

from aiogram import types

from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext

from keyboards.default.all_admin_buttons import first
from keyboards.default.all_admin_buttons import tasdiq
from states.all_admin_states import post_send


from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(text="📤 Post yuborish", chat_id=ADMINS)
async def post(message: Message):
    await message.answer("Marhamat postingizni yuboring")
    await post_send.post.set()


@dp.message_handler(state=post_send.post, content_types=ContentType.ANY)
async def send_post(message: Message, state: FSMContext):
    await message.answer("Post aniqligiga ishonchingiz komilmi ?", reply_markup=tasdiq)
    await state.finish()


@dp.message_handler(text="✅ ha")
@dp.message_handler(text="❌ yo'q")
async def sending_post(message:Message):
    active = 0
    unactive = 0
    num_user = db.count_users()[0]
    count = 1
    c = 1


    if message.text == "✅ ha":
        await message.answer("post yuborilmoqda...")

        for data in db.select_all_users():
            try:
                await bot.copy_message(
                    chat_id = data[0],
                    from_chat_id = message.from_user.id,
                    message_id = message.message_id-2,
                )
                active += 1
                await asyncio.sleep(0.05)

            except Exception as ex:
                unactive += 1


        text = "post aktivlarga yuborildi\n\n"
        text += f"barcha foydalanuvchilar: {active + unactive}\n"
        text += f"activ users: {active}\n"
        text += f"uactive users: {unactive}\n"
        await message.answer(text=text, reply_markup=first)

    elif message.text=="❌ yo'q":
        await message.answer("post yuborilmadi", reply_markup=first)
