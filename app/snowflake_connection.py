import os

import snowflake.connector
import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError


load_dotenv()


def get_secret(name):
    """
    Get a configuration value from Streamlit Secrets when deployed,
    otherwise fall back to environment variables from .env.
    """

    try:
        return st.secrets[name]
    except (StreamlitSecretNotFoundError, KeyError):
        return os.getenv(name)


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=get_secret("SNOWFLAKE_ACCOUNT"),
        user=get_secret("SNOWFLAKE_USER"),
        password=get_secret("SNOWFLAKE_PASSWORD"),
        database=get_secret("SNOWFLAKE_DATABASE"),
        schema="ANALYTICS",
        warehouse=get_secret("SNOWFLAKE_WAREHOUSE"),
        role=get_secret("SNOWFLAKE_ROLE"),
    )