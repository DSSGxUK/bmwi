# Import necessary libraries 
import pandas as pd 
import numpy as np 
import streamlit as st 
import matplotlib.pyplot as plt 

from arch.bootstrap import StationaryBootstrap

from warnings import catch_warnings
from warnings import filterwarnings

# Custom module 
from .utils import fix_ags5, get_table_download_link

## Required functions 
def func(x):
	return x

def app(): 

	''' Dashboard sidebar '''
	st.sidebar.markdown("""
	--- 

	Page Outline: 
	- [Confidence Intervals](#confidence-intervals)
	- [Visualisation](#visualisation-section)

	""")
 
	''' Page Introduction '''
	st.markdown('# Confidence Intervals')
	useful_links = '''
		[Documentation](https://dssgxuk.github.io/bmwi/steps/ci/) |
		[Tutorial Video](https://www.youtube.com/watch?v=9fVbfjKOgvQ&list=PLzWRWFPEUpHbwIHq0T6M72B1_5N04hD0Q&index=4)
		'''
	st.markdown(useful_links)

	st.write("""This section provides confidence intervals for the predictions
				that have been calculated in the previous section.""")

	
	# Get the confidence level
	level = st.slider("Select the confidence level", min_value=0.05, max_value=0.95, step=0.05, value=0.95)
	st.write("**Confidence Level**: ", level)

	st.write("Calculating the confidence intervals. The calculation can take up to 3 minutes...")
	# Read the relevant data (full pred data)
	full_data = pd.read_csv('data/pred_output_full.csv')

	# Fix ags5 
	full_data['ags5'] = full_data['ags5'].apply(fix_ags5) 

	''' Generate the confidence intervals '''

	# Define the confidence intervals dataframe (one for preds and one for all)
	ci_df = pd.DataFrame(columns =  ['date','ags5','lower', 'prediction', 'upper'])
	ci_df['date'] = pd.to_datetime(ci_df['date'], format = '%Y-%m-%d')
	ci_df_full = pd.DataFrame(columns =  ['date','ags5','lower', 'prediction', 'upper'])
	ci_df_full['date'] = pd.to_datetime(ci_df['date'], format = '%Y-%m-%d')

	kreis_list = list(full_data['ags5'].unique())
 
	@st.cache#(allow_output_mutation=True)
	def confidence_interval(ci_df, ci_df_full, kreis_list, full_data):

		# Loop through the data
		for kreis in kreis_list: 
			
			# get kreis data 
			kreis_data = full_data[full_data['ags5'] == kreis][list(full_data.columns[4:])]
			pred_ags5 = kreis_data.T[kreis_data.T.columns[0]].values    # convert the (1, 172) df to a list with 172 items
			
			# Define the bootstrap ci class and get the inveral 
			bs = StationaryBootstrap(10, pred_ags5)
			ci_ags5 = bs.conf_int(func, size=level)
			ci_ags5 = pd.DataFrame(ci_ags5).T
			
			# Add the interval to the dataframe 
			ci_ags5.columns = ['lower', 'upper']
			ci_ags5['prediction'] = list(pred_ags5)
			ci_ags5['ags5'] = kreis
			ci_ags5['date'] = list(kreis_data.columns)

			
			# Append to dataframe
			ci_df = ci_df.append(ci_ags5.iloc[-4:].reset_index(drop=True))
			ci_df_full = ci_df_full.append(ci_ags5.iloc[-25:].reset_index(drop=True)) 

		# Merge with full data to add bundesland and kreis 
		ci_df = pd.merge(ci_df, full_data[['ags5', 'kreis', 'bundesland']])
		ci_df_full = pd.merge(ci_df_full, full_data[['ags5', 'kreis', 'bundesland']])

		return ci_df, ci_df_full

	ci_df, ci_df_full = confidence_interval(ci_df, ci_df_full, kreis_list, full_data)
 
	# st.dataframe(ci_df)
	st.dataframe(ci_df.style.format({
							'lower': '{:.1f}', 
							'prediction': '{:.1f}', 
							'upper': '{:.1f}'
							}))

	# Save the data 
	ci_df.to_csv('data/confidence_intervals.csv', index=False)

	st.markdown(get_table_download_link(ci_df, 
										"Download the confidence intervals", 
										excel=True, 
										filename="confidence_intervals.csv"), unsafe_allow_html=True)

	''' Confidence Interval plots '''
	st.markdown("## Visualisation Section")
	# Select the plotting counties 
	kreis_to_plot = st.selectbox("Select which Kreis to visualize", options=list(ci_df['kreis'].unique()))
	
	# Filter by kreis 
	filter_data = ci_df[ci_df['kreis'] == kreis_to_plot]
	filter_data1 = ci_df_full[ci_df_full['kreis'] == kreis_to_plot]

	# Plot the ground truth in blue
	plt.plot(filter_data1['date'].iloc[:-3 or None], filter_data1['prediction'].iloc[:-3 or None], c='green')
	plt.plot(filter_data1['date'].iloc[-4:], filter_data1['prediction'].iloc[-4:])

	# Plot details 
	plt.xlabel("Dates")
	plt.ylabel(f"Unemployment Rate in {kreis_to_plot}")
	plt.title("Unemployment Rate Predictions with confidence intervals")
	plt.xticks(rotation=90)
	plt.ylim(0, ci_df_full['upper'].max()) 

	plt.fill_between(filter_data['date'], filter_data['lower'], filter_data['upper'], alpha=.3)
	st.pyplot()
