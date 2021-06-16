# Import necessary libraries 
from typing import Optional
import pandas as pd 
import streamlit as st 
import base64
import geopandas as gpd
import json
import matplotlib.pyplot as plt
import json
import plotly.express as px

# Custom modules 
from .utils import *

# Suppress warnings in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

# Create the app that would be run 
def app():

    st.write("Hi I am Cinny")

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
    col_to_display = st.selectbox("Select which column to visualise on the map",
                                 options=data_cols, 
                                 index=4, 
                                 format_func = lambda x: get_english_term(x)
                                 )

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
    data['ags5'] = data['ags5'].apply(fix_ags5)

    # Read the map coordinates data 
    with open('georef-germany-kreis/georef-germany-kreis.geojson') as response:
        geojs = json.load(response)

    # Check if the labels need to be added 
    labels = st.radio("Show labels?", options=["Yes", "No"], index=1)

    fig = px.choropleth(data,
                    geojson=geojs, color="kr_firm",
                    locations="ags5", featureidkey="properties.krs_code",
                    projection="mercator",
                    labels={'kr_firm':'# firms'})
    fig.update_geos(fitbounds="locations", visible=True)
    #fig.show()

    st.plotly_chart(fig)
