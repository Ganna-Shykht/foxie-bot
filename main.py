import telebot
from telebot import types
import time
from datetime import datetime

TOKEN = "8023087340:AAFRPkovu5PK9pBFVbFmo402NaahGuMaLsc"
ADMIN_ID = 572069105
bot = telebot.TeleBot(TOKEN)

# ====== Глобальні змінні ======
ALLOWED_USERS = set()
USER_STATE = {}
GIFT_CODES = {}
USERS_DB = {}

# ====== Пасхалки ======
EASTER_EGGS = {
    "сюрприз": "🎁 Щось чекає попереду...",
    "знову": "🔁 Схоже, комусь сподобалось 😉",
    "гаряче": "🔥 Точно гарячіше, ніж учора…",
    "лисичка": "🦊 Ну ти й знайшла мене! Хочеш ще одну підказку?",
    "foxie": "Foxie завжди поруч. Навіть коли ти не граєш.",
    "ніч": "Ніч — це лише початок. Пиши наступне слово.",
    "вогонь": "🔥 У цій грі може загорітись не тільки серце.",
    "грай": "Грай ніжно. Але до кінця.",
    "танець": "Навіть тіла знають, коли час рухатись разом.",
    "маркер": "Не бійся залишити слід. Він змиється… або ні 😉",
    "таємниця": "Тсс… збережи її до кінця гри.",
    "погляд": "Один погляд — і я вже тут. Продовжуй…",
    "мрія": "Це гра — або твоя мрія стала реальністю?",
}

REMINDER_TEXTS = [
    "А пам’ятаєш, як це було вперше? 🦊 Може, повторимо? Foxie все ще тут…",
    "3 місяці без пригод? Foxie трохи сумує. Хочеш зіграти знову?",
    "Деякі речі варто повторювати… з новим настроєм. Foxie на тебе чекає 😈",
    "А може, вже час для нового рівня? Foxie не забуває своїх лисичок 🦊"
]

COMMANDS_LIST = {
    "1": {
        "words": {
            "touch": "Шия", "moon": "Плече", "kiss": "Зап’ястя", "hot": "Внутрішня сторона руки", "fire": "Стегно",
            "love": "Живіт", "yes": "Литка", "secret": "Талія", "open": "Внутрішня сторона стегна", "lock": "Підборіддя",
            "mine": "Коліно", "blind": "Груди", "claim": "Пальці рук", "tease": "Ліктьовий згин", "wild": "Щока",
            "slide": "Сідниця", "whisper": "Гомілка", "catch": "Шия ззаду", "freeze": "Живіт знизу", "hunt": "Живіт збоку"
        },
        "replies": {
            "touch": "Не питай — просто торкнись. Там, де тобі хочеться.",
            "moon": "Торкнись тільки носом. Веди лінію повільно. Губам — заборонено.",
            "kiss": "Три поцілунки. Там, де я не чекаю. Тільки не на губах.",
            "hot": "Зроби гарячіше. Ти маєш три рухи — і жодного слова.",
            "fire": "Зніми щось із мене. Скажи: “Моє”. І притисни мене ближче.",
            "love": "Торкнись так, щоб на мить перехопило подих. Один дотик. І жодних повторів.",
            "yes": "Запитай тричі пошепки: «Ти хочеш, щоб я…?» Якщо тричі отримаєш “так” — роби що хочеш. Але ніжно. Поки що.",
            "secret": "Поцілуй так, щоб тиша зникла. Якщо вийде — отримаєш мою таємницю. Можеш спитати все, що хочеш.",
            "open": "Зніми одну річ. Назви це “відкриттям”. І поцілуй.",
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
        },
    },
    "2": {
        "words": {
            "drip": "Шия", "echo": "Плече", "bite": "Зап’ястя", "mark": "Внутрішня сторона руки", "fold": "Стегно",
            "burn": "Живіт", "howl": "Литка", "lace": "Талія", "drift": "Внутрішня сторона стегна", "trace": "Підборіддя",
            "murmur": "Коліно", "sneak": "Груди", "melt": "Пальці рук", "nibble": "Ліктьовий згин", "grip": "Щока",
            "spill": "Сідниця", "sway": "Стегно", "trap": "Шия", "glitch": "Живіт знизу", "anchor": "Живіт збоку"
        },
        "replies": {
            "drip": "Проведи кінчиком пальця, ніби капля щойно впала. Повільно, гарячою доріжкою — від найвищої точки, куди зможеш дотягнутись… до найсміливішої. А потім зупинись. І подивись мені в очі. Без усмішки. Без слів. Наче це — твій ритуал.",
            "echo": "Повтори мій рух. Точно. Але з власним відтінком — повільніше, ніжніше, глибше. Зроби так, щоб повірити: ти зрозумів(ла) мене краще, ніж я себе. Один жест — твоя відповідь на мій.",
            "bite": "Залиши слід. Але не просто так. Обери місце — там, де найбільше хочеш володіти. Один укус. Без жалю. Щоб ми ще довго згадували хто чий.",
            "mark": "Проведи невидиму лінію. Повільно, язиком. Самостійно обери, де початок — і де вона має закінчитись. Це твоя межа володіння. І твій підпис. Тільки один рух — але назавжди.",
            "fold": "Затисни мої руки. Не питай дозволу. А тепер — поцілунок, повільний і впевнений. Наче розкладаєш мене, шар за шаром. Я маю здатись, не вирватись. Лише губи. І твоя сила.",
            "burn": "Знайди найгарячішу точку на моєму тілі. І торкнись її, ніби це полум’я. Повільно. Без страху. Твій дотик має не обпекти — а запалити. Щоб ми загорілись разом. І не гасли ще довго.",
            "howl": "Прошепчи моє ім’я. Один раз. Але так, щоб у мені все завмерло. Ніби це молитва — і ти боїшся, що вона зникне в повітрі. Після цього — нічого не кажи. Дай мені відчути тишу.",
            "lace": "Переплети наші тіла так, щоб я не змогла(в) вийти… і не захотіла(в). Руками. Ногами. Подихом. Створи вузол із нас двох. Щоб навіть сон не наважився нас розплутати.",
            "drift": "Проведи пальцем по моїй шкірі, як вітер перед грозою — ледь відчутно, але з натяком на бурю. Не зупиняйся, поки я не подивлюсь на тебе. І тоді — замри. Дай мені вгадати, що буде далі.",
            "trace": "Досліди моє тіло, ніби мапу невідомої країни. Шукай ерогенні зони повільно, без поспіху — пальцями, губами, подихом. Твоє завдання — знайти шлях до задоволення. А моє — відкрити нові межі.",
            "murmur": "Уяви, що ми не знайомі. Нахились і прошепчи мені щось, чим спокушав(ла) б мене вперше. Тільки одне речення. А потім — затримай погляд. Без усмішки. Без пояснень.",
            "sneak": "Зроби те, чого тобі найбільше хочеться зараз. Але раптово. Без попередження. Ніби ми — гра, в якій дозволено все. Один порив — і ніяких вибачень.",
            "melt": "Проведи язиком по вушку — повільно, ніби хочеш розтопити. А потім прошепочи одне бажання. Те, яке зараз неможливо стримати. Нехай я відчую його… ще до того, як воно здійсниться.",
            "nibble": "Уяви, що я — твій улюблений десерт. Скуштуй повільно, затримуючи кожен дотик. Не поспішай — смак має розкритися сам. Один укус. І затишшя після нього.",
            "grip": "Візьми мене міцно. Без пояснень. Один раз. Але так, щоб у цьому дотику було все — і бажання, і контроль, і трохи нетерплячості.",
            "spill": "Скажи мені одну фантазію. Навіть якщо вона божевільна. А може — саме тому. Вимов її вголос. І одразу після — поцілуй, щоб я не встиг(ла) відповісти. Лиш дихання і вогонь.",
            "sway": "Проведи рукою по моєму стегну — повільно, як у танці, який знає тільки наше тіло. А потім поцілуй мене… як ще жодного разу. Сміливіше. Інакше. По-нашому.",
            "trap": "Підкрадися і схопи мене зненацька. Обійми так, щоб було зрозуміло: це пастка. Але з тих, з яких не хочеться вибиратись.",
            "glitch": "Зроби щось, чого я зовсім не чекаю. Але не про секс. Замість дотику — масаж. Замість поцілунку — ковдра на плечі. Нехай мій розум зависне… а тіло подякує.",
            "anchor": "Торкнись до мене так, ніби я — спокій, якого ти шукаєш. Затримай дотик. І коли відчуєш, що вже вдома — прошепочи слово. Одне. Я його запам’ятаю.",
        }
    }
}

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔸 Що це за гра?", "💳 Купити", "🎁 Подарувати іншому", "🟠 Почати гру", "💬 Запитати Foxie")
    return markup

def back_menu():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add("⬅️ Назад", "⬅️ Головне меню")

def shop_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧡 Купити Digital", "🔥 Купити Lite Box")
    markup.add("⬅️ Назад", "⬅️ Головне меню")
    return markup

def gift_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Подарувати Digital — 500 грн", "🎁 Подарувати Lite Box — 800 грн")
    markup.add("⬅️ Назад", "⬅️ Головне меню")
    return markup

def level_choose_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🟠 Рівень 1 (Original)", "🟣 Рівень 2 (Passion)")
    markup.add("⬅️ Назад", "⬅️ Головне меню")
    return markup

def game_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧡 Список команд для напису")
    markup.add("⬅️ Назад", "⬅️ Головне меню")
    return markup

def after_game_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔁 Почати знову", "📩 Поділитися з другом", "⬅️ Головне меню", "🚫 Відписатись")
    return markup

# ========== ЛОГІКА КНОПОК НАЗАД ==========
def handle_back(message):
    state = USER_STATE.get(message.from_user.id, {}).get("step", "")
    if state in ["about", "shop", "gift_choice"]:
        start(message)
    elif state.startswith("playing_") or state == "choose_level":
        send_level_choose(message.from_user.id)
    elif state == "wait_gift_for":
        present_gift(message)
    else:
        start(message)

# ========== ОСНОВНІ ХЕНДЛЕРИ ==========
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    USERS_DB.setdefault(user_id, {"level1": False, "level2": False, "joined": datetime.now().isoformat()})
    bot.send_message(user_id,
        "Привіт.\nТебе щойно занесло в… гру.\n"
        "Це Foxie Code — гра, в якій ви запускаєте бажання з ліхтарика.\n\n"
        "Один із вас — команда. Інший — світло.\nЦе ви + ваша пристрасть.\n\n"
        "Вам не потрібно нічого знати. Просто обери, з чого почати ↓",
        reply_markup=get_main_menu())
    USER_STATE[user_id] = {"step": "main_menu"}

@bot.message_handler(func=lambda m: m.text == "⬅️ Головне меню")
def to_main(message):
    start(message)

@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def to_back(message):
    handle_back(message)

@bot.message_handler(func=lambda m: m.text == "🔸 Що це за гра?")
def what_is_game(message):
    bot.send_message(message.chat.id,
        "Foxie Code — це гра для пари.\n\n"
        "На тілі одного з вас — з’являються команди. "
        "Невидимим маркером. Їх видно тільки під світлом ліхтарика.\n\n"
        "Другий — шукає. Вводить цю команду сюди, в бот. А потім — виконує те, що скаже Foxie.\n\n"
        "Є 20 команд. Але кожна з них — про вас. Про дотик, дію, мовчання. І бажання.\n\n"
        "Навіть якщо у вас тільки ручка й фантазія — гра вже почалась.",
        reply_markup=back_menu())
    USER_STATE[message.from_user.id]["step"] = "about"

@bot.message_handler(func=lambda m: m.text == "💬 Запитати Foxie")
def ask_foxie(message):
    bot.send_message(message.from_user.id, "Напиши тут питання — і Foxie відповість особисто! 🦊", reply_markup=back_menu())
    USER_STATE[message.from_user.id]["step"] = "waiting_support"

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == "waiting_support")
def send_support_message(message):
    text = f"Foxie! Нове повідомлення від @{message.from_user.username} ({message.from_user.id}):\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.from_user.id, "Твоє питання надіслано Foxie! Очікуй відповідь у цьому чаті 🦊", reply_markup=get_main_menu())
    USER_STATE[message.from_user.id]["step"] = "main_menu"

@bot.message_handler(func=lambda m: m.text == "💳 Купити")
def show_shop(message):
    bot.send_message(message.chat.id,
        "Обери свою гру Foxie Code:\n\n"
        "🧡 Digital — 500 грн (лише гра, доступ одразу після оплати)\n"
        "🔥 Lite Box — 800 грн (гра + маркер, ліхтарик, 2 шоколадки, свічка, листівка з QR-кодом)\n"
        "Доступ до гри відкриється одразу після оплати.\n\n"
        "🎁 Хочеш подарувати гру іншій людині?",
        reply_markup=shop_menu())
    USER_STATE[message.from_user.id]["step"] = "shop"

@bot.message_handler(func=lambda m: m.text == "🎁 Подарувати іншому")
def present_gift(message):
    bot.send_message(message.chat.id,
        "Foxie Code — це ще й незвичний подарунок 💌 Гра, яка залишається в пам’яті.\n"
        "Обери, який варіант ти хочеш подарувати:",
        reply_markup=gift_menu())
    USER_STATE[message.from_user.id]["step"] = "gift_choice"

@bot.message_handler(func=lambda m: m.text in [
    "🎁 Подарувати Digital — 500 грн", "🎁 Подарувати Lite Box — 800 грн"])
def buy_gift(message):
    bot.send_message(message.chat.id,
        "Напиши, будь ласка, для кого цей подарунок (нік або номер телефону):",
        reply_markup=back_menu())
    USER_STATE[message.from_user.id]["step"] = "wait_gift_for"

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == "wait_gift_for")
def get_gift_for(message):
    user_id = message.from_user.id
    gift_code = f"fox{user_id}{int(time.time())%10000}"
    GIFT_CODES[gift_code] = {"used": False, "for_id": None, "from_id": user_id}
    bot.send_message(user_id,
        f"Привіт! Тобі подарували гру Foxie Code.\n"
        f"Просто зайди в бот і введи цей код:\n❤️{gift_code}\nFoxie чекає на тебе!\n(Код можна використати лише один раз.)",
        reply_markup=get_main_menu())
    start(message)

@bot.message_handler(func=lambda m: m.text == "🧡 Купити Digital")
def buy_digital(message):
    user_id = message.from_user.id
    ALLOWED_USERS.add(user_id)
    USERS_DB[user_id]["level1"] = False
    USERS_DB[user_id]["level2"] = False
    bot.send_message(user_id, "Дякуємо за оплату 🧡\nТвоя ніч — починається просто зараз.",
                     reply_markup=level_choose_menu())
    send_level_choose(user_id)

@bot.message_handler(func=lambda m: m.text == "🔥 Купити Lite Box")
def buy_lite_box(message):
    user_id = message.from_user.id
    ALLOWED_USERS.add(user_id)
    USERS_DB[user_id]["level1"] = False
    USERS_DB[user_id]["level2"] = False
    bot.send_message(user_id,
        "Дякуємо за оплату! Тепер твоя гра Foxie Code активована.\n\nДля Lite Box напиши: ПІБ, телефон, місто та відділення Нової Пошти.",
        reply_markup=level_choose_menu())
    send_level_choose(user_id)

def send_level_choose(user_id):
    bot.send_message(user_id, "Обери рівень гри:", reply_markup=level_choose_menu())
    USER_STATE[user_id]["step"] = "choose_level"

@bot.message_handler(func=lambda m: m.text in ["🟠 Рівень 1 (Original)", "🟣 Рівень 2 (Passion)"])
def choose_level(message):
    user_id = message.from_user.id
    level = "1" if "Рівень 1" in message.text else "2"
    USER_STATE[user_id]["step"] = f"playing_{level}"
    USER_STATE[user_id]["level"] = level
    USER_STATE[user_id]["commands"] = []
    bot.send_message(user_id,
        "Гра почалась 🦊\n\n"
        "Один із вас — пише команди на тілі.\nДругий — шукає. І коли знаходить — вводить слово сюди, в бот.\n"
        "Foxie відповість… бажанням 😈\n\n"
        "Можеш у будь-який момент натиснути 🧡 Список команд для напису, ⬅️ Назад або ⬅️ Головне меню!",
        reply_markup=game_menu())

@bot.message_handler(func=lambda m: m.text == "🧡 Список команд для напису")
def show_commands(message):
    user_id = message.from_user.id
    level = USER_STATE.get(user_id, {}).get("level", "1")
    block = COMMANDS_LIST[level]
    lines = [f"• {cmd} — {place}" for cmd, place in block["words"].items()]
    bot.send_message(user_id, "Ось твій список із 20 команд 🧡\n\n" + "\n".join(lines), reply_markup=game_menu())

@bot.message_handler(func=lambda m: m.text == "🟠 Почати гру")
def try_start_game(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USERS:
        bot.send_message(user_id, "Це закрита гра. Спершу купи доступ або активуй подарунковий код ❤️",
                         reply_markup=get_main_menu())
        return
    send_level_choose(user_id)

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step", "").startswith("playing_"))
def process_game(message):
    user_id = message.from_user.id
    level = USER_STATE[user_id]["level"]
    cmds = COMMANDS_LIST[level]["words"]
    replies = COMMANDS_LIST[level]["replies"]
    input_word = message.text.strip().lower()
    # Кнопки в грі
    if message.text == "⬅️ Головне меню":
        start(message)
        return
    if message.text == "⬅️ Назад":
        send_level_choose(user_id)
        return
    if message.text == "🧡 Список команд для напису":
        show_commands(message)
        return
    # Пасхалки
    if input_word in EASTER_EGGS:
        bot.send_message(user_id, EASTER_EGGS[input_word], reply_markup=game_menu())
        return
    # Перевірка
    if input_word not in cmds:
        bot.send_message(user_id, "Пфф… Такої команди в мене немає 🦊 Спробуй ще.", reply_markup=game_menu())
        return
    if input_word in USER_STATE[user_id]["commands"]:
        bot.send_message(user_id, "Це слово вже було. Введи інше 🦊", reply_markup=game_menu())
        return
    USER_STATE[user_id]["commands"].append(input_word)
    bot.send_message(user_id, replies[input_word], reply_markup=game_menu())
    if len(USER_STATE[user_id]["commands"]) == 20:
        finish_game(user_id, level)
    else:
        bot.send_message(user_id, "🦊 Чекаю на наступне слово…", reply_markup=game_menu())

def finish_game(user_id, level):
    USERS_DB[user_id][f"level{level}"] = True
    bot.send_message(user_id, "Foxie з вами прощається… до наступної гри 🦊", reply_markup=after_game_menu())
    bot.send_message(user_id, "Оціни гру від 1 до 5 (де 5 — супер!):")
    USER_STATE[user_id]["step"] = "rate_game"

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == "rate_game")
def rate_game(message):
    rate = message.text.strip()
    if rate in ["1", "2", "3", "4", "5"]:
        bot.send_message(ADMIN_ID, f"Оцінка гри від @{message.from_user.username} ({message.from_user.id}): {rate}")
        bot.send_message(message.from_user.id,
            "Дякую за оцінку! Foxie радіє відгукам 🦊\n"
            "Підпишись на Instagram — тут ще більше ідей: https://www.instagram.com/foxie_code/",
            reply_markup=after_game_menu())
        USER_STATE[message.from_user.id]["step"] = "main_menu"
    else:
        bot.send_message(message.from_user.id, "Введи оцінку від 1 до 5. Foxie не образиться! 😉")

@bot.message_handler(func=lambda m: m.text == "🔁 Почати знову")
def restart_game(message):
    send_level_choose(message.from_user.id)

@bot.message_handler(func=lambda m: m.text == "📩 Поділитися з другом")
def share_with_friend(message):
    bot.send_message(message.chat.id,
        "🦊 Хочеш поділитися Foxie з другом?\nНатисни й надішли йому лінк на нашого ботика:\nhttps://t.me/FoxieCodeBot\n"
        "Але тільки тсс… гра відкриється тільки після оплати або з кодом-подарунком 😉",
        reply_markup=after_game_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🚫 Відписатись")
def unsubscribe(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USERS:
        ALLOWED_USERS.remove(user_id)
    bot.send_message(user_id, "Foxie більше не буде турбувати 🦊 Але ти завжди можеш повернутись у гру, просто написавши сюди 💌", reply_markup=get_main_menu())
    USER_STATE[user_id]["step"] = "main_menu"

@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("fox"))
def enter_gift_code(message):
    user_id = message.from_user.id
    code = message.text.strip()
    if code not in GIFT_CODES:
        bot.send_message(user_id, "Код не знайдено або вже використаний.", reply_markup=get_main_menu())
        return
    if GIFT_CODES[code]["used"]:
        bot.send_message(user_id, "Код вже був використаний. Спробуй інший або купи свою Foxie Code!",
                         reply_markup=get_main_menu())
        return
    ALLOWED_USERS.add(user_id)
    GIFT_CODES[code]["used"] = True
    GIFT_CODES[code]["for_id"] = user_id
    bot.send_message(user_id, "Код активовано! Foxie Code готова 🔥\nПопереду — 20 команд. Одна за одною, зростаючи в напрузі й бажанні.",
                     reply_markup=level_choose_menu())
    send_level_choose(user_id)

@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in EASTER_EGGS)
def handle_easter(message):
    bot.send_message(message.chat.id, EASTER_EGGS[message.text.strip().lower()])

@bot.message_handler(commands=["id"])
def show_id(message):
    bot.send_message(message.chat.id, f"Твій Telegram ID: {message.from_user.id}")

# === Адмін-команди ===
@bot.message_handler(commands=["add"])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(ADMIN_ID, "Формат: /add [id]")
        return
    try:
        add_id = int(parts[1])
        ALLOWED_USERS.add(add_id)
        bot.send_message(ADMIN_ID, f"🟢 Користувача з ID {add_id} додано до списку дозволених.")
    except Exception:
        bot.send_message(ADMIN_ID, "ID має бути числом.")

@bot.message_handler(commands=["статистика"])
def show_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    total = len(ALLOWED_USERS)
    level1 = sum(1 for u in USERS_DB if USERS_DB[u].get("level1"))
    level2 = sum(1 for u in USERS_DB if USERS_DB[u].get("level2"))
    gifts = sum(1 for c in GIFT_CODES if GIFT_CODES[c]["used"])
    text = (
        f"🦊 Foxie Code — статистика:\n"
        f"Грали: {total}\n"
        f"Пройшли рівень 1: {level1}\n"
        f"Пройшли рівень 2: {level2}\n"
        f"Купили на подарунок: {gifts}\n"
        f"Всього gift-кодів: {len(GIFT_CODES)}"
    )
    bot.send_message(ADMIN_ID, text)

# === Запуск ===
if __name__ == "__main__":
    print("Foxie Code запущено 🦊")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
