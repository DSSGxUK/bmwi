# Import necessary libraries
import pandas as pd
import numpy as np
import streamlit as st 

import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg')
import seaborn as sns; sns.set()

from pathlib import Path
from functools import reduce

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Custom modules 
from .utils import read_single_file, get_table_download_link

# Define the app 
def app():

    st.header("Cluster Analysis using Principal Component Analysis.")

    # Read the data file with 401 and rows and n columns
    data = read_single_file()

    st.write("Uploaded dataset size:", data.shape)

    # Select a subset of data columns
    X = data.drop(["ags2", "ags5", "kreis"], axis=1)

    ''' Variable and Method Selection '''
    st.subheader("Select non-important variables")
    variables_to_be_dropped = st.multiselect(label="Which variables would you like to drop?", 
                                             options=X.columns, 
                                             help="If none are selected, then all variables will be used for PCA.")

    # Drop the variables from the data
    if variables_to_be_dropped:
        X.drop(variables_to_be_dropped, axis=1, inplace=True)

    ''' Scale the uploaded Data '''
    st.write("Data is being scaled using a Standard Scaler...")
    scaler = StandardScaler()
    scaler.fit(X)
    scaled_data = scaler.transform(X)
    X = pd.DataFrame(scaled_data, columns = X.columns)

    ''' Prinicpal Component Analysis '''
    pca = PCA(n_components=3)
    pca.fit(X)

    ''' PCA Variable Importance Plot '''
    per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
    labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
    
    ''' Component Importance - Need to make it in the new streamlit fig method @cinny'''
    show_importance = st.checkbox("Show Component Importance", value=False)
    if show_importance:
        plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
        plt.ylabel('Percentage of Explained Variance')
        plt.xlabel('Principal Component')
        plt.title('Screen Plot')
        for index, dt in enumerate(per_var):
            plt.text(x=index+0.9 , y =dt+1 , s=f"{dt}%" , fontdict=dict(fontsize=10))
        st.pyplot()
    
    # Create the principal components 
    principalComponents = pca.fit_transform(scaled_data)
    PCA_components = pd.DataFrame(principalComponents)

    ''' Generate importance of each feature '''
    pca_param = pd.DataFrame(pca.components_,columns=X.columns,index = ['PC-1','PC-2','PC-3']).T
    sort_param = st.radio("Which component would you like to sort the app by?", options=pca_param.columns, index=0)
    st.dataframe(pca_param.sort_values(by=sort_param, ascending=[False]).head(20))
    
    ''' 3D Plot for PCA components '''
    make_3d_plot = st.checkbox("Plot a 3D map of the components?", value=False)
    if make_3d_plot:
        ax = plt.axes(projection='3d')
        # Data for three-dimensional scattered points
        ax.scatter3D(PCA_components[0], PCA_components[1], PCA_components[2], c=PCA_components[0], cmap='Blues')
        st.pyplot()

    ''' Clustering using k-means '''
    st.subheader("Clustering Analysis")
    num_clusters = st.slider("Select the number of clusters.", min_value=2, max_value=10, step=1, value=3, help="Suggested:not more than 4")
    
    # Define the k-means object
    km = KMeans(n_clusters=num_clusters).fit(X)

    cluster_map = pd.DataFrame()
    #st.write(data)
    cluster_map['data_index'] = data.index.values
    cluster_map['cluster'] = km.labels_
    data = cluster_map.merge(data, left_on='data_index', right_index=True)
    st.dataframe(data)

    # Print the cluster sizes
    st.write("The following are the cluster sizes:")
    st.dataframe(data['cluster'].value_counts().sort_index())

    # Print the cluster information
    for i in range(num_clusters):
        st.write(f"Cluster {i+1}:", data[data['cluster']==i]['kreis'].to_list())


    # Allow the final file for download
    st.markdown(get_table_download_link(data, text="Download CSV with cluster information"), unsafe_allow_html=True)

    ''' Cluster Visualisation '''
    st.subheader("Cluster Visualisation")

    # Change cluster values 
    cluster_value_map = {0:1, 1:2, 2:3}
    data = data.replace({"cluster": cluster_value_map})
    
    # Create three columns
    col1, col2, col3 = st.beta_columns(3)
    cluster1 = col1.slider("Select the cluster", min_value=1, max_value=num_clusters, step=1, value=1)
    cluster2 = col2.slider("Select the cluster", min_value=1, max_value=num_clusters, step=1, value=2)
    visual_col = col3.selectbox("Select the feature to be visualised", options=X.columns)

   
    
    # Filter data by cluster
    filter_data = data[data['cluster'].isin([cluster1, cluster2])]
    sns.kdeplot(data=filter_data, x=visual_col, hue="cluster",  common_norm=False)
    st.pyplot()
