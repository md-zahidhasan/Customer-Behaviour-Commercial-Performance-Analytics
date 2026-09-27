import sqlite3
import ast
import pandas as pd
import numpy as np

DB_PATH = "Coffee_reward_database.db"
OUTPUT_CSV = "customer_master_full1.csv"

def build_master(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    offers = pd.read_sql_query("SELECT * FROM offers", conn)
    events = pd.read_sql_query("SELECT * FROM events_clean", conn)
    conn.close()

    # Same cleaning logic used in the supplied notebook
    customers["age"] = customers["age"].replace(118, np.nan)
    customers["income"] = pd.to_numeric(customers["income"], errors="coerce")
    customers["age"] = customers["age"].clip(upper=80)
    customers["gender"] = customers["gender"].replace({"O": "Unknown"}).fillna("Unknown")
    customers["became_member_on"] = pd.to_datetime(
        customers["became_member_on"], format="%Y%m%d", errors="coerce"
    )

    events = events.drop_duplicates().copy()

    # Notebook outlier treatment for amount
    q1 = events["amount"].quantile(0.25)
    q3 = events["amount"].quantile(0.75)
    iqr = q3 - q1
    lower = max(0, q1 - 1.5 * iqr)
    upper = q3 + 1.5 * iqr
    events["amount"] = events["amount"].clip(lower=lower, upper=upper)

    event_counts = (
        events.groupby(["customer_id", "event"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={
            "offer received": "offers_received",
            "offer viewed": "offers_viewed",
            "offer completed": "offers_completed",
            "transaction": "transactions_count",
        })
    )

    amount_reward = (
        events.groupby("customer_id")
        .agg(
            total_amount=("amount", "sum"),
            total_reward=("reward", "sum"),
        )
        .reset_index()
    )

    offer_related = events[
        events["event"].isin(["offer received", "offer viewed", "offer completed"])
    ].copy()

    offer_with_type = offer_related.merge(
        offers[["offer_id", "offer_type"]], on="offer_id", how="left"
    )

    offer_type_counts = (
        offer_with_type[offer_with_type["event"] == "offer received"]
        .groupby(["customer_id", "offer_type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={
            "bogo": "bogo_received",
            "discount": "discount_received",
            "informational": "informational_received",
        })
    )

    master = customers.merge(event_counts, on="customer_id", how="left")
    master = master.merge(amount_reward, on="customer_id", how="left")
    master = master.merge(offer_type_counts, on="customer_id", how="left")

    count_cols = [
        "offers_received", "offers_viewed", "offers_completed",
        "transactions_count", "total_amount", "total_reward",
        "bogo_received", "discount_received", "informational_received",
    ]
    for col in count_cols:
        if col not in master:
            master[col] = 0
    master[count_cols] = master[count_cols].fillna(0)

    # Feature engineering from the supplied notebook
    received = master["offers_received"].replace(0, np.nan)
    viewed = master["offers_viewed"].replace(0, np.nan)
    transactions = master["transactions_count"].replace(0, np.nan)
    amount = master["total_amount"].replace(0, np.nan)

    master["view_rate"] = master["offers_viewed"] / received
    master["completion_rate"] = master["offers_completed"] / received
    master["utilization_rate"] = master["offers_completed"] / viewed
    master["avg_transaction_value"] = master["total_amount"] / transactions
    master["transactions_per_offer"] = master["transactions_count"] / received
    master["reward_per_offer"] = master["total_reward"] / received
    master["reward_per_transaction"] = master["total_reward"] / transactions
    master["reward_per_dollar"] = master["total_reward"] / amount
    master["bogo_pct"] = master["bogo_received"] / received
    master["discount_pct"] = master["discount_received"] / received
    master["informational_pct"] = master["informational_received"] / received

    return master, offers, events

if __name__ == "__main__":
    master, _, _ = build_master()
    master.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {OUTPUT_CSV}: {master.shape[0]:,} rows x {master.shape[1]} columns")
