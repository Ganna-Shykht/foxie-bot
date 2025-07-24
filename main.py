import telebot

# Твій токен
TOKEN = "8023087340:AAFRPkovu5PK9pBFVbFmo402NaahGuMaLsc"
bot = telebot.TeleBot(TOKEN)

# Список дозволених користувачів
allowed_users = [572069105]  # Твій ID

# Словник команд
command_dict = {
    "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
    "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
    "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
    "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
    "fire": "Зніми щось із мене. Скажи: “Моє”. І притисни ближче.",
    "love": "Торкнись так, щоб на мить перехопило подих. Один дотик. І жодних повторів.",
    "yes": "Запитай тричі пошепки: «Ти хочеш, щоб я…?» Якщо тричі отримаєш “так” — роби що хочеш. Але ніжно. Поки що.",
    "secret": "Поцілуй так, щоб тиша зникла. Якщо вийде — отримаєш мою таємницю. Можеш спитати все, що хочеш.",
    "open": "Стегно ззаду. Зніми одну річ. Назви це “відкриттям”. І поцілуй.",
    "lock": "Скажи ім’я пошепки. Потім три поцілунки: як у перший день, як у своїх мріях, як ще не було. Якщо всі три прийняті — замок знято. Проси, чого хочеш.",
    "mine": "Обведи пальцем. І скажи, яка частина — твоя.",
    "blind": "Закрий очі. Дай рукам «побачити».",
    "claim": "Обійми ззаду. Притиснись. Прошепочи: «Це все моє». І залиш дотик, який це підтвердить.",
    "tease": "Проведи язиком одну лінію. Потім зупинись — і скажи, чого насправді хочеш. Але тільки одне слово.",
    "wild": "Уяви, що я твоя здобич. У тебе 10 секунд на перший напад. Має бути тихо. Але хижо. Якщо моє тіло не відгукнеться — тепер хижаком стану я.",
    "slide": "Повзи пальцем, ніби ти равлик на місії. Але пам’ятай: фініш — це моя усмішка.",
    "whisper": "Нашепчи щось… але не сексуальне. Щось про борщ, податки або сантехніка. Побачимо, як довго я витримаю серйозно.",
    "catch": "Уяви, що на мені захована таємна кнопка. Знайди її… але маєш лише 30 секунд. Старт!",
    "freeze": "Торкнись — і я завмираю. Твоя роль — провокувати. Моя — не рухатись. Якщо я програю — маєш право на ще одне торкання де завгодно.",
    "hunt": "Я — здобич. Ти — хижак. Підкрадайся повільно, мовчки. І схопи так, щоб не встиг(ла) зреагувати. Тепер я в твоїх лапах."
}

# Перевірка доступу
def is_allowed(user_id):
    return user_id in allowed_users

# Показати ID
@bot.message_handler(commands=['id'])
def get_user_id(message):
    bot.send_message(message.chat.id, f"🔐 Твій Telegram ID: {message.from_user.id}")

# Додати нових користувачів
@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id != 572069105:
        bot.send_message(message.chat.id, "⛔️ У тебе немає прав додавати користувачів.")
        return

    try:
        ids = message.text.split()[1:]
        if not ids:
            bot.send_message(message.chat.id, "❗️ Напиши хоча б один ID після /add")
            return

        added = []
        already = []

        for user_id in ids:
            try:
                uid = int(user_id)
                if uid not in allowed_users:
                    allowed_users.append(uid)
                    added.append(uid)
                else:
                    already.append(uid)
            except ValueError:
                continue

        response = ""
        if added:
            response += f"✅ Додано: {', '.join(map(str, added))}\n"
        if already:
            response += f"👀 Вже у списку: {', '.join(map(str, already))}"
        bot.send_message(message.chat.id, response.strip())

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Сталася помилка під час обробки ID.")

# Стартове повідомлення
@bot.message_handler(commands=['start'])
def start_message(message):
    if not is_allowed(message.from_user.id):
        bot.send_message(message.chat.id, "👋 Привіт! Щоб почати гру, потрібно отримати доступ. Надішли свій ID творцю гри (напиши /id, щоб дізнатись свій).")
        return

    welcome_text = (
        "👋 Привіт.\n"
        "Сьогодні ти граєш зі мною. На тілі сховані коди — слова або числа, що починаються зі /.\n"
        "Світлом знайди напис → введи код сюди → виконай завдання.\n"
        "Кожен крок веде тебе далі… до мене.\n"
        "Не поспішай. Торкайся. Досліджуй.\n"
        "Це гра, в якій ми вже перемогли. 🦊"
    )
    bot.send_message(message.chat.id, welcome_text)

# Обробка команд
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if not is_allowed(message.from_user.id):
        bot.send_message(message.chat.id, "🔒 У тебе ще немає доступу. Надішли свій ID (команда /id) творцю гри.")
        return

    user_input = message.text.lower().strip().lstrip('/')
    if user_input in command_dict:
        bot.send_message(message.chat.id, command_dict[user_input])
    else:
        bot.send_message(message.chat.id, "❓ Я не впізнаю цей код. Спробуй ще раз або знайди інший напис.")

# Запуск бота
bot.polling()
