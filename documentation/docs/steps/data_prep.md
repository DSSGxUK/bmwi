# Data Prep page

Upload the dataset and make any necessary changes to fit the prediction model. 

<span style="color:red">^ What are other data cleaning that could be needed?</span>

## Reshape and merge datasets

This section process data differently for excel or csv files, and for time-series or structural data type. It assumes that:

- **time-series** data are in **wide**-format **excel** workbooks, where each worksheet contains data for one variable

- **structural** data are in **long**-format **csv** files, where each row is a record of one kreis, and each column is one variable

- both assumes to have at least a column containing the kreis-level area code ("")

## Exporting excel worksheets

### Error Handling

![error 1](../prep_screenshots/error1.png)

When you open up the page, you will likely be facing this error. No worries, that just means you haven't uploaded a data yet!

### Upload Excel Workbook

![export excel workbook](../prep_screenshots/export_excel.png)

<span style="color:gray">*When you confirm that you are using an excel workbook containing time-series data, you are prompted to upload the data. In this sample screenshot, you can see that the file "7444_318010_BMWI_Enkelmann_Eckdaten_Zeitreihe_Kreise.xlsx" is being uploaded.*</span>

### Select data to clean

Because each data is formatted differently in the excel workbook, we created different cleaners for different data. Select the appropriate cleaner based on the data input. Currently, we support: 

![select cleanerclass](../prep_screenshots/select_cleaner.png)

- `Unemployment rate` (labor market data, containing unemployment rate information) 

![unemployment rate data](../prep_screenshots/alq_data.png)

<i>
<p style="color:gray">This is the assumed workbook for labor market data:</p>
<ul style="color:gray">
    <li> The index column "Region" shows that each row is a record of one kreis.
    <li> The rest of the columns should represent each year and month.
    <li> Each worksheet represents a different variable. For example, the current worksheet selected is "Alo_Quote", which stands for unemployment rate ("Arbeitslosenquote"). 
</ul>
</i>

- `GDP` (GDP data, containing kreis-level GDP breakdown)

![gdp data](../prep_screenshots/gdp_data.png)

<i>
<p style="color:gray">This is the assumed workbook for GDP data:</p>
<ul style="color:gray">
    <li> The index column is "Regional-schlüssel". We are looking for the ones with 5 numbers, which means they are on the kreis-level (corresponding to the "NUTS 3" column).
    <li> The rest of the columns should represent each year.
    <li> Each worksheet represents a different variable. For example, the current worksheet selected is "1.1", which according to the trailing title means gross domestic product ("bruttoinlandsprodukt"). 
</ul>
</i>


### Select data format

![select data format](../prep_screenshots/select_format.png)

<span style="color:red">^ Change to select "export" data format</span>

#### Long format

![long format one variable](../prep_screenshots/long_one.png)

<span style="color:gray">*This is an example of a single-variable "long" format data. The dataframe contains three columns: the kreis code (`ags5`), the time (`date`), and the variable (e.g. `Alo Quote`). The number of rows of this file is 401 kreis * #dates for each kreis.*</span>

<span style="color:red">^ If this confusing should we just call it wide format?</span>

#### Wide format

![wide format one variable](../prep_screenshots/wide_one.png)

<span style="color:gray">*This is an example of a single-variable "wide" format data. The dataframe contains one index column, the kreis code (`ags5`), and the rest of the columns are dates. The number of rows of this file should be 401.*</span>


### Select variable

![select variable](../prep_screenshots/select_var.png)

<span style="color:gray">*Choose at least one variable. Choosing no variables at all would result in the IndexError above.*</span>

### Merging

#### Long formats merged to one wide format

![long merged wide format](../prep_screenshots/long_merge.png)

<span style="color:gray">*Merging multiple so-called long-format-single-variable data together results in a commonly-knwown "wide format" merged file as shown above. `ags5` and `date` are the index columns. Each column afterwards represents a variable. In this example, the two columns are `SvB_AO` (Sozialversicherungspflichtig Beschäftigte -- Arbeitsort) and `Alo_Quote` (Arbeitslosenquote).*</span>

#### Wide formats merged to one long format

![wide merged long format](../prep_screenshots/wide_merge.png)

<span style="color:gray">*Merging multiple so-called wide-format-single-variable data together results in a commonly-known "long format" merged file as shown above. `ags5` and `variable` are the index columns. Each column afterwards represents a date. In this example, the two variables are `SvB_AO` and `Alo_Quote`, and they are indicated in the `variable` column.*</span>

#### Confirm merge

![confirm merge](../prep_screenshots/confirm_merge.png)

<span style="color:gray">*A preview of the merged data would be shown like the long and wide formats above. Once you confirm to use the merged data, it would be set as the default loaded dataset on the tool.*</span>


## Merging multiple csv files

![csv](../prep_screenshots/csv.png)

<span style="color:gray">*This is a sample of a csv file the tool expects. It should at least contain `ags5`, but could also include metadata such as `ags2`, `bundesland`, `kreis` etc. Each column afterwards is a varaible.*</span>

![merge csv](../prep_screenshots/csv_merge.png)

<span style="color:gray">*A simple merge using the `ags5` column, we have a merged file of 401 rows, and the combination of all the selected columns. In this example, we merged two files, `raumordnung` and `point_of_interest`. Again, a preview of the merged file would be shownn, and once confirmed, it would be the default loaded dataset.*</span>


## Final dataset cleaning

Data cleaning such as cropping to a certain dataframe, checking for NaN data etc.

### Loading dataset

![csv](../prep_screenshots/load_clean.png)

<span style="color:gray">*Here, you load the data you would like to clean. By default, it loads the data that you have confirmed processing and merging in the last section.*</span>

### Cropping timeframe

**Pro Tip**: The purpose of cropping the appropriate timeframe helps differentiate between a normal-time and crisis-time model. For example, we know that there was the economic crisis around 2008 and the COVID pandemic around 2020. Thus, when doing a normal-time unemployment rate prediction, you could crop out those times so that the model is only learning the pattern from normal-time data.

![csv](../prep_screenshots/crop_time.png)

<span style="color:gray">*This is where you can select the timeframe you would like to feed into the model. In this example, a timeframe between 2007-05 and 2007-07 is selected and shown in the preview. Again, once you confirm the dataset, it would be automatically loaded in the model on the next page.*</span>