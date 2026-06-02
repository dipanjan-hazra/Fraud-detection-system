import streamlit as st

from Database.auth import register_user

def register_page():

    st.subheader("Register Yourself 😀")

    username = st.text_input(
        "Username",
        key="reg_user"
    )

    email = st.text_input(
        "Email",
        key="reg_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="reg_password"
    )

    re_enterpass = st.text_input(
        "enter password again",
        type="password"
    )
    

    col1,col2 = st.columns(2) 

    with col1:
        if st.button("Create Account",type='primary'):

            if password != re_enterpass:
                st.error("pls  verify  password and  re pass !")
            
            if not username.strip():

                st.error(
                    "Username is required"
                )

            elif not email.strip():

                st.error(
                    "Email is required"
                )

            elif not password:

                st.error(
                    "Password is required"
                )

            elif len(username) < 3:

                st.error(
                    "Username must be at least 3 characters"
                )

            elif len(password) < 8:

                st.error(
                    "Password must be at least 8 characters"
                )

            elif "@" not in email:

                st.error(
                    "Invalid Email"
                )

            else:
                    try:
                        register_user(username,email,password)

                    except Exception as e:
                        st.error("Internal server error !🤕 ")
                    
                    st.success(
                        "Account Created Successfully"
                    )

                    st.session_state.page = "login"

                    st.rerun()
            
    with col2:
        if st.button("Back To Login",type='secondary'):

            st.session_state.page = "login"

            st.rerun()