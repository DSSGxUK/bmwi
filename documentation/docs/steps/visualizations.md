# Visualizations

This section allowas you to on see visualizations of the model results.



## Predictions Line Plot
A time series of the predictions of each kreis can be plotted. For that, you need to chose a kreis from the drop down menu, or type its name. Then the unemployment rate predictions will be printed, and a time series graph will be plotted. 

It is also possible to choose multiple kreise. Then, the unemployment rate predictions for each kreis will be printed separately, 
and a time series graph for all kreise will be plotted. 

The graph shows the values of each kreis in a different line. The ground truth unemployment rates in different colors on the left,  and the predicted values in red on the right. 

It is also possible to pick the start date for the graph, which is helpful if you are interested in a very short or long time period. 

![](./model_screenshots/viz1.png)

## Predictions Map

### Choose varaible to plot map 

Another option is to plot the unemployment rates on a map of Germany. 

First, you need to choose which unemployment rate to plot. 


![](./model_screenshots/plot_var.png)

The options are: 

- A specific ground truth month

- A specific predicted month

- Difference in unemployment rate compared to last month

- Difference in unemployment rate compared to this month last year 

- Percentage of change in unemployment rate compared to same time last month

- Percentage of change in unemployment rate compared to same time last year

- An average of the three predicted months 

![](./model_screenshots/map5.png)

<span style="color:gray">*This is a kreis-level map of Germany based on unemployment rate on predicted for August 2021.*</span>

### Adding labels to the map

You can add the kreis name and unemployment 
rate of that kreis will be added to the map 
based on your selection. 

#### add labels based on kreis  

![](./model_screenshots/select_bdl.png)

After choosing a column, it is also possible to add labels of a specific kreis to the plot. 
For that,choose a kreis from the drop down menu or type its name. The label of the kreis will be added to the map, along with the value. 

![](./model_screenshots/map_a.png)


#### add labels based on bundesland  

It is also possible to look at a map of a specific bundesland. 
First, you need to choose which unemployment rate to plot. 

Then, chose a bundesland from the drop down menu or type its name. 
Automatically, the kreise with the highest values will be marked and their values will be plotted. 
It is possible to add labels of a specific kreis from this bundesland to the plot. 
For that, choose a kreis from the drop down menu or type its name. The label of the kreis will be added to the map, along with the value. 

![](./model_screenshots/map_b.png)
