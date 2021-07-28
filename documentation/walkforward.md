# Walk-forward validation 

This is a validation technique that we have used to evaluate our models. It is different from a simple test-train split because we want to replicate a real world process. We take steps of three months and then retrain the model for the next three months of prediction, this is then applied on the test set for the testing. 

The steps are mentioned below: 
- Divide the data into train and test sets. Train dataset includes all the data till the end of 2018. Test dataset includes data from 2019 to current time of 2021 (as of the last time this section was written - May 2021).
- Predict for the first three months of 2020 and then add the actual data from the test set to the training set. This step ensures that the models be evaluated the way they would be trained in real-time i.e three months at a time. 
- After the new training dataset is created, the model is retrained on this data and tested on the next three months. This process keeps happening till the time there is some data remaining. 

`num_iterations = test_data_size/num_of_prediction_steps`

- The process results in a more robust evalutation such that the model can also learn from the short-term and long-term changes. 

Maybe add a flowchart like illustration for this. 