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
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_GROUP_ID = int(os.getenv("-1003809204938"))
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
            "Hamari support team