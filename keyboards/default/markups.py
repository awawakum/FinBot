from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db

back_message = '👈 Назад'
confirm_message = '✅ Подтвердить заказ'
all_right_message = '✅ Все верно'
cancel_message = '🚫 Отменить'

res_cb = CallbackData('res', 'id', 'action')

def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(confirm_message)
    markup.add(back_message)

    return markup

def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message)

    return markup

def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)

    return markup

def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(cancel_message, all_right_message)

    return markup

def category_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    


    markup.row(cancel_message)

def product_markup():

    global res_cb
    
    category_cb = CallbackData('category', 'id', 'action')
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    for idx, title, body, _, _, _, _ in db.fetchall('SELECT * FROM products'):
        markup.add(markup.row(title, callback_data=res_cb.new(id=idx, action='view')))

    markup.row(cancel_message)

    return markup