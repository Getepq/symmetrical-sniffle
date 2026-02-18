import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003402516683
DATA_FILE = "data/users_database.json"


class UsersDB:
    def __init__(self, filename):
        self.filename = filename
        self.lock = asyncio.Lock()
        self.data = {}

        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                self.data = {}

    async def save(self):
        async with self.lock:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)

    async def update_user(self, user: types.User):
        user_id = str(user.id)
        async with self.lock:
            self.data[user_id] = {
                "username": user.username,
                "first_name": user.first_name or "Unknown",
                "last_seen": asyncio.get_event_loop().time()
            }
        await self.save()

    def get_all_mentions(self):
        mentions = []
        for user_id, info in self.data.items():
            if info.get("username"):
                mentions.append(f"@{info['username']}")
            else:
                name = info.get('first_name', 'Пользователь')
                mentions.append(f'<a href="tg://user?id={user_id}">{name}</a>')
        return mentions


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
db = UsersDB(DATA_FILE)


@dp.message(F.chat.id == CHAT_ID, Command('all'))
async def cmd_all(message: types.Message):
    mentions = db.get_all_mentions()

    if not mentions:
        await message.reply('<tg-emoji emoji-id="5318972874726339331">🪙</tg-emoji>пусто.')
        return

    text = '<b><tg-emoji emoji-id="5373136788900571050">🔔</tg-emoji>ОбЪявление:</b>\n\n' + " ".join(mentions)

    sent_msg = await message.answer(text)

    await asyncio.sleep(15)

    try:
        await sent_msg.delete()
        await message.delete()
    except Exception:
        pass


@dp.message(F.chat.id == CHAT_ID)
async def track_users(message: types.Message):
    if message.from_user and not message.from_user.is_bot:
        await db.update_user(message.from_user)


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:

        pass
