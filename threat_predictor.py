import joblib
import os

# 📁 Safe path handling
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "..", "email_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "..", "vectorizer.pkl")

# 🔄 Load model
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


# 🛡️ Legit detection
def is_trusted_email(text):
    trusted_keywords = [
        "amazon.in", "hdfc bank", "infosys",
        "thank you for", "order has been",
        "transaction alert", "account has been debited",
        "onboarding", "internship",
        "order confirmed", "meeting", "newsletter"
    ]
    return any(word in text.lower() for word in trusted_keywords)


def is_strong_legit(text):
    strong_legit_patterns = [
        "thank you for shopping",
        "order has been successfully placed",
        "transaction alert",
        "account has been debited",
        "internship",
        "onboarding",
        "meeting invitation"
    ]
    return any(p in text.lower() for p in strong_legit_patterns)


# 🚨 Phishing detection
def is_strong_phishing(text):
    phishing_keywords = [
        "verify your account",
        "click here",
        "urgent action required",
        "login immediately",
        "account suspended",
        "confirm your password",
        "update your details",
        "security alert",
        "limited time",
        "act now",
        "bank details",
        "id proof",
        "no interview required",
        "winner",
        "lottery"
    ]
    return any(word in text.lower() for word in phishing_keywords)


def is_neutral_legit(text):
    patterns = [
        "students", "course", "project", "submission",
        "progress", "learning", "team", "stage", "sprint", "skills"
    ]
    return any(p in text.lower() for p in patterns)


# 🔍 MAIN FUNCTION
def predict_email(text):

    print("🔥 predictor running...")

    text_lower = text.lower()

    # =========================
    # 1. ML BASE (MOST IMPORTANT)
    # =========================
    text_vector = vectorizer.transform([text])
    probability = model.predict_proba(text_vector)[0][1]

    score = round(probability * 100, 2)

    # =========================
    # 2. LIGHT ADJUSTMENTS ONLY
    # =========================

    # 🛡️ Legit (soft reduction)
    if is_trusted_email(text):
        score -= 5

    if is_strong_legit(text):
        score -= 10

    elif is_neutral_legit(text):
        score -= 5

    # 🚨 Phishing (stronger but not forced)
    if is_strong_phishing(text):
        score += 15

    # 🔗 URL presence (light signal)
    if "http://" in text_lower or "https://" in text_lower:
        score += 10

    # =========================
    # 3. NORMALIZE
    # =========================
    score = max(0, min(score, 100))

    # =========================
    # 4. CLEAN THRESHOLDS (ML-based)
    # =========================
    if score < 40:
        severity = "Low Risk"
    elif score < 65:
        severity = "Moderate Risk"
    elif score < 85:
        severity = "High Risk"
    else:
        severity = "Critical Threat"

    print(f"Score: {score} | Severity: {severity}")

    return score, severity