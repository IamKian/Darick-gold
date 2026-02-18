import os
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات برای اتصال به مدل‌های جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darick_backend.settings')
django.setup()
from products.models import Product

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام رئیس! اطلاعات طلا را بفرست:\nنام | قیمت | لینک عکس")

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # دریافت متن و جدا کردن با کاراکتر |
        data = update.message.text.split('|')
        if len(data) == 3:
            name, price, img = data[0].strip(), data[1].strip(), data[2].strip()
            
            # ذخیره مستقیم در دیتابیس جنگو
            Product.objects.create(name=name, price=price, image_url=img)
            
            await update.message.reply_text(f"✅ محصول '{name}' با موفقیت در سایت ثبت شد!")
        else:
            await update.message.reply_text("❌ اشتباه فرستادی! فرمت: نام | قیمت | لینک عکس")
    except Exception as e:
        await update.message.reply_text(f"خطایی رخ داد: {e}")

if __name__ == '__main__':
    # توکن ربات را اینجا بگذار
    app = ApplicationBuilder().token("8322158442:AAGny0pWWUVOH1RzyDTa4lzDUngrHZm5phE").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), add_product))
    
    print("ربات داریک فعال شد... 🚀")
    app.run_polling()