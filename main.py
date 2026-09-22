import os
import difflib
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Store user texts temporarily (in-memory, resets on restart)
user_texts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me two paragraphs and I'll highlight the differences.\n\n"
        "Format:\n"
        "1. Send your FIRST paragraph.\n"
        "2. Send your SECOND paragraph.\n\n"
        "I'll compare them and show you what changed."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How to use:\n"
        "1. Send your first text.\n"
        "2. Send your second text.\n"
        "3. Get a diff with added/removed lines highlighted.\n\n"
        "Use /start to begin fresh."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_texts:
        user_texts[user_id] = {"first": text}
        await update.message.reply_text(
            "Got your first text. Now send the second one to compare."
        )
        return

    first_text = user_texts[user_id]["first"]
    second_text = text

    # Compute diff using difflib
    diff = difflib.ndiff(first_text.splitlines(), second_text.splitlines())
    result_lines = []
    for line in diff:
        if line.startswith('- '):
            result_lines.append(f"➖ {line[2:]}")  # Removed
        elif line.startswith('+ '):
            result_lines.append(f"➕ {line[2:]}")  # Added
        elif line.startswith('  '):
            result_lines.append(f"   {line[2:]}")  # Unchanged

    if len(result_lines) > 50:
        result_lines = result_lines[:50] + ["...", "(truncated)"]

    response = "Here are the differences:\n\n" + "\n".join(result_lines)
    if len(response) > 4000:
        response = response[:4000] + "\n...(truncated)"

    await update.message.reply_text(response)

    # Reset for next comparison
    del user_texts[user_id]

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_texts:
        del user_texts[user_id]
    await update.message.reply_text("Cleared. Send a new first text to start over.")

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot starting with long polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
