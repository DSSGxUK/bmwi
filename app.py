import streamlit as st

import os
from typing import final
import numpy as np

# Custom imports 
from multipage import MultiPage

# import your pages here
from pages import model_page, data_prep, home_page, error_analysis, prediction_viz, ranking, confidence_intervals

# Change the page name and icon 
st.set_page_config(page_title="BMWi Forecasting Tool", page_icon='📊')

# remove rightsidebar 
# st.markdown("""
#     <style>div[data-testid="stToolbar"] { display: none;}</style>
#     """, unsafe_allow_html=True)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("BMWi Tool")
st.markdown('[Documentation](https://dssgxuk.github.io/bmwi/)')
st.markdown('')

# The main app
app.add_page("Home", home_page.app)
app.add_page("Data Preparation", data_prep.app)
app.add_page("Predictions", model_page.app)
app.add_page("Confidence Intervals", confidence_intervals.app)
app.add_page("Visualizations", prediction_viz.app)
app.add_page("Rankings", ranking.app)
app.add_page("Error Analysis", error_analysis.app)

app.run()