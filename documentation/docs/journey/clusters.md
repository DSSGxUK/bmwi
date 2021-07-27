# Cluster Analysis 
This section talks about the clusters that we have built 
and were used for the model. 

## Need for clusters 
We wanted to forecast unemployment rate for all 401 Kreise of Germany. 
Of course, we could have create 401 independent time series models, one for each Kreis. 
However, this would mean that all models won't learn from the unemployment rate time series of other Kreise. 
We believed that some Kreise must be similar to each other, 
and can benefit from incorporating each other's data in the forecasting process.
We used unsupervised classification.  


## Type of Clusters 
We explored 4 different methods to cluster the Kreise

* **Bundesland** - Each Kreise belongs to one out for 16 Bundeslands. 
Kreise that belong to the same Bundesland have a similar geographic location, 
and are also affected by the same decisions that are made on a Bundesland level. 

![Bundesland](./clusters_screenshots/hierarchy_bundesland.png)

* **PCA & K-means** 

![PCA & K-means](./clusters_screenshots/hierarchy_PCA.png)

* **tSNE** 
* **K-modes**

## Cluster graphs 

## Cluster groups 

