''' Functions that need to be used regularly '''

# Import necessary libraries 
from numpy.core.fromnumeric import size
import pandas as pd 
import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt 
import base64

# Function to fix the format of ag5 
def fix_ags5(x):
    if len(str(x))==4:
        return '0'+str(x)
    else:
        return str(x)

# Function to convert the german phrases to english 
@st.cache() # caching to reduce time 
def get_english_term(german_phrase):
    
        
    # This is loading the data each time so there has to be a smarter way to do this. Might help reducing time. 
    translate = pd.read_csv('data/metadata/col_translate.csv')

    german_phrase = german_phrase.upper()
#     print(german_phrase)
#     print(translate[translate['Variablenname'] == german_phrase])
    
    try: 
        return translate[translate['Variable_name'] == german_phrase]['variable_english'].values[0] 
    except: 
        return german_phrase.lower()

# Function to convert data into download link
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    params:  dataframe
    returns: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="combined_final.csv">Download combined csv file</a>'

    return href

''' Visualisation Functions '''

# Funtion to plot a histogram 
def data_histogram(column, no_of_bins, minimum=None, maximum=None):
    
    # default vals
    if minimum is None:
        minimum = min(column)
    if maximum is None:
        maximum = max(column)
        
    # calculate the histogram edges
    bin_edges = np.arange(minimum, maximum, (maximum - minimum)/no_of_bins)
    
    plt.figure(figsize=(5,5))
    plt.hist(column, bin_edges)
      
    plt.show()