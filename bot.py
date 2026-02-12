import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("8527242790:AAEjwurN9fG3nGK9IfTtgwFd7AKHNyAyGjY")
SUPPORT_GROUP_ID = -1003809204938  # Your support group ID
# ============================================

logging.basicConfig(level=logging.INFO)

# ================== TEXT DATA ==================

LANG_TEXT = {
    "en": {
        "welcome": "👋 Welcome to Support\n\nPlease select your language:",
        "issues": "Please select your issue:",
        "deposit": [
            "💰 Deposit Issue",
            "🆔 Please send your UID",
            "📸 Send payment & in-game screenshots",
            "📨 Send **all details in ONE message only**",
            "Our support team will resolve your issue as soon as possible. Please be patient, your patience is appreciated. 😊",
        ],
        "withdraw": [
            "🏦 Withdrawal Issue",
            "🆔 Please send your UID",
            "📸 Send withdrawal & in-game screenshots",
            "📨 Send **all details in ONE message only**",
            "Our support team will resolve your issue as soon as possible. Please be patient, your patience is appreciated. 😊",
        ],
        "other": [
            "❓ Other Issue",
            "🆔 Please send your UID",
            "📝 Explain your issue clearly",
            "📸 Send related screenshots if any",
            "📨 Send **all details in ONE message only**",
            "Our support team will resolve your issue as soon as possible. Please be patient, your patience is appreciated. 😊",
        ],
        "resolved": "✅ Your issue has been resolved. Thank you for your patience! 😊",
    },
    "hi": {
        "welcome": "👋 सपोर्ट में आपका स्वागत है\n\nकृपया अपनी भाषा चुनें:",
        "issues": "कृपया अपनी समस्या चुनें:",
        "deposit": [
            "💰 डिपॉजिट समस्या",
            "🆔 कृपया अपना UID भेजें",
            "📸 भुगतान और गेम के स्क्रीनशॉट भेजें",
            "📨 **सारी जानकारी एक ही मैसेज में भेजें**",
            "हमारी सपोर्ट टीम जल्द ही आपकी समस्या हल करेगी। कृपया धैर्य रखें, आपके धैर्य की सराहना की जाती है। 😊",
        ],
        "withdraw": [
            "🏦 विथड्रॉ समस्या",
            "🆔 कृपया अपना UID भेजें",
            "📸 विथड्रॉ और गेम के स्क्रीनशॉट भेजें",
            "📨 **सारी जानकारी एक ही मैसेज में भेजें**",
            "हमारी सपोर्ट टीम जल्द ही आपकी समस्या हल करेगी। कृपया धैर्य रखें, आपके धैर्य की सराहना की जाती है। 😊",
        ],
        "other": [
            "❓ अन्य समस्या",
            "🆔 कृपया अपना UID भेजें",
            "📝 अपनी समस्या स्पष्ट रूप से लिखें",
            "📸 संबंधित स्क्रीनशॉट भेजें",
            "📨 **सारी जानकारी एक ही मैसेज में भेजें**",
            "हमारी सपोर्ट टीम जल्द ही आपकी समस्या हल करेगी। कृपया धैर्य रखें, आपके धैर्य की सराहना की जाती है। 😊",
        ],
        "resolved": "✅ आपकी समस्या हल हो गई है। आपके धैर्य के लिए धन्यवाद! 😊",
    },
    "hinglish": {
        "welcome": "👋 Support mein aapka swagat hai\n\nPlease apni language select karein:",
        "issues": "Please apni issue select karein:",
        "deposit": [
            "💰 Deposit Issue",
            "🆔 Apna UID bhejein",
            "📸 Payment aur game screenshots bhejein",
            "📨 **Saari details ek hi message mein bhejein**",
            "Hamari support team jaldi hi aapki problem solve karegi. Kripya patience rakhein, aapke patience ki value ki jaati hai. 😊",
        ],
        "withdraw": [
            "🏦 Withdrawal Issue",
            "🆔 Apna UID bhejein",
            "📸 Withdrawal aur game screenshots bhejein",
            "📨 **Saari details ek hi message mein bhejein**",
            "Hamari support team jaldi hi aapki problem solve karegi. Kripya patience rakhein, aapke patience ki value ki jaati hai. 😊",
        ],
        "other": [
            "❓ Other Issue",
            "🆔 Apna UID bhejein",
            "📝 Apni problem clearly explain karein",
            "📸 Related screenshots bhejein",
            "📨 **Saari details ek hi message mein bhejein**",
            "Hamari support team jaldi hi aapki problem solve karegi. Kripya patience rakhein, aapke patience ki value ki jaati hai. 😊",
        ],
        "resolved": "✅ Aapki problem resolve ho chuki hai. Patience rakhne ke liye dhanyavaad! 😊",
    },
}

# ================== START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("हिंदी", callback_data="lang_hi")],
        [InlineKeyboardButton("Hinglish", callback_data="lang_hinglish")],
    ]
    await update.message.reply_text(
        LANG_TEXT["en"]["welcome"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================== CALLBACK HANDLER ==================

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang

        keyboard = [
            [InlineKeyboardButton("💰 Deposit Issue", callback_data="issue_deposit")],
            [InlineKeyboardButton("🏦 Withdrawal Issue", callback_data="issue_withdraw")],
            [InlineKeyboardButton("❓ Other Issue", callback_data="issue_other")],
        ]
        await query.edit_message_text(
            LANG_TEXT[lang]["issues"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data.startswith("issue_"):
        issue = data.split("_")[1]
        context.user_data["issue"] = issue
        lang = context.user_data.get("lang", "en")

        text = "\n".join(LANG_TEXT[lang][issue])
        await query.edit_message_text(text)

    elif data.startswith("reply_"):
        user_id = int(data.split("_")[1])
        context.chat_data["reply_to"] = user_id

    elif data.startswith("resolve_"):
        user_id = int(data.split("_")[1])
        lang = context.application.user_data.get(user_id, {}).get("lang", "en")

        await context.bot.send_message(
            chat_id=user_id,
            text=LANG_TEXT[lang]["resolved"],
        )
        await query.edit_message_reply_markup(None)

# ================== USER MESSAGE ==================

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    issue = context.user_data.get("issue", "Unknown")

    header = (
        f"👤 Name: {user.full_name}\n"
        f"🔗 Username: @{user.username}\n"
        f"🆔 User ID: {user.id}\n"
        f"📂 Issue: {issue.upper()}\n\n"
        f"💬 Message:\n{update.message.text}"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Reply to User", callback_data=f"reply_{user.id}"),
            InlineKeyboardButton("✅ Resolve", callback_data=f"resolve_{user.id}"),
        ]
    ])

    await context.bot.send_message(
        chat_id=SUPPORT_GROUP_ID,
        text=header,
        reply_markup=buttons,
    )

# ================== AGENT REPLY ==================

async def agent_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_to = context.chat_data.get("reply_to")
    if not reply_to:
        return

    await context.bot.send_message(
        chat_id=reply_to,
        text=update.message.text,
    )
    context.chat_data.pop("reply_to", None)

# ================== MAIN ==================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, user_message))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, agent_reply))

    app.run_polling()

if __name__ == "__main__":
    main()