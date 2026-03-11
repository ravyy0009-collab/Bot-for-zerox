def detect_category(text):
    text = text.lower()
    if any(x in text for x in ["deposit", "recharge", "payment"]):
        return "Deposit Issue"
    if any(x in text for x in ["withdraw", "withdrawal", "payout"]):
        return "Withdrawal Issue"
    if any(x in text for x in ["wingo", "bet", "game"]):
        return "Game Issue"
    return "General Issue"

def detect_user_type(text):
    text = text.lower()
    if any(x in text for x in ["salary", "commission", "downline", "agent"]):
        return "Agent"
    return "Player"