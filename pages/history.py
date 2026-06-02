from Database.config import supabase
import streamlit as st
import pandas as pd


def history_page():

    col1,col2 =st.columns(2)

    with col1:
        st.subheader("Prediction History 🍥")
    with col2: 
        if st.button(" ⬅️Back to Dashboard "):
            st.session_state.page = "dashboard"
            st.rerun()
    
    st.divider()

    response = (
        supabase
        .table("prediction_history")
        .select("*")
        .eq(
            "username",
            st.session_state.username
        )
        .order(
            "created_at",
            desc=True
        )
        .limit(200)
        .execute()
    )
    if len(response.data) > 0:
        df = pd.DataFrame(
            response.data
        )
        df = df.drop(
            columns=["id"],
            errors="ignore"
        )
        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()
        total = len(df)

        fraud = (
            df["prediction"]
            == "Fraud"
        ).sum()

        legit = (
            df["prediction"]
            == "Legitimate"
        ).sum()

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "Total Predictions",
                total
            )

        with c2:
            st.metric(
                "Fraud",
                fraud
            )

        with c3:
            st.metric(
                "Legitimate",
                legit
            )


        st.subheader(
        "Risk Score Distribution"
        )

        st.bar_chart(
            df["risk_score"],
            height=250
        )

        daily = (
        df.groupby(
            df["created_at"]
            .str[:10]
        )
        .size()
        )

        st.line_chart(
            daily,
            height=250
        )
    else:
        st.warning("No  results saved")