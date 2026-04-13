"""
🤖 BOT HOSTING SYSTEM - د نورو بوټونو د چلولو سیستم
کارن خپل بوټ فایل استوي، او تاسو تصویب کړئ، نو بوټ به چلیږي
"""

import os
import subprocess
import sqlite3
import shutil
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ========== تنظیمات ==========
TOKEN = "8697889132:AAG9w86MIdw8CbKj_ddaW9dRrTfulY8qcds"
ADMIN_ID = 8518408753
ADMIN_USERNAME = "Kingwahidafg"
APPROVAL_GROUP_ID = -1003987070217  # د تصویب ګروپ آي ډي

BOTS_DIR = "user_bots"  # د بوټونو د ساتلو ځای
DB_FILE = "hosting.db"  # د معلوماتو ډیټابیس
# ==============================

# ډیټابیس جوړول
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # د کارنانو جدول
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        join_date TEXT
    )''')
    
    # د بوټونو جدول (چلیږي بوټونه)
    c.execute('''CREATE TABLE IF NOT EXISTS running_bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        start_time TEXT,
        process_id INTEGER,
        status TEXT
    )''')
    
    # د انتظار بوټونو جدول
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

# ========== مرستندویه دندې ==========
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

def approve_bot(pending_id, admin_bot):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, bot_name, file_path FROM pending_bots WHERE id=?", (pending_id,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return None, None, None
    
    user_id, bot_name, old_path = result
    
    # نوی ځای ته بوټ انتقالول
    new_path = os.path.join(BOTS_DIR, f"user_{user_id}_{int(datetime.now().timestamp())}_{bot_name}")
    shutil.move(old_path, new_path)
    
    # بوټ چلول
    try:
        process = subprocess.Popen(["python", new_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process_id = process.pid
        
        # ډیټابیس ته اضافه کول
        c.execute('''INSERT INTO running_bots (user_id, bot_name, file_path, start_time, process_id, status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, bot_name, new_path, datetime.now().isoformat(), process_id, "running"))
        
        # له انتظار څخه لرې کول
        c.execute("DELETE FROM pending_bots WHERE id=?", (pending_id,))
        conn.commit()
        
        # کارونکي ته خبر ورکول
        admin_bot.send_message(chat_id=user_id, text=f"✅ ستاسو بوټ `{bot_name}` تصویب شو او اوس چلیږي!", parse_mode="Markdown")
        
        conn.close()
        return user_id, bot_name, process_id
        
    except Exception as e:
        conn.close()
        return None, None, str(e)

def reject_bot(pending_id, admin_bot):
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
        admin_bot.send_message(chat_id=user_id, text=f"❌ ستاسو بوټ `{bot_name}` رد شو.", parse_mode="Markdown")
    
    conn.close()

def get_user_bots(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT bot_name, status, start_time FROM running_bots WHERE user_id=?", (user_id,))
    bots = c.fetchall()
    conn.close()
    return bots

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📤 Upload Bot", callback_data="upload")],
        [InlineKeyboardButton("🤖 My Bots", callback_data="mybots")],
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("📤 Upload Bot", callback_data="upload")],
        [InlineKeyboardButton("🤖 My Bots", callback_data="mybots")],
        [InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin")],
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== د بوټ دندې ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username)
    
    welcome_text = f"""✅ *Welcome {user.first_name}!*

🤖 *Bot Hosting System*

📌 Send me your `.py` file
👑 I will run it for you 24/7

📤 Click Upload Bot to start
"""

    if user.id == ADMIN_ID:
        await update.message.reply_text(welcome_text, reply_markup=get_admin_keyboard(), parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data
    
    if data == "upload":
        await query.edit_message_text(
            "📤 *Send Your Bot File*\n\n"
            "Please send me your `.py` file.\n\n"
            "⚠️ Admin will review it first.\n"
            "✅ After approval, your bot will run 24/7!",
            parse_mode="Markdown"
        )
    
    elif data == "mybots":
        bots = get_user_bots(user.id)
        if not bots:
            await query.edit_message_text("📭 *No Bots Found*\n\nYou haven't uploaded any bots yet.", parse_mode="Markdown")
            return
        
        text = "🤖 *Your Bots:*\n\n"
        for bot in bots:
            text += f"📌 `{bot[0]}`\n   Status: {bot[1]}\n   Started: {bot[2][:16]}\n\n"
        await query.edit_message_text(text, parse_mode="Markdown")
    
    elif data == "admin" and user.id == ADMIN_ID:
        pending = get_pending_bots()
        if not pending:
            await query.edit_message_text("📭 *No Pending Bots*", parse_mode="Markdown")
            return
        
        for p in pending:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{p[0]}"),
                 InlineKeyboardButton("❌ Reject", callback_data=f"reject_{p[0]}")]
            ])
            await query.message.reply_text(
                f"📄 *Pending Bot*\n"
                f"ID: `{p[0]}`\n"
                f"User: `{p[1]}`\n"
                f"Bot: `{p[2]}`\n"
                f"Time: `{p[4][:16]}`",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        await query.delete_message()
    
    elif data.startswith("approve_") and user.id == ADMIN_ID:
        pending_id = int(data.split("_")[1])
        user_id, bot_name, result = approve_bot(pending_id, context.bot)
        
        if result is None and user_id is None:
            await query.edit_message_text("❌ Bot not found!")
        elif isinstance(result, str):
            await query.edit_message_text(f"❌ Error: {result}")
        else:
            await query.edit_message_text(f"✅ Bot `{bot_name}` approved and running!", parse_mode="Markdown")
    
    elif data.startswith("reject_") and user.id == ADMIN_ID:
        pending_id = int(data.split("_")[1])
        reject_bot(pending_id, context.bot)
        await query.edit_message_text("❌ Bot rejected and deleted.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file = update.message.document
    
    # یوازې .py فایلونه منل
    if not file.file_name.endswith('.py'):
        await update.message.reply_text("❌ Only `.py` files are allowed!")
        return
    
    # فایل ډاونلوډ کول
    new_file = await file.get_file()
    file_path = f"pending_{user.id}_{int(datetime.now().timestamp())}_{file.file_name}"
    await new_file.download_to_drive(file_path)
    
    # انتظار لیست کې اضافه کول
    pending_id = add_pending(user.id, file.file_name, file_path)
    
    # ادمین ته خبر ورکول
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pending_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pending_id}")]
    ])
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 *New Bot Upload*\n\n"
             f"👤 User: @{user.username or user.id}\n"
             f"📁 File: `{file.file_name}`\n\n"
             f"❓ Do you want to run this bot?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    # ګروپ ته هم خبر ورکول (که تنظیم شوی وي)
    if APPROVAL_GROUP_ID:
        try:
            await context.bot.send_message(
                chat_id=APPROVAL_GROUP_ID,
                text=f"📥 *New Bot Upload*\n\n👤 User: @{user.username or user.id}\n📁 File: `{file.file_name}`",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except:
            pass
    
    await update.message.reply_text(
        f"✅ *File Received!*\n\n"
        f"📌 Name: `{file.file_name}`\n"
        f"⏳ Status: `Pending Approval`\n\n"
        f"Admin will review your bot.\n"
        f"You'll be notified when approved.",
        parse_mode="Markdown"
    )

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """د بوټ د بندولو امر - یوازې ادمین"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Only admin can use this!")
        return
    
    await update.message.reply_text("🛑 Bot is stopping...")
    os._exit(0)

# ========== اصلي دنده ==========
def main():
    print("=" * 50)
    print("🤖 BOT HOSTING SYSTEM STARTING...")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    # دندې ثبتول
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    print("✅ Bot is running!")
    print("📌 Send /start to begin")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()
