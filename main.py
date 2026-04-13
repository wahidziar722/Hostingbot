#!/usr/bin/env python3
"""
🤖 COMPLETE BOT HOSTING SYSTEM
- د نورو بوټونو کوربه توب
- د requirements.txt ملاتړ
- یوازې یو چینل (WahidModeX)
"""

import os
import subprocess
import sqlite3
import shutil
import time
import zipfile
import sys
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

# ==================== کانفیګ ====================
TOKEN = "8697889132:AAG9w86MIdw8CbKj_ddaW9dRrTfulY8qcds"
ADMIN_ID = 8518408753
ADMIN_USERNAME = "Kingwahidafg"

# یوازې یو چینل - ProTech43 لرې شو
REQUIRED_CHANNEL = {
    "username": "@WahidModeX",
    "url": "https://t.me/WahidModeX",
    "name": "𝐖𝐀𝐇𝐈𝐃 𝐌𝐎𝐃"
}

BOTS_DIR = "hosted_bots"
DB_FILE = "hosting.db"
FREE_LIMIT = 999  # هر څوک کولی شي ډیری بوټونه واستوي
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
    c.execute('''CREATE TABLE IF NOT EXISTS bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        bot_path TEXT,
        status TEXT,
        start_time TEXT,
        process_id INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()
os.makedirs(BOTS_DIR, exist_ok=True)

# ========== د چینل تصدیق ==========
def check_channel(user_id, bot):
    """یوازې یو چینل چیک کوي"""
    try:
        member = bot.get_chat_member(chat_id=REQUIRED_CHANNEL["username"], user_id=user_id)
        if member.status in ["left", "kicked"]:
            return False
        return True
    except:
        return False

def get_channel_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"📢 Join {REQUIRED_CHANNEL['name']}", url=REQUIRED_CHANNEL["url"])],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📤 Upload Bot", callback_data="upload")],
        [InlineKeyboardButton("🤖 My Bots", callback_data="mybots")],
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    if update.effective_user.id == ADMIN_ID:
        keyboard.insert(0, [InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin")])
    return InlineKeyboardMarkup(keyboard)

# ========== د بوټ چلول ==========
def install_requirements(bot_path):
    """د requirements.txt نصبول"""
    req_file = os.path.join(bot_path, "requirements.txt")
    if os.path.exists(req_file):
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], 
                          capture_output=True, timeout=120)
            return True
        except:
            return False
    return True

def run_user_bot(bot_path, bot_name):
    """د کارونکي بوټ چلول"""
    try:
        # د requirements نصبول
        install_requirements(bot_path)
        
        # د بوټ فایل موندل
        bot_file = None
        for f in os.listdir(bot_path):
            if f.endswith('.py'):
                bot_file = os.path.join(bot_path, f)
                break
        
        if not bot_file:
            return False, "No .py file found"
        
        # بوټ چلول
        process = subprocess.Popen(
            [sys.executable, bot_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=bot_path
        )
        
        return True, process.pid
    except Exception as e:
        return False, str(e)

def extract_zip(zip_path, extract_to):
    """ZIP فایل استخراج کوي"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except:
        return False

# ========== د بوټ دندې ==========
def start(update, context):
    user = update.effective_user
    
    # چینل چیک کول
    if not check_channel(user.id, context.bot):
        update.message.reply_text(
            f"⚠️ *Access Denied!*\n\nYou must join the channel first:\n👉 {REQUIRED_CHANNEL['url']}",
            reply_markup=get_channel_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # کارونکی خوندي کول
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)",
              (user.id, user.username, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    update.message.reply_text(
        f"✅ *Welcome {user.first_name}!*\n\n"
        f"🤖 *Bot Hosting System*\n\n"
        f"📌 Send me your `.py` or `.zip` file\n"
        f"👑 I will run it for you 24/7\n\n"
        f"🔥 Your bot will start immediately!",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    user = query.from_user
    data = query.data
    
    if data == "check_join":
        if check_channel(user.id, context.bot):
            query.edit_message_text("✅ Access granted! Send your bot file.")
        else:
            query.edit_message_text("❌ You haven't joined the channel yet!", reply_markup=get_channel_keyboard())
    
    elif data == "upload":
        query.edit_message_text(
            "📤 *Upload Your Bot*\n\n"
            "Send me:\n"
            "• `.py` file - Single file bot\n"
            "• `.zip` file - With requirements.txt\n\n"
            "Your bot will run immediately!",
            parse_mode="Markdown"
        )
    
    elif data == "mybots":
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT bot_name, status, start_time FROM bots WHERE user_id=?", (user.id,))
        bots = c.fetchall()
        conn.close()
        
        if not bots:
            query.edit_message_text("📭 *No Bots Found*\n\nSend your .py file to get started!", parse_mode="Markdown")
            return
        
        text = "🤖 *Your Bots:*\n\n"
        for bot in bots:
            text += f"📌 `{bot[0]}`\n   Status: {bot[1]}\n   Started: {bot[2][:16]}\n\n"
        query.edit_message_text(text, parse_mode="Markdown")
    
    elif data == "admin" and user.id == ADMIN_ID:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, user_id, bot_name, status FROM bots")
        bots = c.fetchall()
        conn.close()
        
        if not bots:
            query.edit_message_text("📭 No bots running.")
            return
        
        text = "⚙️ *Admin Panel - All Bots*\n\n"
        for bot in bots:
            text += f"ID: {bot[0]} | User: {bot[1]} | Bot: {bot[2]} | Status: {bot[3]}\n"
        query.edit_message_text(text, parse_mode="Markdown")

def handle_file(update, context):
    """کله چې کارونکی فایل استوي، بوټ یې چلوي"""
    user = update.effective_user
    
    # چینل چیک کول
    if not check_channel(user.id, context.bot):
        update.message.reply_text("❌ Please join the channel first! Use /start")
        return
    
    file = update.message.document
    file_name = file.file_name
    
    # د فایل ډول چیک کول
    if not (file_name.endswith('.py') or file_name.endswith('.zip')):
        update.message.reply_text("❌ Only `.py` or `.zip` files are allowed!")
        return
    
    update.message.reply_text(f"📥 Downloading `{file_name}`...", parse_mode="Markdown")
    
    # د کارونکي فولډر جوړول
    user_folder = os.path.join(BOTS_DIR, f"user_{user.id}_{int(time.time())}")
    os.makedirs(user_folder, exist_ok=True)
    
    # فایل ډاونلوډ کول
    file_path = os.path.join(user_folder, file_name)
    new_file = file.get_file()
    new_file.download(file_path)
    
    # که ZIP وي، استخراج یې کړئ
    if file_name.endswith('.zip'):
        update.message.reply_text("📦 Extracting zip file...")
        if not extract_zip(file_path, user_folder):
            update.message.reply_text("❌ Failed to extract zip file!")
            shutil.rmtree(user_folder)
            return
        os.remove(file_path)  # ZIP فایل ډیلیټ کړئ
        bot_name = file_name.replace('.zip', '')
    else:
        bot_name = file_name.replace('.py', '')
    
    # بوټ چلول
    update.message.reply_text("🚀 Starting your bot...")
    success, result = run_user_bot(user_folder, bot_name)
    
    if success:
        # ډیټابیس کې خوندي کول
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''INSERT INTO bots (user_id, bot_name, bot_path, status, start_time, process_id)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user.id, bot_name, user_folder, "running", datetime.now().isoformat(), result))
        conn.commit()
        conn.close()
        
        update.message.reply_text(
            f"✅ *Bot Started Successfully!*\n\n"
            f"📌 Name: `{bot_name}`\n"
            f"🆔 Process ID: `{result}`\n\n"
            f"🔥 Your bot is now running 24/7!\n"
            f"📝 If your bot has a token, make sure it's correct.",
            parse_mode="Markdown"
        )
        
        # ادمین ته خبر ورکول
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚀 *New Bot Hosted*\n\n👤 User: @{user.username or user.id}\n🤖 Bot: `{bot_name}`\n🆔 PID: `{result}`",
            parse_mode="Markdown"
        )
    else:
        update.message.reply_text(
            f"❌ *Failed to start bot!*\n\nError: `{result}`\n\n"
            f"Make sure your bot has a valid token and no syntax errors.",
            parse_mode="Markdown"
        )
        shutil.rmtree(user_folder)

def list_all_bots(update, context):
    """د ټولو چلیږو بوټونو لست (یوازې ادمین)"""
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ Admin only!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, user_id, bot_name, status, process_id FROM bots")
    bots = c.fetchall()
    conn.close()
    
    if not bots:
        update.message.reply_text("📭 No bots running.")
        return
    
    text = "🤖 *All Running Bots:*\n\n"
    for bot in bots:
        text += f"📌 ID: {bot[0]} | User: {bot[1]}\n   Bot: `{bot[2]}`\n   Status: {bot[3]} | PID: {bot[4]}\n\n"
    update.message.reply_text(text, parse_mode="Markdown")

def stop_bot(update, context):
    """یو بوټ بندول (یوازې ادمین)"""
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ Admin only!")
        return
    
    if len(context.args) != 1:
        update.message.reply_text("Usage: `/stopbot BOT_ID`\n\nUse `/list` to see bot IDs.", parse_mode="Markdown")
        return
    
    try:
        bot_id = int(context.args[0])
    except:
        update.message.reply_text("❌ Please provide a valid bot ID!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT bot_name, bot_path, process_id FROM bots WHERE id=?", (bot_id,))
    result = c.fetchone()
    
    if not result:
        update.message.reply_text(f"❌ Bot with ID `{bot_id}` not found!", parse_mode="Markdown")
        conn.close()
        return
    
    bot_name, bot_path, process_id = result
    
    # پروسه بندول
    try:
        os.kill(process_id, 9)
    except:
        pass
    
    # فولډر ډیلیټ کول
    if os.path.exists(bot_path):
        shutil.rmtree(bot_path)
    
    c.execute("DELETE FROM bots WHERE id=?", (bot_id,))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"✅ Bot `{bot_name}` stopped and deleted!", parse_mode="Markdown")

def error_handler(update, context):
    print(f"Error: {context.error}")

# ==================== اصلي دنده ====================
def main():
    print("=" * 50)
    print("🤖 COMPLETE BOT HOSTING SYSTEM")
    print("=" * 50)
    
    # Create updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list_all_bots))
    dp.add_handler(CommandHandler("stopbot", stop_bot))
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
