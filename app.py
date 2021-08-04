import os
from typing import final
import streamlit as st
import numpy as np

# Custom imports 
from multipage import MultiPage

# import your pages here
from pages import model_page, data_prep, home_page, error_analysis, prediction_viz, ranking

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("BMWi Tool")
st.markdown('[Documentation](https://cinnylin.github.io/bmwi-docs/)')

# The main app
app.add_page("Home Page", home_page.app)
app.add_page("Data Prep", data_prep.app)
app.add_page("Predictions Page", model_page.app)
app.add_page("Visualization Page", prediction_viz.app)
app.add_page("Ranking Page", ranking.app)
app.add_page("Error Analysis", error_analysis.app)

app.run()