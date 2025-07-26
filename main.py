
import telebot
from telebot import types

# Твій токен
TOKEN = "8023087340:AAFRPkovu5PK9pBFVbFmo402NaahGuMaLsc"
bot = telebot.TeleBot(TOKEN)

# Список дозволених користувачів
allowed_users = [572069105]

# Словник команд гри
command_dict = {
    "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
    "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
    "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
    "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
    "fire": "Зніми щось із мене. Скажи: “Моє”. І притисни мене ближче.",
    "love": "Доторкнись до мого серця. Рукою. Повільно.",
    "yes": "Погладь. Без поспіху. Я маю сказати «так».",
    "secret": "Нашепочи мені щось непристойне. Дуже тихо.",
    "open": "Розкрий. Але поки що — тільки очі.",
    "lock": "Закрий очі і не відкривай, поки я не скажу.",
    "mine": "Стисни. Так, щоб я зрозуміла: твоє.",
    "blind": "Зав’яжи мені очі. Або придумай, чим їх закрити.",
    "claim": "Познач мене. Як свою. Вибери як.",
    "tease": "Дражни. Рівно 15 секунд. Не більше.",
    "wild": "Тепер хижаком стану я. Не відступай.",
    "slide": "Повільно ковзай губами… далі сам знаєш куди.",
    "whisper": "Нашепочи, що зробиш після гри.",
    "catch": "Злови мене за талію. І не відпускай.",
    "freeze": "Зупинись. Дай подивитись. Просто так.",
    "hunt": "Полюй. Поцілунками.",
}

# Текст старту гри
start_text = (
    "\U0001F98A Гра почалась!\n"
    "Ти пишеш слова на своєму тілі, партнер шукає їх за допомогою ліхтарика.\n"
    "Що знайде — вводить сюди, в бот.\n\n"
    "Foxie відповість… бажанням 😈"
)

# Список команд гри (блок "Список команд для напису")
command_list_text = (
    "Ось твої 20 команд Foxie Code з місцями напису:\n\n"
    "1. touch — Шия\n"
    "2. moon — Плече\n"
    "3. kiss — Зап’ястя\n"
    "4. hot — Внутрішня сторона руки\n"
    "5. fire — Стегно\n"
    "6. love — Живіт\n"
    "7. yes — Литка\n"
    "8. secret — Талія\n"
    "9. open — Внутрішня сторона стегна\n"
    "10. lock — Підборіддя\n"
    "11. mine — Коліно\n"
    "12. blind — Груди\n"
    "13. claim — Пальці рук\n"
    "14. tease — Ліктьовий згин\n"
    "15. wild — Щока\n"
    "16. slide — Сідниця\n"
    "17. whisper — Гомілка\n"
    "18. catch — Шия ззаду\n"
    "19. freeze — Живіт знизу\n"
    "20. hunt — Живіт збоку"
)

# Список користувачів, які отримали доступ до гри (можна розширювати)
active_users = set()

# Обробка команди /start
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.send_message(user_id, "⛔️ Доступ до гри можливий тільки після покупки.")
        return

    active_users.add(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 Розпочати гру", "📝 Список команд")
    bot.send_message(user_id, "Привіт, лисичко! Обери дію:", reply_markup=markup)

# Розпізнавання повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.lower().strip()

    if text == "🎲 розпочати гру":
        bot.send_message(user_id, start_text)
        return

    if text == "📝 список команд":
        bot.send_message(user_id, command_list_text)
        return

    if text in command_dict:
        bot.send_message(user_id, command_dict[text])
        bot.send_message(user_id, "🦊 Чекаю на наступне слово…")
    else:
        bot.send_message(user_id, "Хмм… Foxie не знає такого слова. Спробуй ще раз.")

# Запуск бота
print("Foxie Bot is running...")
bot.infinity_polling()
