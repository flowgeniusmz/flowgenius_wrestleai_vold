import streamlit as st
from streamlit_extras.stylable_container import stylable_container as sc

class PageSetup():
    def __init__(self, page_number: int = 0, set_manually: bool=False, title: str=None, subtitle: str=None):
        self.page_number = page_number
        self.display_background_image()
        self.get_page_styling()
        self.initialize_page_element_values()
        if not set_manually:
            self.get_page_elements()
            self.get_page_config()
            self.get_page_overview()
        else:
            self.get_page_elements_manual(title=title, subtitle=subtitle)
            self.set_title_manual()
        
   
    def initialize_page_element_values(self):
        self.values_icons = st.secrets.pageconfig.page_icons
        self.values_titles = st.secrets.pageconfig.page_titles
        self.values_subtitles = st.secrets.pageconfig.page_subtitles
        self.values_paths = st.secrets.pageconfig.page_paths
        self.values_headers = st.secrets.pageconfig.page_headers
        self.values_descriptions = st.secrets.pageconfig.page_descriptions
        self.values_abouts = st.secrets.pageconfig.page_abouts
    
    def get_page_elements(self):
        """
        Retrieves configuration data for a given page number and configuration type from an array within Streamlit secrets.

        Args:
        - varPageNumber: int, the page number for which to retrieve the configuration.
        - varPageConfigType: str, the type of configuration to retrieve ('title', 'subtitle', 'description', 'header', 'icon', 'path', 'about').

        Returns:
        - str, the configuration data for the given page number and configuration type from the specified array.
        """
        self.page_icon = self.values_icons[self.page_number]
        self.page_title = self.values_titles[self.page_number]
        self.page_subtitle = self.values_subtitles[self.page_number]
        self.page_path = self.values_paths[self.page_number]
        self.page_header = self.values_headers[self.page_number]
        self.page_description = self.values_descriptions[self.page_number]
        self.page_about = self.values_abouts[self.page_number]
    
    def get_page_elements_manual(self, title, subtitle):
        self.page_title = title
        self.page_subtitle = subtitle
        self.page_icon = self.values_icons[self.page_number]
        self.page_path = self.values_paths[self.page_number]
        self.page_header = self.values_headers[self.page_number]
        self.page_description = self.values_descriptions[self.page_number]
        self.page_about = self.values_abouts[self.page_number]

    def display_background_image(self):
        # Set the Streamlit image for branding as the background with transparency
        self.background_image_path = st.secrets.appconfig.background_image_path
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.90)), url({self.background_image_path});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def get_page_styling(self):
        with open("config/style.css" ) as css:
            st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    def get_page_config(self, show_divider: bool=False):
        headercontainer = st.container(border=False)
        with headercontainer:
            headercols = st.columns([10,2])
            with headercols[0]:
                st.markdown(f"""<span style="font-weight: bold; font-size: 2em; color:#4A90E2;">{self.page_title} </span> <span style="font-weight: bold; color:#FFFFFF; font-size:1.3em;">{self.page_subtitle}</span>""", unsafe_allow_html=True)
            with headercols[1]:
                self.menu = self.get_popover_menu(varPageNumber=self.page_number)
            if show_divider:
                st.divider() 

    def get_popover_menu(self):
        menulist = st.popover(label="🧭 Menu", disabled=False, use_container_width=True)
        with menulist:
            for i in range(len(self.values_paths)):
                st.page_link(page=self.values_paths[i], label=self.values_subtitles[i], disabled=(self.page_number == i))

    def get_page_overview(self):
        st.markdown(f"""<span style="font-weight: bold; color:#4A90E2; font-size:1.3em;">{self.page_header}</span>""", unsafe_allow_html=True)
        if self.page_number == 0:
            st.markdown(body=self.page_description)
        else:
            st.markdown(f"{self.page_description}")
        st.divider()
    
    def get_blue_header(self, varText: str):
        st.markdown(f"""<span style="font-weight: bold; color:#4A90E2; font-size:1.3em;">{varText}</span>""", unsafe_allow_html=True)    

    def get_gray_header(self, varText: str):
        st.markdown(f"""<span style="font-weight: bold; color:#333333; font-size:1.3em;">{varText}</span>""", unsafe_allow_html=True)

    def get_green_header(self, varText: str):
        st.markdown(f"""<span style="font-weight: bold; color:#00b084; font-size:1.3em;">{varText}</span>""", unsafe_allow_html=True)

    def set_title_manual(self, show_divider: bool=True):
        st.markdown(f"""<span style="font-weight: bold; font-size: 2em; color:#4A90E2;">{self.page_title} </span> <span style="font-weight: bold; color:#333333; font-size:1.3em;">{self.page_subtitle}</span>""", unsafe_allow_html=True)
        if show_divider:
            st.divider()