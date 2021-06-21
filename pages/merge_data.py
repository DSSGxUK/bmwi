# Import libraries 
import pandas as pd 
import streamlit as st 

# Custom modules 
from .utils import *

''' App to merge the data sets together'''
def app():

    st.write("Upload multiple csv files.")

    # Read all the files 
    uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)
    if uploaded_files:

        st.write(f"Files found in the data: {len(uploaded_files)}")
        data = pd.read_csv(uploaded_files[0])

        # Iterate through the uploaded files 
        for file in uploaded_files[1:]:
            new_data = pd.read_csv(file)

            # Merge the data 
            data = pd.merge(new_data, data, on='ags5')

        st.write(f"The combined dataset is of the size {data.shape}")

        # Publish the combined df using the function from utils
        st.markdown(get_table_download_link(data, text="Download Combined CSV"), unsafe_allow_html=True)
