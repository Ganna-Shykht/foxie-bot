import telebot
from telebot import types
import time
from datetime import datetime, timedelta

TOKEN = "8023087340:AAFRPkovu5PK9pBFVbFmo402NaahGuMaLsc"
bot = telebot.TeleBot(TOKEN)

# --- Глобальні змінні ---
ALLOWED_USERS = set()
GIFT_CODES = {"GIFT2024", "LOVEYOU", "FIRESTARTER"}
USED_GIFT_CODES = set()
USER_STATES = {}  # user_id: {scenario, commands_entered, finished, activation_time}
REMINDERS = {}    # user_id: remind_at
ADMIN_ID = 572069105

STATISTICS = {
    "total_activated": 0,
    "total_finished": 0,
    "scenario1": 0,
    "scenario2": 0
}

# === Сценарії гри, місця для напису, пасхалки ===

SCENARIOS = {
    "1": {
        "name": "Foxie Code: Original",
        "commands": {
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
            "tease": "Проведи язиком одну лінію. Потім зупинись — і скажи, чого насправді хочеш. Але тільки одне слово..",
            "wild": "Уяви, що я твоя здобич. У тебе 10 секунд на перший напад. Має бути тихо. Але хижо. Якщо моє тіло не відгукнеться — тепер хижаком стану я.",
            "slide": "Повзи пальцем, ніби ти равлик на місії. Але пам’ятай: фініш — це моя усмішка.",
            "whisper": "Нашепчи щось… але не сексуальне. Щось про борщ, податки або сантехніка. Побачимо, як довго я витримаю серйозно.",
            "catch": "Уяви, що на мені захована таємна кнопка. Знайди її… але маєш лише 30 секунд. Старт!",
            "freeze": "Торкнись — і я завмираю. Твоя роль — провокувати. Моя — не рухатись. Якщо я програю — маєш право на ще одне торкання де завгодно.",
            "hunt": "Я — здобич. Ти — хижак. Підкрадайся повільно, мовчки. І схопи так, щоб не встиг(ла) зреагувати. Тепер я в твоїх лапах."
        },
        "body": {
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
    },
    "2": {
        "name": "Foxie Code: Passion",
        "commands": {
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
            "anchor": "Торкнись до мене так, ніби я — спокій, якого ти шукаєш. Затримай дотик. І коли відчуєш, що вже вдома — прошепочи слово. Одне. Я його запам’ятаю."
        },
        "body": {
            "drip": "Шия",
            "echo": "Плече",
            "bite": "Зап’ястя",
            "mark": "Внутрішня сторона руки",
            "fold": "Стегно",
            "burn": "Живіт",
            "howl": "Литка",
            "lace": "Талія",
            "drift": "Внутрішня сторона стегна",
            "trace": "Підборіддя",
            "murmur": "Коліно",
            "sneak": "Груди",
            "melt": "Пальці рук",
            "nibble": "Ліктьовий згин",
            "grip": "Щока",
            "spill": "Сідниця",
            "sway": "Стегно",
            "trap": "Шия",
            "glitch": "Живіт знизу",
            "anchor": "Живіт збоку"
        }
    }
}

EASTER_EGGS = {
    "лисичка": "🦊 Foxie завжди поруч. Ти це знаєш.",
    "foxie": "🦊 Хтось мене кликав? Я тут.",
    "ніч": "🌙 Ніч — час гри. Foxie не спить!",
    "гра": "🎲 Це гра, але з підказкою на щось більше…",
    "світло": "🔦 У світлі знаходяться найцікавіші слова.",
    "ми": "🧡 Ця гра — про вас обох.",
    "ще": "😉 Хочеш ще? Foxie завжди готова до нових пригод.",
    "дотик": "👋 Один дотик — і все змінюється.",
    "правда": "🤫 Правда — у ваших бажаннях.",
    "тихо": "🤫 Тихо-тихо... Хтось спостерігає за грою."
}

# === /start, активація, вибір сценарію ===

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USERS:
        USER_STATES[user_id] = {"step": "awaiting_code"}
        bot.send_message(
            user_id,
            "Привіт! 🦊 Це Foxie Code — гра для двох.\n\nЩоб почати, введи свій унікальний подарунковий код:"
        )
    else:
        if USER_STATES.get(user_id, {}).get("finished"):
            bot.send_message(user_id, "Ти вже проходив(ла) гру. Якщо хочеш ще — напиши адміністратору.")
        else:
            send_scenario_choice(user_id)

@bot.message_handler(func=lambda m: USER_STATES.get(m.from_user.id, {}).get("step") == "awaiting_code")
def handle_gift_code(message):
    user_id = message.from_user.id
    code = message.text.strip()
    if code in GIFT_CODES and code not in USED_GIFT_CODES:
        ALLOWED_USERS.add(user_id)
        USED_GIFT_CODES.add(code)
        USER_STATES[user_id] = {"step": "choose_scenario"}
        STATISTICS["total_activated"] += 1
        remind_time = datetime.now() + timedelta(days=90)
        REMINDERS[user_id] = remind_time
        bot.send_message(user_id, "✅ Код активовано! Тепер обери свій сценарій гри.")
        send_scenario_choice(user_id)
    else:
        bot.send_message(user_id, "⛔️ Невірний або вже використаний код. Спробуй ще раз.")

def send_scenario_choice(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🦊 Foxie Code: Original", callback_data="scenario_1"),
        types.InlineKeyboardButton("🖤 Foxie Code: Passion", callback_data="scenario_2")
    )
    bot.send_message(
        user_id,
        "Обери стиль гри:\n\n1️⃣ Foxie Code: Original — класика, драйв, легкість\n2️⃣ Foxie Code: Passion — чуттєвість, глибина, інтрига",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["scenario_1", "scenario_2"])
def handle_scenario_selected(call):
    user_id = call.from_user.id
    scenario_id = "1" if call.data == "scenario_1" else "2"
    USER_STATES[user_id] = {
        "scenario": scenario_id,
        "commands_entered": [],
        "finished": False,
        "step": "playing",
        "activation_time": datetime.now().isoformat()
    }
    STATISTICS[f"scenario{scenario_id}"] += 1
    bot.answer_callback_query(call.id)
    send_intro(user_id, scenario_id)

def send_intro(user_id, scenario_id):
    bot.send_message(user_id, f"Обрано сценарій: {SCENARIOS[scenario_id]['name']}.\n")
    time.sleep(1)
    bot.send_message(user_id, "Foxie дивиться на тебе…")
    time.sleep(1.2)
    bot.send_message(user_id, "Здається, зараз щось почнеться…")
    time.sleep(1.3)
    bot.send_message(user_id, "🦊 Готова?")
    time.sleep(1.5)
    bot.send_message(user_id, "Тоді… пиши перше слово!")
    send_commands_list(user_id, scenario_id)

# === Основна ігрова логіка, список команд, фінал, пасхалки, відгуки ===

@bot.message_handler(commands=["список"])
def handle_command_list(message):
    user_id = message.from_user.id
    state = USER_STATES.get(user_id)
    if not state or "scenario" not in state:
        bot.send_message(user_id, "Гра ще не активована.")
        return
    scenario_id = state["scenario"]
    send_commands_list(user_id, scenario_id)

def send_commands_list(user_id, scenario_id):
    data = SCENARIOS[scenario_id]
    text = "🖋 Список команд для напису на тілі:\n\n"
    for word, body in data["body"].items():
        text += f"• {word} — {body}\n"
    bot.send_message(user_id, text)

@bot.message_handler(func=lambda m: USER_STATES.get(m.from_user.id, {}).get("step") == "playing")
def handle_game_command(message):
    user_id = message.from_user.id
    text = message.text.strip().lower()
    state = USER_STATES[user_id]
    scenario_id = state["scenario"]
    commands = SCENARIOS[scenario_id]["commands"]

    # Пасхалки ловляться окремо
    if text in EASTER_EGGS:
        bot.send_message(user_id, EASTER_EGGS[text])
        return

    if text in commands:
        if text in state["commands_entered"]:
            bot.send_message(user_id, "Це слово вже було. Введи інше 🦊")
            return
        state["commands_entered"].append(text)
        if len(state["commands_entered"]) == 20:
            state["finished"] = True
            STATISTICS["total_finished"] += 1
            bot.send_message(user_id, f"{commands[text]}")
            time.sleep(1.1)
            bot.send_message(user_id, "Foxie з вами прощається… до наступної гри.")
            send_foxie_letter(user_id)
            send_recommend(user_id)
            send_rating(user_id)
        else:
            bot.send_message(user_id, f"{commands[text]}\n\n🦊 Чекаю на наступне слово…")
    else:
        bot.send_message(user_id, "🦊 Такого слова немає в грі. Спробуй ще раз або перевір написання.")

def send_foxie_letter(user_id):
    letter = (
        "🦊 Foxie:\n\n"
        "Гра завершена, але це тільки початок. Пам’ятай про бажання і тепло цієї ночі!\n"
        "Поділись відгуком або запроси друзів до Foxie Code 🧡"
    )
    bot.send_message(user_id, letter)

def send_recommend(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🦊 Порадити другу", url="https://t.me/foxie_code_bot"))
    bot.send_message(user_id, "Поділись Foxie Code з другом!", reply_markup=markup)

def send_rating(user_id):
    markup = types.InlineKeyboardMarkup()
    for i in range(1, 6):
        markup.add(types.InlineKeyboardButton(f"{i}⭐", callback_data=f"rate_{i}"))
    bot.send_message(user_id, "🦊 Як тобі Foxie Code?\nОціни гру:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rate_"))
def handle_rate(call):
    rating = call.data.split("_")[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"Дякую за оцінку {rating} ⭐️ Foxie вдячна тобі!")

@bot.message_handler(commands=["статистика"])
def handle_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = STATISTICS
    text = (
        f"🦊 Foxie Code — статистика:\n"
        f"Активували гру: {s['total_activated']}\n"
        f"Завершили гру: {s['total_finished']}\n"
        f"Сценарій 1: {s['scenario1']}\n"
        f"Сценарій 2: {s['scenario2']}"
    )
    bot.send_message(message.chat.id, text)

# ———— Пасхалки ловляться тут теж для всіх (крім гри) ————
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in EASTER_EGGS)
def handle_easter_eggs(message):
    user_id = message.from_user.id
    text = message.text.strip().lower()
    bot.send_message(user_id, EASTER_EGGS[text])

# ———— Запуск бота ————
if __name__ == "__main__":
    print("Foxie Code запущено 🦊")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
