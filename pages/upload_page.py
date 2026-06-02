import streamlit as st
import pandas as pd
import numpy as np
import joblib
from Database.history import save_batch_predictions
import time


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

def uploader():


    col1, col2, col3 = st.columns([4,1,1])

    with col1:
        st.subheader(
            "📂 Batch Fraud Detection"
        )

    with col2:

        if st.button(
            "📜 History"
        ):

            st.session_state.page = "history"
            st.rerun()

    with col3:

        if st.button(
            "🏠 Dashboard"
        ):

            st.session_state.page = "dashboard"
            st.rerun()
    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV Or Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(
            ".csv"
        ):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file
            )

        st.success(
            f"{len(df)} Rows Loaded"
        )

        st.subheader(
            "Preview"
        )

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        if st.button(
            "🚀 Run Batch Prediction",
            use_container_width=True
        ):

            required_columns = [

                "Amount Received",
                "Amount Paid",

                "Hour",
                "Day",
                "Weekday",

                "same_bank",
                "same_currency",

                "from_bank_freq",
                "to_bank_freq",

                "account_freq",
                "receiver_account_freq",

                "Payment Format"
            ]

            missing = [

                col
                for col in required_columns
                if col not in df.columns
            ]

            if missing:

                st.error(
                    f"Missing Columns: {missing}"
                )

                st.stop()

            original_df = df.copy()

            # =====================
            # Feature Engineering
            # =====================

            df["log_amount_received"] = (
                np.log1p(
                    df["Amount Received"]
                )
            )

            df["log_amount_paid"] = (
                np.log1p(
                    df["Amount Paid"]
                )
            )

            df["amount_diff"] = (

                df["Amount Received"]

                -

                df["Amount Paid"]
            )

            df["amount_ratio"] = (

                df["Amount Received"]

                /
                    df["Amount Paid"]
            )

            # =====================
            # One Hot Encoding
            # =====================

            df = pd.get_dummies(

                df,

                columns=[
                    "Payment Format"
                ]
            )

            # =====================
            # Match Training Columns
            # =====================

            for col in columns:

                if col not in df.columns:

                    df[col] = 0

                df = df[columns]

                # =====================
                # Prediction
                # =====================

            probs = model.predict_proba(
                df
            )[:, 1]

            preds = model.predict(
                df
            )

            # =====================
            # Results
            # =====================

            results = original_df.copy()

            results[
                "Fraud Probability"
            ] = probs

            results[
                "Risk Score"
            ] = (
                probs * 100
            ).round(2)

            results[
                "Prediction"
            ] = preds

            results[
                "Prediction"
            ] = results[
                "Prediction"
            ].map({

                0: "Legitimate",

                1: "Fraud"
            })

            st.success(
                "Prediction Completed"
            )

            fraud_count = (

                results[
                    "Prediction"
                ] == "Fraud"

            ).sum()

            legit_count = (

                results[
                    "Prediction"
                ] == "Legitimate"

            ).sum()

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"""
                    <div style="
                    padding:20px;
                    border-radius:10px;
                    background-color:#ffebee;
                    border:2px solid red;
                    text-align:center;
                    ">
                    <h3>🚨 Fraud Transactions</h3>
                    <h1>{fraud_count}</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div style="
                    padding:20px;
                    border-radius:10px;
                    background-color:#e8f5e9;
                    border:2px solid green;
                    text-align:center;
                    ">
                    <h3>✅ Legitimate Transactions</h3>
                    <h1>{legit_count}</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.dataframe(
                results,
                use_container_width=True
            )

            csv = results.to_csv(
                index=False
            )

            save_batch_predictions(results)

            st.download_button(

                "📥 Download Results",

                csv,

                "fraud_predictions.csv",

                "text/csv"
            )  

    st.divider()

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.logged_in = False

        st.session_state.page = "login"

        st.rerun()

