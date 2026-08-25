import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

os.makedirs("data", exist_ok=True)
np.random.seed(42)
random.seed(42)

# Customers
n_customers = 200
customers = []
for i in range(1, n_customers + 1):
    customers.append({
        "customer_id": f"CUST{i:04d}",
        "name": f"Customer {i}",
        "age": random.randint(18, 75),
        "country": random.choice(["US", "UK", "IN", "CA", "DE", "AU"]),
        "account_age_days": random.randint(30, 2000),
        "avg_monthly_spend": round(random.uniform(200, 5000), 2),
        "risk_tier": random.choice(["low", "medium", "high"]),
        "is_watchlist": random.choice([False, False, False, True]),
    })
pd.DataFrame(customers).to_csv("data/customers.csv", index=False)

# Transactions
n_tx = 1500
start = datetime(2025, 1, 1)
transactions = []
for i in range(1, n_tx + 1):
    cust = random.choice(customers)
    is_fraud = random.random() < 0.08

    amount = round(random.uniform(5, 8000), 2)
    if is_fraud:
        amount = round(random.uniform(1500, 15000), 2)

    tx_time = start + timedelta(minutes=random.randint(0, 60*24*180))
    country = cust["country"] if random.random() > 0.15 else random.choice(["RU", "NG", "CN", "BR"])
    if is_fraud and random.random() < 0.6:
        country = random.choice(["RU", "NG", "CN", "BR", "PK"])

    transactions.append({
        "transaction_id": f"TXN{i:06d}",
        "customer_id": cust["customer_id"],
        "amount": amount,
        "currency": "USD",
        "merchant": random.choice(["Amazon", "Walmart", "Unknown Merchant", "CryptoExchange", "TravelAgency", "ElectronicsHub", "DarkWebMarket"]),
        "merchant_category": random.choice(["retail", "travel", "crypto", "electronics", "unknown"]),
        "timestamp": tx_time.isoformat(),
        "ip_address": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "device_id": f"DEV{random.randint(1000,9999)}",
        "country": country,
        "is_fraud": is_fraud,
        "channel": random.choice(["web", "mobile", "pos"]),
    })

pd.DataFrame(transactions).to_csv("data/transactions.csv", index=False)
print("Synthetic data generated successfully!")