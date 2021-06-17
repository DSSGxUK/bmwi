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
    st.markdown("## Data Upload and Map Viz.")

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
    data_cols = data.columns
    col_to_display = st.selectbox("Select which column to visualise network",
                                 options=data_cols, 
                                 index=6)
    col_to_display = col_to_display[:-7]

    ### differentiate between numerical and categorical data and their network methods (prob need two separate pages)

    ''' Display the Kreis Map '''
    st.header(f"The network visualisation for **{col_to_display}** at the Kreis-level.")
   
    # Fix the ag5 column using function defined in utils
    data['ags5_fix'] = data['ags5'].apply(fix_ags5)

    # filter df
    index_col = list(data.columns[:5]) # ['_id', 'ags2', 'bundesland', 'ags5', 'kreis']
    filter_col = [col for col in data if col.startswith(col_to_display)]
    filter_df = data[index_col + filter_col]
    filter_df_corr = filter_df.set_index('ags5')[filter_col]
    st.write(filter_df_corr.transpose().corr())

    # show stats
    threshold = st.slider("Select the correlation ratio threshold", min_value=0.8, max_value=1.0, step=0.01)
    sum_links = (sum((filter_df_corr.transpose().corr()>threshold).sum())-401)//2
    st.write(f'# links between kreise: {sum_links}')

    # calculation
    kreise1 = []
    kreise2 = []
    source = []
    target = []
    value = []
    #size = list(data[filter_col[-1]])

    # this takes a long time to run so turn this on to start
    if st.button("Run Calculation"):
      for col in range(400):
          for row in range(col,400):
            ratio = filter_df_corr.transpose().corr().iloc[col].iloc[row]
            # logging
            if (col in list(range(0,401,10))) and (row in list(range(0,401,10))) and (col==row):
                st.write(f'{col}/401 rows processed ...')
            # high correlation
            if (ratio>threshold) and (ratio<1):
                ags5 = filter_df_corr.transpose().corr().index
                kreise1.append(ags5[col])
                kreise2.append(ags5[row])
                source.append(col)
                target.append(row)
                value.append(ratio)
      
      # create match df
      match = pd.DataFrame({'kreise1': kreise1, 'kreise2': kreise2,
                            'source': source, 'target': target, 'value': value})
      match['group'] = match['kreise1'].astype(str).str[:2]

      # plot
      plt.figure(figsize=(20,20))

      G01 = nx.from_pandas_edgelist(match[match['group']=='01'], source='kreise1', target='kreise2')
      G02 = nx.from_pandas_edgelist(match[match['group']=='02'], source='kreise1', target='kreise2')
      G03 = nx.from_pandas_edgelist(match[match['group']=='03'], source='kreise1', target='kreise2')
      G04 = nx.from_pandas_edgelist(match[match['group']=='04'], source='kreise1', target='kreise2')
      G05 = nx.from_pandas_edgelist(match[match['group']=='05'], source='kreise1', target='kreise2')
      G06 = nx.from_pandas_edgelist(match[match['group']=='06'], source='kreise1', target='kreise2')
      G07 = nx.from_pandas_edgelist(match[match['group']=='07'], source='kreise1', target='kreise2')
      G08 = nx.from_pandas_edgelist(match[match['group']=='08'], source='kreise1', target='kreise2')
      G09 = nx.from_pandas_edgelist(match[match['group']=='09'], source='kreise1', target='kreise2')
      G10 = nx.from_pandas_edgelist(match[match['group']=='10'], source='kreise1', target='kreise2')
      G11 = nx.from_pandas_edgelist(match[match['group']=='11'], source='kreise1', target='kreise2')
      G12 = nx.from_pandas_edgelist(match[match['group']=='12'], source='kreise1', target='kreise2')
      G13 = nx.from_pandas_edgelist(match[match['group']=='13'], source='kreise1', target='kreise2')
      G14 = nx.from_pandas_edgelist(match[match['group']=='14'], source='kreise1', target='kreise2')
      G15 = nx.from_pandas_edgelist(match[match['group']=='15'], source='kreise1', target='kreise2')
      G16 = nx.from_pandas_edgelist(match[match['group']=='16'], source='kreise1', target='kreise2')

      Gmatch = nx.from_pandas_edgelist(match, source='kreise1', target='kreise2')
      pos = nx.spring_layout(Gmatch)
      options = {'node_size':20, 'alpha':1, 'width':0.1}

      # Check if the labels need to be added 
      # labels = st.radio("Show all labels?", options=["Yes", "No"], index=1)
      # if labels == "Yes":
      #   bool = True
      # else:
      #   bool = False

      nx.draw_networkx(G01, pos, with_labels=False, node_color="#d3d3d3", label='01', **options)
      nx.draw_networkx(G02, pos, with_labels=False, node_color="#9c9d97", label='02', **options)
      nx.draw_networkx(G03, pos, with_labels=False, node_color="#474f52", label='03', **options)
      nx.draw_networkx(G04, pos, with_labels=False, node_color="#1d1c21", label='04', **options)
      nx.draw_networkx(G05, pos, with_labels=False, node_color="#ffd83d", label='05', **options)
      nx.draw_networkx(G06, pos, with_labels=False, node_color="#f9801d", label='06', **options)
      nx.draw_networkx(G07, pos, with_labels=False, node_color="#b02e26", label='07', **options)
      nx.draw_networkx(G08, pos, with_labels=False, node_color="#825432", label='08', **options)
      nx.draw_networkx(G09, pos, with_labels=False, node_color="#80c71f", label='09', **options)
      nx.draw_networkx(G10, pos, with_labels=False, node_color="#5d7c15", label='10', **options)
      nx.draw_networkx(G11, pos, with_labels=False, node_color="#3ab3da", label='11', **options)
      nx.draw_networkx(G12, pos, with_labels=False, node_color="#169c9d", label='12', **options)
      nx.draw_networkx(G13, pos, with_labels=False, node_color="#3c44a9", label='13', **options)
      nx.draw_networkx(G14, pos, with_labels=False, node_color="#f38caa", label='14', **options)
      nx.draw_networkx(G15, pos, with_labels=False, node_color="#c64fbd", label='15', **options)
      nx.draw_networkx(G16, pos, with_labels=False, node_color="#8932b7", label='16', **options)

      plt.legend()
      st.pyplot()

      st.header('Clustering Results')
      st.write([len(c) for c in sorted(nx.connected_components(Gmatch), key=len, reverse=True)])
      
      # translate code to name
      clusters = [c for c in sorted(nx.connected_components(Gmatch), key=len, reverse=True)]
      for c in clusters:
        c = list(c)
        c = [str(i) for i in c]
        counties = data[data['ags5'].isin(c)]
        st.write(list(counties['kreis']))
