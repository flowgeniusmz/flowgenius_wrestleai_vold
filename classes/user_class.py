import streamlit as st
from supabase import create_client
from openai import OpenAI
from datetime import datetime
from config import pagesetup as ps


class User():
    def __init__(self):
        self.initialize_user_attributes()
        self.initialize_userauth_attributes()
        
    def initialize_user_attributes(self):
        self.username = None
        self.password = None
        self.firstname = None
        self.lastname = None
        self.fullname = None
        self.thread_id = None
        self.vector_store_id = None
        self.user_role = None
        self.user_auth_type = None
        self.user_authenticated = False
        self.user_created = None
        self.usertype_complete = False
        self.userauth_complete = False
        self.userflow_complete = False
        self.usertypes = ["New", "Existing"]
        self.user_data = {}
    
    def initialize_userauth_attributes(self):
        self.username_column = st.secrets.supabase.username_column
        self.password_column = st.secrets.supabase.password_column
        self.vstoreid_column = st.secrets.supabase.vstoreid_column
        self.threadid_column = st.secrets.supabase.threadid_column
        self.userrole_column = st.secrets.supabase.userrole_column
        self.firstname_column = st.secrets.supabase.firstname_column
        self.lastname_column = st.secrets.supabase.lastname_column
        self.fullname_column = st.secrets.supabase.fullname_column
        self.createddate_column = st.secrets.supabase.createddate_column
        self.supabase_client = create_client(supabase_url=st.secrets.supabase.url, supabase_key=st.secrets.supabase.api_key_admin)
        self.openai_client = OpenAI(api_key=st.secrets.openai.api_key)
        self.table = st.secrets.supabase.users_table
        self.existing_user_select_string = f"{self.username_column}, {self.password_column}, {self.vstoreid_column}, {self.threadid_column}, {self.userrole_column}, {self.firstname_column}, {self.lastname_column}, {self.fullname_column}, {self.createddate_column}"
    
    def initialize_user_authentication(self, type, username, password, firstname: str = None, lastname: str = None, userrole: str = None):
        if type == "new":
            self.authenticate_new_user(username=username, password=password, firstname=firstname, lastname=lastname, userrole=userrole)
        elif type == "existing":
            self.authenticate_existing_user(username=username, password=password)
            
            
        
    def authenticate_new_user(self, username, password, firstname, lastname, userrole):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = f"{firstname} {lastname}"
        self.user_role = userrole
        self.thread = self.openai_client.beta.threads.create()
        self.thread_id = self.thread.id
        self.vectore_store = self.openai_client.beta.vector_stores.create(name=f"WrestleAI - {self.fullname}")
        self.vectore_store_id = self.vectore_store.id
        self.user_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.new_user_data = {self.username_column: username, self.password_column: password, self.vstoreid_column: self.vectorstoreid, self.threadid_column: self.thread_id, self.firstname_column: self.firstname, self.lastname_column: self.lastname, self.fullname_column: self.fullname, self.userrole_column: self.user_role, self.createddate_column: self.user_created}
        try: 
            self.add_new_user_response = self.supabase_client.table(self.table).insert(self.new_user_data).execute()
            self.add_new_user_response_data = self.add_new_user_response.data
            if self.add_new_user_response_data and len(self.add_new_user_response_data) > 0:
                self.user_data = self.add_new_user_response_data[0]
                self.user_authenticated = True
                self.userauth_complete = True
            else:
                st.error("ERROR")
                print("error")
        except Exception as e:
            st.error(f"ERROR: {e}")
            
    def authenticate_existing_user(self, username, password, firstname: str = None, lastname: str = None, userrole: str = None):
        self.check_existing_user_response = self.supabase_client.table(self.table).select(self.existing_user_select_string).eq(self.username_column, username).eq(self.password_column, password).execute()
        self.check_existing_user_response_data = self.check_existing_user_response.data
        if self.check_existing_user_response_data and len(self.check_existing_user_response_data) > 0:
            self.user_data = self.check_existing_user_response_data[0]
            self.user_authenticated = True
            self.userauth_complete = True
        else:
            st.error("ERROR: Not recognized")
            print("error")
    

class UserFlow():
    def __init__(self):
        self.userflow_complete = False
        self.userauth_complete = False
        self.usertype_complete = False
        self.user = User()
        
    def userflow1_usertype_form(self):
        usertypeform_container = ps.container_styled2(varKey="usertype") #st.container(border=True)
        with usertypeform_container:
            selectcontainer = ps.container_styled3(varKey="selcont")
            with selectcontainer:
                usertypecols = st.columns([1,50,1])
                with usertypecols[1]:
                    self.select_usertype = st.radio(label="Select New or Existing User", key="selected_usertype", options=st.session_state.auth_types, index=None, on_change=self.userflow1_usertype_callback, horizontal=True)

    def userflow1_usertype_callback(self):
        if st.session_state.selected_usertype is not None:
            st.session_state.usertype_complete = True
            self.usertype_complete = True
            if self.select_usertype == "New User Registration":
                st.session_state.usertype = "new"
                self.usertype = "new"
            else:
                st.session_state.usertype = "existing"
                self.usertype = "existing"
                
    def userflow2_userauth_form(self):
        userauth_container = ps.container_styled2(varKey="userauthcontainer")
        with userauth_container:
            userauth_columns = st.columns([1,20,1])
            with userauth_columns[1]:
                self.username = st.text_input(label="Username", key="username")
                self.password = st.text_input(label="Password", type="password", key="password")
                if self.usertype == "new":
                    self.firstname = st.text_input(label="First Name", key="firstname")
                    self.lastname = st.text_input(label="Last Name", key="lastname")
                    self.userrole = st.radio(label="Select Account Type", options=st.session_state.user_roles, horizontal=True, index=None, key="user_role")
                    submit_new = st.button(label="Submit", key="addnewuser", on_click=self.userflow2_userauth_callback, args=["new", self.username, self.password, self.firstname, self.lastname, self.userrole], type="primary")
                elif self.usertype == "existing":
                    check_existing = st.button(label="Submit", key="checkexistinguser", on_click=self.userflow2_userauth_callback, args=["existing", self.username, self.password], type="primary")
                    
                
                    
    def userflow2_userauth_callback(self, type, username, password, firstname: str=None, lastname: str=None, userrole: str=None):
        if type == "new":
            self.user.authenticate_new_user(username=username, password=password, firstname=firstname, lastname=lastname, userrole=userrole)
        elif type == "existing":
            self.user.authenticate_existing_user(username=username, password=password)
        self.userauth_complete = True
        self.userflow_complete = True
        st.session_state.userauth_complete = True
        st.session_state.userflow_complete = True
        st.session_state.username = self.user.username
        st.session_state.password = self.user.password
        st.session_state.firstname = self.user.firstname
        st.session_state.lastname = self.user.lastname
        st.session_state.fullname = self.user.fullname
        st.session_state.user_role = self.user.user_role
        st.session_state.thread_id = self.user.thread_id
        st.session_state.vector_store_id = self.user.vector_store_id
        st.session_state.created_date = self.user.user_created
        ps.switch_to_homepage()
            
        
            
            