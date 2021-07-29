# Import necesary libraries 
from numpy.core.fromnumeric import size
import pandas as pd
from pandas._config.config import options 
import streamlit as st 
import numpy as np 

# Custom modules 
from .utils import *

# Define the page app 
def app(): 
    
    ''' Load the data and show descriptive statics '''
    data = read_single_file()

    st.write("Basic Data Statistics like mean, median and percentiles.")
    st.dataframe(data.describe())

    ''' Section to select the kreis by variable and percentile'''
    
    st.write("""
        In this section, you can select a variable and a percentile value 
        which will return all the kreis above or below that level.
    """)

    col1, col2 = st.beta_columns(2)
    # Set a dropdown for variables and checklist for upper or lower 
    feature = col1.selectbox("Select the variable", options=list(data.columns))
    level = st.radio("Select whether you want to return the Kreis above the threshold or below", options=["Above", "Below"])
    
    threshold = col2.slider("Select the percentile Threshold", min_value=0.01, max_value=1.0, step=0.01)
    
    # Filter the data 
    if level == "Above":
        filter_data = data[data[feature] > data[feature].quantile(threshold)]
    
    else: 
        filter_data = data[data[feature] < data[feature].quantile(threshold)]
    
    # Return the list 
    st.write(list(filter_data['kreis'].unique()))
    
    
