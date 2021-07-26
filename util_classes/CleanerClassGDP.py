class CleanerClassGDP:
    
    AGS5_LIST = [ 1001,  1002,  1003,  1004,  1051,  1053,  1054,  1055,  1056,
            1057,  1058,  1059,  1060,  1061,  1062,  2000,  3101,  3102,
            3103,  3151,  3153,  3154,  3155,  3157,  3158,  3159,  3241,
            3251,  3252,  3254,  3255,  3256,  3257,  3351,  3352,  3353,
            3354,  3355,  3356,  3357,  3358,  3359,  3360,  3361,  3401,
            3402,  3403,  3404,  3405,  3451,  3452,  3453,  3454,  3455,
            3456,  3457,  3458,  3459,  3460,  3461,  3462,  4011,  4012,
            5111,  5112,  5113,  5114,  5116,  5117,  5119,  5120,  5122,
            5124,  5154,  5158,  5162,  5166,  5170,  5314,  5315,  5316,
            5334,  5358,  5362,  5366,  5370,  5374,  5378,  5382,  5512,
            5513,  5515,  5554,  5558,  5562,  5566,  5570,  5711,  5754,
            5758,  5762,  5766,  5770,  5774,  5911,  5913,  5914,  5915,
            5916,  5954,  5958,  5962,  5966,  5970,  5974,  5978,  6411,
            6412,  6413,  6414,  6431,  6432,  6433,  6434,  6435,  6436,
            6437,  6438,  6439,  6440,  6531,  6532,  6533,  6534,  6535,
            6611,  6631,  6632,  6633,  6634,  6635,  6636,  7111,  7131,
            7132,  7133,  7134,  7135,  7137,  7138,  7140,  7141,  7143,
            7211,  7231,  7232,  7233,  7235,  7311,  7312,  7313,  7314,
            7315,  7316,  7317,  7318,  7319,  7320,  7331,  7332,  7333,
            7334,  7335,  7336,  7337,  7338,  7339,  7340,  8111,  8115,
            8116,  8117,  8118,  8119,  8121,  8125,  8126,  8127,  8128,
            8135,  8136,  8211,  8212,  8215,  8216,  8221,  8222,  8225,
            8226,  8231,  8235,  8236,  8237,  8311,  8315,  8316,  8317,
            8325,  8326,  8327,  8335,  8336,  8337,  8415,  8416,  8417,
            8421,  8425,  8426,  8435,  8436,  8437,  9161,  9162,  9163,
            9171,  9172,  9173,  9174,  9175,  9176,  9177,  9178,  9179,
            9180,  9181,  9182,  9183,  9184,  9185,  9186,  9187,  9188,
            9189,  9190,  9261,  9262,  9263,  9271,  9272,  9273,  9274,
            9275,  9276,  9277,  9278,  9279,  9361,  9362,  9363,  9371,
            9372,  9373,  9374,  9375,  9376,  9377,  9461,  9462,  9463,
            9464,  9471,  9472,  9473,  9474,  9475,  9476,  9477,  9478,
            9479,  9561,  9562,  9563,  9564,  9565,  9571,  9572,  9573,
            9574,  9575,  9576,  9577,  9661,  9662,  9663,  9671,  9672,
            9673,  9674,  9675,  9676,  9677,  9678,  9679,  9761,  9762,
            9763,  9764,  9771,  9772,  9773,  9774,  9775,  9776,  9777,
            9778,  9779,  9780, 10041, 10042, 10043, 10044, 10045, 10046,
           11000, 12051, 12052, 12053, 12054, 12060, 12061, 12062, 12063,
           12064, 12065, 12066, 12067, 12068, 12069, 12070, 12071, 12072,
           12073, 13003, 13004, 13071, 13072, 13073, 13074, 13075, 13076,
           14511, 14521, 14522, 14523, 14524, 14612, 14625, 14626, 14627,
           14628, 14713, 14729, 14730, 15001, 15002, 15003, 15081, 15082,
           15083, 15084, 15085, 15086, 15087, 15088, 15089, 15090, 15091,
           16051, 16052, 16053, 16054, 16055, 16056, 16061, 16062, 16063,
           16064, 16065, 16066, 16067, 16068, 16069, 16070, 16071, 16072,
           16073, 16074, 16075, 16076, 16077]
    
    def __init__(self, file_location, dropna=True, verbose=True):
        
        import pandas as pd
        import numpy as np
        
        self.verbose = verbose
        self.sheets = {}  # by default we store it in the wide format
        self.thrownAwayColumns = {}
        self.thrownAwayRows = {}
        
        if verbose:
            print("Reading the file...")
        self.sheet_to_df_map = pd.read_excel(file_location, engine='openpyxl', sheet_name=None) # use sheet_name = None to read all sheets as an ordered dict
        if verbose:
            print("file read complete!")
        
        
        for sheet_name, sheet_df in self.sheet_to_df_map.items():
            ## loop through all the sheets
            
            sheet = sheet_df.copy()
            
            if self.verbose:
                print("\nprocessing the sheet ", sheet_name, end='')
            
            if self.verbose:
                print('.', end='')
            
            '''
            0. Check metadata sheet
            sheet must pass a simple length check
            '''
            if sheet.shape[0] < 401:
                # this sheet does not have data (in the specified format, i.e. each kreis is a separate row)
                # therefore, not a useful sheet
                continue # to the next sheet
            
            ''' 
            1. Find the starting column of the table
            sheet must contain a few kreis names, all in same column: 
            '''
            #KREIS_NAMES_TO_CHECK = ['hamburg', 'berlin', 'kiel']
            KREIS_CODES_TO_CHECK = ['02000', '11000', '01002']
            KREIS_COL_NO = None 
            KREIS_COL_NAME = None

            for kreis_code in KREIS_CODES_TO_CHECK:

                for i, col in enumerate(sheet.columns):
                    # find if kreis code is in present
                    is_kreis_code = sheet[col].astype(str) == kreis_code # returns a number >0 (position where kreis_code starts)

                    found = sum(is_kreis_code > 0)

                    # if found, just break away, no need to look anymore
                    if found:
                        if KREIS_COL_NO is None:
                            KREIS_COL_NO = i
                            KREIS_COL_NAME = col 
                        else:
                            print('!', kreis_code, KREIS_COL_NO, i)
                            assert KREIS_COL_NO == i

                        break

            if KREIS_COL_NAME is None:
                # no column was found with the kreis names
                # therefore, not a useful sheet
                continue  # to the next sheet
                
                
            if self.verbose:
                print('.', end='')
            ''' 
            2. Find the starting row of the table: 
            '''
            ## we already found the starting column in 1.2 <br>
            ## (actually we find the starting row by finding the row with dates)
            col_names = sheet.columns
            DATE_COUNT_CUTOFF = 5 # the number of dates a column must have to qualify as the row which has the table's col names
            ROW_WITH_DATES = None

            sheet.reset_index(drop=True, inplace=True) # reset index so that we have the index as a range starting from 0

            for index, row in sheet.iterrows():
                is_date_arr = [self.is_date(str(row[col_name])) for col_name in col_names]
                if sum(is_date_arr) >= DATE_COUNT_CUTOFF:
                    # we found the row!
                    ROW_WITH_DATES = index  
                    break
                    
            
            if ROW_WITH_DATES is None:
                # no row had dates
                # therefore, not a table with time series data
                # therefore not a useful sheet (sheet with needed data)
                continue # to the next sheet
                
            if self.verbose:
                print('.', end='')
            '''
            3. Crop out the table
            '''
            '''
            3.1 Crop the columns (from the left)
            (right we currently don't handle because it is automatically handled in the pd.read_excel function;
            but if there is metadata on the side in the right it should be cleaned manually before inputting)
            '''
            columns_to_drop = []

            for col_name in sheet.columns:
                # loop through all the columns adding all the columns until KREIS_COL_NAME to the columns to drop.
                if col_name == KREIS_COL_NAME:
                    # end the loop
                    break

                columns_to_drop.append(col_name)

            sheet.drop(columns_to_drop, axis=1, inplace=True)
            sheet.set_index(KREIS_COL_NAME, inplace=True)
            
            '''
            3.2 Crop the rows (top and bottom are thrown away) (work same as 4...?)
            (check each row and only keep ones with ags5 in ags5_list)
            '''
            sheet.columns = list(sheet.iloc[ROW_WITH_DATES])
            sheet = sheet.iloc[ROW_WITH_DATES+1:] # drop the useless rows
            sheet.index.name = None
            sheet
            
            if self.verbose:
                print('.', end='')
                
            '''
            4. Throw away rows that are not kreis
            '''
            AGS5_LIST_TEMP = self.AGS5_LIST.copy()
#             new_index = []
            rows_to_drop = []

            for index, row in sheet.iterrows():

                row_is_needed = False

                for ags5_loc, ags5 in enumerate(AGS5_LIST_TEMP):

                    if "{:05d}".format(ags5) == str(index):
                        AGS5_LIST_TEMP.pop(ags5_loc) # remove that ags5 from AGS5_LIST_TEMP
#                         new_index.append(ags5) # add that index
                        row_is_needed = True # We need this row
                        break # no need to search for other ags5 in AGS5_LIST_TEMP

                if row_is_needed is False:
                    rows_to_drop.append(index)
            
            
            
            
            
            if len(AGS5_LIST_TEMP) == 2:
                # berlin and hamburg are not divided down into it's kreis
                
                BERLIN_HAMBURG = [2000, 11000]
                BERLIN_HAMBURG_STR = ["{:05d}".format(ags5) for ags5 in BERLIN_HAMBURG]
                BERLIN_HAMBURG_ags2 = [2, 11]
                BERLIN_HAMBURG_ags2_STR = ["{:02d}".format(ags2) for ags2 in BERLIN_HAMBURG_ags2]
                
                ags5s_to_pop = []
                for ags5_loc, ags5 in enumerate(AGS5_LIST_TEMP):
                    if ags5 in BERLIN_HAMBURG or BERLIN_HAMBURG_STR:
                        # this bundesland is not then subdivided bacause these 2 bunds. have only one kreis under them
                        # , so use the bundesland info as the kreis info
                        ags5s_to_pop.append(ags5_loc)
    #                     new_index.append(ags5)
                        for i in range(len(BERLIN_HAMBURG)):
                            if ags5 == BERLIN_HAMBURG[i] or ags5 == BERLIN_HAMBURG_STR[i]:
                                try:
                                    rows_to_drop.remove(BERLIN_HAMBURG_ags2[i])
                                    # replace the ags2 index with corresponding ags5
                                    sheet.index = [BERLIN_HAMBURG_STR[i] if ind == BERLIN_HAMBURG_ags2_STR[i] else ind for ind in sheet.index]
                                except:
                                    rows_to_drop.remove(BERLIN_HAMBURG_ags2_STR[i])
                                    sheet.index = [BERLIN_HAMBURG_STR[i] if ind == BERLIN_HAMBURG_ags2_STR[i] else ind for ind in sheet.index]
                                break
                ags5s_to_pop.sort(reverse=True)
                for ags5_loc in ags5s_to_pop:
                    AGS5_LIST_TEMP.pop(ags5_loc)
                    
            if len(AGS5_LIST_TEMP) != 0:
                # some ags5 does not exist!
                continue # to next sheet
            
            sheet.drop(rows_to_drop, axis=0, inplace=True)
            sheet.index = [int(ind) for ind in sheet.index]
            
            self.thrownAwayRows[sheet_name] = rows_to_drop
            
            
            if self.verbose:
                print('.', end='')
            '''
            5. convert the datatypes of columns
            '''
            cols_with_non_numeric_vals = []

            for col in sheet.columns:
                try:
                    # find if the col has int or float as dtype:
                    rem = sheet[col] % 1
                    if sum(rem) == 0:
                        col_type = 'int64'
                    else:
                        col_type = 'float64'

                    sheet[col] = sheet[col].astype(col_type)
                    
                except:
                    # col cannot be converted to numeric type
                    cols_with_non_numeric_vals.append(col)
                    
            sheet.drop(cols_with_non_numeric_vals, axis=1, inplace=True)
            
            self.thrownAwayColumns[sheet_name] = cols_with_non_numeric_vals
            
            if self.verbose:
                print('.', end='')
               
            
            '''
            6. Drop All Columns with NA
            '''
            '''
            6.1 drop all cols with the name as na, (instead of a valid date)
            '''
            sheet = sheet[sheet.columns.dropna()]
            '''
            6.2 drop sheet with na values
            '''
            cols_with_na = sheet.columns[sheet.isnull().any()]
            sheet.drop(cols_with_na, axis=1, inplace=True)

            self.thrownAwayColumns[sheet_name].extend(cols_with_na)

            if self.verbose:
                print('.', end='')
                
            '''
            7. set the ags5 index to string of length 5
            '''
            sheet.index = ["{:05d}".format(ags5) for ags5 in sheet.index]
            
            '''
            8. sort the sheet by ags 5 value
            '''
            sheet = sheet.sort_index()
            
            '''
            9. throw away empty sheets
            '''
            if 0 in sheet.shape:
                continue # to next sheet
            
                    
            '''
            Done!!!!
            '''
            
            if self.verbose:
                print("\n   Useful Data Found!", end='')
            self.sheets[sheet_name] = sheet
            
        print('\n\nDone!')       
    
        
            
            
                
    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, Whether to allow fuzzy parsing, allowing for string like “Today is January 1, 2047 at 8:21:00AM”.
        """
        from dateutil.parser import parse

        if isinstance(string, str):
            try: 
                parse(string, fuzzy=fuzzy)
                return True

            except ValueError:
                # not a string that can be parsed
                return False
        else:
            # not a string at all
            return False
        
        
        
        
    def getAllUsefulSheets_wide(self):
        return self.sheets
    
    def getAllUsefulSheets_long(self):
        try:
            # if it has been already calculated
            return self.sheets_long
        
        except AttributeError:
            
            import pandas as pd
            
            # self.sheets_long does not exist, yet..
            self.sheets_long = {}
            
            for df_name, df_og in self.sheets.items():
                df = df_og.copy()
                df = pd.DataFrame([ [ags5, time_stamp, row[time_stamp]] 
                                    for ags5, row in df.iterrows() 
                                    for  time_stamp in df.columns ])
                df.columns = ['ags5', 'time_stamp', 'value']
                
                self.sheets_long[df_name] = df
                
            return self.sheets_long
    
    def getThrownAwayRows(self):
        return self.thrownAwayRows
    
    def getThrownAwayColumns(self):
        return self.thrownAwayColumns