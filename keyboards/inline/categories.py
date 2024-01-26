from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db

category_cb = CallbackData('category', 'id', 'action')


def categories_markup():

    global category_cb
    
    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title, callback_data=category_cb.new(id=idx, action='view')))

    markup.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return markup


res_cb = CallbackData('res', 'id', 'action')


def res_markup():
    global res_cb

    markup = InlineKeyboardMarkup()
    for idx, title, body, _, _, _, _ in db.fetchall('SELECT * FROM products'):
        markup.add(InlineKeyboardButton(title, callback_data=res_cb.new(id=idx, action='view')))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='Loans'))

    return markup


def link_markup(name: str, link: str):
    global res_cb
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=name, url=link))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='country'))
    
    return markup


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Займы', callback_data='Loans'))
    markup.add(InlineKeyboardButton(text='Кредистория', callback_data='CreditHistory'), InlineKeyboardButton(text='Банкротство', callback_data='Bankruptcy'))
    markup.add(InlineKeyboardButton(text='Осаго', callback_data='OSAGO'))

    return markup