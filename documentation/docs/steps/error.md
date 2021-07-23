# Error Analysis Page

<span style="color:gray">* Identify the kreis that are hard to get predictions for.*</span>

The error analysis page uses the errors generated from the latest predictions and compares them with the structural data so that you can idenitfy which Kreis are harder to predict unemployment for and see what is different in those Kreis as opposed to the other Kreis. 

**Note:** The errors calculated for the previous quarter based on the recently uploaded data and, hence, this is a retrospective analysis. One can identify which kreis were harder to predict for in the previous quarter. 

### Launching the page

To open the error analysis page, select the 'Error Analysis` Section from the dropdown on the left as can be viewed in the image below.  

![This is the description](https://i.imgur.com/ggb86sd.png)

There are a variety of different plots that can be explored and have been explained in detail below. 

## Map Visualisation 

This is the first step of visualisation that one can view. Select the checkbox `Visualize error on a map?`. This will toggle open the following section. 

![](https://i.imgur.com/3hP3JWJ.png)

Here, you will see the `average` option selected by default. This will make a map with the average value of errors. This average is calculated over all the dates of the predictions. On clicking on the dropdown and selecting a specific date, the errors for that date will be plotted as seen below. 

![](https://i.imgur.com/XozVJQH.png)

## Error Plots by Bundesland 

This section allows for a kreis-level or bundesland-level analysis. The left dropdown allows selection by Kreis or by Bundesland and the right dropdown allows selection of `all` or a particular region. 

![](https://i.imgur.com/JwGjwvt.png)

Selecting `all` displays every kreis or bundesland in the same graph. Selecting an individual entry would plot the errors for a specific kreis or bundesland. The individual entries can be selected from the right dropdown option. 

![](https://i.imgur.com/eu9P1dS.png)

## Kreis Level Overview 

The goal of the application is to break down the predictions as well as the errors at the Kreis level. The following section performs error data analysis. It helps in understanding which Kreis are the hardest to estimate for unemployment rate. 

![](https://i.imgur.com/fSZlYL7.png)

<span style="color:gray">*This dataframe currently shows 5 kreis based on their unemployment rate forecasting errors for <strong>previous</strong> quarter.*</span>

There are two configuration options here:
- `Highest or Lowest`: This lets you select the Kreis with the highest or lowest unemployment rate prediction errors in the previous quarter. 
- `Value Slider`: This lets you select the number of Kreis to be displayed currently. *From UI perspective, the maximum limit is 20* 

To view all the Kreis, download the complete error table by clicking on the option `Download the full error table`. 

## Structural Data Analysis 

The next step is to analyze the errors with regards to the structural data and see hot the errors vary with a particular structural variable. Select a structural variable to compare against the errors. (*Eg: Errors are compared against `eligible_area` in this image*). 

The errors are on the x-axis so the fatter the curve is the more prone that category is to errors. In the following example, the areas where `eligible_area` is 0 are less prone to prediction errors than areas with code 1. 


![](https://i.imgur.com/cNEJJ5p.png)

**Future:** Later, we can add a check to see if the variable is a categorical or numerical variable.  

### Most important Structural Variables 

Write a bit about this method a bit more 

![](https://i.imgur.com/zNZCKye.png)
