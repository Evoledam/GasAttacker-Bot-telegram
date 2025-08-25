import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8001006139:AAEY2m7ZF17klMxBKZxhT13Nwa1UmpMdD8Y"
TARGET_USER = "@Evoledam"
ANIMATION_FRAMES = [
    "💨", "😳", "💨", "😖", "💨", "😵", "💨", "🤢", "💨", "😷", "💨", "💩"
]

RANDOM_MESSAGES = [
    f"Пацан({TARGET_USER}) хочет пернуть! Быстрее подставь губы! 👄💨",
    f"Внимание! {TARGET_USER} собирается пернуть! 🚨",
    f"Опасность! {TARGET_USER} хочет пернуть! 🫘💨",
    f"Срочно! {TARGET_USER} чувствует брожение в животе! 🤰💨",
    f"Тревога! {TARGET_USER} готов выпустить газ! ⚡️💨"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start"""
    keyboard = [
        [InlineKeyboardButton("Подставить лицо 😈", callback_data="face_fart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "💨 *Добро пожаловать в Fart Game!* 💨\n\n"
        f"Готов подставить лицо под пердеж {TARGET_USER}? 😏\n"
        "Жми кнопку ниже и получи свою порцию газа! 🎯"
    )
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "face_fart":
        await query.edit_message_reply_markup(reply_markup=None)

        message = await query.message.reply_text("Подготовка... 🎯")

        for frame in ANIMATION_FRAMES:
            await asyncio.sleep(0.3)
            await message.edit_text(frame)

        result_text = (
            f"💥 *БА-БАХ!* 💥\n\n"
            f"Вам пернул в лицо {TARGET_USER}! 🤢\n\n"
            f"*Реакция:* {random.choice(['🤮', '😵', '🤢', '💩', '😷'])}\n"
            f"*Мощность:* {random.randint(80, 100)}% 💨\n"
            f"*Запах:* {random.choice(['Смертельный', 'Невыносимый', 'Ядерный'])} ☣️"
        )
        
        await message.edit_text(
            result_text, 
            parse_mode='Markdown'
        )
        keyboard = [
            [InlineKeyboardButton("Подставить губы 👄", callback_data="lips_fart")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            "Что будем делать дальше? 😏", 
            reply_markup=reply_markup
        )
    
    elif query.data == "lips_fart":
        await query.edit_message_reply_markup(reply_markup=None)
        message = await query.message.reply_text("Подготовка губ... 👄")
        
        lip_frames = ["👄", "💋", "👅", "😗", "😚", "😘"]
        for frame in lip_frames:
            await asyncio.sleep(0.3)
            await message.edit_text(frame)
        result_text = (
            f"💋 *ЧМОК!* 💋\n\n"
            f"Вы приняли пердеж {TARGET_USER} губами! 😘💨\n\n"
            f"*Вкус:* {random.choice(['Пикантный', 'Острый', 'Специфический'])} 🌶️\n"
            f"*Послевкусие:* {random.choice(['Незабываемое', 'Терпкое', 'Пикантное'])} 🍷\n"
            f"*Рейтинг:* {random.randint(1, 5)}/5 ⭐"
        )
        
        await message.edit_text(
            result_text, 
            parse_mode='Markdown'
        )
        keyboard = [
            [InlineKeyboardButton("Ещё раз! 🔁", callback_data="face_fart")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            "Хочешь ещё порцию? 😈", 
            reply_markup=reply_markup
        )

async def send_random_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    keyboard = [
        [InlineKeyboardButton("Подставить губы 👄", callback_data="lips_fart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=random.choice(RANDOM_MESSAGES),
        reply_markup=reply_markup
    )

async def start_random_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    interval = random.randint(30, 60)
    job = context.job_queue.run_repeating(
        send_random_message, 
        interval=interval, 
        first=10,
        chat_id=chat_id,
        name=str(chat_id)
    )
    
    context.chat_data['job'] = job
    
    await update.message.reply_text(
        f"🚀 Режим случайных пердежей активирован! "
        f"Ожидайте сигналов каждые {interval} секунд! ⏰"
    )

def main():

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random", start_random_messages))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Enable")
    application.run_polling()

if __name__ == "__main__":
    main()
