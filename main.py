#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════
#  DARK HOST BOT - RENDER FIXED VERSION
#  WORKING 100% ON PYTHON 3.9
# ═══════════════════════════════════════════════════════════════════

import os
import time
import sqlite3
import shutil
import subprocess
import random
import string
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

# ==================== CONFIG ====================
TOKEN = "8697889132:AAG9w86MIdw8CbKj_ddaW9dRrTfulY8qcds"
ADMIN_ID = 8518408753
ADMIN_USERNAME = "Kingwahidafg"
APPROVAL_GROUP_ID = -1003987070217

REQUIRED_CHANNELS = [
    {"name": "WAHID MODE X", "url": "https://t.me/WahidModeX", "username": "@WahidModeX"},
    {"name": "PRO TECH 43", "url": "https://t.me/ProTech43", "username": "@ProTech43"}
]

BOTS_DIR = "running_bots"
DB_FILE = "bot_hosting.db"
FREE_LIMIT = 1
# =================================================

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        is_premium INTEGER DEFAULT 0,
        premium_expiry TEXT DEFAULT NULL,
        join_date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        status TEXT,
        start_time TEXT,
        process_id INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS pending_bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        submitted_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS premium_codes (
        code TEXT PRIMARY KEY,
        duration_days INTEGER,
        used_by INTEGER DEFAULT NULL,
        used_at TEXT DEFAULT NULL
    )''')
    conn.commit()
    conn.close()

init_db()
os.makedirs(BOTS_DIR, exist_ok=True)

def is_user_joined_channels(user_id, bot):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False, channel["url"]
        except:
            return False, channel["url"]
    return True, None

def get_channels_keyboard():
    keyboard = []
    for ch in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch["url"])])
    keyboard.append([InlineKeyboardButton("✅ I've Joined Both", callback_data="check_join")])
    return InlineKeyboardMarkup(keyboard)

def get_main_keyboard(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT is_premium FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    is_premium = result[0] if result else 0
    conn.close()
    
    keyboard = [
        [InlineKeyboardButton("📤 Upload Bot", callback_data="upload_bot")],
        [InlineKeyboardButton("🤖 My Bots", callback_data="my_bots")],
        [InlineKeyboardButton("⭐ Buy Premium", callback_data="buy_premium")],
    ]
    
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])
        keyboard.append([InlineKeyboardButton("🔑 Create Code", callback_data="create_code")])
    else:
        keyboard.append([InlineKeyboardButton("🎫 Redeem Code", callback_data="redeem_code")])
    
    keyboard.append([InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")])
    
    return InlineKeyboardMarkup(keyboard)

def get_user_bot_count(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM bots WHERE user_id=?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def save_user(user_id, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)",
              (user_id, username, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def generate_premium_code(duration_days):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO premium_codes (code, duration_days) VALUES (?, ?)", (code, duration_days))
    conn.commit()
    conn.close()
    return code

def redeem_code(user_id, code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT duration_days, used_by FROM premium_codes WHERE code=?", (code,))
    result = c.fetchone()
    if not result:
        conn.close()
        return False, "❌ Invalid code!"
    duration_days, used_by = result
    if used_by:
        conn.close()
        return False, "❌ Code already used!"
    
    expiry = (datetime.now() + timedelta(days=duration_days)).isoformat()
    c.execute("UPDATE users SET is_premium=1, premium_expiry=? WHERE user_id=?", (expiry, user_id))
    c.execute("UPDATE premium_codes SET used_by=?, used_at=? WHERE code=?", (user_id, datetime.now().isoformat(), code))
    conn.commit()
    conn.close()
    return True, f"✅ Premium activated for {duration_days} days!"

def start(update, context):
    user = update.effective_user
    save_user(user.id, user.username)
    
    joined, missing_url = is_user_joined_channels(user.id, context.bot)
    if not joined:
        update.message.reply_text(
            f"⚠️ *Access Denied!*\n\nYou must join both channels first:\n👉 {missing_url}",
            reply_markup=get_channels_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    update.message.reply_text(
        f"✅ *Welcome {user.first_name}!*\n\n"
        f"🎯 *DARK HOST (py)*\n"
        f"👤 User: {user.username or user.first_name}\n"
        f"🆔 ID: {user.id}\n\n"
        f"⚡ Send your .py or .zip file to host.\n"
        f"🆓 Free: 1 bot max\n"
        f"👑 Premium: Unlimited\n\n"
        f"🔥 24/7 Hosting!",
        reply_markup=get_main_keyboard(user.id),
        parse_mode="Markdown"
    )

def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    user = query.from_user
    data = query.data
    
    if data == "check_join":
        joined, missing_url = is_user_joined_channels(user.id, context.bot)
        if joined:
            query.edit_message_text("✅ Access granted! Use /start to continue.")
        else:
            query.edit_message_text(f"❌ You haven't joined: {missing_url}", reply_markup=get_channels_keyboard())
    
    elif data == "upload_bot":
        bot_count = get_user_bot_count(user.id)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT is_premium FROM users WHERE user_id=?", (user.id,))
        result = c.fetchone()
        is_premium = result[0] if result else 0
        conn.close()
        
        if not is_premium and bot_count >= FREE_LIMIT:
            query.edit_message_text(f"❌ *LIMIT REACHED*\n\nFree users can only host {FREE_LIMIT} bot.", parse_mode="Markdown")
        else:
            query.edit_message_text("📤 *Upload Your Bot*\n\nSend me your .py or .zip file.", parse_mode="Markdown")
    
    elif data == "my_bots":
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT bot_name, status, start_time FROM bots WHERE user_id=?", (user.id,))
        bots = c.fetchall()
        conn.close()
        
        if not bots:
            query.edit_message_text("📭 *No Bots Found*", parse_mode="Markdown")
            return
        
        text = "🤖 *Your Bots:*\n\n"
        for bot in bots:
            text += f"📌 `{bot[0]}`\n   Status: {bot[1]}\n   Started: {bot[2][:16] if bot[2] else 'Pending'}\n\n"
        query.edit_message_text(text, parse_mode="Markdown")
    
    elif data == "buy_premium":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
        ])
        query.edit_message_text(
            "⭐ *Premium Features*\n\n• Unlimited bots\n• 24/7 hosting\n• Priority support",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    elif data == "redeem_code":
        query.edit_message_text("🎫 Send your code:\n`/redeem YOURCODE`", parse_mode="Markdown")
    
    elif data == "create_code" and user.id == ADMIN_ID:
        query.edit_message_text("🔑 *Create Code*\n\n`/code 30` (30 days)\n`/code 60`\n`/code 365`", parse_mode="Markdown")
    
    elif data == "admin_panel" and user.id == ADMIN_ID:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, user_id, bot_name, submitted_at FROM pending_bots")
        pending = c.fetchall()
        conn.close()
        
        if not pending:
            query.edit_message_text("📭 No pending bots.")
            return
        
        for p in pending:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{p[0]}"),
                 InlineKeyboardButton("❌ Reject", callback_data=f"reject_{p[0]}")]
            ])
            query.message.reply_text(
                f"📄 *Pending Bot*\nUser: {p[1]}\nBot: {p[2]}",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
    
    elif data.startswith("approve_") and user.id == ADMIN_ID:
        bot_id = int(data.split("_")[1])
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id, bot_name, file_path FROM pending_bots WHERE id=?", (bot_id,))
        result = c.fetchone()
        if result:
            user_id, bot_name, file_path = result
            new_path = f"{BOTS_DIR}/user_{user_id}_{bot_name}"
            shutil.move(file_path, new_path)
            c.execute("INSERT INTO bots (user_id, bot_name, file_path, status, start_time) VALUES (?, ?, ?, ?, ?)",
                      (user_id, bot_name, new_path, "running", datetime.now().isoformat()))
            c.execute("DELETE FROM pending_bots WHERE id=?", (bot_id,))
            conn.commit()
            query.edit_message_text(f"✅ Bot `{bot_name}` approved!", parse_mode="Markdown")
            context.bot.send_message(chat_id=user_id, text=f"✅ Your bot `{bot_name}` is now running 24/7!", parse_mode="Markdown")
        conn.close()
    
    elif data.startswith("reject_") and user.id == ADMIN_ID:
        bot_id = int(data.split("_")[1])
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id, bot_name, file_path FROM pending_bots WHERE id=?", (bot_id,))
        result = c.fetchone()
        if result:
            user_id, bot_name, file_path = result
            if os.path.exists(file_path):
                os.remove(file_path)
            c.execute("DELETE FROM pending_bots WHERE id=?", (bot_id,))
            conn.commit()
            query.edit_message_text(f"❌ Bot `{bot_name}` rejected.", parse_mode="Markdown")
            context.bot.send_message(chat_id=user_id, text=f"❌ Your bot `{bot_name}` was rejected.", parse_mode="Markdown")
        conn.close()

def handle_file(update, context):
    user = update.effective_user
    file = update.message.document
    
    if not file.file_name.endswith(('.py', '.zip')):
        update.message.reply_text("❌ Only .py or .zip files allowed!")
        return
    
    bot_count = get_user_bot_count(user.id)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT is_premium FROM users WHERE user_id=?", (user.id,))
    result = c.fetchone()
    is_premium = result[0] if result else 0
    conn.close()
    
    if not is_premium and bot_count >= FREE_LIMIT:
        update.message.reply_text(f"❌ Limit reached! Free users can only host {FREE_LIMIT} bot.")
        return
    
    new_file = file.get_file()
    file_path = f"pending_{user.id}_{int(time.time())}_{file.file_name}"
    new_file.download(file_path)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO pending_bots (user_id, bot_name, file_path, submitted_at) VALUES (?, ?, ?, ?)",
              (user.id, file.file_name, file_path, datetime.now().isoformat()))
    pending_id = c.lastrowid
    conn.commit()
    conn.close()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pending_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pending_id}")]
    ])
    
    context.bot.send_message(
        chat_id=APPROVAL_GROUP_ID,
        text=f"📥 *New Bot*\nUser: @{user.username or user.id}\nFile: {file.file_name}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    update.message.reply_text(f"✅ File received! Pending admin approval.")

def redeem_command(update, context):
    user = update.effective_user
    if len(context.args) != 1:
        update.message.reply_text("Usage: `/redeem CODE`", parse_mode="Markdown")
        return
    code = context.args[0].upper()
    success, msg = redeem_code(user.id, code)
    update.message.reply_text(msg)

def create_code_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ Admin only!")
        return
    if len(context.args) != 1:
        update.message.reply_text("Usage: `/code 30`", parse_mode="Markdown")
        return
    try:
        days = int(context.args[0])
        code = generate_premium_code(days)
        update.message.reply_text(f"✅ Code: `{code}`\nDuration: {days} days", parse_mode="Markdown")
    except:
        update.message.reply_text("❌ Invalid number!")

def error_handler(update, context):
    print(f"Error: {context.error}")

# ==================== MAIN ====================
def main():
    print("=" * 50)
    print("🤖 DARK HOST BOT STARTING...")
    print("=" * 50)
    
    os.makedirs(BOTS_DIR, exist_ok=True)
    
    try:
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("redeem", redeem_command))
        dp.add_handler(CommandHandler("code", create_code_command))
        dp.add_handler(CallbackQueryHandler(callback_handler))
        dp.add_handler(MessageHandler(Filters.document, handle_file))
        dp.add_error_handler(error_handler)
        
        print("✅ Bot started successfully!")
        print("✅ Press Ctrl+C to stop")
        print("=" * 50)
        
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
