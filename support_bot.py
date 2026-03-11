from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from config import SUPPORT_BOT_TOKEN, SUPPORT_GROUP_ID
from ticket_manager import generate_ticket, get_user, resolve_ticket
from utils import detect_category, detect_user_type

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    ticket = generate_ticket(user.id)

    category = detect_category(text)
    user_type = detect_user_type(text)

    msg = f"""
🎫 Ticket #{ticket}

User: {user.first_name}
UserID: {user.id}

User Type: {user_type}
Category: {category}

Message:
{text}
"""

    await context.bot.send_message(SUPPORT_GROUP_ID, msg)

    await update.message.reply_text(
        f"OK {user.first_name}, message received.\nTicket: {ticket}\nPlease wait for reply.\n\n— Team Goldberg"
    )

async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticket = context.args[0]
    reply_text = " ".join(context.args[1:])
    user_id = get_user(ticket)

    if not user_id:
        await update.message.reply_text("Ticket not found.")
        return

    await context.bot.send_message(user_id, reply_text)
    await update.message.reply_text(f"Reply sent to ticket {ticket}")

async def resolved_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticket = context.args[0]
    resolve_ticket(ticket)
    await update.message.reply_text(f"✅ Ticket {ticket} resolved")

app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.add_handler(CommandHandler("reply", reply_cmd))
app.add_handler(CommandHandler("resolved", resolved_cmd))

print("Support Bot Running...")
app.run_polling()