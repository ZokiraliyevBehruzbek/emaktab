from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import database
from datetime import datetime

API_TOKEN = '7302138312:AAHEoY-o5wxTMUe4v8BrLPqsEKyYsZE1h24' 
ADMIN_ID = 5497388269  # Adminning Telegram ID sini qo'ying
CHANNEL_ID = '@dium_15'  # Sizning kanal nomi yoki ID sini qo'ying

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Botni boshlanganda foydalanuvchini qo'shish
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ''
    username = message.from_user.username or ''
    last_active = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Foydalanuvchini faqat birinchi marta qo'shish
    existing_users = database.get_users()
    user_ids = [user[1] for user in existing_users]
    
    if user_id not in user_ids:
        database.add_user(user_id, first_name, last_name, username, last_active)
    
    # Obuna holatini tekshirish
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Kundalik.com ga kirish uchun bosing! ✅", web_app=types.WebAppInfo(url='https://login.emaktab.uz'))
            keyboard.add(button)
            await message.answer("Assalomu alaykum kundalik.com ning kichik telegram botiga xush kelibsiz!:", reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            subscribe_button = InlineKeyboardButton(text="Kanalga obuna bo'ling", url=f"t.me/{CHANNEL_ID.strip('@')}")
            check_button = InlineKeyboardButton(text="Obuna bo'ldim ✅", callback_data='check_subscription')
            keyboard.add(subscribe_button, check_button)
            await message.answer("Siz kanalga obuna bo'lishingiz kerak. Obuna bo'lganingizdan so'ng tekshirish uchun tugmani bosing.", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

# /admin buyruqni qabul qilish va admin panelni ko'rsatish
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(row_width=2)
        start_time_button = InlineKeyboardButton(text="Bot ishga tushgan vaqti", callback_data='bot_start_time')
        users_info_button = InlineKeyboardButton(text="Foydalanuvchilar ma\'lumotlari", callback_data='users_info')
        user_count_button = InlineKeyboardButton(text="Foydalanuvchilar soni", callback_data='users_count')
        keyboard.add(start_time_button, users_info_button, user_count_button)
        await message.answer("Admin panelga xush kelibsiz🔐:", reply_markup=keyboard)
    else:
        await message.answer("Siz ushbu ma'lumotlarga kirish huquqiga ega emassiz.")

# Callback querylarni qayta ishlash
@dp.callback_query_handler(lambda c: c.data in ['bot_start_time', 'users_info', 'users_count', 'check_subscription'])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ADMIN_ID:
        if callback_query.data == 'bot_start_time':
            start_time = database.get_bot_start_time()
            await callback_query.message.answer(f"Bot started at: {start_time}")
        elif callback_query.data == 'users_info':
            users = database.get_users()
            if users:
                users_info = '\n'.join([
                    f"ID: {user[0]}, User ID: {user[1]}, Name: {user[2]} {user[3]}, Username: @{user[4]}, Last Active: {user[5]}"
                    for user in users
                ])
                await callback_query.message.answer(f"Users Info:\n{users_info}")
            else:
                await callback_query.message.answer("No users found.")
        elif callback_query.data == 'users_count':
            user_count = database.get_user_count()
            await callback_query.message.answer(f"Barcha foydalanuvchilar soni: {user_count}")
        elif callback_query.data == 'check_subscription':
            user_id = callback_query.from_user.id
            try:
                chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
                if chat_member.status in ['member', 'administrator', 'creator']:
                    keyboard = InlineKeyboardMarkup()
                    button = InlineKeyboardButton(text="Kundalik.com ga kirish uchun bosing! ✅", web_app=types.WebAppInfo(url='https://login.emaktab.uz'))
                    keyboard.add(button)
                    await callback_query.message.answer("Xush kelibsiz. Kundalik.com ga kirish uchun pastdagi knopkani bosing", reply_markup=keyboard)
                else:
                    await callback_query.message.answer("Siz kanalga obuna bo'lmagansiz.")
            except Exception as e:
                await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")
    else:
        await callback_query.answer("Siz ushbu ma'lumotlarga kirish huquqiga ega emassiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
