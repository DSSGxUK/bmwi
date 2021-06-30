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
    #X = data.drop(["ags2", "ags5", "kreis"], axis=1)
    X = data.drop(["cluster", "ags5", "kreis"], axis=1)

    ''' Variable and Method Selection '''
    # # Drop variables from data
    # st.subheader("Select non-important variables")
    # variables_to_be_dropped = st.multiselect(label="Which variables would you like to drop?", 
    #                                          options=list(X.columns), 
    #                                          help="If none is selected, then all variables will be used for PCA.")
    # if variables_to_be_dropped:
    #     X.drop(variables_to_be_dropped, axis=1, inplace=True)

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
    clusters = list(range(num_clusters))

    button_run = st.radio("Run KModes Model", options=["Yes", "No"], index=1)
    if button_run == "Yes": 
    #if st.button("Run KModes Model"):
    
        # Model building and fitting
        km = KModes(n_clusters=num_clusters, init='Huang', n_init=5, verbose=1)
        km.fit_predict(X, categorical=cat_cols+variables_to_be_categorical)
        data['cluster'] = km.labels_

        # Print the cluster sizes
        st.write("The following are the cluster sizes:")
        st.write(list(data['cluster'].value_counts().sort_index()))
        
        # Print the cluster information
        for i in range(num_clusters):
            st.write(f"Cluster {i}:", data[data['cluster']==i]['kreis'].to_list())


        ''' Cluster Visualisation '''

        ''' 
            def generate_cluster_map(data): 
                returns fig 
        '''
        st.subheader("Cluster Map")

        #if st.button("Visualize cluster in map"):
        # Plot result in map
        data['ags5_fix'] = data['ags5'].apply(fix_ags5)

        # Read the map coordinates data 
        gdf = gpd.read_file('georef-germany-kreis/georef-germany-kreis-millesime.shp')

        # Merge the coords with the data 
        merged = pd.merge(data, gdf, left_on='ags5_fix', right_on='krs_code')
        
        # Get the geospatial data 
        merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
        merged['coords'] = [coords[0] for coords in merged['coords']]
        merged['longitude'] = merged['coords'].str[0]
        merged['latitude'] = merged['coords'].str[1]

        # Convert to geodata
        merged = gpd.GeoDataFrame(merged)

        # Check if the labels need to be added 
        labels = st.radio("Show all labels?", options=["Yes", "No"], index=1)

        # Check if certain labels need to be added -- by region
        label_ags = st.radio("Show labels by region?", options=["Yes", "No"], index=1)
        if label_ags == "Yes": 
            bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
                '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
                '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
                '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
            txt_to_display_ags = st.selectbox("Select which Bundesland to annotate",
                                        options=bundeslands, index=0)
        
        # Check if certain labels need to be added -- by cluster
        label_cls = st.radio("Show labels by clusters?", options=["Yes", "No"], index=1)
        if label_cls == "Yes": 
            txt_to_display_cls = st.selectbox("Select which cluster group to annotate",
                                        options=clusters, index=0)

        # plot
        col_to_display = 'cluster'
        fig, ax = plt.subplots(figsize=(50,30))
        merged.plot(column=col_to_display, #scheme="NaturalBreaks",
                    #scheme='UserDefined', classification_kwds={'bins':clusters},
                    ax=ax, cmap='viridis', categorical=True, legend=True)
        ax.set_title(f'{col_to_display} in Germany by County', fontsize=15)

        # annotation filters
        # (1) by ags
        if label_ags == "Yes": 
            merged_ags = merged[merged['ags2']==int(txt_to_display_ags[:2])]
            for i in merged_ags.index:
                ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
                        f'{merged_ags["kreis"][i]}\n{merged_ags[col_to_display][i]}', fontsize=10)
        # (2) by cluster
        if label_cls == "Yes": 
            merged_cls = merged[merged['cluster']==int(txt_to_display_cls)]
            for i in merged_cls.index:
                ax.text(merged_cls.longitude[i], merged_cls.latitude[i],
                        f'{merged_cls["kreis"][i]}\n{merged_cls[col_to_display][i]}', fontsize=10)
        # add all text
        if labels == "Yes": 
            for i in range(len(merged)):
                ax.text(merged.longitude[i], merged.latitude[i],
                        f'{merged["kreis"][i]}\n{merged[col_to_display][i]}', fontsize=10)
        
        st.pyplot(fig)

        # export df with clusters using the function from utils
        df_cluster = data[['ags5', 'cluster']]
        st.markdown(get_table_download_link(df_cluster, text="Download Cluster Results"), unsafe_allow_html=True)

        ''' 
            1. Save df_cluster (df_cluster.to_csv('data/cluster_file.csv', index=False))
            2. Read csv
        '''


