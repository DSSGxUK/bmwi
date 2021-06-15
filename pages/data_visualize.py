# Import necessary libraries 
import pandas as pd 
import streamlit as st 
import base64


# Create the app that would be run 
def app():

    # Add the title
    st.title("Data Visualisation")

    # Load the data 
    data = pd.read_csv('data/main_data.csv', encoding='latin_1')

    ''' Select Display Parameters '''
    # col1, col2 = st.co
    