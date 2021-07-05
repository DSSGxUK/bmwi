class Forecaster:
    
    def __init__(self, file_location='', config=[], verbose=False, train=False):
        
        '''
        If Train = True, then file_location and config is a required parameter, else, it is not
        '''
        
        if train:
        
            self.order, self.sorder, self.trend = config

            import pandas as pd
            from statsmodels.tsa.statespace.sarimax import SARIMAX

            # Read the data
            df = pd.read_csv(file_location)
            
            # Fix the ags5 type 
            if 'ags5' in df.columns: 
                df['ags5'] = df['ags5'].apply(Forecaster.fix_ags5)
            
            # Create a pivot dataframe with rows as date (dropped) and ags 5 as column
            df_pivot = df.pivot(index="date", columns="ags5", values="unemployment_rate").reset_index(drop=True)
            self.kreis_list = list(df_pivot)
            
            # Save the data pivoted by ags
            self.df_pivot_by_ags5 = df.pivot(index="ags5", columns="date", values="unemployment_rate")    
            
            df.set_index('ags5', drop=True, inplace=True)
            df_y_grouped = df.groupby('ags5')

            # get all the training data:
            ## Note: I don't want to use date anywhere because date formats can get messed up. Sorting by date can be troublesome at some point. 
            all_train_data = [list(df_for_kreis.sort_values('date').drop(['date'], axis=1)['unemployment_rate']) for ags5, df_for_kreis in df_y_grouped]
            self.all_train_data = { df.index.unique()[i]: all_train_data[i] for i in range(len(all_train_data)) }
            
            # get all the models:
            if verbose:
                print("Fitting 401 models ", end='')
            
            models = [self.get_model(train_data, verbose=True) for train_data in all_train_data[:10]]
            if verbose:
                print("\nAll Models fitted!")
            self.models = { df.index.unique()[i]: models[i] for i in range(len(all_train_data[:10])) }
            
        
        else:
            import pickle
            
            with open('pickles/1/models.pickle', 'rb') as handle:
                self.models = pickle.load(handle)
                
            with open('pickles/1/config.pickle', 'rb') as handle:
                config = pickle.load(handle)
                self.order, self.sorder, self.trend = config
                
            with open('pickles/1/all_train_data.pickle', 'rb') as handle:
                self.all_train_data = pickle.load(handle)
            
    @staticmethod
    def fix_ags5(x):
        """Function to fix the ags5 type of the dataframe which is uploaded. 
        This function makes them all 5 character strings. 

        Args:
            x (Series): ags5 list present in the dataset

        Returns:
            Series: Returns fixed series type
        """
        if len(str(x))==4:
            return '0'+str(x)
        else:
            return str(x)
    
    
    def get_model(self, data, verbose=False):
        
        from warnings import catch_warnings
        from warnings import filterwarnings
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        
        if verbose:
            print(".", end='')
        
        try:
            # define model
            model = SARIMAX(data, order=self.order, seasonal_order=self.sorder, trend=self.trend, enforce_stationarity=False, enforce_invertibility=False)
            # fit model
            with catch_warnings():
                filterwarnings("ignore")
                ### IMP: TODO: CHECKOUT THE WARNINGS, WE IGNORE NOW CAUSE WITH SAME IGNORING WE GOT GOOD MSE. It keeps throwing warnings wvwn though it produces good results.
                model_fit = model.fit(disp=False)
            
            return model_fit
        
        except:
            return None

    def get_models(self):
        return self.models
    
    def get_train_series(self, ags5):
        import numpy as np
        return np.array(self.all_train_data[ags5])
    
    def get_predictions(self, ags5, count=1):
        model = self.models[ags5]
        start = len(self.all_train_data[ags5])
        end = start + count - 1
        yhat = model.predict(start, end)
        
        return yhat
    
    def get_predictions_df(self, count=1):
        """Function to get a dataframe of predictions for all the kreis in a dataframe

        Args:
            count (int, optional): Number of next predctions required. Defaults to 1.
        """
        # Import necessary libraries 
        import pandas as pd

        # Iterate through the kreis list 
        final_preds = []
        for kreis in self.kreis_list[:10]:
            
            # Get single predictions 
            preds = self.get_predictions(ags5=kreis, count=count)
            preds = [kreis] + list(preds)
            final_preds.append(preds)
            
        cols = ['ags5'] + [str(i) for i in range(1, count+1)]
        output_df = pd.DataFrame(final_preds, columns=cols)

        # Fix the date format of the output 
        output_df.set_index('ags5', inplace=True)
        original_df = self.df_pivot_by_ags5

        # Get the last date in the original df
        last_date = original_df.columns[-1]

        # Get the next dates 
        next_dates = pd.date_range(last_date, periods=count+1, freq='M').date.tolist()[1:]
        output_df.columns = next_dates
    
        return output_df
    
    def get_predictions_df_appended(self, count=1):
        """Generate a predcitions df appended to the original data

        Args:
            count (int, optional): Number of next predctions required. Defaults to 1.
        """

        # Import necessary libraries 
        import pandas as pd

        # Get the predictions df and the original df
        original_df = self.df_pivot_by_ags5
        pred_df = self.get_predictions_df(count)
        # pred_df.set_index('ags5', inplace=True)
        # original_df = self.df_pivot_by_ags5

        # # Get the last date in the original df
        # last_date = original_df.columns[-1]

        # # Get the next dates 
        # next_dates = pd.date_range(last_date, periods=count+1, freq='M').date.tolist()[1:]
        # pred_df.columns = next_dates

        # Append to the end of original df
        final_df = pd.concat([original_df, pred_df], axis=1)
        
        return final_df

