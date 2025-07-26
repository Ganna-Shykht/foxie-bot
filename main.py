
import telebot
from telebot import types
import random
import time

# === Конфігурація ===
TOKEN = 'ТВОЙ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

allowed_users = set()
used_codes = set()
user_commands_count = {}
gift_codes = {"ABC123": False, "XYZ789": False}  # Після оплати генеруємо нові
admin_id = 572069105  # Твій ID
second_level_users = set()
broadcast_optout = set()

# === Команди гри ===
commands = {
    "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
    "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
    "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
    "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
    "fire": "Зніми щось із мене. Скажи: “Моє”. І притисни мене ближче.",
    "love": "Скажи три речі, за які ти мене хочеш. І доведи.",
    "yes": "Скажи: “Так” — і дозволь мені більше.",
    "secret": "Прошепчи мені щось, що досі не казав.",
    "open": "Покажи мені те, що хочеш заховати.",
    "lock": "Закрий очі. І просто дозволь.",
    "mine": "Зроби щось, що доведе — я твоя.",
    "blind": "Зав’яжи мені очі. І веди.",
    "claim": "Поклади мою руку туди, де хочеш мене.",
    "tease": "Зупиняйся на півдорозі. І повторюй.",
    "wild": "Стань хижаком. Я твоя здобич.",
    "slide": "Проведи пальцями. Повільно. Ще раз.",
    "whisper": "Назви моє ім’я. Так, як ніколи не називав.",
    "catch": "Схопи мене. Раптово. І не відпускай.",
    "freeze": "Зупинись. Дивись мені в очі.",
    "hunt": "Натисни. Туди, де я найгарячіша."
}

# === Обробка старту ===
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        bot.send_message(user_id, "🦊 Гра почалась!

"
                                  "Ти пишеш слова на своєму тілі.
"
                                  "Партнер шукає їх за допомогою ліхтарика.
"
                                  "Що знайде — вводить сюди, в бот.

"
                                  "Foxie відповість… бажанням 😈")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🛍 Купити собі")
        btn2 = types.KeyboardButton("🎁 Подарувати")
        markup.add(btn1, btn2)
        bot.send_message(user_id, "Обери свою гру Foxie Code:", reply_markup=markup)

# === Обробка вибору ===
@bot.message_handler(func=lambda m: m.text in ["🛍 Купити собі", "🎁 Подарувати"])
def handle_choice(message):
    if message.text == "🛍 Купити собі":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Foxie Code Digital — 500 грн", "Foxie Code Lite Box — 800 грн")
        bot.send_message(message.chat.id, "Обери пакет:", reply_markup=markup)
    elif message.text == "🎁 Подарувати":
        bot.send_message(message.chat.id, "Напиши номер телефону або нік в Telegram того, кому даруєш:")
        bot.register_next_step_handler(message, handle_gift_recipient)

# === Обробка подарунка ===
def handle_gift_recipient(message):
    recipient = message.text.strip()
    code = random.choice(["ABC123", "XYZ789"])  # В майбутньому: згенерований код
    gift_codes[code] = False
    bot.send_message(admin_id, f"🎁 Подарунок для {recipient}. Код: {code}")
    bot.send_message(message.chat.id, f"Готово! Передай цей код: {code} — саме він відкриє доступ до гри 🦊")

# === Обробка введення коду ===
@bot.message_handler(func=lambda m: m.text in gift_codes.keys())
def activate_code(message):
    code = message.text.strip()
    user_id = message.from_user.id
    if gift_codes[code] == False:
        allowed_users.add(user_id)
        gift_codes[code] = True
        bot.send_message(user_id, "Код активовано! 🧡 Тепер ти можеш грати.")
        start(message)
    else:
        bot.send_message(user_id, "Цей код вже використано. 🛑")

# === Додати вручну ID користувача ===
@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id == admin_id:
        parts = message.text.split()
        if len(parts) == 2 and parts[1].isdigit():
            allowed_users.add(int(parts[1]))
            bot.send_message(admin_id, f"Користувач {parts[1]} доданий вручну.")
        else:
            bot.send_message(admin_id, "Невірна команда. Використай /add ID")

# === Список команд ===
@bot.message_handler(commands=['список', 'команди'])
def send_command_list(message):
    text = "Ось твої 20 команд Foxie Code з місцями напису:

"
    text += ("1. touch — Шия
2. moon — Плече
3. kiss — Зап’ястя
4. hot — Внутрішня сторона руки
"
             "5. fire — Стегно
6. love — Живіт
7. yes — Литка
8. secret — Талія
"
             "9. open — Внутрішня сторона стегна
10. lock — Підборіддя
11. mine — Коліно
"
             "12. blind — Груди
13. claim — Пальці рук
14. tease — Ліктьовий згин
"
             "15. wild — Щока
16. slide — Сідниця
17. whisper — Гомілка
"
             "18. catch — Шия ззаду
19. freeze — Живіт знизу
20. hunt — Живіт збоку")
    bot.send_message(message.chat.id, text)

# === Обробка гри ===
@bot.message_handler(func=lambda m: True)
def handle_game(message):
    user_id = message.from_user.id
    text = message.text.strip().lower()
    if user_id not in allowed_users:
        bot.send_message(user_id, "Для початку потрібно активувати гру 🧡")
        return
    if text in commands:
        count = user_commands_count.get(user_id, 0) + 1
        user_commands_count[user_id] = count
        bot.send_message(user_id, commands[text])
        if count == 20:
            bot.send_message(user_id, "Foxie з вами прощається… до наступної гри.")
        else:
            bot.send_message(user_id, "🦊 Чекаю на наступне слово…")
    else:
        bot.send_message(user_id, "Пфф… Такої команди в мене немає 🦊 Спробуй ще")

bot.infinity_polling()
