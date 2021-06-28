# Import necessary libraries
from typing import Optional
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
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Custom modules 
from .utils import read_single_file, get_table_download_link, drop_selected_variables

# Define the app 
def app():

    # Common details and data upload
    st.write("## Cluster Analysis")

    # Read the data file with 401 and rows and n columns
    data = read_single_file()

    st.write("Uploaded dataset size:", data.shape)
    

    # Check if TSNE or PCA
    cluster_type = st.selectbox("Select the type of analysis", options=['t-SNE', 'PCA'], index=1)

    # t-SNE Section
    if cluster_type == 't-SNE':
        st.write("### Principal Component Analysis.")

        # Check if the column cluster is present in the data 
        if 'cluster' in data.columns:
            new_df = data.drop(['cluster'], axis=1)
        else: 
            new_df = data

        # Remove unnecessary cols 
        data_to_fit = new_df.drop(['kreis', 'ags5', 'ags2'], axis=1)
        
        ''' Fix categorical and numerical columns '''
        object_cols = [ 
            # 'labor_market_region',
            'growing_/_shrinking_circles',
            'labor_market_type',
            'grw_funding_framework',
            'settlement_structure_type_of_labor_market_region',
            'room_type_location',
            'district_settlement_structure',
            'type_of_settlement_structure',
            'urban_/_rural',
            'metropolitan_region',
            'metropolitan_area',
            'east_west',
            'border_proximity',
            'support_area_status',
            'eligible_area'
        ]

        # Convert cluster to object type
        data_to_fit[object_cols] = data_to_fit[object_cols].astype('object')

        # Collect numeric data 
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        num_df = data_to_fit.select_dtypes(include=numerics)

        # Scale the numeric columns 
        scaler = StandardScaler()
        numerical_data = scaler.fit_transform(num_df)
        numerical_data = pd.DataFrame(numerical_data, columns=num_df.columns)

        # One hot encoding for categorical 
        categorical_cols = list(set(data_to_fit.columns) - set(num_df.columns))
        categorical_data = pd.get_dummies(data_to_fit[categorical_cols])

        # Concatenate the data 
        scaled_data = pd.concat([numerical_data, categorical_data], axis=1)
        scaled_data.shape

        ''' Variable and Method Selection '''
        scaled_data = drop_selected_variables(scaled_data)

        # Create a tsne instance 
        tsne = TSNE(learning_rate=50, 
                    n_components=3,  
                    random_state=42)  
        
        # Fit the model  
        tsne_features = tsne.fit_transform(scaled_data)

        # Convert to df
        tsne_features = pd.DataFrame(tsne_features)

        ''' 3D Plot for PCA components '''
        make_3d_plot = st.checkbox("Plot a 3D map of the components?", value=False)
        if make_3d_plot:
            ax = plt.axes(projection='3d')
            # Data for three-dimensional scattered points
            ax.scatter3D(tsne_features[0], tsne_features[1], tsne_features[2], c=tsne_features[0])
            st.pyplot()
        
        # Picked three based on the above values
        num_clusters = 3
        km = KMeans(n_clusters=num_clusters, random_state=42).fit(tsne_features)

        # Create a cluster map dataframe
        cluster_map = pd.DataFrame()
        cluster_map['data_index'] = data.index.values
        cluster_map['cluster'] = km.labels_

        # Merge cluster and original data
        data_final = cluster_map.merge(new_df, left_on='data_index', right_index=True)

        # Print the cluster sizes
        st.write("The following are the cluster sizes:")
        st.dataframe(data_final['cluster'].value_counts().sort_index())

        # Print the cluster information
        for i in range(num_clusters):
            st.write(f"Cluster {i+1}:", data_final[data_final['cluster']==i]['kreis'].to_list())

        # Allow the final file for download
        st.markdown(get_table_download_link(data_final, text="Download CSV with cluster information"), unsafe_allow_html=True)

    
    # PCA Section 
    else:
        st.write("### Principal Component Analysis.")

        # Select a subset of data columns
        X = data.drop(["ags2", "ags5", "kreis"], axis=1)

        ''' Variable and Method Selection '''
        X = drop_selected_variables(X)

        ''' Scale the uploaded Data '''
        st.write("Data is being scaled using a Standard Scaler...")
        scaler = StandardScaler()
        scaler.fit(X)
        scaled_data = scaler.transform(X)
        X = pd.DataFrame(scaled_data, columns = X.columns)

        ''' Prinicpal Component Analysis '''
        pca = PCA(n_components=3, random_state=42)
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
            ax.scatter3D(PCA_components[0], PCA_components[1], PCA_components[2], c=PCA_components[1])
            st.pyplot()

        ''' Clustering using k-means '''
        st.subheader("Clustering Analysis")
        num_clusters = st.slider("Select the number of clusters.", min_value=2, max_value=10, step=1, value=3, help="Suggested:not more than 4")
        
        # Define the k-means object
        km = KMeans(n_clusters=num_clusters, random_state=42).fit(X)

        cluster_map = pd.DataFrame()
        #st.write(data)
        cluster_map['data_index'] = data.index.values
        cluster_map['cluster'] = km.labels_
        data_final = cluster_map.merge(data, left_on='data_index', right_index=True)
        # st.dataframe(data_final)

        # Print the cluster sizes
        st.write("The following are the cluster sizes:")
        st.dataframe(data_final['cluster'].value_counts().sort_index())

        # Print the cluster information
        for i in range(num_clusters):
            st.write(f"Cluster {i+1}:", data_final[data_final['cluster']==i]['kreis'].to_list())


        # Allow the final file for download
        st.markdown(get_table_download_link(data_final, text="Download CSV with cluster information"), unsafe_allow_html=True)

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
