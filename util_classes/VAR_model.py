# Import libraries 
import pandas as pd

# Utility functions 
def fix_ags5(x):
    """Function to fix the format of ag5 """
    if len(str(x))==4:
        return '0'+str(x)
    else:
        return str(x)

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
    
    population_data = {0: 83019213,
                        1: 2896712,
                        1001: 89504,
                        1002: 247548,
                        1003: 217198,
                        1004: 79487,
                        1051: 133210,
                        1053: 197264,
                        1054: 165507,
                        1055: 200581,
                        1056: 314391,
                        1057: 128647,
                        1058: 272775,
                        1059: 200025,
                        1060: 276032,
                        1061: 131347,
                        1062: 243196,
                        2: 1841179,
                        2000: 1841179,
                        3: 7982448,
                        3101: 248292,
                        3102: 104948,
                        3103: 124151,
                        3151: 175920,
                        3153: 137014,
                        3154: 91307,
                        3155: 132765,
                        3157: 133965,
                        3158: 119960,
                        3159: 328074,
                        3241: 1157624,
                        3251: 216886,
                        3252: 148559,
                        3254: 276594,
                        3255: 70975,
                        3256: 121386,
                        3257: 157781,
                        3351: 178936,
                        3352: 198213,
                        3353: 252776,
                        3354: 48424,
                        3355: 183372,
                        3356: 113517,
                        3357: 163455,
                        3358: 139755,
                        3359: 203102,
                        3360: 92572,
                        3361: 136792,
                        3401: 77607,
                        3402: 50195,
                        3403: 168210,
                        3404: 164748,
                        3405: 76278,
                        3451: 124071,
                        3452: 189848,
                        3453: 169348,
                        3454: 325657,
                        3455: 98460,
                        3456: 136511,
                        3457: 169809,
                        3458: 130144,
                        3459: 357343,
                        3460: 141598,
                        3461: 88624,
                        3462: 56882,
                        4: 682986,
                        4011: 569352,
                        4012: 113634,
                        5: 17932651,
                        5111: 619294,
                        5112: 498590,
                        5113: 583109,
                        5114: 227020,
                        5116: 261454,
                        5117: 170880,
                        5119: 210829,
                        5120: 110994,
                        5122: 159360,
                        5124: 354382,
                        5154: 310974,
                        5158: 485684,
                        5162: 451007,
                        5166: 298935,
                        5170: 459809,
                        5314: 327258,
                        5315: 1085664,
                        5316: 163838,
                        5334: 555465,
                        5358: 263722,
                        5362: 470089,
                        5366: 192840,
                        5370: 254322,
                        5374: 272471,
                        5378: 283455,
                        5382: 599780,
                        5512: 117383,
                        5513: 260654,
                        5515: 314319,
                        5554: 370676,
                        5558: 219929,
                        5562: 615261,
                        5566: 447614,
                        5570: 277783,
                        5711: 333786,
                        5754: 364083,
                        5758: 250783,
                        5762: 140667,
                        5766: 348391,
                        5770: 310710,
                        5774: 306890,
                        5911: 364628,
                        5913: 587010,
                        5914: 188814,
                        5915: 179111,
                        5916: 156374,
                        5954: 324296,
                        5958: 260475,
                        5962: 412120,
                        5966: 134775,
                        5970: 278210,
                        5974: 301902,
                        5978: 394782,
                        6: 6265809,
                        6411: 159207,
                        6412: 753056,
                        6413: 128744,
                        6414: 278342,
                        6431: 269694,
                        6432: 297399,
                        6433: 274526,
                        6434: 236564,
                        6435: 418950,
                        6436: 237735,
                        6437: 96798,
                        6438: 354092,
                        6439: 187157,
                        6440: 306460,
                        6531: 268876,
                        6532: 253777,
                        6533: 172083,
                        6534: 246648,
                        6535: 105878,
                        6611: 201585,
                        6631: 222584,
                        6632: 120829,
                        6633: 236633,
                        6634: 180222,
                        6635: 156953,
                        6636: 101017,
                        7: 4084844,
                        7111: 114024,
                        7131: 129727,
                        7132: 128705,
                        7133: 158080,
                        7134: 80720,
                        7135: 61587,
                        7137: 214259,
                        7138: 181941,
                        7140: 102937,
                        7141: 122308,
                        7143: 201597,
                        7211: 110636,
                        7231: 112262,
                        7232: 98561,
                        7233: 60603,
                        7235: 148945,
                        7311: 48561,
                        7312: 99845,
                        7313: 46677,
                        7314: 171061,
                        7315: 217118,
                        7316: 53148,
                        7317: 40403,
                        7318: 50378,
                        7319: 83330,
                        7320: 34209,
                        7331: 129244,
                        7332: 132660,
                        7333: 75101,
                        7334: 129075,
                        7335: 106057,
                        7336: 70526,
                        7337: 110356,
                        7338: 154201,
                        7339: 210889,
                        7340: 95113,
                        8: 11069533,
                        8111: 634830,
                        8115: 391640,
                        8116: 533859,
                        8117: 257253,
                        8118: 543984,
                        8119: 426158,
                        8121: 125960,
                        8125: 343068,
                        8126: 112010,
                        8127: 195861,
                        8128: 132321,
                        8135: 132472,
                        8136: 314002,
                        8211: 55123,
                        8212: 313092,
                        8215: 444232,
                        8216: 231018,
                        8221: 160355,
                        8222: 309370,
                        8225: 143535,
                        8226: 547625,
                        8231: 125542,
                        8235: 158397,
                        8236: 198905,
                        8237: 117935,
                        8311: 230241,
                        8315: 262795,
                        8316: 165383,
                        8317: 429479,
                        8325: 139455,
                        8326: 212381,
                        8327: 140152,
                        8335: 285325,
                        8336: 228639,
                        8337: 170619,
                        8415: 286748,
                        8416: 227331,
                        8417: 188935,
                        8421: 126329,
                        8425: 196047,
                        8426: 199742,
                        8435: 216227,
                        8436: 284285,
                        8437: 130873,
                        9: 13076721,
                        9161: 136981,
                        9162: 1471508,
                        9163: 63324,
                        9171: 111210,
                        9172: 105722,
                        9173: 127227,
                        9174: 153884,
                        9175: 142142,
                        9176: 132341,
                        9177: 137660,
                        9178: 179116,
                        9179: 219320,
                        9180: 88467,
                        9181: 120071,
                        9182: 99726,
                        9183: 115250,
                        9184: 348871,
                        9185: 96680,
                        9186: 127151,
                        9187: 260983,
                        9188: 136092,
                        9189: 177089,
                        9190: 135348,
                        9261: 72404,
                        9262: 52469,
                        9263: 47794,
                        9271: 119326,
                        9272: 78355,
                        9273: 122258,
                        9274: 158698,
                        9275: 192043,
                        9276: 77656,
                        9277: 120659,
                        9278: 100649,
                        9279: 96217,
                        9361: 41970,
                        9362: 152610,
                        9363: 42520,
                        9371: 103109,
                        9372: 127882,
                        9373: 133561,
                        9374: 94352,
                        9375: 193572,
                        9376: 147189,
                        9377: 72504,
                        9461: 77592,
                        9462: 74657,
                        9463: 41249,
                        9464: 45930,
                        9471: 147086,
                        9472: 103656,
                        9473: 86906,
                        9474: 116099,
                        9475: 95311,
                        9476: 67135,
                        9477: 71845,
                        9478: 66838,
                        9479: 73178,
                        9561: 41847,
                        9562: 111962,
                        9563: 127748,
                        9564: 518365,
                        9565: 40792,
                        9571: 183949,
                        9572: 136271,
                        9573: 117387,
                        9574: 170365,
                        9575: 100364,
                        9576: 126958,
                        9577: 94393,
                        9661: 70527,
                        9662: 54032,
                        9663: 127880,
                        9671: 174208,
                        9672: 103218,
                        9673: 79690,
                        9674: 84599,
                        9675: 90909,
                        9676: 128756,
                        9677: 126365,
                        9678: 115106,
                        9679: 161834,
                        9761: 295135,
                        9762: 43893,
                        9763: 68907,
                        9764: 43837,
                        9771: 133596,
                        9772: 251534,
                        9773: 96021,
                        9774: 125747,
                        9775: 174200,
                        9776: 81669,
                        9777: 140316,
                        9778: 144041,
                        9779: 133496,
                        9780: 155362,
                        10: 990509,
                        10041: 329708,
                        10042: 103366,
                        10043: 132206,
                        10044: 195201,
                        10045: 142631,
                        10046: 87397,
                        11: 3644826,
                        11000: 3644826,
                        12: 2511917,
                        12051: 72124,
                        12052: 100219,
                        12053: 57873,
                        12054: 178089,
                        12060: 182760,
                        12061: 169067,
                        12062: 102638,
                        12063: 161909,
                        12064: 194328,
                        12065: 211249,
                        12066: 110476,
                        12067: 178658,
                        12068: 99078,
                        12069: 214664,
                        12070: 76508,
                        12071: 114429,
                        12072: 168296,
                        12073: 119552,
                        13: 1609675,
                        13003: 208886,
                        13004: 95818,
                        13071: 259130,
                        13072: 215113,
                        13073: 224684,
                        13074: 156729,
                        13075: 236697,
                        13076: 212618,
                        14: 4077937,
                        14511: 247237,
                        14521: 337696,
                        14522: 306185,
                        14523: 227796,
                        14524: 317531,
                        14612: 554649,
                        14625: 300880,
                        14626: 254894,
                        14627: 242165,
                        14628: 245611,
                        14713: 587857,
                        14729: 257763,
                        14730: 197673,
                        15: 2208321,
                        15001: 81237,
                        15002: 239257,
                        15003: 238697,
                        15081: 83765,
                        15082: 159854,
                        15083: 171734,
                        15084: 180190,
                        15085: 214446,
                        15086: 89928,
                        15087: 136249,
                        15088: 184582,
                        15089: 190560,
                        15090: 111982,
                        15091: 125840,
                        16: 2143145,
                        16051: 213699,
                        16052: 94152,
                        16053: 111407,
                        16054: 34835,
                        16055: 65090,
                        16056: 42370,
                        16061: 100380,
                        16062: 83822,
                        16063: 123025,
                        16064: 102912,
                        16065: 75009,
                        16066: 122347,
                        16067: 135452,
                        16068: 69655,
                        16069: 63553,
                        16070: 108742,
                        16071: 81947,
                        16072: 56196,
                        16073: 106356,
                        16074: 83051,
                        16075: 80868,
                        16076: 98159,
                        16077: 90118}
    
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
    
    def getWalfForwardAgg(self, n):
        '''
        Returns the bundesland wise and full country wise aggregate
        
        NOTE: whole of Germany is represented as ags2: 00
        '''
        
        df = self.getWalkForwardPred(n)
        df['ags2'] = [s[:2] for s in df['ags5']]
    
        # get all the cols to aggregate
        cols = list(df.columns)
        cols = [col for col in cols if col not in ['ags5', 'ags2']]
        # convert the unemployment rate to # of unemployed ppl
        for i, row in df.iterrows():
            row[cols] = row[cols]*self.population_data[int(row['ags5'])]/100
            df.loc[i] = row
        df.drop('ags5', axis=1, inplace=True)
        
        # aggregate
        df2 = df.groupby(['ags2']).sum()

        # convert the # of unemployed ppl to unemployment rate
        for i, row in df2.iterrows():
            df2.loc[i] = row/self.population_data[int(i)]*100

        # aggregate and calculate UR for whole country
        df2.loc['germany'] = df.drop('ags2', axis=1).sum()/self.population_data[0]*100
        
        return df2.reset_index()
    
    def getWalkForwardAgg_3Months(self):
        return self.getWalkForwardAgg(3)
    
    
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
            output_csv.index = [fix_ags5(ags5)  for ags5 in output_csv.index]
            
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