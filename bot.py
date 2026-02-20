# import os
# import django
# import requests
# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, ConversationHandler, CommandHandler

# # تنظیمات جنگو
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darick_backend.settings')
# django.setup()
# from products.models import Product

# # وضعیت‌های گفتگو
# NAME, PRICE, PHOTO = range(3)

# IMGBB_API_KEY = "b346cf64a02bfd784da057ec690e88a2"

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("سلام رئیس! اسم محصول جدید چیه؟")
#     return NAME

# async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data['name'] = update.message.text
#     await update.message.reply_text(f"خب، قیمت '{update.message.text}' چنده؟")
#     return PRICE

# async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data['price'] = update.message.text
#     await update.message.reply_text("حالا عکس محصول رو بفرست (بصورت Image)...")
#     return PHOTO

# async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # ۱. دریافت عکس از تلگرام
#     photo_file = await update.message.photo[-1].get_file()
#     image_url_telegram = photo_file.file_path
    
#     # ۲. آپلود در ImgBB برای گرفتن لینک دائمی
#     response = requests.post(
#         "https://api.imgbb.com/1/upload",
#         params={"key": IMGBB_API_KEY, "image": image_url_telegram}
#     )
    
#     if response.status_code == 200:
#         final_link = response.json()['data']['url']
        
#         # ۳. ذخیره در دیتابیس جنگو
#         Product.objects.create(
#             name=context.user_data['name'],
#             price=context.user_data['price'],
#             image_url=final_link
#         )
#         await update.message.reply_text("✅ ایول! عکس آپلود شد و محصول با موفقیت ثبت شد.")
#     else:
#         await update.message.reply_text("❌ خطا در آپلود عکس. دوباره تلاش کن.")
    
#     return ConversationHandler.END

# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("عملیات لغو شد.")
#     return ConversationHandler.END

# if __name__ == '__main__':
#     app = ApplicationBuilder().token("8322158442:AAGny0pWWUVOH1RzyDTa4lzDUngrHZm5phE").build()
    
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
#             PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
#             PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
#         },
#         fallbacks=[CommandHandler('cancel', cancel)],
#     )
    
#     app.add_handler(conv_handler)
#     print("ربات هوشمند داریک فعال شد... 🚀")
#     app.run_polling()
    
import os
import django
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, ConversationHandler, CommandHandler

# ۱. فعال‌سازی گزارش خطا (Logging) - این خیلی مهم است!
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ۲. تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darick_backend.settings')
django.setup()
from products.models import Product

# وضعیت‌های گفتگو
NAME, PRICE, PHOTO = range(3)

# مقادیر کلیدی
BOT_TOKEN = "8322158442:AAHQkw9nwYjWW6cAYgSTZlO44_h7R-OVr04"
IMGBB_KEY = "b346cf64a02bfd784da057ec690e88a2"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("User started the bot") # چاپ در ترمینال برای تست
    await update.message.reply_text("سلام! اسم محصول جدید چیست؟ (برای لغو /cancel بزنید)")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"قیمت '{update.message.text}' را وارد کنید:")
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text("حالا عکس محصول را بفرستید:")
    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال پردازش و آپلود عکس... لطفا منتظر بمانید.")
    
    try:
        # دریافت فایل از تلگرام
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        file_url = file.file_path
        
        # آپلود در ImgBB
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_KEY, "image": file_url}
        )
        
        if response.status_code == 200:
            final_url = response.json()['data']['url']
            
            # ذخیره در دیتابیس جنگو
            Product.objects.create(
                name=context.user_data['name'],
                price=context.user_data['price'],
                image_url=final_url
            )
            await update.message.reply_text(f"✅ محصول با موفقیت ثبت شد!\nلینک عکس: {final_url}")
        else:
            await update.message.reply_text("❌ خطا در آپلود عکس به ImgBB.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ خطای غیرمنتظره: {e}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد. برای شروع مجدد /start بزنید.")
    return ConversationHandler.END

if __name__ == '__main__':

    proxy_url = "http://127.0.0.1:10809" 
    
    app = ApplicationBuilder().token(BOT_TOKEN).proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    app.add_handler(conv_handler)
    print("ربات با سیستم لاگینگ فعال شد... 🚀")
    app.run_polling()