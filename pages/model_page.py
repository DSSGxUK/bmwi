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

    # st.markdown('''
    # <link
    #   rel="stylesheet"
    #   href="https://use.fontawesome.com/releases/v5.13.0/css/all.css"
    #   integrity="sha384-Bfad6CLCknfcloXFOyFnlgtENryhrpZCe29RTifKEixXQZ38WheV+i/6YWSzkz3V"
    #   crossorigin="anonymous"
    # />

    # ## <i class="fas fa-book"></i> Model Output Page 
    # ''', 
    
    # unsafe_allow_html=True)

    st.subheader("This page will output the predictions for the next three months.")

    # st.write("**Note: Add a flowchart or something here if needed. Looks a bit empty.**")

    ''' Read the Data and set it in the appropriate format '''
    # wide_df = pd.read_csv('data/Alo_Quote.csv')
    wide_df = pd.read_csv('data/main_data.csv')
    wide_df.columns = ['ags5'] + list(wide_df.columns[1:])
    wide_df.set_index('ags5', inplace=True)

    st.write("Loading the data...")
    
    # Create an instance of the Data Class which returns the long format of the data 
    unemploymentRateData = Data(wide_df, 'wide')    # Set the current format of the data as wide to be read properly

    ''' Set the ouput and model params (can be taken externally at a later stage) and prepare the data'''
    output_save_location = 'data/predictions/VAR/output.csv'
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

    ''' Model Fitting and Predictions '''
    # @st.cache
    # def load_model():
    #     return VARModel(output_save_location, params, unemploymentRateData, cluster_df)
    
    # VARObject = load_model()
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
    st.dataframe(pred_output)

    # Reset the prediction index 
    pred_output.reset_index(inplace=True)

    # Download links 
    st.markdown(get_table_download_link(pred_output, 
                                        text="Download the predictions.", 
                                        filename="predictions.csv", 
                                        excel=True),

                                        unsafe_allow_html=True)

    ''' Error Data Collection '''
    error_df = VARObject.getWalkForwardErrors()

    # Calcululate MAPE errors 
    error_df['mape'] = np.abs(error_df['ground_truth'] - error_df['pred'])/error_df['ground_truth']

    # Save the error df
    error_df.to_csv('data/errors/errors_VAR.csv', index=False)
    st.write("Saved the errors...")

    ''' Add visulaisations of the unemployment predictions '''
    
    # Read the index data 
    index_data = pd.read_csv('data/index.csv')

    # Fix ags5
    viz_data = pred_output.copy()
    viz_data['ags5'] = viz_data['ags5'].apply(fix_ags5)
    index_data['ags5'] = index_data['ags5'].apply(fix_ags5)
    
    # Merge with the output data 
    full_data = pd.merge(wide_df.reset_index().rename(columns={'index': 'ags5'}), viz_data, on='ags5')
    full_data = pd.merge(index_data, full_data, on='ags5')
    
    # Sync with home page
    full_data.to_csv('data/pred_output_full.csv', index=False)

    st.markdown("## Visualize prediction results.") 
    st.write("\n")

    # get predictions by kreis 
    display_data = pd.merge(index_data, viz_data, on='ags5')
    kreis_name = st.multiselect("Select the Kreis to get predictions", options=list(display_data['kreis'].values))
    st.dataframe(display_data[display_data['kreis'].isin(kreis_name)].drop(columns=['ags2', 'ags5']))

    """
    This section doesn't work well because the date columns are messed up and we need to fix that.  
    """

    # line plot
    fig1 = plot_line_wide(full_data.drop(columns=['ags5']), kreis_name, 3, df_index='kreis')
    st.pyplot(fig1)

    # map
    st.markdown("### Map")

    # Add the average of the predictions as a column for the plots 
    average_cols = pd.DataFrame(pred_output.mean(axis=1))
    average_cols.columns = ['predictions_average']
    full_data = pd.concat([full_data, average_cols], axis=1)

    print

    map_fig = plot_map_wide(full_data, 'ags5') # MAP gives error 
    st.pyplot(map_fig)
