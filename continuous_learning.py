import sqlite3
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def retrain_model():

    conn = sqlite3.connect("database.db")
    data = pd.read_sql_query("SELECT * FROM scans", conn)
    conn.close()

    if len(data) < 10:
        return  # Not enough data yet

    # Simulated labeling (for academic demo)
    data["label"] = data["severity"].apply(
        lambda x: 1 if x in ["HIGH", "CRITICAL"] else 0
    )

    # For demo purposes using score only
    X = data[["score"]]
    y = data["label"]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, "model.pkl")