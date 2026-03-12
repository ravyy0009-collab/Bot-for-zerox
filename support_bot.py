import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config import SUPPORT_BOT_TOKEN, SUPPORT_GROUP_ID
from ticket_manager import generate_ticket

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

    # forward text
    if text:
        await context.bot.send_message(SUPPORT_GROUP_ID, msg)

    # forward photo
    if update.message.photo:
        await context.bot.send_photo(
            SUPPORT_GROUP_ID,
            update.message.photo[-1].file_id,
            caption=msg
        )

    # confirmation message
    sent = await update.message.reply_text("Message Sent ✓")

    await asyncio.sleep(3)

    try:
        await sent.delete()
    except:
        pass


app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, handle_message))

print("Support Bot Running...")
app.run_polling()