
import telebot
from telebot import types
from datetime import datetime, timedelta
import json
import os

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# === Глобальні змінні === #
allowed_users = set()
used_codes = set()
user_progress = {}
user_reminders = {}
user_scenarios = {}
codes = {"ABC123": "Digital", "XYZ456": "Lite"}  # Пример кодів доступу

# === Список команд (1-й рівень) === #
command_list = [
    "touch", "moon", "kiss", "hot", "fire", "love", "yes", "secret", "open", "lock",
    "mine", "blind", "claim", "tease", "wild", "slide", "whisper", "catch", "freeze", "hunt"
]

command_responses = {
    "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
    "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
    "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
    "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
    "fire": "Зніми щось із мене. Скажи: “Моє”.",
    "love": "Шепочи мені. А потім — зроби навпаки.",
    "yes": "Скажи це так, як ніколи не говорив. Потім покажи.",
    "secret": "Наш секрет — у цьому дотику.",
    "open": "Відчини. Можна лише губами.",
    "lock": "Замкни мене. Очима. Руками. Всім тілом.",
    "mine": "Притисни до себе. Скажи, що твоє.",
    "blind": "Зачини мені очі. І твори без зору.",
    "claim": "Укуси. Ніжно. І не зупиняйся.",
    "tease": "Дразни. Але не давай одразу.",
    "wild": "Тепер хижаком стану я. Не стримуй мене.",
    "slide": "Проведи долонею. Нижче.",
    "whisper": "Скажи мені щось, що збуджує лише тебе.",
    "catch": "Спіймай. І тримай.",
    "freeze": "Застигни. Я хочу роздивитися.",
    "hunt": "Знайди те, чого ще не було."
}

# === Обробка /start === #
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        bot.send_message(user_id, "🦊 Гра почалась!

Пиши слово на своєму тілі. Партнер — знаходить. Вводить сюди. А Foxie відповідає… бажанням 😈")
        user_progress[user_id] = []
        user_scenarios[user_id] = 1
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("В мене є код доступу", callback_data="enter_code"))
        bot.send_message(user_id, "Привіт! Це Foxie Code — гра для вас і вашої пристрасті 🦊

Щоб почати, потрібен доступ.", reply_markup=markup)

# === Код доступу === #
@bot.callback_query_handler(func=lambda call: call.data == "enter_code")
def prompt_access_code(call):
    bot.send_message(call.message.chat.id, "Введи свій код доступу:")

@bot.message_handler(func=lambda m: m.text in codes and m.from_user.id not in allowed_users)
def process_code(message):
    code = message.text.strip()
    user_id = message.from_user.id
    if code in used_codes:
        bot.send_message(user_id, "Цей код вже використано 🦊")
    else:
        allowed_users.add(user_id)
        used_codes.add(code)
        user_progress[user_id] = []
        user_scenarios[user_id] = 1
        bot.send_message(user_id, "Доступ надано! Твоя пригода починається прямо зараз 🦊")
        handle_start(message)

# === Команди гри === #
@bot.message_handler(func=lambda message: message.from_user.id in allowed_users)
def game_logic(message):
    user_id = message.from_user.id
    word = message.text.strip().lower()

    scenario = user_scenarios.get(user_id, 1)
    progress = user_progress.setdefault(user_id, [])

    if scenario == 1:
        if word in command_list and word not in progress:
            progress.append(word)
            bot.send_message(user_id, command_responses[word])
            if len(progress) == 20:
                bot.send_message(user_id, "Foxie з вами прощається… до наступної гри.")
        elif word in progress:
            bot.send_message(user_id, "🦊 Цю команду вже було. Спробуй іншу!")
        else:
            bot.send_message(user_id, "Пфф… Такої команди в мене немає 🦊 Спробуй ще")

# === /add — додати вручну користувача === #
@bot.message_handler(commands=["add"])
def manual_add(message):
    if str(message.from_user.id) != "572069105":
        return
    try:
        target_id = int(message.text.split()[1])
        allowed_users.add(target_id)
        bot.send_message(message.chat.id, f"Користувача {target_id} додано 🦊")
    except:
        bot.send_message(message.chat.id, "Неправильний формат. Спробуй /add ID")

# === Запуск бота === #
print("Foxie Bot is running...")
bot.polling()
