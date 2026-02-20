import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! اگر این پیام را می‌بینی یعنی اتصال برقرار است.")

if __name__ == '__main__':
    # توکن را اینجا بگذار
    app = ApplicationBuilder().token("8322158442:AAHQkw9nwYjWW6cAYgSTZlO44h7R-OVr04").build()
    app.add_handler(CommandHandler("hello", hello))
    print("در حال تست اتصال... در تلگرام دستور /hello را بزنید")
    app.run_polling()