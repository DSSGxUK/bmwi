# Import necessary libraries 
from typing import Optional
import pandas as pd 
import streamlit as st 
import base64
import geopandas as gpd
import json
import matplotlib.pyplot as plt

# Custom modules 
from .utils import *

# Suppress warnings in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

# Create the app that would be run 
def app():

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
    col_to_display = st.selectbox("Select which column to visualise on the map", options=data_cols)

    ''' Display the document containing the various column descriptions '''
    
    # Check if the data description needs to be displayed 
    display_doc = st.radio("Display Column Descriptions", options=["Yes", "No"], index=1)
    if display_doc == "Yes":

        # Read a pdf of the data dictionary
        pdf_file_path = 'documents\pdf\coronadata_description.pdf'
        with open(pdf_file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # HTML for the file to be displayed 
        pdf_display = f'<embed src="data:application/pdf;base64, {base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

    ''' Display the Kreis Map '''
    st.header(f"The Map visualisation for **{col_to_display}** at the Kreiss level.")
   
    # Fix the ag5 column using function defined in utils
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
    labels = st.radio("Show labels?", options=["Yes", "No"], index=1)

    merged.plot(column=col_to_display, scheme="quantiles", figsize=(50, 30), cmap='coolwarm')
    plt.title(f'{col_to_display} in Germany by County', fontsize=15)
    # add text
    
    if labels == "Yes": 
        for i in range(len(merged)):
            plt.text(merged.longitude[i], merged.latitude[i],
                    f'{merged["kreis"][i]}\n{merged[col_to_display][i]}', size=10)

    st.pyplot()

    # plt.title(f'{col_to_display} in Germany by County', fontsize=15)
    # plt.show()
