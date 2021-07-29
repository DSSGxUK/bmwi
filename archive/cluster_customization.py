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
    data['cluster'] = data['cluster'].astype(str)
    clusters = sorted(list(data['cluster'].unique()))
    cluster_dict = {}

    ### bug: one kreis could be in multiple clusters but would only be reflected on the first one assigned
    for i in clusters:
        cluster_list = st.multiselect(label=f"Which kreis are in cluster {i}?", 
                        options=list(data['kreis_options']),
                        default=list(data[data['cluster']==i]['kreis_options']) )
                        #help="If not is selected, the variable will be treated as numerical.")
        cluster_dict[i]=cluster_list

    def assign_cluster(x):
        for i in cluster_dict.keys():
            if x in cluster_dict[i]:
                return i
    data['cluster'] = data['kreis_options'].apply(assign_cluster)
    
    ''' Cluster Visualisation '''
    button_run = st.radio("Cluster visualization", options=["Yes", "No"], index=1)
    if button_run == "Yes": 
        st.subheader("Cluster Map")
        data['ags5_fix'] = data['ags5'].apply(fix_ags5)
        fig = plot_map(data, 'ags5_fix', 'cluster', cat_col=True)
        st.pyplot(fig)
    
    # export customized clusters
    df_cluster = data[['ags5', 'kreis', 'cluster']]
    st.markdown(get_table_download_link(df_cluster, text="Download Cluster Results"), unsafe_allow_html=True)
