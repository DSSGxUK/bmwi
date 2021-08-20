import streamlit as st

import os
from typing import final
import numpy as np

# Custom imports 
from multipage import MultiPage

# import your pages here
from pages import model_page, data_prep, home_page, error_analysis, prediction_viz, ranking

# Change the page name and icon 
st.set_page_config(page_title="BMWi Forecasting Tool", page_icon='📊')

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("BMWi Tool")
st.markdown('[Documentation](https://cinnylin.github.io/bmwi-docs/)&nbsp;&nbsp;&nbsp;[Feedback Form](https://forms.gle/ceXoDGGijXM1JoDr7)')
st.markdown('')

# The main app
app.add_page("Home", home_page.app)
app.add_page("Data Prep", data_prep.app)
app.add_page("Predictions", model_page.app)
app.add_page("Visualization", prediction_viz.app)
app.add_page("Ranking", ranking.app)
app.add_page("Error Analysis", error_analysis.app)

app.run()