from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

# === CONFIGURED FOR YOU ===
BOT_TOKEN = "8004375197:AAFokCjclXL5uW9R7_vCGQk8gws5LzO8Qbg"
YOUR_TELEGRAM_ID = 5575120398

# Store last user who messaged the bot
last_sender = None

# === /start command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a message and I’ll forward it to my owner.")

# === Main message relay handler ===
async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_sender
    user_id = update.effective_chat.id
    message = update.message.text
    username = update.effective_user.username or "No username"
    full_name = update.effective_user.full_name or "No name"

    print(f"📩 Message received from {user_id} (@{username}): {message}")

    if user_id == YOUR_TELEGRAM_ID:
        if last_sender:
            print(f"🔁 Forwarding your reply to {last_sender}: {message}")
            await context.bot.send_message(chat_id=last_sender, text=message)
    else:
        last_sender = user_id
        print(f"📨 Forwarding message to owner: {YOUR_TELEGRAM_ID}")
        await context.bot.send_message(
            chat_id=YOUR_TELEGRAM_ID,
            text=(
                f"📬 New message from:\n"
                f"👤 Name: {full_name}\n"
                f"🔗 Username: @{username}\n"
                f"🆔 User ID: {user_id}\n"
                f"\n💬 Message:\n{message}"
            )
        )

# === Bot launcher ===
def main():
    print("✅ Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), relay_message))

    app.run_polling()

# === Entry point ===
if __name__ == "__main__":
    main()

