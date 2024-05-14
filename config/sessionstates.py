import streamlit as st


class SessionStates():
    def __init__(self):
        self.initialize_user()
        
    def initialize_user(self):
        if "userflow_complete" not in st.session_state:
            st.session_state.user_authenticated = False
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.thread_id = None
            st.session_state.vector_store_id = None
            st.session_state.created_date = None
            st.session_state.firstname = None
            st.session_state.lastname = None
            st.session_state.fullname = None
            st.session_state.user_role = None
            st.session_state.user_roles = ["Athlete", "Coach", "Admin"]
            st.session_state.auth_type = None
            st.session_state.auth_types = ["New User Registration", "Existing User Sign In"]
            st.session_state.usertype_complete = False
            st.session_state.userauth_complete = False
            st.session_state.userflow_complete = False
            st.session_state.usertype = None
            st.session_state.selected_usertype = None
            