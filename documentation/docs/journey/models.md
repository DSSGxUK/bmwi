# Model Descriptions

This section talks about the various models that we have built and tested. It documents the various models which worked well and also the models which did not work well. 


## Vector Autoregression

Vector Autoregression (VAR) is a forecasting algorithm that can be used when two or more time series influence each other. That is, the relationship between the time series involved is bi-directional. 

**Model Introduction**

Vector Autoregression (VAR) is a multivariate forecasting algorithm that is used when two or more time series influence each other. It is considered as an Autoregressive model because, each variable (Time Series) is modeled as a function of the past values, that is the predictors are nothing but the lags (time delayed value) of the series.The primary difference between VAR and other Autoregressive (AR) modesl is that these models are uni-directional, where, the predictors influence the Y and not vice-versa. Whereas, VAR is bi-directional. That is, the variables influence each other.

![](./models_screenshots/AR.png?raw=True)
<span style="color:grey;">*Typical AR Model: Future value only depends on the past values of that series.*</span>

![](./models_screenshots/VAR.png?raw=True)
<span style="color:grey;">*VAR Model: Future values of one series depends on the past value of the same series and the parallel series*</span>

**Training Method**

The training is done using the clusters that were developed based on the stationary data. The cluster development method has been elucidated within the [cluster section](../clusters).

The intuition behind VAR based cluster methods is that the Kreis in each cluster move together in terms of the unemployment rate and affect each other. The regional clusters are made using Bundesland and does not perform as well as the custom clusters which were created using statistical data. Since VAR learns from parallel series, the kreis in each cluster affect each other's unemployment rate within the same cluster. 


## Prophet 

Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

We fitted the Prophet model and did a grid search to chose the hyper-parameters. 
However, it did not perform well for our data. 

## SARIMA 

Autoregressive Integrated Moving Average, or ARIMA, is one of the most widely used forecasting methods for univariate time series data forecasting. Although the method can handle data with a trend, it does not support time series with a seasonal component. An extension to ARIMA that supports the direct modeling of the seasonal component of the series is called SARIMA.

The hyperparameters were tuned for all the time series (time series of unemployment of each kreis) using grid search individually. Most of the series converged best for the hyperparameters p:1, d:1, q:1, s_p:1, s_d:0, s_q:1 with each season containing a year. So these hyperparameters were chosen for all the 401 models that were trained for all the kreise.

## Neural network 

We explored multiple architectures including fully-connected, simple RNN, LSTM, GRU. Fully-Connected networks with the inputs as the unemployment rates of past 12 months always constintently performed better than other architectures. The best Fully Connected Neural Networks was of the shape: 32, 16, 8, 4, 1 with ReLu for the activation function for all but the last layer.

## Hierarchical Time Series 

Hierarchical time series model is a model that utilized the hierarchy in the data. 
It generates forecasts for each individual time series, 
but takes into account the relationships within the hierarchy.
In our case, we considered the hierarchy of the different clusters explained in the [cluster section](../../journey/clusters/). 

We forecasted using different models, 
- SARIMA
- Auto Arima
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
[2] https://facebook.github.io/prophet/docs/quick_start.html
[3] https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
[4] https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/
[5] https://keras.io/guides/sequential_model/
[6] https://scikit-hts.readthedocs.io/en/latest/index.html