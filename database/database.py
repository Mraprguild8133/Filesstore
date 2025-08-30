# Codeflix_Botz
# rohit_1888 on Tg

import asyncio
import logging
import sqlite3
import aiosqlite
from typing import List, Optional, Tuple
from config import DB_NAME  # Now will be SQLite database file

logging.basicConfig(level=logging.INFO)

class Rohit:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize SQL database with required tables"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Admins table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Banned users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS banned_users (
                    user_id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Auto delete timer settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS del_timer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INTEGER DEFAULT 600,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Channels table (for fsub)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER PRIMARY KEY,
                    mode TEXT DEFAULT 'off',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Request force-sub users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS request_forcesub_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(channel_id, user_id),
                    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
                )
            ''')
            
            # Insert default timer if not exists
            cursor.execute('INSERT OR IGNORE INTO del_timer (id, value) VALUES (1, 600)')
            
            conn.commit()

    # USER DATA
    async def present_user(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT 1 FROM users WHERE user_id = ?', 
                (user_id,)
            )
            result = await cursor.fetchone()
            return result is not None

    async def add_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    'INSERT OR IGNORE INTO users (user_id) VALUES (?)', 
                    (user_id,)
                )
                await db.commit()
            except Exception as e:
                logging.error(f"Error adding user: {e}")

    async def full_userbase(self) -> List[int]:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT user_id FROM users')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def del_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            await db.commit()

    # ADMIN DATA
    async def admin_exist(self, admin_id: int) -> bool:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT 1 FROM admins WHERE admin_id = ?', 
                (admin_id,)
            )
            result = await cursor.fetchone()
            return result is not None

    async def add_admin(self, admin_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    'INSERT OR IGNORE INTO admins (admin_id) VALUES (?)', 
                    (admin_id,)
                )
                await db.commit()
            except Exception as e:
                logging.error(f"Error adding admin: {e}")

    async def del_admin(self, admin_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM admins WHERE admin_id = ?', (admin_id,))
            await db.commit()

    async def get_all_admins(self) -> List[int]:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT admin_id FROM admins')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    # BAN USER DATA
    async def ban_user_exist(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT 1 FROM banned_users WHERE user_id = ?', 
                (user_id,)
            )
            result = await cursor.fetchone()
            return result is not None

    async def add_ban_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    'INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)', 
                    (user_id,)
                )
                await db.commit()
            except Exception as e:
                logging.error(f"Error adding banned user: {e}")

    async def del_ban_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM banned_users WHERE user_id = ?', (user_id,))
            await db.commit()

    async def get_ban_users(self) -> List[int]:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT user_id FROM banned_users')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    # AUTO DELETE TIMER SETTINGS
    async def set_del_timer(self, value: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                'UPDATE del_timer SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', 
                (value,)
            )
            await db.commit()

    async def get_del_timer(self) -> int:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT value FROM del_timer WHERE id = 1')
            result = await cursor.fetchone()
            return result[0] if result else 600

    # CHANNEL MANAGEMENT
    async def channel_exist(self, channel_id: int) -> bool:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT 1 FROM channels WHERE channel_id = ?', 
                (channel_id,)
            )
            result = await cursor.fetchone()
            return result is not None

    async def add_channel(self, channel_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    'INSERT OR IGNORE INTO channels (channel_id) VALUES (?)', 
                    (channel_id,)
                )
                await db.commit()
            except Exception as e:
                logging.error(f"Error adding channel: {e}")

    async def rem_channel(self, channel_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            # First delete related request_forcesub_users
            await db.execute(
                'DELETE FROM request_forcesub_users WHERE channel_id = ?', 
                (channel_id,)
            )
            # Then delete the channel
            await db.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))
            await db.commit()

    async def show_channels(self) -> List[int]:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT channel_id FROM channels')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    # Get current mode of a channel
    async def get_channel_mode(self, channel_id: int) -> str:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT mode FROM channels WHERE channel_id = ?', 
                (channel_id,)
            )
            result = await cursor.fetchone()
            return result[0] if result else "off"

    # Set mode of a channel
    async def set_channel_mode(self, channel_id: int, mode: str):
        async with aiosqlite.connect(self.db_name) as db:
            # Update if exists, insert if not
            await db.execute(
                '''INSERT OR REPLACE INTO channels (channel_id, mode) 
                   VALUES (?, ?)''', 
                (channel_id, mode)
            )
            await db.commit()

    # REQUEST FORCE-SUB MANAGEMENT
    async def req_user(self, channel_id: int, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    '''INSERT OR IGNORE INTO request_forcesub_users 
                       (channel_id, user_id) VALUES (?, ?)''', 
                    (channel_id, user_id)
                )
                await db.commit()
            except Exception as e:
                logging.error(f"Error adding user to request list: {e}")

    # Remove a user from the channel set
    async def del_req_user(self, channel_id: int, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                '''DELETE FROM request_forcesub_users 
                   WHERE channel_id = ? AND user_id = ?''', 
                (channel_id, user_id)
            )
            await db.commit()

    # Check if the user exists in the set of the channel's users
    async def req_user_exist(self, channel_id: int, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                '''SELECT 1 FROM request_forcesub_users 
                   WHERE channel_id = ? AND user_id = ?''', 
                (channel_id, user_id)
            )
            result = await cursor.fetchone()
            return result is not None

    # Method to check if a channel exists
    async def reqChannel_exist(self, channel_id: int) -> bool:
        return await self.channel_exist(channel_id)

# Initialize database
db = Rohit(DB_NAME)
