#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#  ██████╗ ████████╗    ██╗  ██╗ ██████╗ ███████╗████████╗
#  ██╔══██╗╚══██╔══╝    ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
#  ██║  ██║   ██║       ███████║██║   ██║███████╗   ██║   
#  ██║  ██║   ██║       ██╔══██║██║   ██║╚════██║   ██║   
#  ██████╔╝   ██║       ██║  ██║╚██████╔╝███████║   ██║   
#  ╚═════╝    ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
#  ═══════════════════════════════════════════════════════════════════════════════
#  [:::: DARK HOST v2.0 - ULTIMATE BOT HOSTING SYSTEM ::::]
#  [:::: CODED BY KING WAHID - HACKER STYLE ::::]
#  [:::: 24/7 EXPLOIT READY ::::]
# ═══════════════════════════════════════════════════════════════════════════════

import os
import sys
import time
import json
import shutil
import sqlite3
import subprocess
import random
import string
import re
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Telegram imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ===================================================================================================
# ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
# ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
# ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
# ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
# ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝
# ===================================================================================================

class DarkConfig:
    """🔥 DARK CONFIG - HACKER SETTINGS 🔥"""
    TOKEN = "8697889132:AAG9w86MIdw8CbKj_ddaW9dRrTfulY8qcds"
    ADMIN_ID = 8518408753
    ADMIN_USER = "Kingwahidafg"
    APPROVAL_GROUP = -1003987070217
    
    # Dark channel requirements
    REQUIRED_CHANNELS = [
        {"name": "WAHID MODE X", "url": "https://t.me/WahidModeX", "username": "@WahidModeX"},
        {"name": "PRO TECH 43", "url": "https://t.me/ProTech43", "username": "@ProTech43"}
    ]
    
    # Exploit paths
    BOTS_DIR = "infected_bots"
    DB_FILE = "dark_host.db"
    LOG_FILE = "exploit.log"
    
    # Hack limits
    FREE_LIMIT = 1
    PREMIUM_UNLIMITED = 999
    
    # Colors for console (hacker style)
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ===================================================================================================
# ██████╗  █████╗ ██████╗ ██╗  ██╗
# ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
# ██║  ██║███████║██████╔╝█████╔╝ 
# ██║  ██║██╔══██║██╔══██╗██╔═██╗ 
# ██████╔╝██║  ██║██║  ██║██║  ██╗
# ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
# ===================================================================================================

class DarkDatabase:
    """💀 DARK DATABASE - INFECTED SYSTEM 💀"""
    
    def __init__(self):
        self.db = DarkConfig.DB_FILE
        self._init_infection()
    
    def _init_infection(self):
        """Initialize infected database"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        
        # Users table (infected targets)
        c.execute('''CREATE TABLE IF NOT EXISTS victims (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            is_premium INTEGER DEFAULT 0,
            premium_expiry TEXT DEFAULT NULL,
            join_date TEXT,
            total_bots INTEGER DEFAULT 0
        )''')
        
        # Bots table (zombie bots)
        c.execute('''CREATE TABLE IF NOT EXISTS zombies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bot_name TEXT,
            file_path TEXT,
            status TEXT,
            start_time TEXT,
            process_id INTEGER,
            port INTEGER,
            FOREIGN KEY(user_id) REFERENCES victims(user_id)
        )''')
        
        # Pending infections
        c.execute('''CREATE TABLE IF NOT EXISTS pending_infections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bot_name TEXT,
            file_path TEXT,
            submitted_at TEXT
        )''')
        
        # Premium codes (dark keys)
        c.execute('''CREATE TABLE IF NOT EXISTS dark_keys (
            code TEXT PRIMARY KEY,
            duration_days INTEGER,
            used_by INTEGER DEFAULT NULL,
            used_at TEXT DEFAULT NULL
        )''')
        
        conn.commit()
        conn.close()
        self._log("💀 DATABASE INFECTED SUCCESSFULLY")
    
    def _log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{DarkConfig.PURPLE}[{timestamp}]{DarkConfig.END} {msg}")

# ===================================================================================================
# ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ ███████╗
# ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝
# ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝███████╗
# ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
# ██║  ██║███████╗███████╗██║     ███████╗██║  ██║███████║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
# ===================================================================================================

class DarkHelpers:
    """⚡ DARK HELPER FUNCTIONS ⚡"""
    
    @staticmethod
    def banner():
        """Display hacker banner"""
        banner_text = f"""
{DarkConfig.RED}{DarkConfig.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ██████╗ ██╗  ██╗    ██╗  ██╗ ██████╗ ███████╗████████╗
║  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
║  ██║  ██║███████║██████╔╝█████╔╝     ███████║██║   ██║███████╗   ██║   
║  ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██╔══██║██║   ██║╚════██║   ██║   
║  ██████╔╝██║  ██║██║  ██║██║  ██╗    ██║  ██║╚██████╔╝███████║   ██║   
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
╠══════════════════════════════════════════════════════════════════╣
║  [:::: DARK HOST v2.0 - ULTIMATE BOT HOSTING SYSTEM ::::]
║  [:::: CODED BY KING WAHID - HACKER MODE ::::]
║  [:::: 24/7 EXPLOIT READY ::::]
╚══════════════════════════════════════════════════════════════════╝
{DarkConfig.END}
        """
        print(banner_text)
    
    @staticmethod
    def is_victim_joined(user_id, context):
        """Check if victim joined dark channels"""
        for channel in DarkConfig.REQUIRED_CHANNELS:
            try:
                member = context.bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
                if member.status in ["left", "kicked"]:
                    return False, channel["url"]
            except:
                return False, channel["url"]
        return True, None
    
    @staticmethod
    def get_dark_keyboard(user_id):
        """Generate dark hacker keyboard"""
        db = sqlite3.connect(DarkConfig.DB_FILE)
        c = db.cursor()
        c.execute("SELECT is_premium FROM victims WHERE user_id=?", (user_id,))
        result = c.fetchone()
        is_premium = result[0] if result else 0
        db.close()
        
        keyboard = [
            [InlineKeyboardButton("📤 UPLOAD BOT", callback_data="upload_bot")],
            [InlineKeyboardButton("🤖 MY ZOMBIES", callback_data="my_bots")],
            [InlineKeyboardButton("💀 BUY PREMIUM", callback_data="buy_premium")],
        ]
        
        if user_id == DarkConfig.ADMIN_ID:
            keyboard.append([InlineKeyboardButton("⚙️ DARK PANEL", callback_data="admin_panel")])
            keyboard.append([InlineKeyboardButton("🔑 CREATE DARK KEY", callback_data="create_code")])
        else:
            keyboard.append([InlineKeyboardButton("🎫 REDEEM DARK KEY", callback_data="redeem_code")])
        
        keyboard.append([InlineKeyboardButton("📞 CONTACT ADMIN", url=f"https://t.me/{DarkConfig.ADMIN_USER}")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def generate_dark_key(days):
        """Generate a dark premium key"""
        code = ''.join(random.choices(string.ascii_uppercase + string.digits + "!@#$%", k=16))
        conn = sqlite3.connect(DarkConfig.DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO dark_keys (code, duration_days) VALUES (?, ?)", (code, days))
        conn.commit()
        conn.close()
        return code

# ===================================================================================================
# ██████╗  ██████╗ ████████╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
# ██╔══██╗██╔═══██╗╚══██╔══╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
# ██████╔╝██║   ██║   ██║       ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
# ██╔══██╗██║   ██║   ██║       ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
# ██████╔╝╚██████╔╝   ██║       ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
# ╚═════╝  ╚═════╝    ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
# ===================================================================================================

class DarkBot:
    """💀 MAIN DARK BOT - HACKER EDITION 💀"""
    
    def __init__(self):
        self.db = DarkDatabase()
        self.helpers = DarkHelpers()
        self.config = DarkConfig
        self.app = None
    
    def run(self):
        """Execute the dark bot"""
        self.helpers.banner()
        
        # Create necessary directories
        os.makedirs(self.config.BOTS_DIR, exist_ok=True)
        
        # Build application
        self.app = Application.builder().token(self.config.TOKEN).build()
        
        # Register handlers
        self._register_handlers()
        
        print(f"{self.config.GREEN}[✓] DARK BOT ACTIVATED{self.config.END}")
        print(f"{self.config.YELLOW}[!] TARGET: TELEGRAM{self.config.END}")
        print(f"{self.config.RED}[!] MODE: 24/7 EXPLOIT{self.config.END}")
        print(f"{self.config.CYAN}[*] WAITING FOR VICTIMS...{self.config.END}\n")
        
        # Start polling
        self.app.run_polling()
    
    def _register_handlers(self):
        """Register all dark handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("redeem", self.redeem_key))
        self.app.add_handler(CommandHandler("darkcode", self.create_dark_key))
        self.app.add_handler(CallbackQueryHandler(self.callback_router))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_upload))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Dark start command"""
        victim = update.effective_user
        
        # Register victim
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO victims (user_id, username, join_date) VALUES (?, ?, ?)",
                  (victim.id, victim.username, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        # Check channel join
        joined, missing = self.helpers.is_victim_joined(victim.id, context)
        if not joined:
            keyboard = []
            for ch in self.config.REQUIRED_CHANNELS:
                keyboard.append([InlineKeyboardButton(f"📢 JOIN {ch['name']}", url=ch["url"])])
            keyboard.append([InlineKeyboardButton("✅ VERIFY ACCESS", callback_data="verify")])
            
            await update.message.reply_text(
                f"🔥 *ACCESS DENIED* 🔥\n\n"
                f"⚠️ You must join our dark channels first!\n"
                f"👉 {missing}\n\n"
                f"┌─⊷ 𝐉𝐨𝐢𝐧 𝐓𝐨 𝐂𝐨𝐧𝐭𝐢𝐧𝐮𝐞\n"
                f"└──⊷ 𝐀𝐟𝐭𝐞𝐫 𝐣𝐨𝐢𝐧𝐢𝐧𝐠 𝐜𝐥𝐢𝐜𝐤 𝐕𝐄𝐑𝐈𝐅𝐘",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return
        
        # Get victim status
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT is_premium FROM victims WHERE user_id=?", (victim.id,))
        result = c.fetchone()
        is_premium = result[0] if result else 0
        conn.close()
        
        status = "👑 PREMIUM HACKER" if is_premium else "🆓 FREE SCRIPT KIDDIE"
        limit = "UNLIMITED" if is_premium else f"{self.config.FREE_LIMIT} BOT"
        
        await update.message.reply_text(
            f"┌─────────────────────────────┐\n"
            f"│  💀 *DARK HOST ACTIVATED* 💀  │\n"
            f"└─────────────────────────────┘\n\n"
            f"🔥 *VICTIM:* `{victim.username or victim.first_name}`\n"
            f"🎯 *ID:* `{victim.id}`\n"
            f"⚡ *STATUS:* {status}\n"
            f"📦 *LIMIT:* {limit}\n\n"
            f"┌─⊷ 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐁𝐎𝐓 𝐅𝐈𝐋𝐄\n"
            f"├─⊷ (.py or .zip)\n"
            f"└──⊷ 𝐀𝐃𝐌𝐈𝐍 𝐖𝐈𝐋𝐋 𝐀𝐏𝐏𝐑𝐎𝐕𝐄",
            reply_markup=self.helpers.get_dark_keyboard(victim.id),
            parse_mode="Markdown"
        )
    
    async def callback_router(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route all callbacks"""
        query = update.callback_query
        await query.answer()
        user = query.from_user
        data = query.data
        
        if data == "verify":
            await self._verify_access(query, context, user)
        elif data == "upload_bot":
            await self._upload_prompt(query, user)
        elif data == "my_bots":
            await self._list_zombies(query, user)
        elif data == "buy_premium":
            await self._premium_info(query)
        elif data == "redeem_code":
            await self._redeem_prompt(query)
        elif data == "create_code" and user.id == self.config.ADMIN_ID:
            await self._create_code_prompt(query)
        elif data == "admin_panel" and user.id == self.config.ADMIN_ID:
            await self._admin_panel(query, context)
        elif data.startswith("approve_"):
            await self._approve_bot(query, context)
        elif data.startswith("reject_"):
            await self._reject_bot(query, context)
    
    async def _verify_access(self, query, context, user):
        """Verify channel access"""
        joined, missing = self.helpers.is_victim_joined(user.id, context)
        if joined:
            await query.edit_message_text("✅ *ACCESS GRANTED* ✅\n\nUse /start to enter the dark system.", parse_mode="Markdown")
        else:
            await query.edit_message_text(f"❌ *ACCESS DENIED*\n\nYou haven't joined: {missing}", parse_mode="Markdown")
    
    async def _upload_prompt(self, query, user):
        """Prompt for bot upload"""
        # Check limit
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM zombies WHERE user_id=?", (user.id,))
        bot_count = c.fetchone()[0]
        c.execute("SELECT is_premium FROM victims WHERE user_id=?", (user.id,))
        result = c.fetchone()
        is_premium = result[0] if result else 0
        conn.close()
        
        if not is_premium and bot_count >= self.config.FREE_LIMIT:
            await query.edit_message_text(
                f"💀 *LIMIT REACHED* 💀\n\n"
                f"Free victims can only host `{self.config.FREE_LIMIT}` bot.\n\n"
                f"🔑 Buy premium to unlock:\n"
                f"├─⊷ UNLIMITED BOTS\n"
                f"├─⊷ 24/7 UPTIME\n"
                f"└─⊷ PRIORITY SUPPORT",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                f"📤 *UPLOAD YOUR BOT* 📤\n\n"
                f"┌─⊷ Send your file:\n"
                f"├─⊷ `.py` - Single file bot\n"
                f"└─⊷ `.zip` - With requirements.txt\n\n"
                f"⚠️ Admin will review your submission",
                parse_mode="Markdown"
            )
    
    async def _list_zombies(self, query, user):
        """List user's zombie bots"""
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT bot_name, status, start_time FROM zombies WHERE user_id=?", (user.id,))
        bots = c.fetchall()
        conn.close()
        
        if not bots:
            await query.edit_message_text(
                f"💀 *NO ZOMBIES FOUND* 💀\n\n"
                f"┌─⊷ You haven't uploaded any bots yet.\n"
                f"└──⊷ Use UPLOAD BOT to start your infection.",
                parse_mode="Markdown"
            )
            return
        
        text = f"💀 *YOUR ZOMBIE ARMY* 💀\n\n"
        for i, bot in enumerate(bots, 1):
            text += f"┌─⊷ `{bot[0]}`\n"
            text += f"├─⊷ Status: {bot[1]}\n"
            text += f"└─⊷ Started: {bot[2][:16] if bot[2] else 'Pending'}\n\n"
        
        await query.edit_message_text(text, parse_mode="Markdown")
    
    async def _premium_info(self, query):
        """Show premium info"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 CONTACT ADMIN", url=f"https://t.me/{self.config.ADMIN_USER}")]
        ])
        await query.edit_message_text(
            f"💀 *PREMIUM HACKER ACCESS* 💀\n\n"
            f"┌─⊷ *FEATURES:*\n"
            f"├─⊷ 🔥 Unlimited bot hosting\n"
            f"├─⊷ ⚡ 24/7 uptime guaranteed\n"
            f"├─⊷ 🚀 Priority approval\n"
            f"├─⊷ 🛡️ DDoS protection\n"
            f"└─⊷ 💀 Dark support\n\n"
            f"💵 *PRICE:* Contact @{self.config.ADMIN_USER}\n\n"
            f"┌─⊷ Payment methods:\n"
            f"├─⊷ USDT / BTC\n"
            f"└─⊷ Perfect Money",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    async def _redeem_prompt(self, query):
        """Prompt for redeem code"""
        await query.edit_message_text(
            f"🔑 *REDEEM DARK KEY* 🔑\n\n"
            f"Send your premium code:\n"
            f"`/redeem YOUR_DARK_KEY`\n\n"
            f"Example:\n"
            f"`/redeem XK9!@#$%ABC123`",
            parse_mode="Markdown"
        )
    
    async def _create_code_prompt(self, query):
        """Prompt admin to create code"""
        await query.edit_message_text(
            f"🔑 *CREATE DARK KEY* 🔑\n\n"
            f"Usage:\n"
            f"`/darkcode 30` - 30 days premium\n"
            f"`/darkcode 60` - 60 days premium\n"
            f"`/darkcode 365` - 1 year premium\n\n"
            f"Example:\n"
            f"`/darkcode 30`",
            parse_mode="Markdown"
        )
    
    async def _admin_panel(self, query, context):
        """Admin panel to view pending bots"""
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, user_id, bot_name, file_path, submitted_at FROM pending_infections")
        pending = c.fetchall()
        conn.close()
        
        if not pending:
            await query.edit_message_text("💀 *NO PENDING INFECTIONS* 💀", parse_mode="Markdown")
            return
        
        for p in pending:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{p[0]}"),
                 InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{p[0]}")]
            ])
            await query.message.reply_text(
                f"💀 *PENDING BOT* 💀\n\n"
                f"┌─⊷ ID: `{p[0]}`\n"
                f"├─⊷ User: `{p[1]}`\n"
                f"├─⊷ Bot: `{p[2]}`\n"
                f"└─⊷ Time: `{p[4][:16]}`",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
    
    async def _approve_bot(self, query, context):
        """Approve and run the bot"""
        if query.from_user.id != self.config.ADMIN_ID:
            await query.edit_message_text("❌ *ACCESS DENIED* - Admin only!", parse_mode="Markdown")
            return
        
        bot_id = int(query.data.split("_")[1])
        
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id, bot_name, file_path FROM pending_infections WHERE id=?", (bot_id,))
        result = c.fetchone()
        
        if not result:
            await query.edit_message_text("❌ Bot not found!", parse_mode="Markdown")
            conn.close()
            return
        
        user_id, bot_name, file_path = result
        
        # Move to zombies
        new_path = f"{self.config.BOTS_DIR}/zombie_{user_id}_{int(time.time())}_{bot_name}"
        shutil.move(file_path, new_path)
        
        # Insert into zombies
        c.execute("INSERT INTO zombies (user_id, bot_name, file_path, status, start_time) VALUES (?, ?, ?, ?, ?)",
                  (user_id, bot_name, new_path, "running", datetime.now().isoformat()))
        zombie_id = c.lastrowid
        c.execute("DELETE FROM pending_infections WHERE id=?", (bot_id,))
        conn.commit()
        conn.close()
        
        # Run the zombie bot
        process = subprocess.Popen(["python", new_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Update process ID
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("UPDATE zombies SET process_id=? WHERE id=?", (process.pid, zombie_id))
        conn.commit()
        conn.close()
        
        await query.edit_message_text(f"✅ *BOT APPROVED* ✅\n\nBot `{bot_name}` is now running 24/7!", parse_mode="Markdown")
        await context.bot.send_message(chat_id=user_id, text=f"💀 *YOUR BOT IS ACTIVE* 💀\n\nBot `{bot_name}` has been approved and is now running 24/7!\n\n🔥 Welcome to the dark side.", parse_mode="Markdown")
    
    async def _reject_bot(self, query, context):
        """Reject and delete bot"""
        if query.from_user.id != self.config.ADMIN_ID:
            await query.edit_message_text("❌ *ACCESS DENIED* - Admin only!", parse_mode="Markdown")
            return
        
        bot_id = int(query.data.split("_")[1])
        
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id, bot_name, file_path FROM pending_infections WHERE id=?", (bot_id,))
        result = c.fetchone()
        
        if result:
            user_id, bot_name, file_path = result
            if os.path.exists(file_path):
                os.remove(file_path)
            c.execute("DELETE FROM pending_infections WHERE id=?", (bot_id,))
            await query.edit_message_text(f"❌ *BOT REJECTED* ❌\n\nBot `{bot_name}` has been deleted.", parse_mode="Markdown")
            await context.bot.send_message(chat_id=user_id, text=f"❌ Your bot `{bot_name}` was rejected by admin.\n\nReason: Does not meet our standards.", parse_mode="Markdown")
        
        conn.commit()
        conn.close()
    
    async def handle_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle file upload from victim"""
        victim = update.effective_user
        file = update.message.document
        
        # Check file type
        if not file.file_name.endswith(('.py', '.zip')):
            await update.message.reply_text("❌ *INVALID FILE* ❌\n\nOnly `.py` or `.zip` files are allowed!", parse_mode="Markdown")
            return
        
        # Check limit
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM zombies WHERE user_id=?", (victim.id,))
        bot_count = c.fetchone()[0]
        c.execute("SELECT is_premium FROM victims WHERE user_id=?", (victim.id,))
        result = c.fetchone()
        is_premium = result[0] if result else 0
        conn.close()
        
        if not is_premium and bot_count >= self.config.FREE_LIMIT:
            await update.message.reply_text(
                f"💀 *LIMIT REACHED* 💀\n\n"
                f"Free victims: `{self.config.FREE_LIMIT}` bot only!\n"
                f"Buy premium for unlimited access.",
                parse_mode="Markdown"
            )
            return
        
        # Download file
        new_file = await file.get_file()
        file_path = f"infection_{victim.id}_{int(time.time())}_{file.file_name}"
        await new_file.download_to_drive(file_path)
        
        # Save to pending
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO pending_infections (user_id, bot_name, file_path, submitted_at) VALUES (?, ?, ?, ?)",
                  (victim.id, file.file_name, file_path, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        # Send to approval group
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{c.lastrowid}"),
             InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{c.lastrowid}")]
        ])
        
        await context.bot.send_message(
            chat_id=self.config.APPROVAL_GROUP,
            text=f"💀 *NEW BOT UPLOAD* 💀\n\n"
                 f"┌─⊷ Victim: @{victim.username or victim.id}\n"
                 f"├─⊷ File: `{file.file_name}`\n"
                 f"├─⊷ Type: {'PREMIUM' if is_premium else 'FREE'}\n"
                 f"└─⊷ Time: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
                 f"❓ *APPROVE THIS BOT?*",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(
            f"💀 *FILE RECEIVED* 💀\n\n"
            f"┌─⊷ Name: `{file.file_name}`\n"
            f"├─⊷ Size: `{file.file_size:,}` bytes\n"
            f"└─⊷ Status: `PENDING REVIEW`\n\n"
            f"⚡ Admin will review your submission.\n"
            f"You'll be notified when approved.",
            parse_mode="Markdown"
        )
    
    async def redeem_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redeem dark premium key"""
        user = update.effective_user
        
        if len(context.args) != 1:
            await update.message.reply_text("💀 *USAGE* 💀\n\n`/redeem DARK_KEY`", parse_mode="Markdown")
            return
        
        code = context.args[0].upper()
        
        conn = sqlite3.connect(self.config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT duration_days, used_by FROM dark_keys WHERE code=?", (code,))
        result = c.fetchone()
        
        if not result:
            await update.message.reply_text("❌ *INVALID DARK KEY* ❌", parse_mode="Markdown")
            conn.close()
            return
        
        duration_days, used_by = result
        if used_by:
            await update.message.reply_text("❌ *DARK KEY ALREADY USED* ❌", parse_mode="Markdown")
            conn.close()
            return
        
        expiry = (datetime.now() + timedelta(days=duration_days)).isoformat()
        c.execute("UPDATE victims SET is_premium=1, premium_expiry=? WHERE user_id=?", (expiry, user.id))
        c.execute("UPDATE dark_keys SET used_by=?, used_at=? WHERE code=?", (user.id, datetime.now().isoformat(), code))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            f"✅ *PREMIUM ACTIVATED* ✅\n\n"
            f"┌─⊷ Duration: `{duration_days}` days\n"
            f"├─⊷ Status: `PREMIUM HACKER`\n"
            f"└─⊷ Limit: `UNLIMITED BOTS`\n\n"
            f"🔥 Welcome to the dark side!",
            parse_mode="Markdown"
        )
    
    async def create_dark_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Create dark key (admin only)"""
        if update.effective_user.id != self.config.ADMIN_ID:
            await update.message.reply_text("❌ *ACCESS DENIED* - Admin only!", parse_mode="Markdown")
            return
        
        if len(context.args) != 1:
            await update.message.reply_text("💀 *USAGE* 💀\n\n`/darkcode 30`", parse_mode="Markdown")
            return
        
        try:
            days = int(context.args[0])
            if days <= 0:
                raise ValueError
        except:
            await update.message.reply_text("❌ *INVALID DAYS* - Must be a positive number!", parse_mode="Markdown")
            return
        
        code = self.helpers.generate_dark_key(days)
        
        await update.message.reply_text(
            f"🔑 *DARK KEY CREATED* 🔑\n\n"
            f"┌─⊷ Code: `{code}`\n"
            f"├─⊷ Duration: `{days}` days\n"
            f"└─⊷ Status: `UNUSED`\n\n"
            f"⚠️ Share this key with victims.",
            parse_mode="Markdown"
        )

# ===================================================================================================
# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
# ===================================================================================================

if __name__ == "__main__":
    bot = DarkBot()
    bot.run()
