# Import necessary libraries
import json
import streamlit as st 
import pandas as pd 

# Custom modules 
from .utils import fix_ags5
from util_classes.Forecaster import Forecaster

# model imports 
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Model training function 
def get_Model(data, verbose=False):
        
        from warnings import catch_warnings
        from warnings import filterwarnings
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        
        if verbose:
            print(".", end='')
        
        try:
            # define model
            model = SARIMAX(data, order=self.order, seasonal_order=self.sorder, trend=self.trend, enforce_stationarity=False, enforce_invertibility=False)
            # fit model
            with catch_warnings():
                filterwarnings("ignore")
                ### IMP: TODO: CHECKOUT THE WARNINGS, WE IGNORE NOW CAUSE WITH SAME IGNORING WE GOT GOOD MSE. It keeps throwing warnings wvwn though it produces good results.
                model_fit = model.fit(disp=False)
            
            return model_fit
        
        except:
            return None

def app():
    
    # Load the data
    df = pd.read_csv('data/data_from_2010_to_2019_unemployment_rate.csv')
    st.write(df.shape)

    # Fix ags 5 format 
    df['ags5'] = df['ags5'].apply(fix_ags5)

    # Use the  indexing as date but later can be changed from date to ags 5
    df = df.pivot(index="date", columns="ags5", values="unemployment_rate")

    # Get a kreis list 
    kreis_list = list(df.columns)

    # Get all the training values 
    all_train_data = [list(df[kreis_code].values) for kreis_code in kreis_list]
    all_train_data = { kreis_list[i]: all_train_data[i] for i in range(len(kreis_list)) }

    ''' Model Training '''
    st.write("fitting all 401 models...")

    # Loop through the kreis list
    preds = []

    # Predefined config - to be made dynamic later
    config = [(1, 1, 2), (1, 0, 2, 12), 't']

    order, sorder, trend = config

    for kreis in kreis_list[:5]:

        print(kreis)

        try:
            # define model
            train_data = all_train_data[kreis] 
            print("Train Data:", len(train_data))
            model = SARIMAX(train_data, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False, enforce_invertibility=False)
            
            # fit model
            with catch_warnings():
                filterwarnings("ignore")
                ### IMP: TODO: CHECKOUT THE WARNINGS, WE IGNORE NOW CAUSE WITH SAME IGNORING WE GOT GOOD MSE. It keeps throwing warnings wvwn though it produces good results.
                model_fit = model.fit(disp=False)
            
            # return model_fit

            # Prediction section 
            count = 10
            start = len(all_train_data[kreis])
            end = start + count - 1
            yhat = model.predict(start, end)
            print(yhat)
            output = [kreis] + list(yhat)
            preds.append(output)
        
        except:
            return None

    # Convert yhat to dataframe
    cols = ['ags5'] + [str(i) for i in range(1, count+1)]
    output_df = pd.DataFrame(preds, columns=cols)
    st.dataframe(output_df)

    # # Pivot to get a table of ags5 as rows and dates as columns 
    # df = df.pivot(index="ags5", columns="date", values="unemployment_rate")







    ''' Load the model configurations '''
    # Load model config using json 
    # config = [(1, 1, 2), (1, 0, 2, 12), 't']
    # file_location = 'data/data_from_2010_to_2019_unemployment_rate.csv'

    # forecaster = Forecaster(file_location, config, verbose=True, train=True)

    # # Select the ags2 type 
    # AGS5 = 1002
    # forecaster.getTrainSeries(AGS5)

    # # Get the number of predictions 
    # NUM_PREDICTIONS = 10
    # preds = forecaster.getPredictions(AGS5, NUM_PREDICTIONS)

    # st.write(preds)