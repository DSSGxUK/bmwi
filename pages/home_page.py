# Import necessary libraries 
from typing import Optional
from numpy import disp
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

    ''' Dashboard home page '''
    st.markdown("## Unemployment Rate Ranking")
    st.markdown('**Pro Tip**: click on the column to sort')

    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    The contents of this page are: 
    * [Unemployment Rate Ranking](#unemployment-rate-ranking)
        * [Kreise Rankings](#kreise-rankings)
        * [Bundesland Rankings](#bundesland-group-rankings)
    

    We can also put images here and anything under the sun. 

    """)

    # --- adds a horizontal line

# -- read in data ------------------------------------------

    df = pd.read_csv('data/pred_output_full.csv')
    date_cols = list(df.columns[4:])
    df['last_time%'] = (df[date_cols[-1]]-df[date_cols[-2]])/df[date_cols[-1]]*100
    df['last_year%'] = (df[date_cols[-1]]-df[date_cols[-13]])/df[date_cols[-1]]*100
    data_cols = date_cols + ['last_time%', 'last_year%']
    
# -- functions ----------------------------------------------

    def top_n(df, cols=[date_cols[-1], 'last_time%', 'last_year%'], n=10):
        return df.sort_values(cols, ascending=False)[:n][['ags5', 'bundesland', 'kreis']+cols]
    
    def top_n_group(df, col, group_col, n=100):
        return df.sort_values(col, ascending=False)[:n].groupby(group_col).count()[[col]].sort_values([col], ascending=False)

    def plot_pie(df, col, group_col, n):
        result_df = top_n_group(df, col, group_col, n=n)
        # set vals
        labels = [str(col) for col in result_df.index]
        sizes = result_df[col]
        explode = np.zeros(len(result_df))
        explode[0] = 0.1 #only explode max
        # plot
        fig, ax = plt.subplots(figsize=(10,10))
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', startangle=90)
        ax.axis('equal') 
        return fig
    
    def plot_bar(x_col, y_col):
        fig, ax = plt.subplots(figsize=(25,10))
        ax.bar(x_col, y_col)
        plt.xticks(rotation=60)
        if max(y_col)>=0.5:
            plt.axhline(y=0.5, alpha=0.3, c='r')
        return fig

# --------------------------------------------------------

    ''' Print the features of the data to sort '''
    
    st.markdown('### Kreise rankings')
    n1 = st.slider("Print top n results", min_value=10, max_value=100, step=10,
                    help='Print top n results by kreise.')
    cols_to_sort = st.multiselect("Select which columns to sort by", options=data_cols, 
                                    default=[date_cols[-1], 'last_time%', 'last_year%'],
                                    help='Fetching data based on first selected column, and displaying data for other selected columns.')
    kreise_ranking = top_n(df, cols=cols_to_sort, n=n1)
    # for display per suggestion
    if 'ags2' in kreise_ranking.columns:
        kreise_ranking.drop(columns=['ags2'], inplace=True)
    if 'ags5' in kreise_ranking.columns:
        kreise_ranking.drop(columns=['ags5'], inplace=True)
    st.dataframe(kreise_ranking)

# --------------------------------------------------------

    st.markdown('### Bundesland / Group rankings')
    n2 = st.slider("Print top n results", min_value=50, max_value=200, step=50, 
                    help='Get top n results of the column.')
    col_to_sort = st.selectbox("Select which column to sort by", options=data_cols, index=len(data_cols)-1)
    
    df_cat = pd.read_csv('data/categorical_groups.csv')
    df_group = pd.merge(df_cat, df, left_on='ags5', right_on='ags5')
    group_cols = ['bundesland'] + list(df_cat.columns)[2:] # crop out ags5
    # col_to_group = st.selectbox("Select which column to group by", options=group_cols, index=0)
    default_cols = [group_cols[2], group_cols[-1]]
    col_to_group = st.multiselect("Select which columns to group by", options=group_cols, default=default_cols)
    
    # get %
    result_df = top_n_group(df_group, col_to_sort, col_to_group, n=n2)
    n_group = df_group.groupby(col_to_group).count()[['kreis']]
    result_df = pd.merge(result_df, n_group, left_index=True, right_index=True)
    result_df['%counts'] = result_df[col_to_sort]/result_df['kreis']
    result_df.rename(columns={'kreis': '#kreis'}, inplace=True)
    st.dataframe(result_df)
    fig1 = plot_pie(df_group, col_to_sort, col_to_group, n=n2)
    result_df = result_df.sort_values('%counts', ascending=False)
    fig2 = plot_bar([str(col) for col in result_df.index], result_df['%counts'])
    
    st.markdown('**Pro Tip**: Visualizations work better when only grouping by one or a few columns.')
    display_fig1 = st.checkbox('Pie chart', help='Visualizes selected column counts by groups.')
    if display_fig1:
        st.pyplot(fig1)
    
    display_fig2 = st.checkbox('Bar chart', help='Visualizes selected column percentage counts by group.')
    if display_fig2:
        st.pyplot(fig2)