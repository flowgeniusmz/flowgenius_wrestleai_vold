import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from openai import OpenAI
import time


def get_container(key, height: int=100, border: bool=False):
    styled_container = ps.container_styled2(varKey=f"adfads{key}")
    with styled_container:
        styled_container_inner = ps.container_styled3(varKey=f"adsfadsfasda{key}")
        with styled_container_inner:
            container = st.container(height=height, border = border)
            return container



client = OpenAI(api_key=st.secrets.openai.api_key)
existing_thread_id = "thread_dfgkQIPEGfBhf8O4lACBAsh1"
initial_thread_messages = client.beta.threads.messages.list(thread_id=existing_thread_id)
assistant_id = st.secrets.openai.assistant_id

# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 1
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)

def get_chat_container(tab_number):
    main_container = ps.container_styled2(varKey=f"dafdsfadsfasadsf{tab_number}")
    with main_container:
        sub_container = ps.container_styled3(varKey=f"dadfad{tab_number}")
        with sub_container:
            chat_container = st.container(height=400, border=False)
    return chat_container

chat_tab_names = ["Existing Chat Example", "New Chat Example", "Test"]

chat_tabs = st.tabs(tabs=chat_tab_names)
with chat_tabs[0]:
    chat_container1 = get_chat_container(0)
    with chat_container1:
        for msg in initial_thread_messages:
            with st.chat_message(name=msg.role):
                st.markdown(msg.content[0].text.value)

        if prompt := st.chat_input("Enter your question here...", key="adfad"):
            new_message = client.beta.threads.messages.create(role="user", thread_id=existing_thread_id, content=prompt)
            with chat_container1:
                with st.chat_message("user"):
                    st.markdown(prompt)
            run = client.beta.threads.runs.create(thread_id=existing_thread_id, assistant_id=assistant_id)
            while run.status != "completed":
                time.sleep(2)
                run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=existing_thread_id)
                if run.status == "completed":
                    thread_messages = client.beta.threads.messages.list(thread_id=existing_thread_id, run_id=run.id)
                    for msg in thread_messages:
                        if msg.role == "assistant":
                            with chat_container1:
                                with st.chat_message(name="assistant"):
                                    st.markdown(msg.content[0].text.value)
    
with chat_tabs[1]:
    chat_container2 = get_chat_container(1)
    
    
with chat_tabs[2]:
    container1 = get_container(key="dafdfdafdadfad", height=200, border=False)
    with container1:
        with st.chat_message("assistant"):
            st.markdown("Yo homie")
            
        with st.chat_message("user"):
            st.markdown("Your a chat")
    
    
    
