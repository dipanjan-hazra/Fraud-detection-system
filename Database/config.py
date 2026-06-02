from supabase import create_client, Client
import streamlit as st


@st.cache_resource
def get_supabase() -> Client:

    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    return supabase


supabase = get_supabase()