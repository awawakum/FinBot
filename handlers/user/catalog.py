import imghdr
import logging
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.categories import categories_markup, category_cb, res_markup, res_cb, link_markup
from keyboards.inline.products_from_catalog import product_cb, product_markup
from aiogram.utils.callback_data import CallbackData
from aiogram.types.chat import ChatActions
from aiogram.types.input_media import InputMedia
from loader import dp, db, bot
from .menu import loans
from filters import IsUser, IsAdmin
import json
import base64


@dp.message_handler(IsUser(), text=loans)
async def process_catalog(message: Message):
    await message.answer('Выберите страну:',
                         reply_markup=categories_markup())

@dp.callback_query_handler(lambda c: c.data == 'country')
async def process_catalog(query: CallbackQuery):
    await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)

@dp.callback_query_handler(lambda c: c.data == 'Loans')
async def process_catalog(query: CallbackQuery):
    await bot.edit_message_text(text='Выберите страну:', chat_id=query.message.chat.id, message_id=query.message.message_id,
                           reply_markup=categories_markup())

@dp.callback_query_handler(IsUser(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict):

    products = db.fetchall('''SELECT * FROM products product
    WHERE product.tag = (SELECT title FROM categories WHERE idx=?)''',
                           [callback_data['id']])

    await query.answer('Все доступные ресурсы.')
    await get_res_buttons(query.message, products)


async def get_res_buttons(m, products):

    if len(products) == 0:

        await m.answer('Здесь ничего нет 😢')
        await process_catalog(m)

    else:

        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)

        await bot.edit_message_text(message_id=m.message_id, chat_id=m.chat.id, text='Доступные ресурсы: ')
        await bot.edit_message_reply_markup(message_id=m.message_id, chat_id=m.chat.id, reply_markup=res_markup(products))


@dp.callback_query_handler(IsUser(), res_cb.filter(action='view'))
async def res_callback_handler(query: CallbackQuery, callback_data: dict):
    resources = db.fetchall('''SELECT * FROM products WHERE idx =?''', (callback_data['id'], ))
    await bot.send_photo(chat_id=query.message.chat.id, photo=resources[0][3], caption=str(resources[0][1]), reply_markup=link_markup(resources[0][1], resources[0][2]))
