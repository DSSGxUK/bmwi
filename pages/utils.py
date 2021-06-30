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

''' File Upload Functions '''


def read_single_file():
    """Function to read a single csv file

    Returns:
        data: Returns a dataframe of the uploaded csv file
    """
    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global data
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)    # encoding='latin_1' : can be added to read non-English Data
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file, encoding='latin_1')
    
    return data

''' Data Filtering methods '''

def drop_selected_variables(df):
    """Function to drop selected variables in a dataframe

    Args:
        df (DataFrame): dataframe to be filtered

    Returns:
        df: Returns the filtered data
    """
    
    st.subheader("Select non-important variables")
    variables_to_be_dropped = st.multiselect(label="Which variables would you like to drop?", 
                                            options=list(df.columns), 
                                            help="If none are selected, then all variables will be used for PCA.")

    # Drop the variables from the data
    if variables_to_be_dropped:
        df.drop(variables_to_be_dropped, axis=1, inplace=True)
    
    return df





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


''' Misc. Functions '''

# Function to convert the german phrases to english 
@st.cache() # caching to reduce time 
def get_english_term(german_phrase):
    
        
    # This is loading the data each time so there has to be a smarter way to do this. Might help reducing time. 
    translate = pd.read_csv('data/metadata/col_translate.csv')

    german_phrase = german_phrase.upper()
    
    try: 
        return translate[translate['Variable_name'] == german_phrase]['variable_english'].values[0] 
    except: 
        return german_phrase.lower()

# Function to convert data into download link
def get_table_download_link(df, text, filename="final.csv"):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    params:  
        dataframe
        text: Text to be printed in the file download option
        filename: Filename to be downloaded [optional]
    returns: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

    return href

