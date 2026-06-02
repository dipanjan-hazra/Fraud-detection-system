import yagmail
import streamlit as st
import datetime 


def send_alert(
    recipient,
    probability,
    amount_received,
    amount_paid
):

    yag = yagmail.SMTP(
        st.secrets["EMAIL_ADDRESS"],
        st.secrets["EMAIL_PASSWORD"]
    )

    yag.send(
        to=recipient,
        subject="🚨 Fraud Alert",
        contents=f"""
🚨 High Risk Transaction Detected

        User:
        {st.session_state.username}

        Amount Received:
        ₹{amount_received:,.2f}

        Amount Paid:
        ₹{amount_paid:,.2f}

        Fraud Probability:
        {probability:.2%}

        Risk Score:
        {probability*100:.2f}

        Time:
        {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

        Please review this transaction immediately.
        """
    )