import streamlit as st
from datetime import datetime
from config import pagesetup as ps

class User():
    def __init__(self):
        self.user_data = st.session_state.user
        self.auth_settings = st.session_state.auth_settings

    def initialize_user_authentication(self, user_type, username, password, firstname=None, lastname=None, userrole=None):
        if user_type == "new":
            self.authenticate_new_user(username, password, firstname, lastname, userrole)
        elif user_type == "existing":
            self.authenticate_existing_user(username, password)
        self.update_session_state()

    def authenticate_new_user(self, username, password, firstname, lastname, userrole):
        self.thread_metadata= {"username": username, "password": password, "firstname": firstname, "lastname": lastname, "fullname": f"{firstname} {lastname}", "userrole": userrole, "createddate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.user_data.update({
            'username': username,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'fullname': f"{firstname} {lastname}",
            'user_role': userrole,
            'thread_id': self.auth_settings['openai_client'].beta.threads.create(metadata=self.thread_metadata).id,
            'vector_store_id': self.auth_settings['openai_client'].beta.vector_stores.create(name=f"WrestleAI - {firstname} {lastname}").id,
            'user_created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        new_user_data = {
            self.auth_settings['username_column']: username,
            self.auth_settings['password_column']: password,
            self.auth_settings['vstoreid_column']: self.user_data['vector_store_id'],
            self.auth_settings['threadid_column']: self.user_data['thread_id'],
            self.auth_settings['firstname_column']: firstname,
            self.auth_settings['lastname_column']: lastname,
            self.auth_settings['fullname_column']: self.user_data['fullname'],
            self.auth_settings['userrole_column']: userrole,
            self.auth_settings['createddate_column']: self.user_data['user_created']
        }

        try:
            response = self.auth_settings['supabase_client'].table(self.auth_settings['users_table']).insert(new_user_data).execute()
            if response.data:
                self.user_data.update({
                    'user_data': response.data[0],
                    'user_authenticated': True,
                    'userauth_complete': True
                })
            else:
                st.error("Error creating new user.")
        except Exception as e:
            st.error(f"Error: {e}")

    def authenticate_existing_user(self, username, password):
        response = self.auth_settings['supabase_client'].table(self.auth_settings['users_table']).select(self.auth_settings['existing_user_select_string']).eq(self.auth_settings['username_column'], username).eq(self.auth_settings['password_column'], password).execute()
        if response.data:
            self.user_data.update({
                'user_data': response.data[0],
                'user_authenticated': True,
                'userauth_complete': True
            })
        else:
            st.error("Error: User not recognized.")
            
    def update_session_state(self):
        self.username = self.user_data['username']
        self.password = self.user_data['password']
        self.createddate = self.user_data['user_created']
        self.thread_id = self.user_data['thread_id']
        self.vector_store_id = self.user_data['vector_store_id']
        self.firstname = self.user_data['firstname']
        self.lastname = self.user_data['lastname']
        self.fullname = self.user_data['fullname']
        self.user_role = self.user_data['user_role'] 
        st.session_state.user.update({
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            'firstname': self.user_data['firstname'],
            'lastname': self.user_data['lastname'],
            'fullname': self.user_data['fullname'],
            'user_role': self.user_data['user_role'],
            'thread_id': self.user_data['thread_id'],
            'vector_store_id': self.user_data['vector_store_id'],
            'user_created': self.user_data['user_created'],
        })       
         

class UserFlow():
    def __init__(self):
        self.user = User()
        self.userflow_complete = False
        self.userauth_complete = False
        self.usertype_complete = False

    def userflow1_usertype_form(self):
        usertypeform_container = ps.container_styled2(varKey="usertype")
        with usertypeform_container:
            selectcontainer = ps.container_styled3(varKey="selcont")
            with selectcontainer:
                usertypecols = st.columns([1, 50, 1])
                with usertypecols[1]:
                    st.radio(
                        label="Select New or Existing User",
                        key="selected_usertype",
                        options=st.session_state.user['usertypes'],
                        on_change=self.userflow1_usertype_callback,
                        horizontal=True,
                        index=None
                    )

    def userflow1_usertype_callback(self):
        selected_usertype = st.session_state.selected_usertype
        if selected_usertype:
            st.session_state.user['usertype_complete'] = True
            self.usertype_complete = True
            st.session_state.user['user_auth_type'] = 'new' if selected_usertype == "New User Registration" else 'existing'

    def userflow2_userauth_form(self):
        userauth_container = ps.container_styled2(varKey="userauthcontainer")
        with userauth_container:
            userauth2_container = ps.container_styled3(varKey="userauth2container")
            with userauth2_container:
                userauth_columns = st.columns([1, 20, 1])
                with userauth_columns[1]:
                    st.text_input(label="Username", key="username")
                    st.text_input(label="Password", type="password", key="password")
                    if st.session_state.user['user_auth_type'] == "new":
                        st.text_input(label="First Name", key="firstname")
                        st.text_input(label="Last Name", key="lastname")
                        st.radio(
                            label="Select Account Type",
                            options=st.session_state.user['userroles'],
                            horizontal=True,
                            key="user_role",
                            index=None
                        )
                        st.button(
                            label="Submit",
                            key="addnewuser",
                            on_click=self.userflow2_userauth_callback,
                            args=("new", st.session_state.username, st.session_state.password, st.session_state.firstname, st.session_state.lastname, st.session_state.user_role),
                            type="primary"
                        )
                    elif st.session_state.user['user_auth_type'] == "existing":
                        st.button(
                            label="Submit",
                            key="checkexistinguser",
                            on_click=self.userflow2_userauth_callback,
                            args=("existing", st.session_state.username, st.session_state.password),
                            type="primary"
                        )

    def userflow2_userauth_callback(self, user_type, username, password, firstname=None, lastname=None, userrole=None):
        if userrole is not None:
            userrole = userrole.lower()
        self.user.initialize_user_authentication(user_type, username, password, firstname, lastname, userrole)
        st.session_state.user['userauth_complete'] = True
        st.session_state.user['userflow_complete'] = True
        st.session_state.user['username'] = self.user.user_data['username']
        st.session_state.user['password'] = self.user.user_data['password']
        st.session_state.user['firstname'] = self.user.user_data['firstname']
        st.session_state.user['lastname'] = self.user.user_data['lastname']
        st.session_state.user['fullname'] = self.user.user_data['fullname']
        st.session_state.user['user_role'] = self.user.user_data['user_role']
        st.session_state.user['thread_id'] = self.user.user_data['thread_id']
        st.session_state.user['vector_store_id'] = self.user.user_data['vector_store_id']
        st.session_state.user['created_date'] = self.user.user_data['user_created']
        ps.switch_to_homepage()