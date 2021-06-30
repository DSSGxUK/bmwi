# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

import streamlit as st 
from pathlib import Path
from functools import reduce


# Custom modules 
from .utils import *

# Define the app 
def app():

    st.header("Cluster Result Customization")

    # Read the data file with 401 and rows and n columns
    data = pd.read_csv('data/cluster_km.csv', encoding='latin_1')
    #st.write("Uploaded dataset size:", data.shape)

    data['kreis_options'] = data['ags5'].astype(str)+' '+data['kreis']
    clusters = sorted(list(data['cluster'].unique()))

    for i in clusters:
        st.multiselect(label=f"Which kreis are in cluster {i}?", 
            options=list(data['kreis_options']),
            default=list(data[data['cluster']==int(i)]['kreis_options']) )
            #help="If not is selected, the variable will be treated as numerical.")
    
    # export customized clusters
    # df_cluster = data[['ags5', 'kreis', 'km_cluster']]
    # st.markdown(get_table_download_link(df_cluster, text="Download Cluster Results"), unsafe_allow_html=True)

    ''' Cluster Visualisation '''
    ### this needs to be based on customized cluster results
    button_run = st.radio("Cluster visualization", options=["Yes", "No"], index=1)
    if button_run == "Yes": 
        st.subheader("Cluster Map")
        data['ags5_fix'] = data['ags5'].apply(fix_ags5)
        fig = data_map(data, 'ags5_fix', 'cluster', cat_col=True)
        st.pyplot(fig)