print("Training started...")

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ---------------- LOAD FINAL DATASET ----------------

data = pd.read_csv("dataset/final_dataset.csv")

print("Columns:", data.columns)
print("Class distribution:\n", data["label"].value_counts())

# ---------------- PREPARE DATA ----------------

X = data["email_text"].astype(str)
y = data["label"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=7000,
    ngram_range=(1,2)
)

X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------- TRAIN MODEL ----------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

print("Training completed")

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:\n")
print(classification_report(y_test, pred))

# ---------------- SAVE ----------------

joblib.dump(model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully!")