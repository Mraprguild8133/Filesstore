#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileStore Bot - Main Entry Point
Created by: Codeflix Bots
A comprehensive Telegram bot for file storage and sharing
"""

import asyncio
import logging
import sys
import pyrogram.utils
from bot import bot
from config import Config


pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        logger.info("Starting FileStore Bot...")
        logger.info(f"Bot Token: {Config.TG_BOT_TOKEN[:10]}...")
        logger.info(f"Owner ID: {Config.OWNER_ID}")
        logger.info(f"Channel ID: {Config.CHANNEL_ID}")
        
        # Start the bot
        await bot.start()
        logger.info("Bot started successfully!")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
