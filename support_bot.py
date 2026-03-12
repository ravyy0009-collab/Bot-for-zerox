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


tickets = {}                 # ticket_id -> user_id
user_active_ticket = {}      # user_id -> ticket_id
daily_counter = {}           # daily ticket counter


# Generate ticket
def generate_ticket(user_id):

    if user_id in user_active_ticket:
        return user_active_ticket[user_id]

    now = datetime.now()
    key = now.strftime("%y%d%m")

    if key not in daily_counter:
        daily_counter[key] = 1
    else:
        daily_counter[key] += 1

    number = str(daily_counter[key]).zfill(2)

    ticket = f"{key}{number}"

    tickets[ticket] = user_id
    user_active_ticket[user_id] = ticket

    return ticket


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
Welcome 👋

Send your question or query.
JOE will reply soon.
"""

    await update.message.reply_text(msg)


# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type != "private":
        return

    user = update.message.from_user
    text = update.message.text or ""

    ticket = generate_ticket(user.id)

    msg = f"""
🎫 Ticket: {ticket}

User: {user.first_name}
UserID: {user.id}

Message:
{text}
"""

    # send text
    if text:
        await context.bot.send_message(SUPPORT_GROUP_ID, msg)

    # send photo
    if update.message.photo:
        await context.bot.send_photo(
            SUPPORT_GROUP_ID,
            photo=update.message.photo[-1].file_id,
            caption=msg
        )

    # send document
    if update.message.document:
        await context.bot.send_document(
            SUPPORT_GROUP_ID,
            document=update.message.document.file_id,
            caption=msg
        )

    sent = await update.message.reply_text("Message Sent ✓")

    await asyncio.sleep(3)

    try:
        await sent.delete()
    except:
        pass


# Reply command
async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <ticket> <message>")
        return

    ticket = context.args[0]
    message = " ".join(context.args[1:])

    user_id = tickets.get(ticket)

    if not user_id:
        await update.message.reply_text("Ticket not found")
        return

    await context.bot.send_message(user_id, message)

    await update.message.reply_text(f"Reply sent to ticket {ticket}")


# Close ticket
async def close_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /close <ticket>")
        return

    ticket = context.args[0]

    user_id = tickets.get(ticket)

    if not user_id:
        await update.message.reply_text("Ticket not found")
        return

    user_active_ticket.pop(user_id, None)

    await context.bot.send_message(
        user_id,
        f"Your ticket {ticket} has been closed.\nIf you need further help, please send a new message."
    )

    await update.message.reply_text(f"Ticket {ticket} closed")


# Resolve ticket
async def resolved_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /resolved <ticket>")
        return

    ticket = context.args[0]

    user_id = tickets.get(ticket)

    if not user_id:
        await update.message.reply_text("Ticket not found")
        return

    user_active_ticket.pop(user_id, None)

    await context.bot.send_message(
        user_id,
        f"Your issue for ticket {ticket} has been resolved.\nThank you for contacting us."
    )

    await update.message.reply_text(f"Ticket {ticket} resolved")


# Start bot
app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, handle_message))

app.add_handler(CommandHandler("reply", reply_cmd))
app.add_handler(CommandHandler("close", close_cmd))
app.add_handler(CommandHandler("resolved", resolved_cmd))

print("Support Bot Running...")

app.run_polling()