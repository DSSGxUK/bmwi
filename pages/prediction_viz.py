from numpy.lib.ufunclike import fix
import streamlit as st 
import pandas as pd 

# Custom modules 
from .utils import fix_ags5, plot_line_wide, plot_map_wide

def app(): 
    
    ''' Dashboard sidebar '''
    st.sidebar.markdown("""
    --- 

    Page Outline: 
    - [Time-Series Line Plot](#line-plot)
    - [Map of Germany on Kreis-level](#map)
    """)

    st.markdown("## Prediction Visualisation Page")

    st.write("This page has been added to visualize the results of the predictions for the next three months.")

    ''' Read the predictions data '''
    pred_output = pd.read_csv('data/output.csv', index_col=0)

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
    st.write("\n")

    # get predictions by kreis 
    display_data = pd.merge(index_data, viz_data, on='ags5')
    kreis_name = st.multiselect("Select the Kreis to get predictions", options=list(display_data['kreis'].values))
    st.dataframe(display_data[display_data['kreis'].isin(kreis_name)].drop(columns=['ags2', 'ags5']))

    """
    This section doesn't work well because the date columns are messed up and we need to fix that.  
    """

    # line plot
    fig1 = plot_line_wide(full_data.drop(columns=['ags5']), kreis_name, 3, df_index='kreis')
    st.pyplot(fig1)

    # map
    st.markdown("### Map of Germany on Kreis-level")

    # Add the average of the predictions as a column for the plots 
    # average_cols = pd.DataFrame(pred_output.mean(axis=1))
    # average_cols.columns = ['predictions_average']
    # full_data = pd.concat([full_data, average_cols], axis=1)

    map_fig = plot_map_wide(full_data, 'ags5') # MAP gives error 
    st.pyplot(map_fig)
