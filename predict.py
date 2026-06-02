import joblib 
import pandas as pd
import numpy as np

model = joblib.load("fraud_model.pkl")
columns = joblib.load("feature_columns.pkl")

def predict_transaction():

    row = {
    "Amount Received": 11300.38,
    "Amount Paid": 11300.38,

    "Hour": 14,
    "Day": 12,
    "Weekday": 0,

    "same_bank": 0,
    "same_currency": 1,

    "from_bank_freq": 185,
    "to_bank_freq": 1017,

    "account_freq": 1,
    "receiver_account_freq": 3,

    "payment_format": "ACH"
    }

    data = pd.DataFrame(
        [[0] * len(columns)],
        columns=columns
    )

    row["log_amount_received"] = np.log1p(
        row["Amount Received"]
    )

    row["log_amount_paid"] = np.log1p(
        row["Amount Paid"]
    )

    row["amount_diff"] = (
        row["Amount Received"]
        - row["Amount Paid"]
    )

    row["amount_ratio"] = (
        row["Amount Received"]
        /
        (row["Amount Paid"] + 1e-6)
    )

    data.loc[0, "Amount Received"] = row["Amount Received"]
    data.loc[0, "Amount Paid"] = row["Amount Paid"]

    data.loc[0, "log_amount_received"] = row["log_amount_received"]
    data.loc[0, "log_amount_paid"] = row["log_amount_paid"]

    data.loc[0, "amount_diff"] = row["amount_diff"]
    data.loc[0, "amount_ratio"] = row["amount_ratio"]

    data.loc[0, "Hour"] = row["Hour"]
    data.loc[0, "Day"] = row["Day"]
    data.loc[0, "Weekday"] = row["Weekday"]

    data.loc[0, "same_bank"] = row["same_bank"]
    data.loc[0, "same_currency"] = row["same_currency"]

    data.loc[0, "from_bank_freq"] = row["from_bank_freq"]
    data.loc[0, "to_bank_freq"] = row["to_bank_freq"]

    data.loc[0, "account_freq"] = row["account_freq"]
    data.loc[0, "receiver_account_freq"] = row["receiver_account_freq"]

    payment_col = (
        f"Payment Format_{row['payment_format']}"
    )

    if payment_col in data.columns:
        data.loc[0, payment_col] = 1


    prob = model.predict_proba(data)[0][1]

    print("Fraud Probability:", prob)
    print("Risk Score:", round(prob * 100, 2))
    
    pred = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]
    print(data.T)   

    print("Prediction:", pred)



predict_transaction()

