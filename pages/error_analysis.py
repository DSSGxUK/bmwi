# Import necessary libraries 
from numpy.lib.function_base import average
from numpy.lib.ufunclike import fix
import numpy as np 
import pandas as pd
import geopandas as gpd
import streamlit as st 

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import matplotlib.dates as mdates

import json 
import statsmodels.api as sm

# Custom modules 
from .utils import fix_ags5, get_table_download_link, plot_map

# DEFINE THE CONSTANTS
# Read the categorical data inside the file 
with open('data/metadata/data_types.json') as f:
    data = json.load(f)
    CAT_COLS = data["data_types"]["categorical"]

''' Functions for this page '''

# Function to get a dataframe of p-values and features 
def results_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf_lower = results.conf_int()[0]
    conf_higher = results.conf_int()[1]

    results_df = pd.DataFrame({"pvals":pvals})

    #Reordering...
    results_df = results_df[["pvals"]]
    
    # Set columns and index
    results_df.reset_index(inplace=True)
    results_df = results_df.rename(columns={'index': 'feature'})
    
    return results_df

# function to do that for a spesific column 
def compare_error_in_two_groups(df, column_name): 
    
    # Check if the variable is structural 
    if column_name in CAT_COLS: 
        kdefig, ax = plt.subplots(figsize=(10,6))
        sns.kdeplot(data=df, x="error", hue=column_name,  common_norm=False, ax=ax)
        st.pyplot(kdefig)

    else: 
        scatterfig, ax = plt.subplots(figsize=(10,6))
        sns.scatterplot(data=df, x="error", y=column_name, ax=ax)
        st.pyplot(scatterfig)

    
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
    title = f"Errors in prediction in Germany by Kreis {(date_string)}" 
    
    # numerical data_col
    fig, ax = plt.subplots(figsize=(30, 10))
    merged.plot(column='mape', scheme="quantiles",
                ax=ax, cmap='coolwarm', legend=True)
    ax.set_title(title, fontsize=15)

    return fig 

def app():
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Error Plots by Bundesland or Kreis](#error-plots-by-bundesland-or-kreis)
    - [Kreis Level Overview](#kreis-level-overview)
    - [Structural Data Analysis](#structural-data-analysis)
    - [Most Important Structure](#most-important-structure)

    """)
    
    st.markdown("## Error Analysis Page")
    st.write('There error analysis is an attempt to see where the unemployment rate predictions “fail”. The errors are Mean absolute percentage errors (MAPE), and each one represent how different the prediction is from the ground truth. The errors can be used to see which kreise were difficult to predict for, potentially suggesting the something spacial happened there. The errors can also be easily compared with the structural data, to identify the type of kreise that are harder to predict for.')

    # Load error data 
    error_data = pd.read_csv('data/errors/errors_VAR.csv')
    error_data['ags5'] = error_data['ags5'].apply(fix_ags5)

    ''' Data Addition '''
    # Add the bundesland kreis and ags2 to the data
    ags5_data = pd.read_csv('data/index.csv')
    ags5_data['ags5'] = ags5_data['ags5'].apply(fix_ags5)
    error_data = pd.merge(ags5_data[['ags5', 'kreis', 'bundesland', 'ags2']], error_data, on='ags5')
    
    # Fix date format 
    error_data['date'] = pd.to_datetime(error_data['date'], format = '%Y-%m-%d')

    # Fix ags2
    error_data['ags2'] = error_data['ags2'].astype('str')


    ''' Visualisation Section '''
    st.subheader("Error Plots by Bundesland or Kreis")
    
    # Make two columns if kreis then list of kreis else list of bundesland 
    # add all in both subcolumns by default
    col1, col2 = st.beta_columns(2)

    viz_area = col1.selectbox(label="Select Kreis or Bundesland", options=["Kreis", "Bundesland"], index=0)

    # Get the options based on column one 
    if viz_area == 'Kreis':
        dropdown_options = list(ags5_data['kreis'].unique())
    
    elif viz_area == 'Bundesland':
        dropdown_options = list(ags5_data['bundesland'].unique())
    
    # Create a multiselect for the subarea
    viz_sub_area = col2.multiselect("Select all or a particular geographical entitity", 
                                    options=dropdown_options, 
                                    default=[dropdown_options[0]])

    if viz_area=='Kreis':

        # filter data by kreis 
        filter_data = error_data[error_data['kreis'].isin(viz_sub_area)]
        g = sns.lineplot(data=filter_data, x="date", y="mape", hue='kreis')
        plt.title(f"{viz_area} Plot")
        g.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        st.pyplot()
        
    
    elif viz_area=='Bundesland':
    
        # filter data by kreis 
        filter_data = error_data[error_data['bundesland'].isin(viz_sub_area)]
        filter_data = filter_data.groupby(['date', 'bundesland'], as_index=False).mean()
        g = sns.lineplot(data=filter_data, x='date', y='mape', hue='bundesland')
        plt.title(f"{viz_area} Plot")
        g.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        st.pyplot()

    st.markdown("""---""")
    
    # ''' Error Map Viz '''
    st.markdown("### Error visualization on a Map")
    
    fig = plot_map(error_data, merge_col='ags5', data_col='error')
    st.pyplot(fig)
        
    st.markdown("""---""")
    

    ''' MEAN ERROR ANALYSIS '''
    
    df_mean_error = error_data.groupby(['ags5','ags2','bundesland','kreis'], as_index=False).mean()

    st.subheader("Kreis Level Overview")
    st.write("You can check the top-n or bottom-n kreis based on the prediction errors.")
    
    value_choice = st.radio("Select whether you want the highest or lowest values", options=["Highest", "Lowest"])
    n_value = st.slider("Select the number of values to be displayed", min_value=1, max_value=20, step=1, value=5)

    if value_choice == 'Highest':
        output_df = df_mean_error.sort_values(by='mape', ascending=False)[['kreis', 'mape', 'ags5', 'bundesland']]
        st.dataframe(output_df.head(n_value).reset_index(drop=True))
    else: 
        st.write(f"Here are the bottom {n_value} kreis based on prediction errors")
        output_df = df_mean_error.sort_values(by='mape', ascending=True)[['kreis', 'mape', 'ags5', 'bundesland']]
        st.dataframe(output_df.head(n_value).reset_index(drop=True))
    
    # Add the full table download link 
    st.markdown(get_table_download_link(df_mean_error, 
                                        text="Download the full error table", 
                                        filename="mean_error_table.csv", 
                                        excel=True), 
                                        unsafe_allow_html=True)

    st.markdown("""---""")

    ''' Analysis with Structural Data '''
    st.subheader("Structural Data Analysis")
    st.write("Compare the structural variable to the error values")


    # Add structural data and combine with the error data 
    df_structural = pd.read_csv('data/df_final_stationary.csv', converters={'ags5': str} )
    df_structural['ags5'] = df_structural['ags5'].apply(fix_ags5)
    
    # Fix structual cols 
    df_structural["urban_/_rural"] = np.where(df_structural["urban_/_rural"]==1, 'urban', 'rural')
    df_structural['eligible_area'] = np.where(df_structural['eligible_area']==1, 'eligible_area', 'not_eligible_area')
    df_structural['east_west'] = np.where(df_structural['east_west']==1, 'west', 'east')
    
    # Create a mixed dataset
    df_mixed = pd.merge(df_structural.drop(['cluster'], axis=1), df_mean_error.drop(['kreis', 'ags2'], axis=1), on='ags5')

    df_mixed['bundesland'] = df_mixed['bundesland'].astype('category')  

    # Select the structural variable and plot a graph 
    try: 
        index_val = list(df_mixed.columns).index('eligible_area') - 6
    except: 
        index_val = 1
    structure_var = st.selectbox("Select the variable to plot", options=list(df_mixed.columns)[6:], index=index_val)
    compare_error_in_two_groups(df_mixed, structure_var)

    st.markdown("""---""")
    st.subheader("Most important structure")

    run_lr = st.checkbox('Run linear regression model', value=False)
    
    if run_lr:
        st.write("Takes around 2 minutes to run...")
        df_mixed.set_index('ags5', drop=True, inplace=True)

        # Convert categorical columns to str type 
        for col in CAT_COLS: 
            df_mixed[col] = df_mixed[col].astype(str)

        # Create X and y 
        X = df_mixed.drop(['kreis','pred','mape', 'error', 'ground_truth'], axis=1)

        # Conditional column removal 
        if 'ags2' in X.columns and 'bundesland' in X.columns: 
            X = X.drop(['ags2'], axis=1)
        if 'labor_market_region' in X.columns: 
            X.drop(['labor_market_region'], axis=1, inplace=True)
        if 'labor_market_type' in X.columns: 
            X.drop(['labor_market_type'], axis=1, inplace=True)
        Y = np.log(df_mixed['mape'])
        X = pd.get_dummies(data=X, drop_first=True)

        # Fit the Linear Ression model 
        regr_model = sm.OLS(Y, X)
        results = regr_model.fit()

        # get p-values table
        res = results_summary_to_dataframe(results)

        # Display the results 
        high_low = st.radio("Select highest or lowest p-values", options=["Lowest", "Highest"])
        top_n = st.slider("Select the top-n features", min_value=1, max_value=10, step=1, value=5)

        if high_low == 'Highest':
            res.sort_values(by='pvals', inplace=True, ascending=False)
        else: 
            res.sort_values(by='pvals', inplace=True)

        st.write(f"The {high_low} features with the {high_low} p-values are:")
        st.dataframe(res.iloc[:top_n].reset_index(drop=True))
