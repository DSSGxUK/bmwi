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