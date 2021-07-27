# Import libraries 
from os import read, write
import pandas as pd 
import streamlit as st 
from datetime import datetime

# Custom modules 
from .utils import *
from util_classes.CleanerClassGDP import CleanerClassGDP
from util_classes.CleanerClassUR import CleanerClassUR
# from .CleanerClass import CleanerClass

''' App to merge the data sets together'''
def app():

    st.markdown("## Export and merge datasets")


    ## --------- Upload an excel workbook with multiple worksheets
    st.markdown("### Exporting excel worksheets.")
    time_series = st.radio("Time-series data.", options=["Yes", "No"], index=1,
        help='This excel workbook may contain one or multiple worksheets.')
    
    if time_series == "Yes":

        # Read in excel workbook
        uploaded_file = st.file_uploader("Upload Excel Workbook", type="xlsx")
        
        # cache cleaning results
        @st.cache(suppress_st_warning=True, allow_output_mutation=True)
        def load_cleanerObject(uploaded_file, data='Unemployment rate'):
            # get cleanerclass
            if data=='GDP':
                return CleanerClassGDP(uploaded_file)
            else:
                return CleanerClassUR(uploaded_file)
        

        # ------------------------------ Cleaner Class workflow -------------------
        # (0) Select cleanerclass
        st.markdown("**Pro Tip**: If you are encountering problems, try clearing cache and run again.")
        
        select_cleaner = st.selectbox("Select data to clean.", options=['Unemployment rate', 'GDP'], index=0,
                                        help='Refer to documentation for details about input excel workbook format.')
        cleanerObject = load_cleanerObject(uploaded_file, data=select_cleaner)
        sheet_names = [sheet_name for sheet_name, _ in cleanerObject.getAllUsefulSheets_long().items()]
        
        # # (1) Select the variables you want
        # select_var = st.multiselect("Select variables to merge data in the specified format.", options=sheet_names,
        #                             help='Refer to documentation for details about merging best practices.')
        # st.markdown('**Pro Tip**: One single wide format data is suitable for univariate analysis.\
        #             Multiple long format variable data merged together are known as the "wide format" data.')

        # (1) Select the variable you want
        select_var = st.selectbox("Select the one variable you want to feed in the model.", options=sheet_names,
                                    help='Refer to documentation for details about merging best practices.')
        
        # (2) Select wide or long format
        select_format = st.selectbox("Select export data format.", options=['long', 'wide'], index=0,
                                    help='Refer to documentation for details about input and output formats.')
        st.markdown('**Pro Tip**: Wide format is when each column is a date, and long format is when all dates are recorded in one column.')
        
        # get cleaned data
        if select_format=='long':
            for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_long().items():
                if sheet_name == select_var:
                    merged_df = sheet_data.rename(columns={'value': sheet_name})
                    # deal with monthly date values
                    if select_cleaner == 'Unemployment rate':
                        merged_df['date'] = pd.to_datetime(merged_df['date'])
                        merged_df['date'] = merged_df['date'].dt.date

        else: #select_format=='wide'
            for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_wide().items():
                if sheet_name == select_var:
                    merged_df = sheet_data
                    
                    # deal with monthly date values
                    #merged_df.columns = pd.to_datetime(merged_df.columns, format='%Y-%m-%d')
                    if select_cleaner == 'Unemployment rate':
                        date_list = merged_df.columns
                        datetime_list = pd.to_datetime(date_list)
                        date_only_list = []
                        for date in datetime_list:
                            date = datetime.strftime(date, '%Y-%m-%d')
                            date_only_list.append(date)
                        merged_df.columns = date_only_list
        
        st.write(merged_df)
        
        # # Merge files
        # if select_format=='long':
        #     # get selected sheet data
        #     select_data = []
        #     for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_long().items():
        #         if sheet_name in select_var:
        #             select_data.append(sheet_data)
        #     # merge function
        #     merged_df = long_merge_to_wide(select_data, select_var)
        
        # else: #select_format=='wide'
        #     # get selected sheet data
        #     select_data = []
        #     for sheet_name, sheet_data in cleanerObject.getAllUsefulSheets_wide().items():
        #         if sheet_name in select_var:
        #             select_data.append(sheet_data)
        #     # merge function
        #     merged_df = wide_merge_to_long(select_data, select_var)

        # st.write(merged_df)
        
        # Confirm merge and then saves to next section of this page to crop timeframe
        # confirm_merge_data = st.radio("Confirm merged dataframe", options=["Yes", "No"], index=1,
        #                                 help='Preview and confirm merged data brings you to timeframe cropping section of data prepartion.')
        confirm_merge_data = st.radio("Confirm dataframe", options=["Yes", "No"], index=1,
                                        help='Preview and confirm data brings you to timeframe cropping section of data prepartion.')
        
        if confirm_merge_data == 'Yes':
            merged_df.to_csv('data/merged_df.csv', index=False, encoding='latin_1')
        


    ## ------ Upload multiple csv files
    st.markdown("### Merging multiple csv files.")
    non_time_series = st.radio("Structural data.", options=["Yes", "No"], index=1,
        help='Structural data are non-time-series and contain 401 rows representing each kreis, and with "ags5" column.')
    
    if non_time_series == "Yes": 
        # Read all the files 
        uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)
        
        if uploaded_files:
            data = pd.read_csv(uploaded_files[0])
            
            # Iterate through the uploaded files 
            for file in uploaded_files[1:]:
                new_data = pd.read_csv(file)
                # Merge the data 
                data = pd.merge(new_data, data, on=['_id', 'ags2', 'ags5', 'bundesland', 'kreis'])
                data.drop(columns=['id', '_id', 'ags2', 'bundesland', 'kreis'], inplace=True)
            #st.write(f"The combined dataset is of the size {data.shape}")
            st.write(data)
            
            # Confirm merge and then saves to next section of this page to crop timeframe
            confirm_merge_data = st.radio("Confirm merged dataframe", options=["Yes", "No"], index=1,
                                            help='Preview and confirm merged data brings you to timeframe cropping section of data prepartion.')
            if confirm_merge_data == 'Yes':
                data.to_csv('data/merged_df.csv', index=False, encoding='latin_1')
            
            # Publish the combined df using the function from utils
            #st.markdown(get_table_download_link(data, text="Download Combined CSV"), unsafe_allow_html=True)


    ## -------- Data to pass on to final_page_v1
    st.markdown("## Final dataset cleaning")
    st.write('Data cleaning such as cropping to a certain dataframe, checking for NaN data etc.')
    
    clean_data = st.radio("Cleaning time-series data", options=["Yes", "No"], index=1,
        help='Crop the time-series data to the appropriate timeframe for model prediction.')
    
    if clean_data == "Yes":
        
        upload_data = st.radio("Upload new data", options=["Yes", "No"], index=1)
        if upload_data == "Yes":
            data = read_single_file()
        else:
            data = pd.read_csv('data/merged_df.csv')
        
        # Raw data display  
        st.dataframe(data)
        
        # Show data statistics 
        st.write("**Data Size:**", data.shape)
        
        # Crop timeframe
        st.markdown("## Cropping timeframe")
        st.write('Cropping the timeframe of the data is useful for the model to differentiate between normal and crisis time.')

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