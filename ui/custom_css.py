import streamlit as st
import os


def apply_css(file_name):

    base_path = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_path+"\styles", file_name)
    try:
        if not os.path.exists(css_path):
            st.warning(f"⚠️ CSS file not found: `{file_name}` (Expected Path: `{css_path}`)")
            return

        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error while loading `{file_name}`: {str(e)}")
