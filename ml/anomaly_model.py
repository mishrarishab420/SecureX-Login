import sqlite3
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import os

DB_URL = os.environ.get("DATABASE_URL", "instance/securex.db")


def load_logs():

    if DB_URL.startswith("sqlite"):
        conn = sqlite3.connect("instance/securex.db")
    else:
        import psycopg2
        conn = psycopg2.connect(DB_URL)

    query = """
    SELECT user_id, ip_address, user_agent, login_time, status
    FROM login_log
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def preprocess(df):

    df["login_time"] = pd.to_datetime(df["login_time"])

    # Time feature
    df["hour"] = df["login_time"].dt.hour

    # Failed login flag
    df["failed"] = df["status"].apply(
        lambda x: 1 if x == "failed" else 0
    )

    # Encode IP (simple hash)
    df["ip_hash"] = df["ip_address"].apply(
        lambda x: hash(x) % 10000
    )

    # Encode device
    df["device_hash"] = df["user_agent"].apply(
        lambda x: hash(x) % 10000
    )

    features = df[
        ["hour", "failed", "ip_hash", "device_hash"]
    ]

    return features, df


def train_model(X):

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    model.fit(X)

    return model


def detect_anomalies(model, X, df):

    df["anomaly"] = model.predict(X)
    df["score"] = model.decision_function(X)

    return df


if __name__ == "__main__":

    df = load_logs()

    if len(df) < 10:
        print("⚠️ Not enough data yet. Generate more logins.")
        exit()

    X, df = preprocess(df)

    model = train_model(X)

    result = detect_anomalies(model, X, df)

    print("\n=== Anomaly Detection Result ===\n")

    print(
        result[
            [
                "user_id",
                "ip_address",
                "hour",
                "failed",
                "anomaly",
                "score"
            ]
        ]
    )