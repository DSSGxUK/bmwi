# Import libraries 
import pandas as pd 
import streamlit as st 

# Custom modules 
from .utils import *
from .CleanerClass import CleanerClass

''' App to merge the data sets together'''
def app():

    # Upload multiple csv files
    multi_csv = st.radio("Upload multiple csv files.", options=["Yes", "No"], index=1,
        help='Every csv file should have the column "ags5" containing unique code for each Kreis.')
    
    if multi_csv == "Yes": 
        st.markdown("## Merging multiple csv files.")
        
        # Read all the files 
        uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)
        
        if uploaded_files:
            st.write(f"{len(uploaded_files)} files found in the data")
            data = pd.read_csv(uploaded_files[0])
            
            # Iterate through the uploaded files 
            for file in uploaded_files[1:]:
                new_data = pd.read_csv(file)
                # Merge the data 
                data = pd.merge(new_data, data, on='ags5')
            st.write(f"The combined dataset is of the size {data.shape}")
            
            # Save data
            data.to_csv('data/main_data.csv', index=False, encoding='latin_1')
            
            # Publish the combined df using the function from utils
            st.markdown(get_table_download_link(data, text="Download Combined CSV"), unsafe_allow_html=True)
    

    # Upload an excel workbook with multiple worksheets
    excel_workbook = st.radio("Upload an excel workbook.", options=["Yes", "No"], index=1,
        help='This excel workbook may contain one or multiple worksheets.')
    
    if excel_workbook == "Yes":
        st.markdown("## Exporting excel worksheets.")

        # Read in excel workbook
        uploaded_file = st.file_uploader("Upload Excel Workbook", type="xlsx")
        cleanerObject = CleanerClass(uploaded_file)

        # Print useful worksheets
        # (1) wide format
        st.markdown("### Useful Worksheets in Wide Format")
        for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_wide().items():
            st.markdown(get_table_download_link(sheet_data, 
                text=f"Download {sheet_name.replace(' ', '_')}.csv in wide format"), unsafe_allow_html=True)
            st.write(sheet_name, sheet_data.shape)
        # (2) long format
        st.markdown("### Useful Worksheets in Long Format")
        for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_long().items():
            st.markdown(get_table_download_link(sheet_data, 
                text=f"Download {sheet_name.replace(' ', '_')}.csv in long format"), unsafe_allow_html=True)
            st.write(sheet_name, sheet_data.shape)
        