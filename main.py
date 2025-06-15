import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from rembg import remove
from PIL import Image
from io import BytesIO

BACKGROUND_PATH = "background.png"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте мне фото, и я удалю фон.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_data = await file.download_as_bytearray()

    input_image = Image.open(BytesIO(image_data)).convert("RGBA")
    no_bg = remove(input_image)

    background = Image.open(BACKGROUND_PATH).convert("RGBA").resize(no_bg.size)
    result = Image.alpha_composite(background, no_bg)

    output = BytesIO()
    result.save(output, format='PNG')
    output.seek(0)

    await update.message.reply_photo(InputFile(output, filename="result.png"))

def main():
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()