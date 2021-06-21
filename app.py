import os
import streamlit as st
import numpy as np

# Custom imports 
from multipage import MultiPage
from pages import data_upload, data_analysis, data_visualize, cinny_page, network_numerical, merge_data, cluster_analysis, network_categorical # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("BMWi Tool")

# The main app
app.add_page("Upload Data", data_upload.app)
app.add_page("Data Analysis", data_analysis.app)
app.add_page("Data Visualization", data_visualize.app)
app.add_page("Merge Data", merge_data.app)
app.add_page("Cluster Analysis", cluster_analysis.app)
app.add_page("Network: Time-Series", network_numerical.app)
app.add_page("Network: Categorical", network_categorical.app)
app.add_page("Testing Page", cinny_page.app)
app.run()