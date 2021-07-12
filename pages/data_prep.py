# Import libraries 
from os import read, write
import pandas as pd 
import streamlit as st 

# Custom modules 
from .utils import *
from .CleanerClass import CleanerClass

''' App to merge the data sets together'''
def app():

    st.markdown("## Export and merge datasets")


    # Upload an excel workbook with multiple worksheets
    st.markdown("### Exporting excel worksheets.")
    time_series = st.radio("Time-series data.", options=["Yes", "No"], index=1,
        help='This excel workbook may contain one or multiple worksheets.')
    
    if time_series == "Yes":

        # Read in excel workbook
        uploaded_file = st.file_uploader("Upload Excel Workbook", type="xlsx")

        @st.cache(suppress_st_warning=True, allow_output_mutation=True)
        def load_cleanerObject():
            return CleanerClass(uploaded_file)
        
        cleanerObject = load_cleanerObject()

        # Print useful worksheets
        # (1) wide format
        st.markdown("#### Useful Worksheets in Wide Format")
        st.write('Pro tip: Here, each column is a date. \
            The shape of the format is 401 rows. \
            This format is suitable for univariate analysis.')
        for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_wide().items():
            st.write(f'{sheet_name}_wide', sheet_data.shape, \
                get_table_download_link(sheet_data, text="download csv", \
                    filename=f"{sheet_name.replace(' ', '_')}_wide.csv"), unsafe_allow_html=True)
        
        # (2) long format
        st.markdown("#### Useful Worksheets in Long Format")
        st.write('Pro tip: Here, all the dates are recorded in one column. \
            The shape of the format is (401 * range of dates) rows. \
            This format is suitable to merge multiple variables. \
            The merged file of multiple long format variable is the commonly known wide format data.')
        cleanerObject_long = cleanerObject.getAllUsefulSheets_long()
        for sheet_name, sheet_data in cleanerObject_long.items():
            st.write(f'{sheet_name}_long', sheet_data.shape, \
                get_table_download_link(sheet_data, text="download csv", \
                    filename=f"{sheet_name.replace(' ', '_')}_long.csv"), unsafe_allow_html=True)
        
        # (3) select long format files to merge
        st.markdown('#### Merge Useful Long Format Worksheets')
        df_final_long = pd.read_csv('data/df_final_date_wide_2007.csv')
        df_final_long = df_final_long.loc[:, ['ags2', 'ags5','date']]

        long_sheets = [sheet_name for sheet_name, sheet_data in cleanerObject_long.items()]
        selected_long_sheets = st.multiselect('Select variables to merge.', options=long_sheets)
        
        
        for sheet_name, sheet_data in cleanerObject_long.items():
            if sheet_name in selected_long_sheets:
                df_final_long = wide_merge(sheet_data, df_final_long, f'{sheet_name}')
        
        st.dataframe(df_final_long)

        confirm_merge_data = st.radio("Confirm new data", options=["Yes", "No"], index=1,
            help='Merge multiple long format files to one wide format for model prediction.')
        
        if confirm_merge_data == "Yes":
            st.write("Last used data now updated to the merged data.")
            df_final_long.to_csv('data/main_data.csv', index=False, encoding='latin_1')
            st.write(get_table_download_link(df_final_long, text="download csv", \
                filename=f"df_final_long.csv"), unsafe_allow_html=True)

        # ** manually get unemployment rate sheet and load it in final_page
        # cleanerObject.getAllUsefulSheets_wide()['Alo Quote'].to_csv('data/AloQuote_wide.csv', index=False)
        # cleanerObject.getAllUsefulSheets_long()['Alo Quote'].to_csv('data/AloQuote_long.csv', index=False)


    # Upload multiple csv files
    st.markdown("### Merging multiple csv files.")
    non_time_series = st.radio("Structural data.", options=["Yes", "No"], index=1,
        help='Structural data are non-time-series and contain 401 rows representing each kreis, and with "ags5" column.')
    
    if non_time_series == "Yes": 
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