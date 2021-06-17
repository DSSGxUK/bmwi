# Import necessary libraries 
from operator import index
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn.external.docscrape import indent 
from scipy.stats import skew, kurtosis
    
# from pandas._config.config import options 
import streamlit as st 
import base64

# Custom modeules 
from .utils import *


# Create the app that would be run 
def app():

    # Add the title
    st.title("Data Visualisation")

    # Load the data 
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:

        # Read the data 
        data = pd.read_csv('data/main_data.csv', encoding='latin_1')

        ''' Display a correlation matrix '''
        corr_matrix = st.checkbox("Do you want a correlation matrix?", value=False)
        if corr_matrix:
            sns.heatmap(data.corr(), annot=True)
            st.pyplot() 

        ''' Select Display Parameters and plot the charts '''
        col1, col2 = st.beta_columns(2)

        # Select the feature 
        feature = col1.selectbox("Select the feature you want to visualize.", options=list(data.columns), index=5)

        # Select the type of chart you want 
        chart = col2.selectbox("Select the type of chart you want to see.", 
                                options=["Histogram", "Distribution", "Line Plot"], index=1)

        # Plot a histogram 
        if chart == "Distribution":
            
            kde_check = st.checkbox("Show Kernel Density Estimation?", value=False)
            # pLot distribution 
            if kde_check: 
                sns.distplot(data[feature], 10, kde=True)
            else: 
                sns.distplot(data[feature], 10, kde=False)
            
            st.pyplot()

             # Add the stats about skewness and kurtosis 
            skewness = skew(data[feature])
            excess_kurtosis = kurtosis(data[feature])

            st.write(f"The skewness is {skewness} and kurtosis is {excess_kurtosis}.")


        elif chart == "Histogram":

            # calculate the histogram edges
            data_histogram(data[feature], 10, None, None)
            st.pyplot()

        ''' Section for bivariate analysis '''
        st.write("Bivariate Analysis")
        
        col1, col2 = st.beta_columns(2)
        
        # Select the feature 
        feature1 = col1.selectbox("Select the first feature", options=list(data.columns), index=5)
        feature2 = col1.selectbox("Select the second feature.", options=list(data.columns), index=6)

        # Check if either of the features are categorical 
        if data[feature1].dtype.name == 'category' or data[feature2].dtype.name == 'category':
            print('category')
        
        else: 
            # Create a two column subplot with lmplot and scatter
            fig = sns.lmplot(x=feature1, y=feature2, data=data, scatter=True)
            st.subheader("Scatter Plot with regression line.")
            st.pyplot(fig)
            st.write(f"Correlation Coefficient: {data[feature1].corr(data[feature2])}")
