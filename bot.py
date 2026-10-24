from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv
from pathlib import Path
import random
import json
import os

# Надёжная загрузка .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Токен не найден!")
    print(f"Ищем .env здесь: {env_path}")
    print("Убедись, что в файле .env есть строка:")
    print("TOKEN=твой_токен_от_BotFather")
    exit()

print("✅ Токен успешно загружен")

USERS_FILE = "users.json"

FACTS = [
    "🌌 В космосе нет звука, потому что звук не может распространяться в вакууме.",
    "☀️ Солнечный свет достигает Земли примерно за 8 минут 20 секунд.",
    "🪐 Сатурн обладает системой колец, состоящей преимущественно из льда и частиц пыли.",
    "🌕 Луна удаляется от Земли примерно на 3,8 сантиметра в год.",
    "⭐ Нейтронные звёзды настолько плотные, что чайная ложка их вещества весила бы миллиарды тонн.",
]

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = load_users()
    users[str(user.id)] = {
        "name": user.first_name,
        "username": user.username
    }
    save_users(users)

    keyboard = [
        [KeyboardButton("🎲 Случайный факт")],
        [KeyboardButton("🪐 Интересные факты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Привет, {user.first_name}!\nЯ бот с интересными фактами о космосе 🚀",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎲 Случайный факт":
        await update.message.reply_text(random.choice(FACTS))
    
    elif text == "🪐 Интересные факты":
        keyboard = [
            [InlineKeyboardButton("🌕 Луна", callback_data="moon")],
            [InlineKeyboardButton("☀️ Солнце", callback_data="sun")],
            [InlineKeyboardButton("🪐 Сатурн", callback_data="saturn")],
            [InlineKeyboardButton("⭐ Нейтронные звёзды", callback_data="neutron")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выбери тему:", reply_markup=reply_markup)
    
    else:
        await update.message.reply_text("Нажми кнопку ниже 👇")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "moon":
        text = "🌕 Луна удаляется от Земли примерно на 3,8 см в год."
    elif data == "sun":
        text = "☀️ Свет от Солнца идёт до Земли 8 минут 20 секунд."
    elif data == "saturn":
        text = "🪐 Сатурн — планета с красивыми кольцами из льда и пыли."
    elif data == "neutron":
        text = "⭐ Нейтронные звёзды — самые плотные объекты во Вселенной."
    else:
        text = "Неизвестная кнопка"

    await query.edit_message_text(text=text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()