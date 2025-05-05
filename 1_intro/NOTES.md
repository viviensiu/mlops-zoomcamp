Links:
* [unit 1 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/01-intro)

**1.1 Intro**
* ML Ops is a set of best practices to running ML in production environment. 
* ML project basically consists of 3 stages:
    * Design: Focuses on application design to solve the problem. This is where one decide if ML is suitable for the use case.
    * Train: Training and evaluating ML models with data to find the optimal solution for the problem. Covers inferencing.
    * Operate: Deploy and run the application and ML model in production environment to predict with real-time unseen data.
* ML Ops ensures that the deployed model maintains its quality over time. It does so by:
    * Monitoring model drift for performance issues.
    * Automate inferencing to receive latest data, perform feature engineering and feeding into the training stage.
    * Automate retraining model with latest data to minimise model drift.
    * Automate deployment of retrained model.