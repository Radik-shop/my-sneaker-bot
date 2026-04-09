import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() # Этот вызов "оживит" сервер для Render

import telebot
from telebot import types

# Настройки
token = '8752828930:AAGb21_s0gBdqeRx4HZA3CCzEvN87IlR4ng'
bot = telebot.TeleBot(token)

admin_nickname = "Radik_angel" 
card_number = "4400 4302 6543 2556"
card_holder = "Ратмир Т."
admin_id = 743054481

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть каталог")
    btn2 = types.KeyboardButton("О нас")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Салам, {message.from_user.first_name}! Выбери действие:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Посмотреть каталог":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Nike Air Force"), types.KeyboardButton("Adidas Forum Low"), types.KeyboardButton("Назад"))
        bot.send_message(message.chat.id, "Выбери модель:", reply_markup=markup)

    elif message.text == "Nike Air Force":
        url = 'https://cdn-images.farfetch-contents.com/19/30/28/51/19302851_42366110_600.jpg'
        cap = "<b>👟 Nike Air Force 1</b>\n💰 Цена: 55 000 ₸"
        send_item(message, url, cap)

    elif message.text == "Adidas Forum Low":
        url = 'https://a.lmcdn.ru/img600x866/A/D/AD093AMUNT26_5489896_1_v1.jpg'
        cap = "<b>👟 Adidas Forum Low</b>\n💰 Цена: 48 000 ₸"
        send_item(message, url, cap)

    elif message.text == "Назад":
        start(message)

    elif message.text == "О нас":
        bot.send_message(message.chat.id, "Лучший магазин кроссовок в Алматы! 🇰🇿")

def send_item(message, url, cap):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 Оплатить", callback_data="pay"))
    markup.add(types.InlineKeyboardButton("💬 Чат", url=f"https://t.me/{admin_nickname}"))
    bot.send_photo(message.chat.id, url, caption=cap, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "pay")
def pay(call):
    text = (f"<b>✅ Реквизиты для оплаты:</b>\n\n🏦 Kaspi.kz\n💳 Карта: <code>{card_number}</code>\n👤 ФИО: <b>{card_holder}</b>\n\n"
            f"‼️ Пришлите скриншот чека сюда.\nДоставка Яндекс (оплата при получении или сразу).")
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Чек получен! Выберите способ получения:", reply_markup=deliv_markup())
    bot.send_message(admin_id, f"💰 ЧЕК от @{message.from_user.username}")
    bot.forward_message(admin_id, message.chat.id, message.message_id)

def deliv_markup():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("🚕 Яндекс Доставка", callback_data="yandex"))
    m.add(types.InlineKeyboardButton("🏃‍♂️ Самовывоз", callback_data="self"))
    return m

@bot.callback_query_handler(func=lambda call: call.data in ["yandex", "self"])
def deliv_choice(call):
    if call.data == "yandex":
        m = bot.send_message(call.message.chat.id, "Напишите адрес и номер телефона для доставки (Яндекс):\n<i>Доставка за ваш счет.</i>", parse_mode='HTML')
        bot.register_next_step_handler(m, save_addr)
    else:
        bot.send_message(call.message.chat.id, "Напишите @Radik_angel для согласования самовывоза. 🤝")

def save_addr(message):
    bot.send_message(message.chat.id, "Данные приняты! Скоро свяжемся. ❤️")
    bot.send_message(admin_id, f"📍 АДРЕС: {message.text} от @{message.from_user.username}")

if __name__ == '__main__':
    # Эта строчка заставляет бота работать бесконечно
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
