# Import libraries 
import pandas as pd

class Data():
    
    def __init__(self, dataFrame, file_format):
        '''
        INPUTS:
        ------
        dataFrame: pandas dataframe containing no null values in either wide or long format
        file_format: either 'wide' or 'long'
            'Wide': must have dates as columns, ags5s as index
            'Long': Must have 3 columns: ['ags5', 'date', 'unemployment_rate']
        
        Constraints:
        ------------
        input csv file must have a column called ags5 for both long and wide
        if the input csv is wide: # TODO
        if the input csv is long, there must be a column called 'unemployment_rate' and a column called 'date'      
        '''
        
        ## imports
        import pandas as pd
        
        # convert to lowercase
        file_format = file_format.lower()
        assert file_format == 'wide' or file_format == 'long'
        
        if file_format == 'long':
            
            data_long = dataFrame
            
            # do all the checks
            assert all(necessary_col in data_long.columns for necessary_col in ['ags5', 'date', 'unemployment_rate'])
            
            # process:
            data_long = data_long[['ags5', 'date', 'unemployment_rate']] # throw away other columns
            data_long['ags5'] = data_long['ags5'].apply(self.fix_ags5)
        
            # save:
            self.data_long = data_long
            
        elif file_format == 'wide':
            # TODO
            data_wide = dataFrame
            
            # process
            data_wide.index = [self.fix_ags5(ags5) for ags5 in data_wide.index]
            
            # save
            self.data_wide = data_wide            
            
        
        
    def long(self):
        '''
        Returns:
        --------
        A dataframe with columns: 'ags5', 'date', 'unemployment_rate'
        '''
        try:
            return self.data_long
        except AttributeError:
            # create the long version
            data_long = pd.DataFrame(   
                [(self.data_wide.index[i], self.data_wide.columns[j], self.data_wide.iloc[i, j]) 
                for i in range(len(self.data_wide.index)) 
                for j in range(len(self.data_wide.columns))])
            
            data_long.columns = ['ags5', 'date', 'unemployment_rate']
            
            self.data_long = data_long # store
            
            return self.data_long
        
    def wide(self):
        '''
        Returns:
        --------
        A dataframe with ags5 as index and dates as columns
        '''
        
        try:
            return self.data_wide
        
        except AttributeError:
            # create the wide version
            all_dates = self.data_long['date'].unique()
            all_ags5 = self.data_long['ags5'].unique()
            all_dates.sort()
            all_ags5.sort()
            grouped_data_long = self.data_long.groupby('date')
            
            data_wide = pd.DataFrame(index=all_ags5)
            for date in all_dates:
                df_of_date = grouped_data_long.get_group(date)
                df_of_date.set_index('ags5', inplace=True, drop=True)
                df_of_date = df_of_date.drop('date', axis=1)
                data_wide = data_wide.merge(df_of_date, left_index=True, right_index=True)
            
            data_wide.columns = all_dates
            
            self.data_wide = data_wide
            
            return data_wide
        
        
    ## util functions: 
    def fix_ags5(self, x):
        """Function to fix the format of ag5 """
        if len(str(x))==4:
            return '0'+str(x)
        else:
            return str(x)

class AbstractModel():
    
    def __init__(self, output_save_location, params=None, unemploymentRateData=None, otherData=None, model_save_location=None):
        '''
        Inputs:
        -------
        pretrained: set True if you want to load a model, set false of you want to retrain a model
        output_save_location: location, including the csv file where the outputs are stored
        model_save_location: currently only used by neural network, i.e. used for all models which you don't do walk forward validation or any kind of retraining
        if model_save_location = None:
            i.e. we do walk forward validation
            params: params of the model, a dictionary
            unemploymentRateData: an instance of the Data class containing the unemployment rate, use it to train a model
            otherData: a dictionary containing other data, e.g. cluster values for VAR model
        '''
        
        import numpy as np
        import pandas as pd
        
        self.output_save_location = output_save_location
        self.params = params
        
        if model_save_location is None:
            ## we use walk forward validation i.e. retraining happens
            assert params is not None
            assert unemploymentRateData is not None
            
            self.unemploymentRateData = unemploymentRateData
            self.otherData = otherData
        else:
            ## a fixed network without retraining, e.g a NN 
            self.model_save_location = model_save_location
            self.unemploymentRateData = unemploymentRateData
            self.otherData = otherData
    
    
    ## abstractmethod
    def wf_pred(self, data, otherData, n, params):
        '''
        Inputs:
        -------
        self: contains all the training data, params etc
        n: number of timestamps to pred, with walk forward validation
        params: can contain THE IMPORTANT PARAMETER end_date. So check if this key exists, if it does, crop the training data from data accordingly
        
        '''
        pass
    
    
    def getWalkForwardPred(self, n):
        '''
        Inputs:
        -------
        n: number of timestamps to pred, with walk forward validation
        '''
        
        ur_data_long = self.unemploymentRateData.long()
        
        if 'end_date' in self.params.keys():
            last_date_train = self.params['end_date']
        else:
            last_date_train = max(ur_data_long['date'])
        
        '''1. Check if it is already calculated'''
        ## read the file
        try:
            output_csv = pd.read_csv(self.output_save_location, index_col=0)
            output_csv.index = [self.fix_ags5(ags5)  for ags5 in output_csv.index]
            
            ## check if the calculation has already been done
            columns_needed= [str(last_date_train)+'_'+str(i) for i in range(n)]
            
            if all(col_needed in output_csv.columns for col_needed in columns_needed):
                # this data has already been generated
                return_df = output_csv[columns_needed]
                return_df = return_df.sort_index(axis=1) # sort columns
                return_df.columns = list(range(n)) # rename columns
                print("directly from csv")
                
                return_df.insert(0, 'ags5', return_df.index) # make the ags5 a separate column
                return_df.columns = [str(col) for col in return_df.columns] # make all the col names str
                return return_df.reset_index(drop=True).sort_values('ags5', ignore_index=True)

            else:
                predictions = self.wf_pred(self.unemploymentRateData, self.otherData, n, self.params) # get the preds
                predictions.columns = [str(last_date_train)+'_'+str(i) for i in predictions.columns] #rename the columns
                # save the predictions
                output_csv.drop([col for col in predictions.columns if col in output_csv.columns], axis=1, inplace=True) # drop columns that already exist
                output_csv = output_csv.merge(predictions, left_index=True, right_index=True)
                output_csv.to_csv(self.output_save_location)
                print('Appending to csv')
                
                
                predictions.columns = [col[11:] for col in predictions.columns]# remove the prefix in col names, use only in cacheing
                predictions.insert(0, 'ags5', predictions.index)
                predictions.columns = [str(col) for col in predictions.columns] # make all the col names str
                return predictions.reset_index(drop=True).sort_values('ags5', ignore_index=True)
                
            
        except FileNotFoundError:
            # make the file
            predictions = self.wf_pred(self.unemploymentRateData, self.otherData, n, self.params) # get the preds
            predictions.columns = [str(last_date_train)+'_'+str(i) for i in predictions.columns] #rename the columns            
            predictions.to_csv(self.output_save_location)   
            print('making csv')
            
            predictions.columns = [col[11:] for col in predictions.columns]
            predictions.insert(0, 'ags5', predictions.index)
            predictions.columns = [str(col) for col in predictions.columns] # make all the col names str
            return predictions.reset_index(drop=True).sort_values('ags5', ignore_index=True)
    
    def getWalkForwardPred_3Months(self):
        return self.getWalkForwardPred(3)
    
    
    
    def getWalkForwardErrors(self, n=3):
        
        input_df = self.unemploymentRateData.long()

        ''' set the end date to 3 timestamps ahead '''
        params_of_errors = self.params.copy()
        dates = list(input_df['date'].unique())
        dates.sort()
        
        # find the index of end date of training set
        if 'end_date' in params_of_errors.keys():
            # end date was a parameter that was passed
            end_date_index = dates.index(params_of_errors['end_date'])
        else:
            end_date_index = len(dates)-1
        
        # set the end date to 3 time stamps ahead
        params_of_errors['end_date'] = dates[end_date_index-n]
        
        ''' Temporarily change the class's params to prarams needed for generating errors, generate predictions, revert back '''
        original_params = self.params
        self.params = params_of_errors
        
        preds = self.getWalkForwardPred_3Months()
        
        self.params = original_params
        
        ''' create the output df '''
        # make the df with ground truths
        dates_for_errors = dates[end_date_index-3: end_date_index]
        ground_truths = input_df[[date in dates_for_errors for date in input_df['date']]]
        ground_truths.columns = ['ags5', 'date', 'ground_truth']
        
        # sort the ground truth and preds df by ags5
        ground_truths = ground_truths.sort_values(['ags5', 'date']) # sort by ags5 first then within it, by dates
        preds = preds.sort_values(['ags5']) # sort ags5 here too to match
        
        # assign values to the pred column
        output_df = ground_truths
        output_df['pred'] =[float(preds[preds['ags5'] == ags5][str(j)]) for ags5 in ground_truths['ags5'].unique() for j in range(n)]
        
        # assign values to the error column
        output_df['error'] = (output_df['pred'] - output_df['ground_truth']).apply(abs)
        
        return output_df.reset_index(drop=True)
    
    ## Utils
    def fix_ags5(self, x):
        """Function to fix the format of ag5 """
        if len(str(x))==4:
            return '0'+str(x)
        else:
            return str(x)


class VARModel(AbstractModel):
    
    def __init__(self, output_save_location, params, unemploymentRateData, cluster_df):
        '''
        Inputs:
        -------
        pretrained: set True if you want to load a model, set false of you want to retrain a model
        output_save_location: location, including the csv file where the outputs are stored
        params: a dictionary containing
            required keys: 'second_diff' and 'lag_value'
            optional keys: 'start_date', 'end_date'
        unemploymentRateData: an instance of the class Data()
        cluster_df: a df with two columns:
            'ags5': ags5 of a kreis
            'cluster': the cluster id
        '''
        
        self.cluster_df = cluster_df
        
        super().__init__(output_save_location, params, unemploymentRateData, otherData=cluster_df, model_save_location=None)     
            


    def wf_pred(self, data, cluster_df, n, params):
        '''
        Inputs:
        -------
        input_df: a dataframe containing unemployment data in LONG format, required columns:
            'ags5' as a string of len 5,
            'date' as a numpy.datetime64
            'unemployment_rate'
        cluster_df: a df with two columns:
            'ags5': ags5 of a kreis
            'cluster': the cluster id
        n: number of timestamps od prediction
        params: a dictionary containing
            required keys: 'second_diff' and 'lag_value'
            optional keys: 'start_date', 'end_date'
            
        Returns:
        --------
        a pd DataFrame with:
            0, 1, 2, ... n: as columns
            ags5 as rows
        '''



        ''' Utility Functions '''

        # Invert the transformation to get the real forecast
        def invert_transformation(df_train, df_forecast, second_diff=False):

            """Revert back the differencing to get the forecast to original scale."""
            df_fc = df_forecast.copy()
            columns = df_train.columns
            for col in columns:        
                # Roll back 2nd Diff
                if second_diff:
                    df_fc[str(col)+'_diff'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_diff'].cumsum()
                # Roll back 1st Diff
                df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_diff'].cumsum()
            return df_fc

        '''Get the long format from the Data class'''
        input_df = data.long()
        
        ''' Data Preparation '''
        ## cropping dates
        if 'start_date' in params.keys() or 'end_date' in params.keys():
            ## cropping required:
            if 'start_date' not in params.keys():
                params['start_date'] = min(input_df['date'])
            if 'end_date' not in params.keys():
                params['end_date'] = max(input_df['date'])
            # clip the data
            start_date = params['start_date']
            end_date = params['end_date']
            mask = (input_df['date'] >= start_date) & (input_df['date'] < end_date)
            input_df = input_df[(mask)].reset_index(drop=True)

        # Create unemployment dataframe
        unemployment_rate_df = pd.DataFrame(input_df['date'].unique())
        unemployment_rate_df.columns = ['date']

        kreis_list = list(input_df['ags5'].unique())
        for kreis in kreis_list:
            unemployment_rate_df[kreis] = input_df.loc[input_df['ags5']==kreis, 'unemployment_rate'].reset_index(drop=True)

        # set date as index
        unemployment_rate_df.set_index('date', inplace=True)

        ''' Cluster iterations '''

        # output df:
        output_df = pd.DataFrame(index=range(n))

        # Get cluster list 
        cluster_list = list((cluster_df['cluster'].unique()))

        for cluster in cluster_list:
            cluster_kreis_list = list(cluster_df.loc[(cluster_df['cluster']==cluster), 'ags5'].unique())

            # Check if the kreis has a single item
            if len(cluster_kreis_list) == 1:
                print("Single item in the cluster. Hence skipping.")
                continue

            # get cluster data 
            cluster_data = unemployment_rate_df[cluster_kreis_list]

            num_steps = 1 # number of pred per wf step
            for i in range(n):

                # Differentiate the data twice if asked else once
                if_second_diff = params['second_diff']

                df_differenced = cluster_data.diff().dropna()
                if if_second_diff:
                    df_differenced = df_differenced.diff().dropna()

                # Get the lag value 
                lag_value = params['lag_value']

                # Feed the model data
                from statsmodels.tsa.api import VAR
                import warnings
                warnings.filterwarnings("ignore")
                model = VAR(df_differenced)

                # Fit the model to lag
                model_fitted = model.fit(lag_value)

                '''Forecasting section'''
                # Get the lag order
                lag_order = model_fitted.k_ar

                # Input data for forecasting
                forecast_input = df_differenced.values[-lag_order:]

                # Get the forecasts            
                fc = model_fitted.forecast(y=forecast_input, steps=num_steps)
                df_forecast = pd.DataFrame(fc, index=[i], columns=cluster_data.columns + '_diff')

                # Invert the forecast results
                df_results = invert_transformation(cluster_data, df_forecast, second_diff=if_second_diff)
                final_results = df_results.filter(regex='_forecast')

                # add the preds to training data
                final_results.columns = [col_name[:5] for col_name in final_results.columns] ## remove _forecast
                cluster_data = cluster_data.append(final_results) # add to the training data

            output_df = output_df.join(cluster_data.iloc[-n:]) # append the preds

        return output_df.T