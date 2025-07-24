import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем задания из файла
with open("challenges.json", "r", encoding="utf-8") as f:
    challenges = json.load(f)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я бот челленджей. Напиши /challenge, чтобы получить задание.")

async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = random.choice(challenges)
    user_data[user_id] = user_data.get(user_id, {"completed": 0, "skipped": 0})
    user_data[user_id]["current_task"] = task["id"]
    await update.message.reply_text(f"🎯 Твое задание на сегодня:\n\n{task['text']}")

async def completed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data and "current_task" in user_data[user_id]:
        user_data[user_id]["completed"] += 1
        del user_data[user_id]["current_task"]
        await update.message.reply_text("✅ Задание отмечено как выполненное!")
    else:
        await update.message.reply_text("❌ У тебя нет активного задания.")

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data and "current_task" in user_data[user_id]:
        user_data[user_id]["skipped"] += 1
        del user_data[user_id]["current_task"]
        await update.message.reply_text("⚠️ Задание пропущено.")
    else:
        await update.message.reply_text("❌ У тебя нет активного задания.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = user_data.get(user_id, {"completed": 0, "skipped": 0})
    await update.message.reply_text(
        f"📊 Статистика:\n✅ Выполнено: {stats['completed']}\n⏭️ Пропущено: {stats['skipped']}"
    )

TOKEN = "8427261120:AAHGE_1LIEXsjxlut4Jyt_9aKqtfGY0HLDg"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("challenge", challenge))
app.add_handler(CommandHandler("completed", completed))
app.add_handler(CommandHandler("skip", skip))
app.add_handler(CommandHandler("stats", stats))

app.run_polling()
