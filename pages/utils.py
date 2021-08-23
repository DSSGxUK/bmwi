''' Functions that need to be used regularly '''

# Import necessary libraries 
from numpy.core.fromnumeric import size, sort
import pandas as pd 
import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt 
import base64
import geopandas as gpd
from io import BytesIO

''' Data Fix Functions'''
def fix_ags5(x):
    """Function to fix the format of ag5 """
    if len(str(x))==4:
        return '0'+str(x)
    else:
        return str(x)

''' File Upload Functions '''
def read_single_file():
    """Function to read a single csv file
    Returns:
        data: Returns a dataframe of the uploaded csv file
    """
    # Code to read a single file 
    uploaded_file = st.file_uploader(
        "The app loads the last-used dataset by default.", 
        type = ['csv', 'xlsx'])
    global data
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)    # encoding='latin_1' : can be added to read non-English Data
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file, encoding='latin_1')
    else:
        data = pd.read_csv('data/main_data.csv', encoding='latin_1')
        if data.columns[0]=='Unnamed: 0':
            data = pd.read_csv('data/main_data.csv', encoding='latin_1', index_col=0)
    return data

''' Data Filtering methods '''
def drop_selected_variables(df):
    """Function to drop selected variables in a dataframes
    Args:
        df (DataFrame): dataframe to be filtered
    Returns:
        df: Returns the filtered data
    """
    st.subheader("Select non-important variables")
    variables_to_be_dropped = st.multiselect(label="Which variables would you like to drop?", 
                                            options=list(df.columns), 
                                            help="If none are selected, then all variables will be used for PCA.")
    # Drop the variables from the data
    if variables_to_be_dropped:
        df.drop(variables_to_be_dropped, axis=1, inplace=True)
    return df


''' Visualisation Functions '''
# Function to plot a map
def plot_map(data, merge_col, data_col, cat_col=False):
    """
    ## Assumes long format, i.e. dates are in one columns
    Input variables:
    - data: pd.df; dataframe info to plot the map
    - merge_col: str; the ags5 col to merge with gdf
    - data_col: str; col to map
    - cat_col: bool; whether data_col is categorical, default to False
    Return:
    - fig: plt.fig; the plot figure
    """
    # read the map coordinates data 
    gdf = gpd.read_file('georef-germany-kreis/georef-germany-kreis-millesime.shp')
    
    # merge the coords with the data 
    try:
        merged = pd.merge(data, gdf, left_on=merge_col, right_on='krs_code')
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
    
    # annotation
    ## they can type in the bundesland or kreis they want to annotate
    bundeslands = list(merged['bundesland'].unique())
    bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
            '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
            '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
            '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
    kreise = list(merged['kreis'])
    regions_to_annotate = st.multiselect('Type in the Kreis or whole Bundesland to annotate:',
                                         options=sorted(bundeslands+kreise),
                                         default=['Berlin', 'Hamburg', 'München, Kreis'])
    
    # plot
    # (1) categorical data_col
    if cat_col == True:
        fig, ax = plt.subplots(figsize=(25,15))
        merged.plot(column=data_col, #scheme="NaturalBreaks",
                    #scheme='UserDefined', classification_kwds={'bins':clusters},
                    ax=ax, cmap='Set3', categorical=True, legend=True)
        ax.set_title(f'{data_col} in Germany by County', fontsize=15)
    
    # (2) numerical data_col
    else:
        fig, ax = plt.subplots(figsize=(25,15))
        merged.plot(column=data_col, scheme="quantiles",
                    ax=ax, cmap='coolwarm', legend=True)
        ax.set_title(f'{data_col} in Germany by County', fontsize=15)

    
    fontsize = 15
    for region in regions_to_annotate:
        # bundesland
        if region[0].isdigit():
            merged_ags = merged[merged['ags2']==int(region[:2])]
            for i in merged_ags.index:
                ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
                        f'{merged_ags["kreis"][i]}\n{round(merged_ags[data_col][i], 2)}', fontsize=fontsize)
        
        # kreise
        else:
            merged_kreis = merged[merged['kreis']==region]
            
            # highlight kreis boundary
            merged_kreis.boundary.plot(ax=ax, color='#FFFF00', linewidth=3, hatch="///")
            
            # annotate text
            for i in merged_kreis.index:
                ax.text(merged_kreis.longitude[i], merged_kreis.latitude[i],
                        f'{merged_kreis["kreis"][i]}\n{round(merged_kreis[data_col][i], 2)}', 
                        fontsize=fontsize, color='k', weight='bold')
    
    
    # # check if the labels need to be added 
    # labels = st.radio("Show all labels?", options=["Yes", "No"], index=1)

    # # check if certain labels need to be added -- by region
    # label_ags = st.radio("Show labels by region?", options=["Yes", "No"], index=1)
    # if label_ags == "Yes": 
    #     bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
    #         '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
    #         '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
    #         '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
    #     txt_to_display_ags = st.selectbox("Select which Bundesland to annotate",
    #                                 options=bundeslands, index=0)
    
    # # check if certain labels need to be added -- by stats
    # if cat_col==False:
    #     label_stats = st.radio("Show labels by stats?", options=["Yes", "No"], index=1)
    #     if label_stats == "Yes": 
    #         stats = ['mean', 'min', '25%', '50%', '75%', 'max']
    #         stats_values = merged[data_col].describe()[stats].sort_values()
    #         st.write(stats_values)
    #         txt_to_display_stats = st.slider("Select a range of values", 
    #                                         float(stats_values['min']), float(stats_values['max']), 
    #                                         (float(stats_values['25%']), float(stats_values['75%'])))
    # # check if certain labels need to be added -- by category
    # if cat_col==True:
    #     label_cls = st.radio("Show labels by category?", options=["Yes", "No"], index=1)
    #     if label_cls == "Yes": 
    #         txt_to_display_cls = st.selectbox("Select which category to annotate",
    #                                     options=sorted(list(data[data_col].astype(str).unique())), 
    #                                     index=0)
    
    # # annotation filters
    # # (1) by ags
    # if label_ags == "Yes": 
    #     merged_ags = merged[merged['ags2']==int(txt_to_display_ags[:2])]
    #     for i in merged_ags.index:
    #         ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
    #                 f'{merged_ags["kreis"][i]}\n{merged_ags[data_col][i]}', fontsize=10)
    # # (2) add by stats
    # if cat_col==False:
    #     if label_stats == "Yes": 
    #         # get filtered df
    #         merged_stats = merged[
    #             (merged[data_col]>=txt_to_display_stats[0]) & 
    #             (merged[data_col]<=txt_to_display_stats[1])]
    #         # add text with filters
    #         for i in merged_stats.index:
    #             ax.text(merged_stats.longitude[i], merged_stats.latitude[i],
    #                     f'{merged_stats["kreis"][i]}\n{merged_stats[data_col][i]}', fontsize=10)
    # # (3) add by category
    # if cat_col==True:
    #     if label_cls == "Yes": 
    #         merged_cls = merged[merged[data_col]==txt_to_display_cls]
    #         for i in merged_cls.index:
    #             ax.text(merged_cls.longitude[i], merged_cls.latitude[i],
    #                     f'{merged_cls["kreis"][i]}\n{merged_cls[data_col][i]}', fontsize=10)
    # # (4) add all text
    # if labels == "Yes": 
    #     for i in range(len(merged)):
    #         ax.text(merged.longitude[i], merged.latitude[i],
    #                 f'{merged["kreis"][i]}\n{merged[data_col][i]}', fontsize=10)
    
    return fig

def plot_map_wide(data, merge_col):
    
    # read the map coordinates data 
    gdf = gpd.read_file('georef-germany-kreis/georef-germany-kreis-millesime.shp')
    index = pd.read_csv('data/index.csv')
    
    # merge the coords with the data 
    try:
        merged = pd.merge(data, gdf, left_on=merge_col, right_on='krs_code')
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
    date_cols = merged.columns[4:-12]

    # useful stats
    merged['predictions average'] = merged[date_cols[:-3]].mean(axis=1)
    merged['difference compared to last month'] = merged[date_cols[-1]]-merged[date_cols[-2]]
    merged['difference compared to last year'] = merged[date_cols[-1]]-merged[date_cols[-13]]
    merged['percentage difference compared to last month'] = (merged[date_cols[-1]]-merged[date_cols[-2]])/merged[date_cols[-1]]*100
    merged['percentage difference compared to last year'] = (merged[date_cols[-1]]-merged[date_cols[-13]])/merged[date_cols[-1]]*100
    stats_cols = ['predictions_average', 
                  'difference compared to last month', 'difference compared to last year', 
                  'percentage difference compared to last month', 'percentage difference from last year']
    
    num_cols = list(date_cols) + stats_cols
    num_cols = num_cols[-9:]
    latest_date = num_cols.index('predictions_average')
    col = st.selectbox("Select a column", options=num_cols, index=latest_date)

    # plot
    fig, ax = plt.subplots(figsize=(25,15))
    merged.plot(column=col, scheme="quantiles",
                ax=ax,
                cmap='coolwarm', legend=True)
    ax.set_title(f'{col} in Germany on Kreis-level',fontsize=15)

    # annotation
    ## they can type in the bundesland or kreis they want to annotate
    bundeslands = list(merged['bundesland'].unique())
    bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
            '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
            '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
            '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
    kreise = list(merged['kreis'])
    regions_to_annotate = st.multiselect('Type in the Kreis or whole Bundesland to annotate:',
                                         options=sorted(bundeslands+kreise),
                                         default=['Berlin', 'Hamburg', 'München, Kreis'])
    
    fontsize = 15
    for region in regions_to_annotate:
        # bundesland
        if region[0].isdigit():
            merged_ags = merged[merged['ags2']==int(region[:2])]
            for i in merged_ags.index:
                ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
                        f'{merged_ags["kreis"][i]}\n{round(merged_ags[col][i], 2)}', fontsize=fontsize)
        
        # kreise
        else:
            merged_kreis = merged[merged['kreis']==region]
            
            # highlight kreis boundary
            merged_kreis.boundary.plot(ax=ax, color='#FFFF00', linewidth=3, hatch="///")
            
            # annotate text
            for i in merged_kreis.index:
                ax.text(merged_kreis.longitude[i], merged_kreis.latitude[i],
                        f'{merged_kreis["kreis"][i]}\n{round(merged_kreis[col][i], 2)}', 
                        fontsize=fontsize, color='k', weight='bold')
    
    # # (1) by bundesland
    # label_ags = st.radio("Show labels by Bundesland?", options=["Yes", "No"], index=1)
    # if label_ags == "Yes": 
    #     bundeslands = ['1 Schleswig-Holstein', '2 Hamburg', '3 Niedersachsen', '4 Bremen',
    #         '5 Nordrhein-Westfalen', '6 Hessen', '7 Rheinland-Pfalz', '8 Baden-Wurttemberg',
    #         '9 Freistaat Bayern', '10 Saarland', '11 Berlin', '12 Brandenburg',
    #         '13 Mecklenburg-Vorpommern', '14 Sachsen', '15 Sachsen-Anhalt', '16 Thuringen']
    #     txt_to_display_ags = st.selectbox("Select which Bundesland to annotate",
    #                                 options=bundeslands, index=0)
    #     merged_ags = merged[merged['ags2']==int(txt_to_display_ags[:2])]
    #     for i in merged_ags.index:
    #         ax.text(merged_ags.longitude[i], merged_ags.latitude[i],
    #                 f'{merged_ags["kreis"][i]}\n{round(merged_ags[col][i], 2)}', fontsize=10)

    # # (2) by numerical stats
    # label_stats = st.radio("Show labels by stats?", options=["Yes", "No"], index=1, 
    #                     help="Show labels of Kreise in a particular range of values.")
    # if label_stats == "Yes": 
    #     stats = ['mean', 'min', '25%', '50%', '75%', 'max']
    #     stats_values = merged[col].describe()[stats].sort_values()
    #     st.write(stats_values)
    #     txt_to_display_stats = st.slider("Select a range of values", 
    #                                     float(stats_values['min']), float(stats_values['max']), 
    #                                     # (float(stats_values['25%']), float(stats_values['75%'])))
    #                                     (float(stats_values['75%']), float(stats_values['max'])))
    #     # get filtered df
    #     merged_stats = merged[(merged[col]>=txt_to_display_stats[0]) & (merged[col]<=txt_to_display_stats[1])]
    #     # add text with filters
    #     for i in merged_stats.index:
    #         ax.text(merged_stats.longitude[i], merged_stats.latitude[i],
    #                 f'{merged_stats["kreis"][i]}\n{round(merged_stats[col][i], 2)}', fontsize=10)

    # # (3) add all text
    # labels = st.radio("Show all labels?", options=["Yes", "No"], index=1)
    # if labels == "Yes": 
    #     for i in range(len(merged)):
    #         ax.text(merged.longitude[i], merged.latitude[i],
    #                 f'{merged["kreis"][i]}\n{round(merged[col][i], 2)}', fontsize=10)
                    
    return fig


# Function to plot a (time-series) line plot
def plot_line_long(df, x_col, y_col, filter_col=None, filter_val=None):
    '''
    Input data: date is one single column
    '''
    fig, ax = plt.subplots(figsize=(50,20))
    if (filter_col==None) or (filter_val==None):
        df.plot(x_col, y_col, ax=ax)
        ax.set_title(f'{y_col} in Germany')
    else:
        filter_df = df[df[filter_col]==filter_val]
        filter_df.plot(x_col, y_col, ax=ax)
        ax.set_title(f"{filter_val}'s {y_col} in Germany")
    return fig

def plot_line_wide(df, filter_kreis, num_pred, df_index='ags5'):
    '''
    Input data: columns are dates
    '''
    fig, ax = plt.subplots(figsize=(30,10))
    filter_df = df.copy()
    
    # drop non-date cols
    if 'bundesland' in filter_df.columns:
        filter_df.drop(columns=['bundesland'], inplace=True)
    if 'ags2' in filter_df.columns:
        filter_df.drop(columns=['ags2'], inplace=True)
    
    # set index col
    filter_df = filter_df.set_index(df_index)
    dates = [str(date) for date in filter_df.columns]
    filter_df.columns = dates
    for kreis in filter_kreis:
        plt.plot(filter_df[dates[:-num_pred]].loc[kreis], label=kreis)
        plt.plot(filter_df[dates[-(num_pred+1):]].loc[kreis], 'r')
    
    # line between truth and prediction
    plt.axvline(x=filter_df.columns[-(num_pred+1)], alpha=0.5, linestyle='--', c='k')
    
    # date labels on x-axis
    n_cols = len(list(df.columns))-4
    interval = int(n_cols/6)
    ax.set_xticks(list(range(0, len(dates), interval)))
    ax.set_xticklabels(dates[::interval])
    ax.legend()
    
    return fig

# Funtion to plot a histogram 
def data_histogram(column, no_of_bins, minimum=None, maximum=None):
    # default vals
    if minimum is None:
        minimum = min(column)
    if maximum is None:
        maximum = max(column)
    # calculate the histogram edges
    bin_edges = np.arange(minimum, maximum, (maximum - minimum)/no_of_bins)
    # plot
    plt.figure(figsize=(5,5))
    plt.hist(column, bin_edges)
    plt.show()



''' Misc. Functions '''

# Function to convert the german phrases to english 
@st.cache() # caching to reduce time 
def get_english_term(german_phrase):
    # This is loading the data each time so there has to be a smarter way to do this. Might help reducing time. 
    translate = pd.read_csv('data/metadata/col_translate.csv')
    german_phrase = german_phrase.upper()
    try: 
        return translate[translate['Variable_name'] == german_phrase]['variable_english'].values[0] 
    except: 
        return german_phrase.lower()

# Function to convert data into download link
def get_table_download_link(df, text, excel=False, filename="final.csv"):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    params:  
        dataframe
        text: Text to be printed in the file download option
        filename: Filename to be downloaded [optional]
    returns: href string
    """
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    if excel == False: 
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    
    elif excel == True: 
        val = to_excel(df)
        b64 = base64.b64encode(val)  # val looks like b'...'
        href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename[:-4]}.xlsx">{text}</a>' # decode b'abc' => abc
    
    return href


''' Data Functions '''
def fix_day(date):
    return date.replace(day=1)

def long_merge_to_wide(sheet_data, sheet_name):
    '''
    Input:
        - sheet_data: list of dataframes in long format
        - sheet_name: list of sheet names corresponding to sheet_data
        - Note: long format in one variable data: date is one column, #rows = (401 kreis) * (time range)
    Output:
        - wide format merged multi-variable data: apart from index columns (ags, date), each column is a feature
    '''
    # sanity check
    if len(sheet_data) != len(sheet_name):
        return 'length of sheet_data and sheet_name does not match'
    
    # fix and unify sheet formats
    for i in range(len(sheet_data)):
        # convert time column to datetime
        if 'time_stamp' in sheet_data[i].columns:
            if len(str(sheet_data[i]['time_stamp'][0]))>6:   #not only year
                sheet_data[i]['time_stamp'] = pd.to_datetime(sheet_data[i]['time_stamp'])
        # change column name "value" in long format to actual variable name
        sheet_data[i].rename(columns={'value': f'{sheet_name[i]}'}, inplace=True)
    
    # merge sheets
    merged_sheet = sheet_data[0]
    for i in range(1, len(sheet_data)):
        # merge by outer so because data can have different available time frames
        try:
            merged_sheet = pd.merge(merged_sheet, sheet_data[i], left_on=['ags5', 'time_stamp'], right_on=['ags5', 'time_stamp'], how='outer')
        except KeyError: #left data already has time_stamp column renamed
            merged_sheet = pd.merge(merged_sheet, sheet_data[i], left_on=['ags5', 'date'], right_on=['ags5', 'time_stamp'], how='outer')
    
    # final minor fixes
    merged_sheet.rename(columns={'time_stamp': 'date'}, inplace=True)
    merged_sheet.sort_values(['ags5', 'date'], inplace=True)
    merged_sheet.reset_index(inplace=True, drop=True)
    
    return merged_sheet



def wide_merge_to_long(sheet_data, sheet_name):
    '''
    Input:
        - sheet_data: list of dataframes in wide format
        - sheet_name: list of sheet names corresponding to sheet_data
        - Note: wide format one variable data: all columns are dates, 401 rows representing each kreis
    Output:
        - long format multi-variable data: apart from index columns (ags, variable), each column is a date
    '''
    # sanity check
    if len(sheet_data) != len(sheet_name):
        return 'length of sheet_data and sheet_name does not match'
    
    # fix and unify sheet formats
    for i in range(len(sheet_data)):
        # add a column named variable and put the variable name in
        sheet_data[i]['variable'] = sheet_name[i]
        # get ags5 column
        sheet_data[i].reset_index(inplace=True)
        sheet_data[i].rename(columns={'index': 'ags5'}, inplace=True)

    # merge sheets
    merged_sheet = pd.concat(sheet_data, ignore_index=True)
    
    # final minor fixes
    merged_sheet.sort_values(['variable', 'ags5'], inplace=True)
    merged_sheet.reset_index(inplace=True, drop=True)
    
    # TypeError: '<' not supported between instances of 'Timestamp' and 'str'
    #merged_sheet = merged_sheet.reindex(sorted(merged_sheet.columns), axis=1)
    merged_sheet_index = merged_sheet[['ags5', 'variable']]
    merged_sheet_data = merged_sheet.drop(columns=['ags5', 'variable'])
    merged_sheet_data = merged_sheet_data.reindex(sorted(merged_sheet_data.columns), axis=1)
    merged_sheet_sorted = pd.merge(merged_sheet_index, merged_sheet_data, right_index=True, left_index=True)
    
    return merged_sheet_sorted



def long_merge2(df_long, df_final_long, varname):
    df_final_long['date'] = pd.to_datetime(df_final_long['date']).dt.date
    df_final_long = df_final_long[df_final_long['variable']!=varname]
    df_long['ags2'] = df_long['ags5'].astype(str).str[:-3]
    df_long.rename(columns={f'{varname}': "value"}, inplace=True)
    df_long['variable'] = f'{varname}'
    df_long = df_long[['ags2', 'ags5', 'variable', 'date', 'value']]
    df_final_long = pd.concat([df_final_long, df_long], ignore_index=True)
    return df_final_long

def wide_merge2(df_wide, df_final_wide, varname):
    # fix and convert
    df_wide['date'] = pd.to_datetime(df_wide['time_stamp'], format='%Y-%m-%d').apply(fix_day).dt.date
    df_final_wide['date'] = pd.to_datetime(df_final_wide['date']).dt.date
    df_wide['ags5'] = df_wide['ags5'].apply(fix_ags5)
    df_final_wide['ags5'] = df_final_wide['ags5'].apply(fix_ags5)
    # select and merge
    df_wide = df_wide[['ags5', 'date', 'value']]
    df_wide.columns = ['ags5', 'date', f'{varname}']
    #df_final_wide = df_final_wide.drop(columns=[f'{varname}'])
    df_final_wide = pd.merge(df_final_wide, df_wide, on=['ags5', 'date'])
    return df_final_wide