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

    ''' Dashboard home page '''
    st.markdown("## Unemployment Ranking")
    st.markdown('**Pro Tip**: click on the column to sort')

    df = pd.read_csv('data/combined_df_pro.csv')
    date_cols = df.columns[4:]
    df['last_time%'] = (df[date_cols[-1]]-df[date_cols[-2]])/df[date_cols[-1]]*100
    df['last_year%'] = (df[date_cols[-1]]-df[date_cols[-13]])/df[date_cols[-1]]*100
    
    # funcs
    def top_n(df, cols=[date_cols[-1], 'last_time%', 'last_year%'], n=10):
        return df.sort_values(cols, ascending=False)[:n][['ags5', 'bundesland', 'kreis']+cols]
    
    def top_n_group(df, col, n=100):
        return df.sort_values(col, ascending=False)[:n].groupby('bundesland').count()[[col]].sort_values([col], ascending=False)

    def plot_pie(df, col, n):
        result_df = top_n_group(df, col, n=n)
        # set vals
        labels = result_df.index
        sizes = result_df[col]
        explode = np.zeros(len(result_df))
        explode[0] = 0.1 #only explode max
        # plot
        fig, ax = plt.subplots(figsize=(10,10))
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', startangle=90)
        ax.axis('equal') 
        return fig
    
    def plot_bar(x_col, y_col, hline=False):
        fig, ax = plt.subplots(figsize=(25,10))
        ax.bar(x_col, y_col)
        plt.xticks(rotation=60)
        if max(y_col)>=0.5:
            plt.axhline(y=0.5, alpha=0.3, c='r')
        return fig

    ''' Print the features of the data to sort '''
    
    st.markdown('### Kreise rankings')
    n1 = st.slider("Print top n results", min_value=10, max_value=100, step=10)
    cols_to_sort = st.multiselect("Select which columns to sort by", options=list(df.columns), 
                                    default=[date_cols[-1], 'last_time%', 'last_year%'])
    st.dataframe(top_n(df, cols=cols_to_sort, n=n1))

    st.markdown('### Bundesland rankings')
    n2 = st.slider("Print top n results", min_value=50, max_value=200, step=50)
    col_to_sort = st.selectbox("Select which column to sort by", options=list(df.columns), index=len(df.columns)-1)
    # get %
    n_kreise = pd.DataFrame(df['bundesland'].value_counts())
    result_df = top_n_group(df, col=col_to_sort, n=n2)
    result_df = pd.merge(result_df, n_kreise, left_index=True, right_index=True)
    result_df['%counts'] = result_df[col_to_sort]/result_df['bundesland']
    st.dataframe(result_df)
    fig1 = plot_pie(df, col_to_sort, n=n2)
    result_df = result_df.sort_values('%counts', ascending=False)
    fig2 = plot_bar(result_df.index, result_df['%counts'], hline=True)
    st.pyplot(fig1)
    st.pyplot(fig2)