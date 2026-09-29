import streamlit as st


def get_snowflake_connection():
    return st.connection(
        "snowflake",
        type="snowflake"
    )