
import streamlit as st
from Database.config import supabase


def save_prediction(
    username,
    amount_received,
    amount_paid,
    fraud_probability,
    risk_score,
    prediction
):

    supabase.table(
        "prediction_history"
    ).insert({

        "username": username,

        "amount_received":
            amount_received,

        "amount_paid":
            amount_paid,

        "fraud_probability":
            fraud_probability,

        "risk_score":
            risk_score,

        "prediction":
            prediction

    }).execute()




def save_batch_predictions(results):

    records = []

    for _, row in results.iterrows():

        records.append({

            "username":
                st.session_state.username,

            "amount_received":
                float(row["Amount Received"]),

            "amount_paid":
                float(row["Amount Paid"]),

            "fraud_probability":
                float(
                    row["Fraud Probability"]
                ),

            "risk_score":
                float(
                    row["Risk Score"]
                ),

            "prediction":
                row["Prediction"]
        })

    supabase.table(
        "prediction_history"
    ).insert(
        records
    ).execute()


    