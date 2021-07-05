import streamlit as st 
import pandas as pd 
from .utils import *

def app(): 
    pass 

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

    ''' Do a SARIMAX Training and get the error value @prakhar '''

    ''' Make the predictions @prakhar'''

    ''' Add the predictions to the merged data / or give prediction output for each kreis in excel @prakhar'''


    ''' Add visulaisations of the unemployment predictions @cinny '''
    st.markdown("## Visualize prediction results.") 
    st.write("\n")
    data_cols = data.columns
    # set default values: x=date, y=unemployment_rate, filter=None
    alq_i = list(data.columns).index('unemployment_rate')
    date_i = list(data.columns).index('date')
    # set visualization options
    x_col = st.selectbox("Select x-axis", options=list(data_cols), index=date_i)
    y_col = st.selectbox("Select y-axis", options=list(data_cols), index=alq_i)
    fig1 = plot_line(data, x_col, y_col)
    # show plot
    st.pyplot(fig1)
    
    # filtered
    # set default values: filter=ags5
    ags5_i = list(data.columns).index('ags5')
    # set visualization options
    filter_col = st.selectbox("Select filter column", options=list(data_cols), index=ags5_i)
    filter_val = st.selectbox("Select filter value", options=list(data[filter_col].unique()), index=0)
    fig2 = plot_line(data, x_col, y_col, filter_col=filter_col, filter_val=filter_val)
    # show plot
    st.pyplot(fig2)

    # map
    st.write("Map")
    # set default value
    recent_date_i = list(data['date'].unique()).index(max(data['date']))
    # set visualization options
    map_col = st.selectbox("Select column to visualize", options=list(data_cols), index=alq_i)
    date_val = st.selectbox("Select date to visualize", options=list(data['date'].unique()), index=recent_date_i)
    date_data = data[data['date']==date_val]
    map_fig = plot_map(date_data, 'ags5', map_col)
    st.pyplot(map_fig)
