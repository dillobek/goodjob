from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.phone import get_number, start, yes_no
from states.anketa import VacancyState

from data.config import ADMINS
from loader import dp, bot, db


@dp.message_handler(text="Vakansiya")
async def select_button(message:types.Message):
    await message.answer("Companiya nomini kiriting!\n\nMasalan: <b>GooD JoB</b>", reply_markup=ReplyKeyboardRemove())
    await VacancyState.cname.set()

@dp.message_handler(state=VacancyState.cname)
async def answer_fullname(message: types.Message, state: FSMContext):
    cname = message.text
    if cname.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {"cname": cname}
        )
        await message.answer("Ishlash tartibi: Online & Offline")
        await VacancyState.type.set()

@dp.message_handler(state=VacancyState.type)
async def answer_fullname(message: types.Message, state: FSMContext):
    type = message.text
    if type.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {"type": type}
        )
        await message.answer("Vakansiya turi\n\nMasalan: <b>Digital Marketing </b>")
        await VacancyState.job.set()

@dp.message_handler(state=VacancyState.job)
async def answer_fullname(message: types.Message, state: FSMContext):
    job = message.text
    if job.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {"job": job}
        )
        await message.answer("Tajribasi\n\nMasalan: <b>3 yil</b>")
        await VacancyState.jobexperience.set()


@dp.message_handler(state=VacancyState.jobexperience)
async def answer_fullname(message: types.Message, state: FSMContext):
    jobexperience = message.text
    await state.update_data(
        {"jobexperience": jobexperience}
    )
    await message.answer("Telefon raqam yuboring", reply_markup=get_number)
    await VacancyState.phone.set()

@dp.message_handler(content_types='contact', state=VacancyState.phone)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    await state.update_data(
        {"phone": phone}
    )
    await message.answer("Qo'shimcha raqam kiriting!\n\nMasalan: <b>+998994359365</b>", reply_markup=ReplyKeyboardRemove())
    await VacancyState.sphone.set()

@dp.message_handler(state=VacancyState.sphone)
async def answer_sphone(message: types.Message, state:FSMContext):
    sphone = message.text
    if sphone.startswith("+998"):

        await state.update_data(
            {"sphone":sphone}
        )
        await message.answer("Qancha maosh taklif qilasiz ?\n\nMasalan: <b>2000000</b>")
        await VacancyState.salary.set()

    else:
        await message.answer("Iltimos tekshirib qaytadan kiriting!")

@dp.message_handler(state=VacancyState.salary)
async def enter_salary(message:types.Message, state:FSMContext):
    salary = message.text
    if salary.isdigit():
        await state.update_data(
            {"salary":salary}
        )
        await message.answer("Iltimos viloyatni kiriting.\n\n<b>Masalan:</b>\nAndijon")
        await VacancyState.region.set()
    else:
        await message.answer("Iltimos maoshni to'g'ri kiriting!\n\nMasalan: <b>2000000</b>")

@dp.message_handler(state=VacancyState.region)
async def enter_find(message:types.Message, state:FSMContext):
    region = message.text
    await state.update_data(
        {"region":region}
    )
    await message.answer("Iltimos arizani yakunlash uchun qisqa ma'lumot yuboring!")
    await VacancyState.about.set()

@dp.message_handler(state=VacancyState.about)
async def enter_region(message:types.Message, state:FSMContext):
    about = message.text
    if about.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting")
    else:
        await state.update_data(
            {"about": about}
        )
    await message.answer("Iltimos arizani yakunlash uchun rasm yuboring!\n\n<b>Bu rasm vebsaytga qo'yiladi iltimos e'tiborliroq bo'ling</b>")
    await VacancyState.photo.set()

@dp.message_handler(state=VacancyState, content_types=types.ContentType.PHOTO)
async def enter_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(
        {"photo": photo}
    )
    data = await state.get_data()
    photo = f"{data['photo']}"

    msg = "<b>Quyidagi ma'lumotlar qabul qilindi</b>\n\n"
    msg += f"1. Kompaniya nomi ➖ {data['cname']}\n\n"
    msg += f"2. Ish turi ➖ {data['type']}\n\n"
    msg += f"3. Vakansiya ➖ {data['job']}\n\n"
    msg += f"4. Tajriba➖ {data['jobexperience']}\n\n"
    msg += f"5. Telefon ➖ {data['phone']}\n\n"
    msg += f"6. qo'shimcha tel ➖ {data['sphone']}\n\n"
    msg += f"7. Maosh ➖ {data['salary']}\n\n"
    msg += f"8. Viloyat ➖ {data['region']}\n\n"
    msg += f"9. Ish haqida ➖ {data['about']}\n\n"

    await message.answer_photo(photo=photo, caption=msg)
    await message.answer(f"<b>Tasdiqlaysizmi? </b>\n", reply_markup=yes_no)
    await VacancyState.check.set()


@dp.message_handler(state = VacancyState.check)
async def fiveteen(message: types.Message, state: FSMContext):
    matn = message.text
    if matn == "✅ Ha":
        data = await state.get_data()
        photo = f"{data['photo']}"

        msg = "<b>Quyidagi vakansiya qabul qilindi</b>\n\n"
        msg += f"1. Kompaniya nomi ➖ {data['cname']}\n\n"
        msg += f"2. Ish turi ➖ {data['type']}\n\n"
        msg += f"3. Vakansiya ➖ {data['job']}\n\n"
        msg += f"4. Tajriba➖ {data['jobexperience']}\n\n"
        msg += f"5. Telefon ➖ {data['phone']}\n\n"
        msg += f"6. qo'shimcha tel ➖ {data['sphone']}\n\n"
        msg += f"7. Maosh ➖ {data['salary']}\n\n"
        msg += f"8. Viloyat ➖ {data['region']}\n\n"
        msg += f"9. Ish haqida ➖ {data['about']}\n\n"
        msg += f"10. Username ➖ {message.from_user.username}\n\n"


        await bot.send_photo(chat_id=-1001882349838, photo=photo, caption=msg)
        await message.answer("<b>Vakansiya qabul qilindi!\n\n24 soat ichida kanalga\n48 soat ichida vebsaytga yuklanadi", reply_markup=start)
    elif matn == "❌ Yo'q":
        await message.answer("Elon bekor qilindi\n\nBoshqatdan boshlashingiz mumkin!", reply_markup=start)