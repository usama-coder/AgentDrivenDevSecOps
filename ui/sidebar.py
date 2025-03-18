import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to:", ["Summary", "Vulnerabilities by File"])
    return selected_page
