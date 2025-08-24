import os
import streamlit as st
from dotenv import load_dotenv

# ----------------------------
# Setup environment
# ----------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") or st.secrets["SECRET_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME") or st.secrets["MODEL_NAME"]
