# Import necessary libraries 
import streamlit as st 
import pandas
from pathlib import Path

# Custom modules 
from .utils import *

# Suppress warnings in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)


# Create the app that would be run 
def app():

    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [About](#about)
    - [User Workflow](#user-workflow)
    - [Prediction Results](#prediction-results)

    """)
    
    ''' Page Introduction '''
    st.markdown('# BMWi Tool')
    useful_links = '''
        [Documentation](https://dssgxuk.github.io/bmwi/start/start/) |
        [Tutorial Video](https://www.youtube.com/watch?v=US5DkvE1Ogs&list=PLzWRWFPEUpHbwIHq0T6M72B1_5N04hD0Q&index=1)
        '''
    st.markdown(useful_links)
    
    st.markdown('## About')
    about = '''
        This project is a collaboration between 
        German Federal Ministry for Economic Affairs and Energy 
        ([BMWi](https://www.bmwi.de/Navigation/EN/Home/home.html))
        and 
        the Data Science for Social Good Foundation 
        ([DSSGxUK](https://warwick.ac.uk/research/data-science/warwick-data/dssgx/)). 
        
        This tool allows you to forecast monthly unemployment rate 
        for the next quarter at the Kreis level in Germany, 
        based on the historic unemployment rate data. 
        
        You can read more about the project and how to use the tool 
        [here](https://cinnylin.github.io/bmwi-docs/).
        '''
    # about_section = st.beta_expander("About the Project", False)
    # about_section.markdown(about)
    st.markdown(about)

    st.markdown('## User Workflow')
    
    ''' Flowchart '''
    # flowchart_section = st.beta_expander("User Flowchart", False)
    # flowchart_section.image('img/flowchart.png')
    st.image('img/flowchart.png')
    
    ''' Workflow in detail '''
    sample_input = pd.read_excel('data/7444_318010_BMWI_Enkelmann_Eckdaten_Zeitreihe_Kreise.xlsx')
    sample_link = get_table_download_link(sample_input, text="Click here", filename="data", excel=True)
    
    # data1 = '''
    #     Your prediction journey starts on the **Data Prep** page. 
    #     There, you upload the data, and do necessary preprocessing that would then feed into the model.
    #     '''
    # data2 = '''
    #     to download an Excel file containing data till May 2021. 
    #     This Excel file contains the format of the input that our tool was tested on.
    #     '''
    data_section = st.beta_expander("Data Prep page", False)
    # data_section.markdown(data1+sample_link+data2, unsafe_allow_html=True)
    data_link = 'https://dssgxuk.github.io/bmwi/data/7444_318010_BMWI_Enkelmann_Eckdaten_Zeitreihe_Kreise.xlsx'
    data = f'''
        Your prediction journey starts on the **Data Prep** page. 
        There, you upload the data, and do necessary preprocessing that would then feed into the model.
        [Click here]({data_link}) to download an Excel file containing data till May 2021. 
        This Excel file contains the format of the input that our tool was tested on.
        '''
    data_section.markdown(data, unsafe_allow_html=True)
    
    pred = '''
        Once you "confirm" the preprocessed data on the **Data Prep** page, 
        you can go to the **Predictions** page. 
        The preprocessed data from the page before is automatically loaded. 
        The predictions may take a while to run. 
        The prediction results are cached, which means it should run faster 
        the second time you try to predict the same data. 
        '''
    pred_section = st.beta_expander("Predictions page", False)
    pred_section.markdown(pred)
    
    ci = '''
        This **Confidence Intervals** page provides confidence intervals 
        for the predictions that have been calculated in the **Predictions** page.
        '''
    ci_section = st.beta_expander("Confidence Intervals page", False)
    ci_section.markdown(ci)
    
    viz = '''
        The **Visualization** page shows line plots and map visualizations of the prediction results
        to quickly understand the prediction results, 
        e.g. which kreis has the highest unemployment rate, 
        whether the trend for that kreis is going up or down.
        '''
    viz_section = st.beta_expander("Visualizations page", False)
    viz_section.markdown(viz)
    
    rank = '''
        The **Ranking** page is also automatically loaded with the prediction results. 
        Apart from the map and line plot from the **Visualization** page, 
        this page contains kreis-level rankings and 
        grouped rankings of unemployment rates and their percentage changes. 
        '''
    rank_section = st.beta_expander("Rankings page", False)
    rank_section.markdown(rank)
    
    error = '''
        The **Error Analysis** page would be automatically loaded with the prediction results. 
        This page helps you look closer into which kreise were harder to predict, 
        and how that compares with their basic infrastructures, 
        such as number of hospitals, number of schools etc.
        '''
    error_section = st.beta_expander("Error Analysis page", False)
    error_section.markdown(error)
    
    ''' Prediction Results '''
    st.markdown('## Prediction Results')
    pred_output = pd.read_csv('data/pred_output_full.csv')
    prediction1 = '''
            Once the model is run, you can always go to the Visualization page \
            or Ranking page for quick access of the prediction results and interpretation.\
            You can also go to the Error Analysis page to validate prediction results.
            '''
    pred_link = get_table_download_link(pred_output, text="Here", filename="predictions", excel=True)
    prediction2 = '''
        is the link to download the latest prediction results.
        '''
    st.markdown(prediction1)
    st.markdown(pred_link+prediction2, unsafe_allow_html=True)