# Import libraries 
from os import read
import pandas as pd 
import streamlit as st 

# Custom modules 
from .utils import *
from .CleanerClass import CleanerClass

''' App to merge the data sets together'''
def app():

    st.markdown("## Merge and export datasets")

    # Upload multiple csv files
    multi_csv = st.radio("Upload multiple csv files.", options=["Yes", "No"], index=1,
        help='Every csv file should have the column "ags5" containing unique code for each Kreis.')
    
    if multi_csv == "Yes": 
        st.markdown("### Merging multiple csv files.")
        
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
        st.markdown("### Exporting excel worksheets.")

        # Read in excel workbook
        uploaded_file = st.file_uploader("Upload Excel Workbook", type="xlsx")
        cleanerObject = CleanerClass(uploaded_file)

        # Print useful worksheets
        # (1) wide format
        st.markdown("#### Useful Worksheets in Wide Format")
        for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_wide().items():
            st.write(sheet_name, sheet_data.shape, \
                get_table_download_link(sheet_data, text="download csv", \
                    filename=f"{sheet_name.replace(' ', '_')}_wide.csv"), unsafe_allow_html=True)
        
        # (2) long format
        st.markdown("#### Useful Worksheets in Long Format")
        for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_long().items():
            st.write(sheet_name, sheet_data.shape, \
                get_table_download_link(sheet_data, text="download csv", \
                    filename=f"{sheet_name.replace(' ', '_')}_long.csv"), unsafe_allow_html=True)
        
        # ** manually get unemployment rate sheet and load it in final_page
        cleanerObject.getAllUsefulSheets_wide()['Alo Quote'].to_csv('data/AloQuote_wide.csv', index=False)
        cleanerObject.getAllUsefulSheets_long()['Alo Quote'].to_csv('data/AloQuote_long.csv', index=False)


    # Data to pass on to final_page_v1
    st.markdown("## Final dataset cleaning")

    crop_data = st.radio("Crop time-series data", options=["Yes", "No"], index=1,
        help='Crop the time-series data to the appropriate timeframe for model prediction.')
    
    if crop_data == "Yes":
        data = read_single_file()
        # Raw data display  
        st.dataframe(data)
        # Show data statistics 
        st.write("**Data Size:**", data.shape)

        # get default values
        data_cols = list(data.columns)
        min_date_i = data_cols.index(min(data_cols))
        max_date_i = data_cols.index(max(data_cols))
        # get input values
        start_date = st.selectbox("Select start date", options=data_cols, index=min_date_i)
        end_date = st.selectbox("Select end date", options=data_cols[min_date_i:], index=max_date_i)
        start_date_i = data_cols.index(start_date)
        end_date_i = data_cols.index(end_date)
        # crop dataframe
        cropped_data = data[data.columns[start_date_i:end_date_i+1]]
        # Raw data display  
        st.dataframe(cropped_data)
        # Show data statistics 
        st.write("**Data Size:**", cropped_data.shape)
        confirm_crop_data = st.radio("Confirm new timeframe", options=["Yes", "No"], index=1,
            help='Crop the time-series data to the appropriate timeframe for model prediction.')
        if confirm_crop_data == "Yes":
            st.write("Last used data now updated to the cropped data.")
            cropped_data.to_csv('data/main_data.csv', index=False, encoding='latin_1')
            st.write(get_table_download_link(cropped_data, text="download csv", \
                filename=f"cropped_data.csv"), unsafe_allow_html=True)