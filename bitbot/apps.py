from django.apps import AppConfig
import os, threading, asyncio
from . import bot


class BitbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bitbot"
    
    def ready(self):
        if bool(int(os.environ.get("DISCORD_BOT_STARTED", "0"))):
            print("[BitBot] Discord bot is already running")
        else:
            self.start_bot()
    
    def start_bot(self):
        print("[BitBot] Starting the Discord bot")
        
        threading.Thread(
            target=bot.main
        ).start()
        
        os.environ["DISCORD_BOT_STARTED"] = "1"
    
    def stop_bot(self, client):
        print("[BitBot] Stopping the Discord bot")
        
        loop = asyncio.get_event_loop()
        loop.create_task(client.close())
        
        os.environ["DISCORD_BOT_STARTED"] = "0"