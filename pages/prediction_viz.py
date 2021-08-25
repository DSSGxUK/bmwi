from numpy.lib.ufunclike import fix
import streamlit as st 
import pandas as pd 

# Custom modules 
from .utils import fix_ags5, plot_line_wide, plot_map_bundesland, plot_map_wide, get_table_download_link

def app(): 
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Time-Series Line Plot](#time-series-line-plot)
    - [Map of Germany on Kreis-level](#map-of-germany-on-kreis-level)
    - [Map of Bundesland on Kreis-level](#map-of-bundesland-on-kreis-level)
    """)

    st.markdown("## Prediction Visualisation Page")

    st.write("This page has been added to visualize the results of the predictions for the next three months.")

    ''' Read the predictions data '''
    pred_output = pd.read_csv('data/prediction_output_from_model_page.csv', index_col=0)

    # Reset the prediction index 
    pred_output.reset_index(inplace=True)
    pred_output.rename(columns={'index':'ags5'}, inplace=True)

    ''' Add visulaisations of the unemployment predictions '''
    
    # Read the index data 
    index_data = pd.read_csv('data/index.csv')

    # Load wide df 
    wide_df = pd.read_csv('data/main_data.csv')
    wide_df.columns = ['ags5'] + list(wide_df.columns[1:])
    # wide_df.set_index('ags5', inplace=True)
    wide_df['ags5'] = wide_df['ags5'].apply(fix_ags5)

    # Fix ags5
    viz_data = pred_output.copy()
    viz_data['ags5'] = viz_data['ags5'].apply(fix_ags5)
    index_data['ags5'] = index_data['ags5'].apply(fix_ags5)
    
    # Merge with the output data 
    full_data = pd.merge(wide_df, viz_data, on='ags5')
    full_data = pd.merge(index_data, full_data, on='ags5')
    
    # Sync with home page
    full_data.to_csv('data/pred_output_full.csv', index=False)

    st.markdown("### Time-Series Line Plot") 
    st.markdown('''
                _The Kreise options are listed in alphabetical order.
                You can also directly type the name of the Kreis 
                you want to visualize in the box._
                ''')

    # get predictions by kreis 
    display_data = pd.merge(index_data, viz_data, on='ags5')
    kreis_options = sorted(list(display_data['kreis'].values))
    kreis_name = st.multiselect("Select the Kreis to get predictions", 
                                options=kreis_options, 
                                default=[kreis_options[0]])
    # resulting df
    viz_output = display_data[display_data['kreis'].isin(kreis_name)].drop(columns=['ags2', 'ags5'])
    
    # get viz output columns to be formated 
    viz_output_cols = viz_output.columns[2:]
    st.dataframe(viz_output.style.format({
            viz_output_cols[0]: '{:.2f}', 
            viz_output_cols[1]: '{:.2f}', 
            viz_output_cols[2]: '{:.2f}'
            }))

    # Download links 
    st.markdown(get_table_download_link(viz_output, 
                                        text="Download the subset ranking data", 
                                        filename="subset_ranking_data.csv", 
                                        excel=True),
                                        unsafe_allow_html=True)

    """
    This section doesn't work well because the date columns are messed up and we need to fix that.  
    """

    # customize start date
    date_cols = list(full_data.columns)[4:]
    default_start_date = date_cols[-13] #one year
    default_start_date_index = date_cols.index(default_start_date)
    # the start date cant be less than 6 months because of date labels on x-axis
    start_date = st.selectbox("Pick start date:", options=date_cols[:-6], 
                              index=default_start_date_index)
    start_date_index = date_cols.index(start_date)
    
    # crop dataframe with start date
    index_cols = list(full_data.columns)[:4]
    selected_cols = date_cols[start_date_index:]
    cropped_data = full_data[index_cols+selected_cols] 
    
    # line plot
    fig1 = plot_line_wide(cropped_data.drop(columns=['ags5']), kreis_name, 3, df_index='kreis')
    st.pyplot(fig1)

    # Add the average of the predictions as a column for the plots 
    # average_cols = pd.DataFrame(pred_output[pred_output.columns[1:]].mean(axis=1))
    # average_cols.columns = ['predictions average']
    # full_data = pd.concat([full_data, average_cols], axis=1)
    # partial_data = full_data.iloc[:,-4:]
    # partial_data['ags5'] = full_data['ags5']
    
    # partial_data = 
    
    # map
    st.markdown("### Map of Germany on Kreis-level")
    map_fig = plot_map_wide(full_data, 'ags5') 
    st.pyplot(map_fig)
    
    # map
    st.markdown("### Map of Bundesland on Kreis-level")
    map_fig2 = plot_map_bundesland(full_data, 'ags5') 
    st.pyplot(map_fig2)
