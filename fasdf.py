from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets.openai.api_key)
threadid = "thread_4qiPJGGBWGziiRn0IaYkfyhd"

thread = client.beta.threads.retrieve(thread_id=threadid)
print(thread)
print(thread.metadata)