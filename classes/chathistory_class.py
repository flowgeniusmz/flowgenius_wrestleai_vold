import streamlit as st
from openai import OpenAI
from config import pagesetup as ps
import pandas as pd


class ChatHistory():
    def __init__(self):
        self.initialize_openai()
        self.initialize_messages()
        self.get_messages()
    
    def initialize_openai(self):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)
        self.thread_id = st.session_state.user['user_data']['thread_id']
        self.thread_id1 = "thread_dfgkQIPEGfBhf8O4lACBAsh1"
        
        
    def initialize_messages(self):
        self.user_messages = []
        self.assistant_messages = []
        self.messages = []
        
    def get_messages(self):
        self.thread_messages = self.client.beta.threads.messages.list(thread_id=self.thread_id1)
        for thread_message in self.thread_messages:
            new_row = {
                "role": thread_message.role,
                "content": thread_message.content[0].text.value,
                "run_id": thread_message.run_id
            }
            self.messages.append(new_row)
        self.chat_history_dataframe = pd.DataFrame(self.messages)
        print(self.messages)
        self.chat_history_dataframe_grouped = self.chat_history_dataframe.groupby('run_id')
        for run_id, group in self.chat_history_dataframe_grouped:
            self.user_msgs = group[group['role'] == 'user']['content']
            self.assistant_msgs = group[group['role'] == 'assistant']['content']
            run_container = ps.container_styled3(varKey=f"runcontainer_{run_id}")
            with run_container:
                header_container = st.container(border=False)
                with header_container:
                    runid = st.text_input(label="Run Id", value=run_id, disabled=True)
                body_container = st.container(border=False)
                with body_container:
                    cols = st.columns([10,1,10])
                    with cols[0]:
                        usermessages = st.popover(label="User Messages", use_container_width=True, disabled=False)
                        with usermessages:
                            for msg in self.user_msgs:
                                st.markdown(msg)
                    with cols[2]:
                        asstmessages = st.popover(label="Assistant Messages", use_container_width=True, disabled=False)
                        with asstmessages:
                            for msg in self.assistant_msgs:
                                st.markdown(msg)
                
    