import asyncio
from twitchio.ext import commands
from collections import deque
import time

# Füge deinen Token und Kanalnamen ein
TOKEN = "6bn6iyrw13rrzwrx8pyhg4nip3jd6z"
CHANNEL = "raphael065"

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, prefix="!", initial_channels=[CHANNEL])
        self.omegalul_queue = deque(maxlen=2)  # speichert die letzten 2 OMEGALUL-Timestamps

    async def event_ready(self):
        print(f"Bot ist bereit und eingeloggt als | {self.nick}")

    async def event_message(self, message):
        print(f"Nachricht erhalten: {message.content} von {message.author.name}")

        # Ignoriere Nachrichten vom Bot selbst
        if message.author.name.lower() == self.nick.lower():
            return

        # Überprüfe, ob die Nachricht "OMEGALUL" ist
        if message.content == "OMEGALUL":
            print("OMEGALUL erkannt")
            self.omegalul_queue.append(time.time())  # füge aktuellen Timestamp hinzu

            # Überprüfe, ob in den letzten 10 Sekunden 2 OMEGALUL-Messages vorhanden sind
            if len(self.omegalul_queue) == 2:
                if self.omegalul_queue[-1] - self.omegalul_queue[0] <= 10:
                    print("Sende OMEGALUL in den Chat")
                    await message.channel.send("OMEGALUL")

        await self.handle_commands(message)

# Starte den Bot
bot = MyBot()
bot.run()
