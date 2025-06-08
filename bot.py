import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

@dp.message_handler()
async def check_fake_news(message: types.Message):
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
        await message.reply(f"🤖 Fact Check Result:\n\n{result}")

    except Exception as e:
        await message.reply("❌ Error while checking the message. Please try again later.")
        print(f"Error: {e}")

if __name__ == '__main__':
    print("🤖 Bot is running...")
    executor.start_polling(dp, skip_updates=True)
