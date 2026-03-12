import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import SUPPORT_BOT_TOKEN, SUPPORT_GROUP_ID


tickets = {}
daily_counter = {}


# Ticket generator
def generate_ticket(user_id):
    now = datetime.now()
    key = now.strftime("%y%d%m")

    if key not in daily_counter:
        daily_counter[key] = 1
    else:
        daily_counter[key] += 1

    number = str(daily_counter[key]).zfill(2)
    ticket = f"{key}{number}"

    tickets[ticket] = user_id

    return ticket


def get_user(ticket):
    return tickets.get(ticket)


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
Welcome 👋

Send your question or query.
Joe will reply soon.❤️
"""

    await update.message.reply_text(msg)


# User message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type != "private":
        return

    user = update.message.from_user
    text = update.message.text or ""

    ticket = generate_ticket(user.id)

    msg = f"""
🎫 Ticket: {ticket}

👤 User: {user.first_name}
🆔 UserID: {user.id}

💬 Message:
{text}
"""

    # text message
    if text:
        await context.bot.send_message(SUPPORT_GROUP_ID, msg)

    # photo
    if update.message.photo:
        await context.bot.send_photo(
            SUPPORT_GROUP_ID,
            photo=update.message.photo[-1].file_id,
            caption=msg,
        )

    # document
    if update.message.document:
        await context.bot.send_document(
            SUPPORT_GROUP_ID,
            document=update.message.document.file_id,
            caption=msg,
        )

    # confirmation message
    sent = await update.message.reply_text("Message Sent ✓")

    await asyncio.sleep(3)

    try:
        await sent.delete()
    except:
        pass


# Reply command
async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <ticket> <message>")
        return

    ticket = context.args[0]
    reply_text = " ".join(context.args[1:])

    user_id = get_user(ticket)

    if not user_id:
        await update.message.reply_text("Ticket not found")
        return

    await context.bot.send_message(user_id, reply_text)

    await update.message.reply_text(f"Reply sent to ticket {ticket}")


# Bot start
app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, handle_message))
app.add_handler(CommandHandler("reply", reply_cmd))

print("Support Bot Running...")

app.run_polling()