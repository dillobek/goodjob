import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.phone import get_number, start, yes_no
from keyboards.default.all_admin_buttons import first
from states.anketa import UserState

from data.config import ADMINS
from loader import dp, bot, db



@dp.message_handler(commands="start", user_id=ADMINS)
async def hi_admin(message: types.message):
    await message.answer(f"Assalamu hurmatli admin", reply_markup=first)

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fullname = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=fullname)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)
    await message.answer(f"Assalamu alaykum <b>GooD JoB</b> rasmiy botiga hush kelibsiz!\n\n"
                         f"Iltimos sizning rezyume va vakansiyangizni joylashimiz uchun savollarning barchasiga aniq javob bering!\n\n"
                         f"Tugmani tanlab arizani to'ldirishni boshlang!"
                         ,reply_markup=start)

@dp.message_handler(text="Rezyume")
async def bot_boshla(message:types.Message):
    await message.answer("To'liq ismingizni kiriting\n\nMasalan: <b>Saydullo Xaydarov</b>", reply_markup=ReplyKeyboardRemove())
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def answer_fullname(message: types.Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {"name": name}
        )
        await message.answer("Tug'ulgan yilingizni kiriting! (1980-2015)")
        await UserState.year.set()

@dp.message_handler(state=UserState.year)
async def answer_year(message: types.Message, state: FSMContext):
   # year =int(message.text)
    try:
        year = int(message.text)
        if year >= 1970 and year <= 2010:
            await state.update_data(
                {"year": year}
                )
            await message.answer("Telefon raqam jo'nating", reply_markup=get_number)
            await UserState.phone.set()
        else:
            await message.answer("iltimos tekshirib qayta kiriting")
    except Exception:
        await message.answer("iltimos tekshirib qayta kiriting")

@dp.message_handler(content_types='contact', state=UserState.phone)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    await state.update_data(
        {"phone": phone}
    )
    await message.answer("Qo'shimcha raqam kiriting!\n\nMasalan: <b>+998994359365</b>", reply_markup=ReplyKeyboardRemove())
    await UserState.sphone.set()

@dp.message_handler(state=UserState.sphone)
async def answer_sphone(message: types.Message, state:FSMContext):
    sphone = message.text
    if sphone.startswith("+998"):

        await state.update_data(
            {"sphone":sphone}
        )
        await message.answer("Iltimos sohangizni kiriting.\n\nMasalan: <b>Digital Marketolog</b>!")
        await UserState.job.set()

    else:
        await message.answer("Iltimos tekshirib qaytadan kiriting!")

@dp.message_handler(state=UserState.job)
async def enter_job(message:types.Message, state: FSMContext):
    job = message.text
    if job.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {'job': job}
        )
        await message.answer("Bu sohada qancha tajribangiz bor ?")
        await UserState.jobexperience.set()

@dp.message_handler(state=UserState.jobexperience)
async def enter_jobex(message:types.Message, state:FSMContext):
    jobexperience = message.text
    await state.update_data(
        {"jobexperience":jobexperience}
    )

    await message.answer("Qancha maosh hohlamoqdasiz ?\n\nMasalan: <b>2000000</b>")
    await UserState.salary.set()

@dp.message_handler(state=UserState.salary)
async def enter_salary(message:types.Message, state:FSMContext):
    salary = message.text
    if salary.isdigit():
        await state.update_data(
            {"salary":salary}
        )
        await message.answer("Iltimos o'zingiz haqingizda qisqacha ma'lumot bering.\n\n<b>Masalan:</b>\nHozirda freelancer bo'lib ishlab kelmoqdaman. Ingliz va Rus tillarida gaplasha olaman. Word & Exel dasturlarida ishlay olaman.")
        await UserState.about.set()
    else:
        await message.answer("Iltimos maoshni to'g'ri kiriting!\n\nMasalan: <b>2000000</b>")

@dp.message_handler(state=UserState.about)
async def enter_region(message:types.Message, state:FSMContext):
    about = message.text
    if about.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting")
    else:
        await state.update_data(
            {"about": about}
        )
        await message.answer("Iltimos Viloyatingizni kiriting!\n\n<b>Bu ish beruvchi uchun muhim</b>")
        await UserState.region.set()

@dp.message_handler(state=UserState.region)
async def enter_find(message:types.Message, state:FSMContext):
    region = message.text
    await state.update_data(
        {"region":region}
    )
    await message.answer("Iltimos arizani yakunlash uchun rasm yuboring!\n\n<b>Bu rasm vebsaytga qo'yiladi iltimos e'tiborliroq bo'ling</b>")
    await UserState.photo.set()

@dp.message_handler(state=UserState, content_types=types.ContentType.PHOTO)
async def enter_photo(message:types.Message, state:FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(
        {"photo":photo}
    )

    data = await state.get_data()
    photo = f"{data['photo']}"
    msg = "<b>Quyidagi ma'lumotlar qabul qilindi</b>\n\n"
    msg += f"1. Ismingiz ➖ {data['name']}\n\n"
    msg += f"2. yilingiz ➖ {data['year']}\n\n"
    msg += f"3. Telefon ➖ {data['phone']}\n\n"
    msg += f"4. Qo'shimcha tel➖ {data['sphone']}\n\n"
    msg += f"5. Yuborgan sohangiz ➖ {data['job']}\n\n"
    msg += f"6. Tajribangiz ➖ {data['jobexperience']}\n\n"
    msg += f"7. Maosh ➖ {data['salary']}\n\n"
    msg += f"8. Viloyatingiz ➖ {data['region']}\n\n"
    msg += f"9. O'zingiz haqingizda ➖ {data['about']}\n\n"

    await message.answer_photo(photo= photo, caption=msg)
    await message.answer(f"<b>Tasdiqlaysizmi? </b>\n", reply_markup=yes_no)
    await UserState.check.set()

@dp.message_handler(state = UserState.check)
async def fiveteen(message: types.Message, state: FSMContext):
    matn = message.text
    if matn == "✅ Ha":

        data = await state.get_data()
        photo = f"{data['photo']}"
        msg = "<b>Quyidagi ma'lumotlar qabul qilindi</b>\n\n"
        msg += f"1. Ismi ➖ {data['name']}\n\n"
        msg += f"2. yili ➖ {data['year']}\n\n"
        msg += f"3. Telefon ➖ {data['phone']}\n\n"
        msg += f"4. Qo'shimcha tel➖ {data['sphone']}\n\n"
        msg += f"5. Mutahasisligi ➖ {data['job']}\n\n"
        msg += f"6. Tajribasi ➖ {data['jobexperience']}\n\n"
        msg += f"7. So'rayotgan maosh ➖ {data['salary']}\n\n"
        msg += f"8. Viloyati ➖ {data['region']}\n\n"
        msg += f"8. O'zi haqida ➖ {data['about']}\n\n"


        await bot.send_photo(chat_id=-1001882349838, photo=photo, caption=msg)
        await message.answer("Biz 72 soat ichida saytga yuklab qo'yamiz!", reply_markup=start)
    elif matn == "❌ Yo'q":
        await message.answer("Elon bekor qilindi\n\nBoshqatdan boshlashingiz mumkin!", reply_markup=start)


