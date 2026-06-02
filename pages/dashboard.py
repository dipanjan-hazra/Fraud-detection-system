import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import joblib
import time 
from Database.history import save_prediction
from Util.mail import send_alert


@st.cache_resource
def load_model():
    model = joblib.load(
        "Models/fraud_model.pkl"
    )

    columns = joblib.load(
        "Models/feature_columns.pkl"
    )
    

    return model, columns


model, columns = load_model()


def dashboard_page():

    if "dashboard_mode" not in st.session_state:
        st.session_state.dashboard_mode = "manual"

    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None


    st.write(
        f"Welcome, {st.session_state.username}"
    )

    st.divider()

    # =====================================
    # MANUAL PREDICTION PAGE
    # =====================================

    if st.session_state.dashboard_mode == "manual":

        top_col1, top_col2, top_col3 = st.columns([4,1,1])

        with top_col1:

            st.subheader(
                "Enter Below To Check Manually Your Transaction"
            )

        with top_col2:

            if st.button(
                "📂 Upload CSV"
            ):

                st.session_state.page = "upload"

                st.rerun()

        with top_col3:

            if st.button(
                "📜 History"
            ):

                st.session_state.page = "history"

                st.rerun()

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            amount_received = st.number_input(
                "Amount Received",
                min_value=0.0,
                step=100.0
            )

            transaction_date = st.date_input(
                "Transaction Date"
            )

            payment_format = st.selectbox(
                "Payment Format",
                [
                    "ACH",
                    "Bitcoin",
                    "Cash",
                    "Cheque",
                    "Credit Card",
                    "Reinvestment",
                    "Wire"
                ]
            )

            same_bank = st.toggle(
                "Sender And Receiver Use Same Bank?"
            )

            from_bank_freq = st.number_input(
                "Sender Bank Transaction Frequency",
                min_value=0
            )

            account_freq = st.number_input(
                "Sender Account Transaction Frequency",
                min_value=0
            )

        with col2:

            amount_paid = st.number_input(
                "Amount Paid",
                min_value=0.0,
                step=100.0
            )

            transaction_time = st.time_input(
                "Transaction Time"
            )

            same_currency = st.toggle(
                "Same Currency?"
            )

            receiver_account_freq = st.number_input(
                "Receiver Account Transaction Frequency",
                min_value=0
            )

        st.divider()

        if st.button(
            "🚀 Predict Fraud Risk",
            use_container_width=True
        ):

            if amount_received <= 0:

                st.error(
                    "Amount Received must be greater than 0"
                )

            elif amount_paid <= 0:

                st.error(
                    "Amount Paid must be greater than 0"
                )

            else:

                dt = datetime.combine(
                    transaction_date,
                    transaction_time
                )

                hour = dt.hour
                day = dt.day
                weekday = dt.weekday()

                data = pd.DataFrame(
                    [[0.0] * len(columns)],
                    columns=columns
                )

                data.loc[0, "Amount Received"] = amount_received
                data.loc[0, "Amount Paid"] = amount_paid

                data.loc[0, "log_amount_received"] = np.log1p(
                    amount_received
                )

                data.loc[0, "log_amount_paid"] = np.log1p(
                    amount_paid
                )

                data.loc[0, "amount_diff"] = (
                    amount_received
                    - amount_paid
                )

                data.loc[0, "amount_ratio"] = (
                    amount_received
                    /
                    (amount_paid + 1e-6)
                )

                data.loc[0, "Hour"] = hour
                data.loc[0, "Day"] = day
                data.loc[0, "Weekday"] = weekday

                data.loc[0, "same_bank"] = int(
                    same_bank
                )

                data.loc[0, "same_currency"] = int(
                    same_currency
                )

                data.loc[0, "from_bank_freq"] = (
                    from_bank_freq
                )

                data.loc[0, "to_bank_freq"] = (
                    receiver_account_freq
                )

                data.loc[0, "account_freq"] = (
                    account_freq
                )

                data.loc[
                    0,
                    "receiver_account_freq"
                ] = receiver_account_freq

                payment_col = (
                    f"Payment Format_{payment_format}"
                )

                if payment_col in data.columns:

                    data.loc[
                        0,
                        payment_col
                    ] = 1

                prob = model.predict_proba(
                    data
                )[0][1]

                pred = model.predict(
                    data
                )[0]


                if prob >= 0.80:

                    send_alert(
                        st.session_state.email,
                        prob,
                        amount_received,
                        amount_paid
                    )

                st.session_state.prediction_result = {

                    "prob": prob,

                    "pred": pred,
                }

        if st.session_state.prediction_result:

            prob = (
                st.session_state
                .prediction_result["prob"]
            )

            pred = (
                st.session_state
                .prediction_result["pred"]
            )
         
            st.divider()

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Fraud Probability",
                    f"{prob*100:.2f}%"
                )

            with c2:

                st.metric(
                    "Risk Score",
                    round(
                        prob * 100,
                        2
                    )
                )

            if pred == 1:

                st.error(
                    "🚨 Fraudulent Transaction Detected"
                )

                
            else:

                st.success(
                    "✅ Legitimate Transaction"
                )
        
            if st.button("save results"):
                try:
                    save_prediction(
                        st.session_state.username,

                        amount_received,

                        amount_paid,

                        float(prob),

                        float(prob * 100),

                        "Fraud" if pred == 1
                        else "Legitimate"
                    )
                    st.success("✅ Result saved")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.warning("! ⚠️Internal problem Reults not  save  try  again ")
