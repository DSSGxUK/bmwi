# Import necessary libraries 
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
    
# from pandas._config.config import options 
import streamlit as st 
import base64


# Create the app that would be run 
def app():

    # Add the title
    st.title("Data Visualisation")

    # Load the data 
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:

        # Read the data 
        data = pd.read_csv('data/main_data.csv', encoding='latin_1')

        ''' Display a correlation matrix '''
        corr_matrix = st.checkbox("Do you want a correlation matrix?", value=False)
        if corr_matrix:
            pass 

        ''' Select Display Parameters '''
        col1, col2 = st.beta_columns(2)

        # Select the feature 
        feature = col1.selctbox("Select the feature you want to visualize.", options=list(data.columns), index=4)

        # Select the type of chart

        