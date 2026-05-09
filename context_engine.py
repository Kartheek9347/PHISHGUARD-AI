import re

def analyze_context(text):

    text_lower = text.lower()

    context_flags = []
    score = 0

    # 🔥 Intent categories
    intent = "Neutral"

    # 1. URGENCY
    urgency_words = ["urgent", "immediately", "now", "asap", "within 24 hours"]
    if any(word in text_lower for word in urgency_words):
        context_flags.append("Urgency detected")
        score += 20
        intent = "Urgent Action Request"

    # 2. ACCOUNT THREAT
    threat_words = ["suspended", "blocked", "terminated", "deactivated"]
    if any(word in text_lower for word in threat_words):
        context_flags.append("Account threat mentioned")
        score += 25
        intent = "Threat / Fear Manipulation"

    # 3. ACTION REQUEST
    action_words = ["click", "verify", "login", "update", "confirm"]
    if any(word in text_lower for word in action_words):
        context_flags.append("Action request present")
        score += 20

    # 4. FINANCIAL BAIT
    money_words = ["win", "prize", "reward", "lottery", "cash"]
    if any(word in text_lower for word in money_words):
        context_flags.append("Financial bait detected")
        score += 15
        intent = "Incentive Scam"

    # 5. SUSPICIOUS SENDER LANGUAGE
    if "dear user" in text_lower or "dear customer" in text_lower:
        context_flags.append("Generic greeting used")
        score += 10

    # FINAL RISK
    if score < 30:
        risk = "Low"
    elif score < 60:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "intent": intent,
        "risk": risk,
        "context": context_flags,
        "score": score
    }