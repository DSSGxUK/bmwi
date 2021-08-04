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
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Export and merge datasets](#exporting-excel-worksheets)
    - [Dataset Cleaning](#dataset-cleaning)
        - [Cropping Timeframe](#cropping-timeframe)

    """)

    st.markdown("## Export and merge datasets")
    st.write("""
        Upload the dataset and make any necessary changes to fit the prediction model.
        This section processes the input excel workbook for time-series or structural data type.
    """)

    ## --------- Upload an excel workbook with multiple worksheets
    st.markdown("### Exporting excel worksheets.")
    # time_series = st.checkbox("Upload time series data?", 
    #                             value=False, 
    #                             help="This excel workbook may contain one or multiple worksheets.")
    
    # if time_series:
        
    st.markdown("**Pro Tip**: If you are encountering problems, try clearing cache and run again.")

    # Read in excel workbook
    uploaded_file = st.file_uploader("Upload Excel Workbook", type="xlsx")
    st.write("""**Note**: It takes roughly 5 minutes to load the data. 
    If you see a `Running` statement on the top right, then everything is working fine. Please wait while the data loads. """)
    
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
    # select_cleaner = st.selectbox("Select data to clean.", options=['Unemployment rate', 'GDP'], index=0,
    # select_cleaner = st.selectbox("Select data to clean.", options=['Unemployment rate'], index=0,
    #                                 help='Refer to documentation for details about input excel workbook format.')
    select_cleaner = 'Unemployment rate'
    
    try:
        # cleanerObject = load_cleanerObject(uploaded_file, data=select_cleaner)
        cleanerObject = load_cleanerObject(uploaded_file, data=select_cleaner)
        sheet_names = [sheet_name for sheet_name, _ in cleanerObject.getAllUsefulSheets_long().items()]
        alq = sheet_names.index('Alo Quote')
    
    except ValueError:
        st.write("**Please upload a dataset.**")

        # st.markdown('A sample of the data format can be found \
        #             [here](https://cinnylin.github.io/bmwi-docs/steps/data_prep/#time-series-data-excel-workbook) \
        #             and is automatically loaded by default.')
        
        # cleanerObject = CleanerClassUR('data/7444_318010_BMWI_Enkelmann_Eckdaten_Zeitreihe_Kreise.xlsx')
    
    try: 
        select_var = st.selectbox("Select the one variable you want to feed in the model.", options=sheet_names, index=alq,
                                    help='Refer to documentation for details about merging best practices.')
        
        # (2) Select wide or long format
        select_format = st.selectbox("Select export data format.", options=['long', 'wide'], index=1,
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
    
        confirm_merge_data = st.radio("Save dataframe", options=["Yes", "No"], index=1,
                                        help='Preview and confirm data brings you to timeframe cropping section of data prepartion.')
        
        if confirm_merge_data == 'Yes':
            st.markdown('Last used data is now updated to the selected data. \
                    Proceed to the **"Final Dataset Cleaning"** section below if you want to crop the timeframe. \
                    Alternatively, you could directly proceed to the **"Model"** page and proceed with \
                    unemployment rate prediction.')
            # formatting
            merged_df.reset_index(inplace=True)
            merged_df['index'] = merged_df['index'].apply(fix_ags5)
            merged_df.set_index('index', inplace=True)
            # export data
            merged_df.to_csv('data/main_data.csv', index=True, encoding='latin_1')
            # merged_df.to_csv('data/main_data.csv', index=False, encoding='latin_1')
        
    
        st.markdown("""---""")
        
        ## -------- Data to pass on to final_page_v1
        st.markdown("## Dataset cleaning")
        st.write('Data cleaning such as restricting to a certain timeframe, checking for missing values in the dataset etc.')
        
        clean_data = st.radio("Cleaning time-series data", options=["Yes", "No"], index=1,
            help='Crop the time-series data to the appropriate timeframe for model prediction.')
        
        if clean_data == "Yes":
            
            upload_data = st.radio("Upload new data", options=["Yes", "No"], index=1)
            if upload_data == "Yes":
                data = read_single_file()
            else:
                data = pd.read_csv('data/main_data.csv', index_col=0)
                # data.set_index('Unnamed: 0', inplace=True)
            
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
                st.markdown('Last used data is now updated to the cropped data. \
                        You can move on to the **"Model page"** to proceed with data prediction.')
                cropped_data.reset_index(inplace=True)
                cropped_data['index'] = cropped_data['index'].apply(fix_ags5)
                cropped_data.set_index('index', inplace=True)
                cropped_data.to_csv('data/main_data.csv', index=True, encoding='latin_1')
                st.write(get_table_download_link(cropped_data, text="Download cropped data in excel", \
                    filename=f"cropped_data", excel=True), unsafe_allow_html=True)
    except: 
        pass