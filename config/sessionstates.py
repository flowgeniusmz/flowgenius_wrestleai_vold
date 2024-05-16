import streamlit as st
from supabase import create_client
from openai import OpenAI

def initialize_session_states():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'username': None,
            'password': None,
            'firstname': None,
            'lastname': None,
            'fullname': None,
            'thread_id': None,
            'vector_store_id': None,
            'user_role': None,
            'user_auth_type': None,
            'user_authenticated': False,
            'user_created': None,
            'usertype_complete': False,
            'userauth_complete': False,
            'userflow_complete': False,
            'usertypes': ["New User Registration", "Existing User Sign In"],
            'userroles': ["Admin", "Athlete", "Coach"],
            'user_data': {},
        }
        

    if 'auth_settings' not in st.session_state:
        st.session_state.auth_settings = {
            'username_column': st.secrets.supabase.username_column,
            'password_column': st.secrets.supabase.password_column,
            'vstoreid_column': st.secrets.supabase.vstoreid_column,
            'threadid_column': st.secrets.supabase.threadid_column,
            'userrole_column': st.secrets.supabase.userrole_column,
            'firstname_column': st.secrets.supabase.firstname_column,
            'lastname_column': st.secrets.supabase.lastname_column,
            'fullname_column': st.secrets.supabase.fullname_column,
            'createddate_column': st.secrets.supabase.createddate_column,
            'supabase_client': create_client(supabase_url=st.secrets.supabase.url, supabase_key=st.secrets.supabase.api_key_admin),
            'openai_client': OpenAI(api_key=st.secrets.openai.api_key),
            'users_table': st.secrets.supabase.users_table,
            'existing_user_select_string': f"{st.secrets.supabase.username_column}, {st.secrets.supabase.password_column}, {st.secrets.supabase.vstoreid_column}, {st.secrets.supabase.threadid_column}, {st.secrets.supabase.userrole_column}, {st.secrets.supabase.firstname_column}, {st.secrets.supabase.lastname_column}, {st.secrets.supabase.fullname_column}, {st.secrets.supabase.createddate_column}"
        }

    if 'request_headers' not in st.session_state:
        st.session_state.request_headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}

    