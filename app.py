import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from data import config
from handlers.user import menu
from keyboards.inline.categories import menu_markup
from loader import dp, bot, db
import filters
import logging

filters.setup(dp)


user_message = 'Пользователь'
admin_message = 'Админ'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    user = db.is_user(message.chat.id)
    if not user:
        db.add_user(message.chat.id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if message.from_user.id in config.ADMINS:
        markup.row(user_message, admin_message)
    else:
        markup = await menu.get_user_menu()

    await message.answer('''😳Срочно нужны деньги ?
🤑 Тогда добро пожаловать в ваш бот
😎Дорогие друзья! 
Если вы попали в тяжёлую финансовую ситуацию или вы не знаете где взять деньги до ЗП то милости просим к нам 🤗
Здесь представлен список быстро займов где вы можете без проблем взять деньги и при соблюдении правил избежать процентов. 💸
На большинстве сайтов есть акция " Первый займ под ноль процентов" используйте каждый раз новый сайты, что бы избежать переплат. Но не забывайте укладываться в беспроцентный период.⏳
  ''', reply_markup=menu_markup())


@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_catalog(query: CallbackQuery):
    await bot.edit_message_text(text='''😳Срочно нужны деньги ?
🤑 Тогда добро пожаловать в ваш бот
😎Дорогие друзья! 
Если вы попали в тяжёлую финансовую ситуацию или вы не знаете где взять деньги до ЗП то милости просим к нам 🤗
Здесь представлен список быстро займов где вы можете без проблем взять деньги и при соблюдении правил избежать процентов. 💸
На большинстве сайтов есть акция " Первый займ под ноль процентов" используйте каждый раз новый сайты, что бы избежать переплат. Но не забывайте укладываться в беспроцентный период.⏳
  ''', message_id=query.message.message_id, chat_id=query.message.chat.id, reply_markup=menu_markup())

@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    await handlers.user.menu.user_menu(message)
    await message.answer('Включен пользовательский режим.')


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        await handlers.user.menu.admin_menu(message)
        await message.answer('Включен админский режим.')


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()


async def on_shutdown():
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
