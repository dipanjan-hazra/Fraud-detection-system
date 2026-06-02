import streamlit as st
from Database.auth import login_user

def login_page():


    st.subheader("🔐 Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        width="stretch",
        type='primary'
    ):

        try:

            user = login_user(
                username=username,
                password=password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = (
                    user["username"]
                )

                st.session_state.email = (
                    user["email"]
                )

                st.session_state.page = (
                    "dashboard"
                )

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        except Exception as e:

            st.error(
                f"Login Failed: {e}"
            )

    st.divider()

    st.write(
        "Don't have an account?"
    )

    if st.button(
        "Register Now",
        width="stretch"
    ):

        st.session_state.page = (
            "register"
        )

        st.rerun()


