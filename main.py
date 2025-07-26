import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time

TOKEN = "8023087340:AAFRPkovu5PK9pBFVbFmo402NaahGuMaLsc"
bot = telebot.TeleBot(TOKEN)

# Дозволені користувачі
allowed_users = [572069105]

# Список активованих користувачів
activated_users = {}

# Список використаних команд
user_commands_used = {}

# Словник команд Foxie Code – Сценарій 1
foxie_commands = {
    "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
    "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
    "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
    "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
    "fire": "Зніми щось із мене. Скажи: “Моє”. І притисни мене ближче.",
    "love": "Обійми. Міцно. Мовчи.",
    "yes": "Покажи очима, що тобі подобається.",
    "secret": "Нашепочи мені бажання. Без цензури.",
    "open": "Заплющ мені очі. І роби що хочеш.",
    "lock": "Ти не маєш права зупинятись протягом 1 хвилини.",
    "mine": "Познач мене. Зубами.",
    "blind": "Зв’яжи мені руки. А потім — поцілуй.",
    "claim": "Зроби щось, що я точно запам’ятаю.",
    "tease": "Муч мене. Але щоб я просила ще.",
    "wild": "Зміни правила. Стань хижаком.",
    "slide": "Поклади мене. Повільно. І вже не відпускай.",
    "whisper": "Скажи щось брудне. І зроби це.",
    "catch": "Піймай мене. Навіть якщо я тікаю. Особливо тоді.",
    "freeze": "Зупинись. А потім — знову.",
    "hunt": "Ти ведеш гру. І я вже в твоїх руках."
}

# Список команд для напису
command_locations = {
    "touch": "Шия",
    "moon": "Плече",
    "kiss": "Зап’ястя",
    "hot": "Внутрішня сторона руки",
    "fire": "Стегно",
    "love": "Живіт",
    "yes": "Литка",
    "secret": "Талія",
    "open": "Внутрішня сторона стегна",
    "lock": "Підборіддя",
    "mine": "Коліно",
    "blind": "Груди",
    "claim": "Пальці рук",
    "tease": "Ліктьовий згин",
    "wild": "Щока",
    "slide": "Сідниця",
    "whisper": "Гомілка",
    "catch": "Шия ззаду",
    "freeze": "Живіт знизу",
    "hunt": "Живіт збоку"
}

# Стартова команда
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in allowed_users:
        bot.send_message(user_id, "Цей бот доступний лише для активованих користувачів 🦊")
        return
    activated_users[user_id] = True
    user_commands_used[user_id] = set()
    bot.send_message(user_id, "🦊 Гра почалась!\n\n"
                              "Ти пишеш слова на своєму тілі, партнер шукає їх за допомогою ліхтарика.\n"
                              "Що знайде — вводить сюди, в бот.\n\n"
                              "Foxie відповість… бажанням 😈")

# Обробка команд
@bot.message_handler(func=lambda message: True)
def handle_command(message):
    user_id = message.chat.id
    if user_id not in activated_users or not activated_users[user_id]:
        bot.send_message(user_id, "Ти ще не активував(ла) гру. Надішли /start")
        return

    text = message.text.lower().strip()
    used = user_commands_used.get(user_id, set())

    if text in foxie_commands and text not in used:
        user_commands_used[user_id].add(text)
        bot.send_message(user_id, f"{foxie_commands[text]}\n\n🦊 Чекаю на наступне слово…")

        if len(user_commands_used[user_id]) == 20:
            bot.send_message(user_id, "Foxie з вами прощається… до наступної гри.")
            # Тут пізніше активується сценарій 2
    elif text in used:
        bot.send_message(user_id, "Це слово вже було 🦊 Обери інше!")
    else:
        bot.send_message(user_id, "Пфф… Такої команди в мене немає 🦊 Спробуй ще")

# Список команд
@bot.message_handler(commands=['список'])
def send_command_list(message):
    user_id = message.chat.id
    if user_id not in allowed_users:
        return
    full_list = "📝 Список команд для напису на тілі:\n\n"
    for cmd, place in command_locations.items():
        full_list += f"{cmd} — {place}\n"
    bot.send_message(user_id, full_list)

# Додати вручну ID користувача
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = message.chat.id
    if user_id != 572069105:
        return
    try:
        new_id = int(message.text.split()[1])
        if new_id not in allowed_users:
            allowed_users.append(new_id)
            bot.send_message(user_id, f"Користувача {new_id} додано до списку.")
        else:
            bot.send_message(user_id, f"Користувач {new_id} вже є у списку.")
    except:
        bot.send_message(user_id, "Формат: /add ID")

# Запуск
print("Bot is running…")
bot.polling()
