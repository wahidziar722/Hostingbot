#!/usr/bin/env python3
"""
🤖 BOT HOSTING SYSTEM - د نورو بوټونو د چلولو سیستم
دا کوډ په ریندر کې 100% کار کوي
"""

import os
import subprocess
import sqlite3
import shutil
import time
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

# ==================== کانفیګ ====================
TOKEN = "8697889132:AAG9w86MIdw8CbKj_ddaW9dRrTfulY8qcds"
ADMIN_ID = 8518408753
ADMIN_USERNAME = "Kingwahidafg"
APPROVAL_GROUP_ID = -1003987070217  # ستاسو د تصویب ګروپ آي ډي

BOTS_DIR = "user_bots"
DB_FILE = "hosting.db"
# ================================================

# ډیټابیس جوړول
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        join_date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS running_bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        start_time TEXT,
        process_id INTEGER,
        status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS pending_bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        submitted_at TEXT
    )''')
    conn.commit()
    conn.close()

init_db()
os.makedirs(BOTS_DIR, exist_ok=True)

# مرستندویه دندې
def save_user(user_id, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)",
              (user_id, username, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_pending_bots():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, user_id, bot_name, file_path, submitted_at FROM pending_bots")
    rows = c.fetchall()
    conn.close()
    return rows

def add_pending(user_id, bot_name, file_path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO pending_bots (user_id, bot_name, file_path, submitted_at) VALUES (?, ?, ?, ?)",
              (user_id, bot_name, file_path, datetime.now().isoformat()))
    pending_id = c.lastrowid
    conn.commit()
    conn.close()
    return pending_id

def approve_bot(pending_id, bot):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, bot_name, file_path FROM pending_bots WHERE id=?", (pending_id,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return False
    
    user_id, bot_name, old_path = result
    new_path = os.path.join(BOTS_DIR, f"user_{user_id}_{int(time.time())}_{bot_name}")
    shutil.move(old_path, new_path)
    
    try:
        process = subprocess.Popen(["python", new_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        c.execute('''INSERT INTO running_bots (user_id, bot_name, file_path, start_time, process_id, status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, bot_name, new_path, datetime.now().isoformat(), process.pid, "running"))
        c.execute("DELETE FROM pending_bots WHERE id=?", (pending_id,))
        conn.commit()
        bot.send_message(chat_id=user_id, text=f"✅ ستاسو بوټ `{bot_name}` تصویب شو او اوس چلیږي!")
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False

def reject_bot(pending_id, bot):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, bot_name, file_path FROM pending_bots WHERE id=?", (pending_id,))
    result = c.fetchone()
    if result:
        user_id, bot_name, file_path = result
        if os.path.exists(file_path):
            os.remove(file_path)
        c.execute("DELETE FROM pending_bots WHERE id=?", (pending_id,))
        conn.commit()
        bot.send_message(chat_id=user_id, text=f"❌ ستاسو بوټ `{bot_name}` رد شو.")
    conn.close()

def get_user_bots(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT bot_name, status, start_time FROM running_bots WHERE user_id=?", (user_id,))
    bots = c.fetchall()
    conn.close()
    return bots

def get_keyboard(user_id):
    keyboard = [
        [InlineKeyboardButton("📤 Upload Bot", callback_data="upload")],
        [InlineKeyboardButton("🤖 My Bots", callback_data="mybots")],
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    if user_id == ADMIN_ID:
        keyboard.insert(2, [InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin")])
    return InlineKeyboardMarkup(keyboard)

# ==================== د بوټ دندې ====================
def start(update, context):
    user = update.effective_user
    save_user(user.id, user.username)
    
    update.message.reply_text(
        f"✅ *Welcome {user.first_name}!*\n\n"
        f"🤖 *Bot Hosting System*\n\n"
        f"📌 Send me your `.py` file\n"
        f"👑 I will run it for you 24/7\n\n"
        f"📤 Click Upload Bot to start",
        reply_markup=get_keyboard(user.id),
        parse_mode="Markdown"
    )

def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    user = query.from_user
    data = query.data
    
    if data == "upload":
        query.edit_message_text(
            "📤 *Send Your Bot File*\n\n"
            "Please send me your `.py` file.\n\n"
            "⚠️ Admin will review it first.",
            parse_mode="Markdown"
        )
    
    elif data == "mybots":
        bots = get_user_bots(user.id)
        if not bots:
            query.edit_message_text("📭 *No Bots Found*", parse_mode="Markdown")
            return
        text = "🤖 *Your Bots:*\n\n"
        for bot in bots:
            text += f"📌 `{bot[0]}`\n   Status: {bot[1]}\n   Started: {bot[2][:16]}\n\n"
        query.edit_message_text(text, parse_mode="Markdown")
    
    elif data == "admin" and user.id == ADMIN_ID:
        pending = get_pending_bots()
        if not pending:
            query.edit_message_text("📭 *No Pending Bots*", parse_mode="Markdown")
            return
        for p in pending:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{p[0]}"),
                 InlineKeyboardButton("❌ Reject", callback_data=f"reject_{p[0]}")]
            ])
            query.message.reply_text(
                f"📄 *Pending Bot*\nUser: `{p[1]}`\nBot: `{p[2]}`",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        query.delete_message()
    
    elif data.startswith("approve_") and user.id == ADMIN_ID:
        pending_id = int(data.split("_")[1])
        if approve_bot(pending_id, context.bot):
            query.edit_message_text("✅ Bot approved and running!")
        else:
            query.edit_message_text("❌ Failed to approve bot!")
    
    elif data.startswith("reject_") and user.id == ADMIN_ID:
        pending_id = int(data.split("_")[1])
        reject_bot(pending_id, context.bot)
        query.edit_message_text("❌ Bot rejected.")

def handle_file(update, context):
    user = update.effective_user
    file = update.message.document
    
    if not file.file_name.endswith('.py'):
        update.message.reply_text("❌ Only `.py` files are allowed!")
        return
    
    # Download file
    new_file = file.get_file()
    file_path = f"pending_{user.id}_{int(time.time())}_{file.file_name}"
    new_file.download(file_path)
    
    pending_id = add_pending(user.id, file.file_name, file_path)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pending_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pending_id}")]
    ])
    
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 *New Bot Upload*\n\n👤 User: @{user.username or user.id}\n📁 File: `{file.file_name}`\n\n❓ Do you want to run this bot?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    update.message.reply_text(
        f"✅ *File Received!*\n\n📌 Name: `{file.file_name}`\n⏳ Status: `Pending Approval`",
        parse_mode="Markdown"
    )

def error_handler(update, context):
    print(f"Error: {context.error}")

# ==================== اصلي دنده ====================
def main():
    print("=" * 50)
    print("🤖 BOT HOSTING SYSTEM STARTING...")
    print("=" * 50)
    
    # Create directories
    os.makedirs(BOTS_DIR, exist_ok=True)
    
    # Create updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    dp.add_error_handler(error_handler)
    
    print("✅ Bot is running!")
    print("📌 Send /start to begin")
    print("=" * 50)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
