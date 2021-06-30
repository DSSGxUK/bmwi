''' Functions that need to be used regularly '''

# Import necessary libraries 
from numpy.core.fromnumeric import size
import pandas as pd 
import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt 
import base64
import geopandas as gpd

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

# Function to plot a map
def data_map(data, merge_col, data_col, cat_col=False):
    '''
    Input variables:
    - data: pd.df; dataframe info to plot the map
    - merge_col: str; the ags5 col to merge with gdf
    - data_col: str; col to map
    - cat_col: bool; whether data_col is categorical, default to False
    Return:
    - fig: plt.fig; the plot figure
    '''
    # read the map coordinates data 
    gdf = gpd.read_file('georef-germany-kreis/georef-germany-kreis-millesime.shp')
    
    # merge the coords with the data 
    merged = pd.merge(data, gdf, left_on=merge_col, right_on='krs_code')
    
    # get the geospatial data 
    merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
    merged['coords'] = [coords[0] for coords in merged['coords']]
    merged['longitude'] = merged['coords'].str[0]
    merged['latitude'] = merged['coords'].str[1]
    
    # convert to geodata
    merged = gpd.GeoDataFrame(merged)
    
    # check if the labels need to be added 
    labels = st.radio("Show all labels?", options=["Yes", "No"], index=1)

    # check if certain labels need to be added -- by region
    label_ags = st.radio("Show labels by region?", options=["Yes", "No"], index=1)
    if label_ags == "Yes": 
        bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
            '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
            '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
            '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
        txt_to_display_ags = st.selectbox("Select which Bundesland to annotate",
                                    options=bundeslands, index=0)
    
    # check if certain labels need to be added -- by stats
    if cat_col==False:
        label_stats = st.radio("Show labels by stats?", options=["Yes", "No"], index=1)
        if label_stats == "Yes": 
            stats = ['mean', 'min', '25%', '50%', '75%', 'max']
            stats_values = merged[data_col].describe()[stats].sort_values()
            st.write(stats_values)
            txt_to_display_stats = st.slider("Select a range of values", 
                                            float(stats_values['min']), float(stats_values['max']), 
                                            (float(stats_values['25%']), float(stats_values['75%'])))
    # check if certain labels need to be added -- by category
    if cat_col==True:
        label_cls = st.radio("Show labels by category?", options=["Yes", "No"], index=1)
        if label_cls == "Yes": 
            txt_to_display_cls = st.selectbox("Select which category to annotate",
                                        options=sorted(list(data[data_col].astype(str).unique())), 
                                        index=0)
    
    # plot
    # (1) categorical data_col
    if cat_col == True:
        fig, ax = plt.subplots(figsize=(50,30))
        merged.plot(column=data_col, #scheme="NaturalBreaks",
                    #scheme='UserDefined', classification_kwds={'bins':clusters},
                    ax=ax, cmap='Set3', categorical=True, legend=True)
        ax.set_title(f'{data_col} in Germany by County', fontsize=15)
    
    # (2) numerical data_col
    else:
        fig, ax = plt.subplots(figsize=(50,30))
        merged.plot(column=data_col, scheme="quantiles",
                    ax=ax, cmap='coolwarm', legend=True)
        ax.set_title(f'{data_col} in Germany by County', fontsize=15)

    # annotation filters
    # (1) by ags
    if label_ags == "Yes": 
        merged_ags = merged[merged['ags2']==int(txt_to_display_ags[:2])]
        for i in merged_ags.index:
            ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
                    f'{merged_ags["kreis"][i]}\n{merged_ags[data_col][i]}', fontsize=10)
    # (2) add by stats
    if cat_col==False:
        if label_stats == "Yes": 
            # get filtered df
            merged_stats = merged[
                (merged[data_col]>=txt_to_display_stats[0]) & 
                (merged[data_col]<=txt_to_display_stats[1])]
            # add text with filters
            for i in merged_stats.index:
                ax.text(merged_stats.longitude[i], merged_stats.latitude[i],
                        f'{merged_stats["kreis"][i]}\n{merged_stats[data_col][i]}', fontsize=10)
    # (3) add by category
    if cat_col==True:
        if label_cls == "Yes": 
            merged_cls = merged[merged[data_col]==txt_to_display_cls]
            for i in merged_cls.index:
                ax.text(merged_cls.longitude[i], merged_cls.latitude[i],
                        f'{merged_cls["kreis"][i]}\n{merged_cls[data_col][i]}', fontsize=10)
    # (4) add all text
    if labels == "Yes": 
        for i in range(len(merged)):
            ax.text(merged.longitude[i], merged.latitude[i],
                    f'{merged["kreis"][i]}\n{merged[data_col][i]}', fontsize=10)
    
    return fig



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

