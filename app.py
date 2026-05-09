from flask import Flask, render_template, request, redirect, session
import sqlite3

# 🔮 Modules
from modules.threat_predictor import predict_email
from modules.url_analyzer import analyze_url
from modules.context_engine import analyze_context

app = Flask(__name__)
app.secret_key = "secret123"


# =========================
# 🗄️ DATABASE INIT
# =========================
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# 🏠 ROUTES
# =========================

# HOME
@app.route("/")
def home():
    return render_template("index.html")


# FEATURES
@app.route("/features")
def features():
    return render_template("features.html")


# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# 📧 EMAIL ANALYSIS
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():
    email_text = request.form.get("email", "").strip()

    if not email_text:
        return render_template("result.html", score=0, severity="LOW")

    score, severity = predict_email(email_text)


    print("📩 Email analyzed")
    print(f"Score: {score}, Severity: {severity}")

    return render_template("result.html", score=score, severity=severity)


# =========================
# 🔗 URL CHECK PAGE
# =========================
@app.route("/url")
def url_page():
    return render_template("url_check.html")



@app.route("/context")
def context_page():
    return render_template("context.html")

@app.route('/project-insights')
def project_insights():
    if 'user' not in session:
        return redirect('/signin')  # 🔐 block access

    return render_template('project_insights.html')


@app.route("/analyze_context", methods=["POST"])
def analyze_context_route():
    text = request.form["email"]

    result = analyze_context(text)

    return render_template("context_result.html", result=result)


# =========================
# 🔗 URL ANALYSIS
# =========================
@app.route("/check_url", methods=["POST"])
def check_url():
    url = request.form.get("url", "").strip()

    if not url:
        return redirect("/url")

    score, severity, reasons = analyze_url(url)

    return render_template(
        "url_result.html",
        score=score,
        severity=severity,
        reasons=reasons
    )


# =========================
# 👤 AUTH SYSTEM
# =========================

# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/signin")

    return render_template("signup.html")


# SIGNIN
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("signin.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# CONTACT
@app.route('/contact')
def contact():
    return render_template('contact.html')


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    print("🚀 Flask app running...")
    app.run(debug=True)