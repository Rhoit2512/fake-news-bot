import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize bot and dispatcher
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
openai.api_key = OPENAI_API_KEY

@dp.message()
async def check_fake_news(message: Message):
    user_input = message.text

    prompt = (
        f"You're an AI that checks for fake news. "
        f"Classify the following message as True, False, Misleading, or Unverifiable. "
        f"Also explain briefly why:\n\n\"{user_input}\""
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        result = response['choices'][0]['message']['content'].strip()
        await message.answer(f"🤖 Fact Check Result:\n\n{result}")

    except Exception as e:
        await message.answer("❌ Error while checking the message. Please try again later.")
        print(f"Error: {e}")

async def main():
    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
