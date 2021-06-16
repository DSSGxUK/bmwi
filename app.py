import os
import streamlit as st
import numpy as np

# Custom imports 
from multipage import MultiPage
from pages import data_upload, data_analysis, data_visualize, cinny_page # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("German Data Tool")

# The main app
app.add_page("Upload Data", data_upload.app)
app.add_page("Data Analysis", data_analysis.app)
app.add_page("Data Visualization", data_visualize.app)
app.add_page("Testing Page", cinny_page.app)
app.run()