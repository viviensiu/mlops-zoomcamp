Links:
* [unit 1 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/01-intro)

**1.1 Intro**
* ML Ops is a set of best practices to run ML in production environment. 
* ML project basically consists of 3 stages:
    * Design: Focuses on application design to solve the problem. This is where one decide if ML is suitable for the use case.
    * Train: Training and evaluating ML models with data to find the optimal solution for the problem. Covers inferencing.
    * Operate: Deploy and run the application and ML model in production environment to predict with real-time unseen data.
* ML Ops ensures that the deployed model maintains its quality over time. It does so by:
    * Monitoring model drift for performance issues.
    * Automate inferencing to receive latest data, perform feature engineering and feeding into the training stage.
    * Automate retraining model with latest data to minimise model drift.
    * Automate deployment of retrained model.

**1.2 Env Setup**
* Install [Docker Desktop](https://docs.docker.com/desktop/).
* Or run directly using Github Codespaces in your own ML Ops Zoomcamp repo.
* If using Github Codespaces, you should also install Anaconda distribution of Python as well to use Jupyter Notebook within Codespaces.
* Note that AWS EC2 instance isn't necessary for env setup as long as you could run Docker, Jupyter Notebook and Python on local workstation.

**Skipped optional unit 1.3**

**1.4 Course overview**
What we would learn from this course:
* Experiment tracker - log the metrics of various experimental models' performances.
* Model registry - a repository of the experimental models for reproducibility.
* ML Pipelines - a parameterisable ML process flow for consistent inferencing process from data loading, preprocessing to training and validating the model(s).
* Model Deployment - Methods to serve the optimal model for usage.
* Model Monitoring - Tracking the served model's performance on unseen data to ensure it does its job well. If not, this indicates model drift and the model should be retrained and redeployed to correct the drift.
* Best practices to automate the above, making the codes easily maintainable, plus easy to distribute and scale using Dockers and Kubernetes.
* And finally the different levels of ML Ops maturity from 0 to 4, where 0 indicates no ML Ops present and 4 means no human intervention present in the practices above. 

**1.5 ML Ops Maturity Model**
* [Microsoft MLOps Maturity Model](https://microsoft.github.io/azureml-ops-accelerator/1-MLOpsFoundation/1-MLOpsOverview/2-MLOpsMaturityModel.html)
* Level 0: No ML Ops automation. Usually just experimentation codes only, e.g. POC.
* Level 1: DevOps, no ML Ops. E.g. releases are automated, unit and integration test, CI/CD, following best practices in devops. However, none of the best practices of ML Ops and the data scientists are separated from engineers.
* Level 2: Automated training. There is ML pipeline and no manual execution of training. Contains experiment tracking, model registry, low friction deployment, data scientists work with engineers.
* Level 3: Automated deployment. Easy to deploy model with minimal/no human intervention. Can be a part of training pipeline where model is deployed automatically after training. Also contains A/B test to test 2 versions of models to see which one is better, and model monitoring.
* Level 4: Full ML Ops automation, i.e. automated training, deployment, and monitoring. Production systems are automatically improved with new models.
* We need to be pragmatic when it comes to the level of ML Ops we should apply, to ensure resources are utilised properly and the extent suits our use cases.

**Homework**
* [Link to questions](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2025/01-intro/homework.md)