# Import libs 
import pickle
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st 

# Custom Modules 
from .utils import read_single_file

def app():
    st.write("Categorical Data Networks")

    # Read the data file with 401 and rows and n columns
    spatial_planning = read_single_file()

    ## Convert column names 
    categorical_columns = ['kr_amr', 'kr_wa_schr_kl', 'kr_amt_kl', 'kr_grw_fg_kl', 'kr_sr_am_kl', 'kr_rl_kl', 'kr_ssk_kl', 'kr_ssr_kl', 'kr_stla_kl', 'kr_mra_kl', 'kr_mrb_kl', 'kr_wo_kl', 'kr_grenze']
    categorical_columns_translated = ['labor market region', 'growing / shrinking circles', 'labor market type', 'grw funding framework', 'settlement structure type of labor market region', 'room type location', 'district settlement structure', 'type of settlement structure', 'urban / rural', 'metropolitan region', 'metropolitan area', 'east west', 'border proximity']
    
    # Check if len of column lists is the same 
    assert len(categorical_columns) == len(categorical_columns_translated)

    # Create a usable dataframe 
    useful_df = spatial_planning[categorical_columns]
    useful_df.columns = [col.replace(' ', '_') for col in categorical_columns_translated]
    useful_df.index = spatial_planning['ags5']
    
    # Code Block 1
    data_dict = {}

    for col in useful_df.columns:
        for val in useful_df[col].unique():
            data_dict[col + '_' + str(val)] = list(useful_df.index[useful_df[col] == val])


    ## Code block 2
    edge_weights = {}
    
    for key, kreis_list in data_dict.items():
        
        kreis_list.sort() # sort it to force the pairs to the lower triangle
        
        # make all the edges (kr1, kr2)
        pairs = [(kreis_list[p1], kreis_list[p2]) for p1 in range(len(kreis_list)) for p2 in range(p1+1,len(kreis_list))]
        
        for pair in pairs:
            try:
                edge_weights[(pair[0], pair[1])] +=1
            except:
                edge_weights[(pair[0], pair[1])] = 1
    
    ## Code block 3
    weight_treshold = 10

    G = nx.Graph()
    G.add_nodes_from(spatial_planning['ags5'])

    for key, val in edge_weights.items():
        if val > weight_treshold:
            G.add_edge(*key)

    plt.figure(figsize =(10, 10))
    nx.draw_networkx(G, edge_color=(1,0,0), node_size=50, with_labels=False)
    st.pyplot()

    # Get clusters 
    clusters = [c for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    for c in clusters:
        c = list(c)
        c = [str(i) for i in c]
        counties = spatial_planning[spatial_planning['ags5'].isin(c)]
        st.write(list(counties['kreis']))