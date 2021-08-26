from numpy.lib.function_base import average
import streamlit as st 
import pandas as pd 
import numpy as np 
from datetime import datetime
from dateutil import relativedelta

# Custom modules
from util_classes.VAR_model import Data, VARModel
from .utils import fix_ags5, get_table_download_link, plot_line_wide, plot_map_wide

def app(): 

    st.markdown("## Model Output Page")
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Prediction Results](#prediction-results)
    """)

    st.write("This page will output the predictions for the next three months.")

    # st.write("**Note: Add a flowchart or something here if needed. Looks a bit empty.**")

    st.markdown('### Prediction Results')
    ''' Read the Data and set it in the appropriate format '''
    wide_df = pd.read_csv('data/main_data.csv')
    wide_df.columns = ['ags5'] + list(wide_df.columns[1:])
    wide_df.set_index('ags5', inplace=True)

    # st.write("Loading the data...")
    
    # Create an instance of the Data Class which returns the long format of the data 
    unemploymentRateData = Data(wide_df, 'wide')    # Set the current format of the data as wide to be read properly

    ''' Set the ouput and model params (can be taken externally at a later stage) and prepare the data'''
    output_save_location = 'data/output.csv'
    params = {
        'lag_value': 9, 
        'second_diff': False,
        'start_date': '2007-05-01' # there are null values before this
    }

    # NOTEE: A lot of these values can be read from a config file and saved inside the params 

    # Read the cluster data 
    cluster_data = pd.read_csv('data/cluster_data.csv')
    cluster_data['ags5'] = cluster_data['ags5'].apply(fix_ags5)
    
    # Set the cluster to use and the columns to map
    CLUSTER_TO_USE = 'PCA_Cluster'
    cluster_df = cluster_data[['ags5', CLUSTER_TO_USE]]
    cluster_df.columns = ['ags5', 'cluster']

    st.write("Fitting Model Predictions...")
    st.write("Estimated prediction time: 2 minutes...")

    ''' Model Fitting and Predictions '''
    VARObject = VARModel(output_save_location, params, unemploymentRateData, cluster_df)

    # Get model predictions 
    pred_output = VARObject.getWalkForwardPred_3Months()

    # Set the ags5 as index 
    pred_output.set_index('ags5', inplace=True)

    '''fix date format '''

    # (1) get next n dates
    last_date_str = unemploymentRateData.wide().columns[-1]
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    datetime_list = []
    n = len(pred_output.columns)
    for _ in range(n):
        next_date = last_date + relativedelta.relativedelta(months=1)
        last_date = next_date
        datetime_list.append(next_date)
    # (2) fix date to only show date and not time
    date_only_list = []
    for date in datetime_list:
        date = datetime.strftime(date, '%Y-%m-%d')
        date_only_list.append(date)
    pred_output.columns = date_only_list 

    # Display the dataframe  
    df_index = pd.read_csv('data/index.csv')
    df_index.drop(columns=['ags2'], inplace=True)
    df_index['ags5'] = df_index['ags5'].apply(fix_ags5)
    df_pred = pred_output.reset_index()
    df_pred.rename(columns={'index': 'ags5'})
    df_display = pd.merge(df_index, df_pred, on='ags5')
    df_display.set_index('ags5', inplace=True)  
    st.dataframe(df_display.style.format({
            date_only_list[0]: '{:.1f}', 
            date_only_list[1]: '{:.1f}', 
            date_only_list[2]: '{:.1f}'
            }))

    pred_output.to_csv('data/prediction_output_from_model_page.csv', index=True)

    # Reset the prediction index 
    pred_output.reset_index(inplace=True)

    # Download links 
    st.markdown(get_table_download_link(df_display, 
                                        text="Download the predictions.", 
                                        filename="predictions.csv", 
                                        excel=True),

                                        unsafe_allow_html=True)

    ''' Get aggregate data '''
    st.markdown("### Aggregate Predictions")
    st.write('Aggregated predictions on Bundesland level and for the whole country.')
    agg_output = VARObject.getWalfForwardAgg(3)
    agg_output.columns = ['ags2'] + date_only_list 
    # Save the last row 
    last_row = agg_output.iloc[agg_output.shape[0]-1]

    # merge with index data 
    df_index['ags2'] = df_index['ags5'].apply(lambda x: x[:2])
    df_index_bundesland = df_index.drop_duplicates(subset=['ags2', 'bundesland'])
    agg_output = pd.merge(df_index_bundesland[['ags2', 'bundesland']], agg_output, how='inner')
    agg_output.drop(['ags2'], axis=1, inplace=True)

    # add the last row 
    last_row = last_row.reindex(['bundesland']+date_only_list)
    last_row['bundesland'] = 'Germany'    
    agg_output = agg_output.append(last_row)
    st.dataframe(agg_output.style.format({
            date_only_list[0]: '{:.1f}', 
            date_only_list[1]: '{:.1f}', 
            date_only_list[2]: '{:.1f}'
            }))

    # Download links 
    st.markdown(get_table_download_link(agg_output, 
                                        text="Download the aggregate predictions.", 
                                        filename="aggregate_predictions.csv", 
                                        excel=True),
                                        unsafe_allow_html=True)

    ''' Error Data Collection '''
    error_df = VARObject.getWalkForwardErrors()

    # Calcululate MAPE errors 
    error_df['mape'] = np.abs(error_df['ground_truth'] - error_df['pred'])/error_df['ground_truth']

    # Save the error df
    error_df.to_csv('data/errors/errors_VAR.csv', index=False)
    st.write("Saved the errors...")
    
    st.markdown('Go to **Visualization** page and **Ranking** page for interpretation of the predictions.\
                Check out **Confidence Intervals** \
                and **Error Analysis** page for prediction validation.')

    