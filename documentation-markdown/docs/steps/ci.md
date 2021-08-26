# Confidence intervals 

This section focuses on getting 95% confidence intervals for the predictions of the model.
The results will include unemployment rate confidence interval predictions the next three months, for all 401 kreise.

### Video Documentation 

The following video will walk you through this section and how to use the various interactive widgets. 

<div style="text-align:center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/watch?v=gSpz9Lcbl7A&list=PLzWRWFPEUpHbwIHq0T6M72B1_5N04hD0Q&index=4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

<hr>

The confidence intervals are calculated using stationary bootstrap for time-series data, which uses blocks with an exponentially distributed lengths.
For more information see the [Arch package](https://arch.readthedocs.io/en/latest/bootstrap/timeseries-bootstraps.html
). 
## Fit confidence intervals
This page automatically takes the fitted the model, and calculates 95% confidence intervals for each forecast. 

After the confidence intervals are calculated, 
it is possible to click the "Download the confidence intervals" link and and xslx table with the confidence intervals will be downloaded. 

![](./ci_screenshots/1.png)

## Plot confidence intervals by kreis 

A time series of the predictions and confidence intervals of each kreis can be plotted. For that, chose a kreis from the drop down menu, or type its name. 
Then the unemployment rates will be printed, and a time series graph will be plotted. 
The blue line, which has  the confidence intervals plotted around it, shows the predictions. 
The green line, with all previous values, is the ground truth, and therefore don't require confidence intervals. 


![](./ci_screenshots/2.png)
