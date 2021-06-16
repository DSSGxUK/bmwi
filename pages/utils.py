''' Functions that need to be used regularly '''

# Import necessary libraries 
import pandas as pd 
import streamlit as st 
import numpy as np 

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
    print(german_phrase)
    print(translate[translate['German_Variable'] == german_phrase])
    
    try: 
        return translate[translate['German_Variable'] == german_phrase]['Translation'].values[0] 
    except: 
        return german_phrase.lower()