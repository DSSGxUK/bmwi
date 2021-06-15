# Import necessary libraries 
import pandas as pd 
import streamlit as st 
import base64


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
        pdf_file_path = 'documents\pdf\Economic Forecasting Chap01.pdf'
        with open(pdf_file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # HTML for the file to be displayed 
        pdf_display = f'<embed src="data:application/pdf;base64, {base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

    ''' Display the Kreis Map '''

    st.write("This is where we will show the map of the kreises for the column:", col_to_display)