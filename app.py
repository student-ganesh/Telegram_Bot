import os
import re
from dotenv import load_dotenv
from telegram import Update 
from telegram.ext import Application, CommandHandler , MessageHandler,ContextTypes 
from telegram.ext import filters
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

groq_api_key =os.getenv("GROQ_API_KEY")

def setup_llm_chain(topic = "Technology"):
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're a stand-up comedian. Generate a joke based on the user's topic."),
        ("user", "generate a joke on topic: {topic}")
    ]
)
    
    llm = ChatGroq(
    model = "llama3-8b-8192",
    groq_api_key = groq_api_key 
)
    chain =  prompt|llm|StrOutputParser()
    return chain

async def start(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mention me with topic like '@ChalaHasu_bot python' to get a joke")

async def help_command(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mention me with topic like '@ChalaHasu_bot python' to get funny a joke")

async def generate_joke(update: Update , context: ContextTypes.DEFAULT_TYPE, topic = str):
    await update.message.reply_text(f"Generating joke on: {topic}")
    
    chain = setup_llm_chain()
    joke = chain.invoke({"topic": topic}).strip()
    await update.message.reply_text(joke)

async def handle_message(update: Update , context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    bot_username = context.bot.username

    pattern = rf"@{re.escape(bot_username)}\s+(.+)"
    match = re.search(pattern, msg)

    if match:
        topic = match.group(1).strip()
        if topic:
            await generate_joke(update, context, topic)
        else:
            await update.message.reply_text("You mentioned me, but didn't include a topic. Try: '@ChalaHasuya_bot Python'")
    else:
        await update.message.reply_text("Please mention me with a topic like '@ChalaHasuya_bot Python'.")


def main():
    token = os.getenv("TELEGRAM_API_KEY")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , handle_message))
    app.run_polling(allowed_updates = Update.ALL_TYPES)

if __name__ == "__main__":
    main()


