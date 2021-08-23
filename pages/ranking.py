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
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Kreise Rankings](#kreise-rankings)
    - [Grouped Rankings](#bundesland-group-rankings)

    """)

    ''' Dashboard home page '''
    st.markdown("## Unemployment Rate Ranking")
    st.write('This page shows the highest unemployment rates based on Kreis-level or a categorical group of your choice.')
    

# -- read in data ------------------------------------------

    df = pd.read_csv('data/pred_output_full.csv')
    date_cols = list(df.columns[4:])
    df['percentage difference compared to last month'] = (df[date_cols[-1]]-df[date_cols[-2]])/df[date_cols[-1]]*100
    df['percentage difference compared to last year'] = (df[date_cols[-1]]-df[date_cols[-13]])/df[date_cols[-1]]*100
    data_cols = date_cols + ['percentage difference compared to last month', 'percentage difference compared to last year']
    
# -- functions ----------------------------------------------

    def top_n(df, cols=[date_cols[-1], 'percentage difference compared to last month', 'percentage difference compared to last year'], n=10, ascending=False):
        return df.sort_values(cols, ascending=ascending)[:n][['ags5', 'bundesland', 'kreis']+cols]
    
    def top_n_group(df, col, group_col, n=100, ascending=False):
        return df.sort_values(col, ascending=ascending)[:n].groupby(group_col).count()[[col]].sort_values([col], ascending=ascending)

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
    st.markdown('**Pro Tip**: click on the column to sort')

    st.markdown('### Kreise rankings')
    n1 = st.slider("Print top n results", min_value=10, max_value=401, step=10,
                    help='Print top n results by kreise.')
    cols_to_sort = st.multiselect("Select which columns to sort by", options=data_cols, 
                                    default=[date_cols[-1], 'percentage difference compared to last month', 'percentage difference compared to last year'],
                                    help='Fetching data based on first selected column, and displaying data for other selected columns.')
    kreise_sort_direction = st.checkbox('Ascending order?', value=False, 
                                        help='default descending order shows the kreise with highest unemployment rates.')
    kreise_ranking = top_n(df, cols=cols_to_sort, n=n1, ascending=kreise_sort_direction)
    # for display per suggestion
    if 'ags2' in kreise_ranking.columns:
        kreise_ranking.drop(columns=['ags2'], inplace=True)
    if 'ags5' in kreise_ranking.columns:
        kreise_ranking.drop(columns=['ags5'], inplace=True)
    st.dataframe(kreise_ranking)
    
    kreise_ranking_text = '''
        The default shows the top 10 kreis based on their unemployment rate for the latest predicted month, 
        and is also sorted by the percentage change compared to last month and last year.
        '''
    kreise_ranking_section = st.beta_expander('Kreise Ranking Default Interpretation', False)
    kreise_ranking_section.markdown(kreise_ranking_text)


# --------------------------------------------------------

    st.markdown('### Bundesland / Group rankings')
    n2 = st.slider("Print top n results", min_value=50, max_value=401, step=50, 
                    help='Get top n results of the column.')
    col_to_sort = st.selectbox("Select which column to sort by", options=data_cols, index=len(data_cols)-1)
    group_sort_direction = st.checkbox('Ascending order?', value=False, 
                                        help='default descending order shows the groups with highest unemployment rates.')
    
    df_cat = pd.read_csv('data/categorical_groups.csv')
    df_group = pd.merge(df_cat, df, left_on='ags5', right_on='ags5')
    group_cols = ['bundesland'] + list(df_cat.columns)[2:] # crop out ags5
    # col_to_group = st.selectbox("Select which column to group by", options=group_cols, index=0)
    default_cols = [group_cols[2], group_cols[-1]]
    col_to_group = st.multiselect("Select which columns to group by", options=group_cols, default=default_cols)
    
    # get %
    result_df = top_n_group(df_group, col_to_sort, col_to_group, n=n2, ascending=group_sort_direction)
    n_group = df_group.groupby(col_to_group).count()[['kreis']]
    result_df = pd.merge(result_df, n_group, left_index=True, right_index=True)
    result_df['%counts'] = result_df[col_to_sort]/result_df['kreis']
    result_df.rename(columns={'kreis': '#kreis'}, inplace=True)
    st.dataframe(result_df)
    
    group_ranking_default_text = '''
        *For example, the default dataframe shows the top `50` kreise, 
        sorted by `percentage difference compared to last year`, grouped by `east_west` and `eligible area`.*

        Reading the first row (`west`-`eligible for funding`-group):
            
        - the first column, `percentage difference compared to last year`, means that in the top 50 kreise with highest percentage change in unemployment rate compared to last year, `21` of them belong to kreise in west Germany that are not eligible for funding.
            
        - the second column, `#kreis` means that there is a total of `93` (out of all 401) kreise that are kreise in west Germany that are not eligible for funding.
            
        - the third column, `%counts`, means that 21 kreise accounts for `22.58%` of all the kreise in the eligible-for-funding-West-Germany group.
            
        Note the number of multi-indices shown in the example. 
        Since `eligible_area` is a binary varaible with two categories, 
        and `east_west` is also a binary variable with two categories, 
        there should be a total of 4 category groups in the index rows. 
        
        However, the reason why not all combinations are shown is because some categories do not have Kreise in it. 
        
        _Sometimes, it could be useful to see what category groups are not in the top lists. 
        In this case, we see that there are no Kreise in East Germany not eligible for funding 
        in the top 50 highest unemployment rates._
        '''
    group_ranking_section = st.beta_expander('Grouped Ranking Default Interpretation', False)
    group_ranking_section.markdown(group_ranking_default_text)
    
    fig1 = plot_pie(df_group, col_to_sort, col_to_group, n=n2)
    result_df = result_df.sort_values('%counts', ascending=False)
    fig2 = plot_bar([str(col) for col in result_df.index], result_df['%counts'])
    
    
    st.markdown('**Pro Tip**: Visualizations work better when only grouping by one or a few columns.')
    display_fig1 = st.checkbox('Pie chart', help='Visualizes selected column counts by groups.')
    if display_fig1:
        st.pyplot(fig1)
        
        pie_text = '''
            *As shown above, the default pie chart visualizes the percentage each category group takes 
            in total from the `percentage difference compared to last year` column. For example, the not-eligible-for-funding-West-Germany group 
            accounts for `21` out of the total of `50` top kreise, 
            therefore, it takes up `42%` as shown in the pie chart.*
            '''
        pie_section = st.beta_expander('Pie Chart Interpretation', False)
        pie_section.markdown(pie_text)
    
    display_fig2 = st.checkbox('Bar chart', help='Visualizes selected column percentage counts by group.')
    if display_fig2:
        st.pyplot(fig2)
        
        bar_text = '''
            *As shown above, the default bar chart visualizes the percentage 
            the top 50 kreise took up for its whole category group. 
            Note that you could use the two arrows on the top right to expand the plot if the
            display column names is too small on your screen.*
            '''
        bar_section = st.beta_expander('Bar Chart Interpretation', False)
        bar_section.markdown(bar_text)