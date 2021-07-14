# Import necessary libraries 
from numpy.lib.function_base import average
from numpy.lib.ufunclike import fix
import pandas as pd
import geopandas as gpd
from pandas._config.config import options 
import streamlit as st 

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from matplotlib import pyplot
import matplotlib.dates as mdates

import random
from scipy.stats import ttest_ind
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression, RidgeCV, Ridge
from regressors import stats
from mlxtend.feature_selection import SequentialFeatureSelector as sfs

# Custom modules 
from .utils import fix_ags5, get_table_download_link


''' Functions for this page '''

# function to do that for a spesific column 
def compare_error_in_two_groups(df, column_name): 
    sns.kdeplot(data=df, x="error", hue=column_name,  common_norm=False)
    st.pyplot()
    # df[column_name] = df[column_name].astype(str)
    # one, two = list(set(df[column_name]))
    # df_one = df[df[column_name]==one]
    # df_two = df[df[column_name]==two]
    # return ttest_ind(df_one['error'], df_two['error'], equal_var=False)

# Function to plot error maps 
def plot_error_map(data, date_string="by average"):
    # read the map coordinates data 
    gdf = gpd.read_file('georef-germany-kreis/georef-germany-kreis-millesime.shp')
    
    # merge the coords with the data 
    try:
        merged = pd.merge(data, gdf, left_on='ags5', right_on='krs_code')
    except ValueError:
        data['ags5_fix'] = data['ags5'].apply(fix_ags5)
        merged = pd.merge(data, gdf, left_on='ags5_fix', right_on='krs_code')
    
    # get the geospatial data 
    merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
    merged['coords'] = [coords[0] for coords in merged['coords']]

    merged['longitude'] = merged['coords'].str[0]
    merged['latitude'] = merged['coords'].str[1]

    # convert to geodata
    merged = gpd.GeoDataFrame(merged)
    
    # Set title 
    title = f"Errors in prediction in Germany by County {(date_string)}" 
    
    # numerical data_col
    fig, ax = plt.subplots(figsize=(30, 10))
    merged.plot(column='error', scheme="quantiles",
                ax=ax, cmap='coolwarm', legend=True)
    ax.set_title(title, fontsize=15)

    return fig 

def app():
    
    st.title("Error Analysis Page")

    # Load error data 
    error_data = pd.read_csv('data\error_2018_2019_nn.csv')
    error_data['ags5'] = error_data['ags5'].apply(fix_ags5)

    ''' Error Map Viz '''
    error_checkbox = st.checkbox("Visualize error on a map?", value=False)

    if error_checkbox: 
        st.subheader("Error visualization on a Map")
        st.write("\nLoading Map..")
        
        # Display a date range
        method = st.selectbox("Select a date or method.", options=['average']+list(error_data['date'].unique()))
        
        # Show for average predictions
        if method == 'average': 
            filter_data = error_data[['ags5', 'error']].groupby('ags5', as_index=False).mean()
        else: 
            # Filter by date 
            filter_data = error_data[error_data['date'] == method]
            
        st.pyplot(plot_error_map(filter_data, date_string=method))
        
        st.markdown("""---""")

    ''' Data Addition '''
    # Add the bundesland kreis and ags2 to the data
    ags5_data = pd.read_csv('data\index.csv')
    ags5_data['ags5'] = ags5_data['ags5'].apply(fix_ags5)
    error_data = pd.merge(ags5_data[['ags5', 'kreis', 'bundesland', 'ags2']], error_data, on='ags5')
    
    # Fix date format 
    error_data['date'] = pd.to_datetime(error_data['date'], format = '%Y-%m-%d')


    ''' Visualisation Section '''
    st.subheader("Error Plots by Bundesland or Kreis")
    
    # Make two columns if kreis then list of kreis else list of bundesland 
    # add all in both subcolumns by default
    col1, col2 = st.beta_columns(2)

    viz_area = col1.selectbox(label="Select Kreis or Bundesland", options=["Kreis", "Bundesland"])

    col2.write()

    # Get the options based on column one 
    if viz_area == 'Kreis':
        dropdown_options = list(error_data['ags5'].unique())
        dropdown_options = ['all'] + dropdown_options 
    elif viz_area == 'Bundesland':
        dropdown_options = list(error_data['ags2'].unique())
        dropdown_options = ['all'] + dropdown_options 
    
    viz_sub_area = col2.selectbox("Select all or a particular geographical entitity", options=dropdown_options)

    if viz_area=='Kreis':
        if viz_sub_area=='all': 
            g = sns.lineplot(data=error_data, x="date", y="error",  hue='ags5')
            plt.title(f"{viz_area} : {viz_sub_area}")
            g.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            g.legend_.remove()
            
            st.pyplot()
        
        else: 

            # filter data by kreis 
            filter_data = error_data[error_data['ags5'] == viz_sub_area]
            g = sns.lineplot(data=error_data, x="date", y="error")
            plt.title(f"{viz_area} : {viz_sub_area}")
            g.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            # g.legend_.remove()
        
    
    elif viz_area=='Bundesland':
        if viz_sub_area=='all': 

            g = sns.lineplot(data=error_data, x="date", y="error",  hue='ags2')
            plt.title(f"{viz_area} : {viz_sub_area}")
            g.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            g.legend_.remove()
            st.pyplot()

        else: 
            # filter data by kreis 
            filter_data = error_data[error_data['ags5'] == viz_sub_area]
            g = sns.lineplot(data=error_data, x="date", y="error")
            plt.title(f"{viz_area} : {viz_sub_area}")
            g.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            g.legend_.remove()

    st.markdown("""---""")

    ''' MEAN ERROR ANALYSIS '''
    df_mean_error = error_data.groupby(['ags5','ags2','bundesland','kreis'], as_index=False).mean()

    st.subheader("Kreis Level Overview")
    st.write("You can check the top-n or bottom-n kreis based on the prediction errors.")
    
    value_choice = st.radio("Select whether you want the highest or lowest values", options=["Highest", "Lowest"])
    n_value = st.slider("Select the number of values to be displayed", min_value=1, max_value=20, step=1, value=5)

    if value_choice == 'Highest':
        output_df = df_mean_error.sort_values(by='error', ascending=False)[['kreis', 'error', 'ags5', 'bundesland']]
        st.dataframe(output_df.head(n_value).reset_index(drop=True))
    else: 
        st.write(f"Here are the bottom {n_value} kreis based on prediction errors")
        output_df = df_mean_error.sort_values(by='error', ascending=True)[['kreis', 'error', 'ags5', 'bundesland']]
        st.dataframe(output_df.head(n_value).reset_index(drop=True))
    
    # Add the full table download link 
    st.markdown(get_table_download_link(df_mean_error, text="Download the full error table", filename="mean_error_table.csv"), unsafe_allow_html=True)

    st.markdown("""---""")

    ''' Analysis with Structural Data '''
    st.subheader("Structural Data Analysis")

    # Add structural data and combine with the error data 
    df_structural = pd.read_csv('data\df_final_stationary.csv', converters={'ags5': str} )
    df_structural['ags5'] = df_structural['ags5'].apply(fix_ags5)
    df_mixed = pd.merge(df_structural, df_mean_error[['ags5','bundesland']], on='ags5')

    st.dataframe(df_mixed)
    
    df_mixed['bundesland'] = df_mixed['bundesland'].astype('category')  

    # Select the structural variable and plot a graph 
    structure_var = st.selectbox("Select the variable to plot", options=list(df_mixed.columns)[6:], value=0)
    compare_error_in_two_groups(df_mixed, 'eligible_area')