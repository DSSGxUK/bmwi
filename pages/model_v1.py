import streamlit as st 
import pandas as pd 


# Custom modules
from util_classes.Forecaster import Forecaster
from .utils import *

def app(): 

    ''' Upload datasets in the German Kreis format @cinny'''

    # Upload all data files '''
    st.markdown("## Upload csv files for analysis.") 
    st.write("\n")
    # Read and save data
    data = read_single_file()
    data.to_csv('data/main_data.csv', index=False, encoding='latin_1')
    # Raw data display  
    st.dataframe(data)
    # Show data statistics 
    st.write("**Data Size:**", data.shape)

    ''' Clean using the cleaner class and merge the data and get final dataset @cinny'''
    # Implemented on data_prep.py page
    
    ''' Do a SARIMAX Training and get the error value @prakhar '''
    # Set the config for the models
    config = [(1, 1, 2), (1, 0, 2, 12), 't']

    # Unemployment Data from 2010 to 2019
    file_location = 'data/data_from_2010_to_2019_unemployment_rate.csv'

    # Create a forecaster instance
    st.write("Fitting 401 models. Estimated time: 7 minutes...")
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def load_forecaster(file_location, config):
        return Forecaster(file_location, config, verbose=True, train=True)

    forecaster = load_forecaster(file_location, config)

    st.write("Model Fitting Complete...")
    
    st.header("Predictions for the next three months!")

    # Get the prediction data
    NUM_PREDICTIONS = 3
    pred_df = forecaster.get_predictions_df(NUM_PREDICTIONS)

    # Get the combined predictions 
    combined_df = forecaster.get_predictions_df_appended(NUM_PREDICTIONS)
    combined_df = combined_df.loc[:,~combined_df.columns.duplicated()] # drop duplicated ags5 column

    st.write("There are two output formats:")

    st.write("1. This is 'predictions only' format.")
    df_index = pd.read_csv('data/index.csv')
    df_index['ags5'] = df_index['ags5'].apply(fix_ags5)
    pred_df_pro = pd.merge(df_index, pred_df, left_on='ags5', right_on='ags5')
    st.markdown('**Pro tip**: sort by prediction results to quickly see which kreis may need most help.')
    st.dataframe(pred_df_pro)

    st.write("2. This is combined format.")
    st.dataframe(combined_df)
    combined_df_pro = pd.merge(df_index, combined_df, left_on='ags5', right_on='ags5')
    combined_df_pro.to_csv('data/combined_df_pro.csv', index=False)

    # Download links 
    st.markdown(get_table_download_link(pred_df, 
                                        text="Download predictions only.", 
                                        filename="predictions.csv"), unsafe_allow_html=True)
    st.markdown(get_table_download_link(combined_df, 
                                        text="Download combined data.", 
                                        filename="combined_predictions.csv"), unsafe_allow_html=True)

    ''' Add visulaisations of the unemployment predictions @cinny '''
    st.markdown("## Visualize prediction results.") 
    st.write("\n")

    # get predictions by kreis 
    kreis_code = st.multiselect("Select the Kreis to get predictions", options=list(pred_df['ags5'].values))
    st.dataframe(pred_df[pred_df['ags5'].isin(kreis_code)])

    # line plot
    fig1 = plot_line_wide(combined_df, kreis_code, NUM_PREDICTIONS)
    st.pyplot(fig1)

    # map
    st.markdown("### Map")
    map_fig = plot_map_wide(combined_df, 'ags5')
    st.pyplot(map_fig)
