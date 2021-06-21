## network stuff

# Import necessary libraries 
from typing import Optional
import pandas as pd 
import streamlit as st 
import base64
import geopandas as gpd
import json
import matplotlib.pyplot as plt
import networkx as nx

# Custom modules 
from .utils import *

# Suppress warnings in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

# Create the app that would be run 
def app():
    
    st.write("Hi, I am Cinny.")

    ''' Section to upload all the data file '''
    st.markdown("## Data Upload and Network Approach of Time-Series Data.")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis.") 
    st.write("\n")

    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global data
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file, encoding='latin_1')
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file, encoding='latin_1')
    
    ''' Load the data and save the dataset in a separate folder to allow for quick reloads '''
    
    # Save the data
    data.to_csv('data/main_data.csv', index=False, encoding='latin_1')

    # Raw data display  
    st.dataframe(data)

    # Show data statistics 
    st.write("**Data Size:**", data.shape)

    ''' Display the features of the data which can be visualized '''

    # Collect the columns
    #data_cols = data.columns
    data_cols = []
    for col in list(data.columns)[5:]:
        if col[:-7] not in data_cols:
            data_cols.append(col[:-7])
    
    col_to_display = st.selectbox("Select which column to visualise network",
                                 options=data_cols, 
                                 index=6)
    #col_to_display = col_to_display[:-7]

    ''' Display the Network '''
    st.header(f"The correlation matrix for **{col_to_display}** at the Kreis-level.")
   
    # Fix the ag5 column using function defined in utils
    data['ags5_fix'] = data['ags5'].apply(fix_ags5)

    # filter df
    index_col = list(data.columns[:5]) # ['_id', 'ags2', 'bundesland', 'ags5', 'kreis']
    filter_col = [col for col in data if col.startswith(col_to_display)]
    filter_df = data[index_col + filter_col]
    filter_df = filter_df.set_index('ags5')[filter_col]
    filter_df_corr = filter_df.transpose().corr()
    st.write(filter_df_corr)

    # show stats
    threshold = st.slider("Select the correlation ratio threshold", min_value=0.8, max_value=1.0, step=0.01)
    sum_links = (sum((filter_df_corr>threshold).sum())-401)//2
    st.header(f'# links between kreise: {sum_links}')

    # calculation
    if st.button("Run Calculation"):
        G = nx.Graph()
        kreis = filter_df_corr.index #df['ags5'].unique()
        G.add_nodes_from(kreis)

        df_filtered = (filter_df_corr>threshold) & (filter_df_corr!=1)
        edge_lists = [
            [row_no, kreis[col_no]] 
            for row_no, row in df_filtered.iterrows() 
            for col_no, col_val in enumerate(row[:row_no]) 
            if col_val==True]
        G.add_edges_from(edge_lists)

        ''' Display the Network '''
        st.header(f"The network visualisation for **{col_to_display}** at the Kreis-level.")
    
        # plot
        plt.figure(figsize =(10, 10))
        nx.draw_networkx(G, node_size=10, with_labels=False)
        st.pyplot()

        st.header('Clustering Results')
        st.subheader('Clustering distribution')
        st.write([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True) if len(c)!=1])
        st.subheader('# single-group clusters')
        st.write(sum([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True) if len(c)==1]))
        
        # translate code to name
        st.subheader('Clustering groups')
        clusters = [c for c in sorted(nx.connected_components(G), key=len, reverse=True)]
        for c in clusters:
            c = list(c)
            #c = [str(i) for i in c]
            counties = data[data['ags5'].isin(c)]
            if len(counties)!=1:
                st.write(list(counties['kreis']))
