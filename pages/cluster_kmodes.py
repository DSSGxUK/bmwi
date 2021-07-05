# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from kmodes.kmodes import KModes

import streamlit as st 
from pathlib import Path
from functools import reduce


# Custom modules 
from .utils import *

# Define the app 
def app():

    st.header("Cluster Analysis using KModes.")

    # Read the data file with 401 and rows and n columns
    data = read_single_file()

    st.write("Uploaded dataset size:", data.shape)

    # Select a subset of data columns
    X = data.drop(["cluster", "ags5", "kreis"], axis=1)

    ''' Variable and Method Selection '''
    X = drop_selected_variables(X)

    # Select categorical variables from data
    st.subheader("Select categorical variables")
    cat_cols = ['labor_market_region', 'growing_/_shrinking_circles',
            'labor_market_type', 'grw_funding_framework',
            'settlement_structure_type_of_labor_market_region',
            'room_type_location', 'district_settlement_structure',
            'type_of_settlement_structure', 'urban_/_rural',
            'metropolitan_region', 'metropolitan_area',
            'east_west', 'border_proximity',
            'support_area_status', 'eligible_area']
    #st.write("Default catergorical variables:", cat_cols)
    variables_to_be_categorical = st.multiselect(label="Which other variables are categorical?", 
                                options=list(X.columns),
                                #options=sorted(list(set(X.columns).difference(set(cat_cols)))),
                                default=cat_cols,
                                help="If not is selected, the variable will be treated as numerical.")

    ''' Clustering using k-modes '''
    st.subheader("K-Modes Clustering")
    num_clusters = st.slider("Select the number of clusters.", min_value=2, max_value=10, step=1, value=3, help="Suggested:not more than 4")

    button_run = st.radio("Run KModes Model", options=["Yes", "No"], index=1)
    if button_run == "Yes": 
    #if st.button("Run KModes Model"):
    
        # Model building and fitting
        km = KModes(n_clusters=num_clusters, init='Huang', n_init=5, verbose=1)
        km.fit_predict(X, categorical=cat_cols+variables_to_be_categorical)
        data['cluster'] = km.labels_
        data['cluster'] = data['cluster'].astype(str)

        # Print the cluster sizes
        st.write("The following are the cluster sizes:")
        st.write(list(data['cluster'].value_counts().sort_index()))
        
        # Print the cluster information
        for i in range(num_clusters):
            st.write(f"Cluster {i}:", data[data['cluster']==str(i)]['kreis'].to_list())


        ''' Cluster Visualisation '''
        st.subheader("Cluster Map")
        data['ags5_fix'] = data['ags5'].apply(fix_ags5)
        fig = plot_map(data, 'ags5_fix', 'cluster', cat_col=True)
        # show plot
        st.pyplot(fig)

        # export df with clusters using the function from utils
        df_cluster = data[['cluster', 'ags5', 'kreis']]
        df_cluster.to_csv('data/cluster_km.csv', index=False)
        st.markdown(get_table_download_link(df_cluster, text="Download Cluster Results"), unsafe_allow_html=True)


