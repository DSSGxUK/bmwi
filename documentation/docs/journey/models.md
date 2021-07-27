# Model Descriptions

This section talks about the various models that we have built and tested. It documents the various models which worked well and also the models which did not work well. 


## Vector Autoregression

Vector Autoregression (VAR) is a forecasting algorithm that can be used when two or more time series influence each other. That is, the relationship between the time series involved is bi-directional. 

### Model Introduction

Vector Autoregression (VAR) is a multivariate forecasting algorithm that is used when two or more time series influence each other. It is considered as an Autoregressive model because, each variable (Time Series) is modeled as a function of the past values, that is the predictors are nothing but the lags (time delayed value) of the series.The primary difference between VAR and other Autoregressive (AR) modesl is that these models are uni-directional, where, the predictors influence the Y and not vice-versa. Whereas, VAR is bi-directional. That is, the variables influence each other.

![](https://i.imgur.com/eL8M1io.png)
<span style="color:grey;">*Typical AR Model: Future value only depends on the past values of that series.*</span>

![](https://i.imgur.com/PBSbjM1.png)
<span style="color:grey;">*VAR Model: Future values of one series depends on the past value of the same series and the parallel series*</span>

### Training Method

The training is done using the clusters that were developed based on the stationary data. The cluster development method has been elucidated within the [cluster section]().

The intuition behind VAR based cluster methods is that the Kreis in each cluster move together in terms of the unemployment rate and affect each other. The regional clusters are made using Bundesland and does not perform as well as the custom clusters which were created using statistical data. Since VAR learns from parallel series, the kreis in each cluster affect each other's unemployment rate within the same cluster. 

*Should I explain walk-forward?*

## Prophet 

## Hierarchical Time Series 

Hierarchical time series model is a model that utilized the hierarchy in the data. 
It generates forecasts for each individual time series, 
but takes into account the relationships within the hierarchy.
In our case, we considered the hierarchy of the different clusters explained in the [cluster section](). 

We forecasted using different models, 
- SARIMA
- auto_arima​
- Prophet

We aggregated using different methods, 
- Top-Down
    - AHP 
    - PHA​
- Bottom-Up​
- WLSS

Unfortunately, the bottom up approach was best, 
which means that the hierarchy does not add any useful information. 

## References

[1] https://www.machinelearningplus.com/time-series/vector-autoregression-examples-python/