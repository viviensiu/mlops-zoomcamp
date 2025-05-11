Links:
* [unit 2 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/02-experiment-tracking)

**2.1 intro**
* "ML experiment" here refers to the process of building an ML model, not A/B testing. E.g. playing with hyperparameters and different models.
* "Experiment run": a trial in an ML experiment.
* "(Experiment) Run artifact": any file associated with an ML run.
* "Experiment metadata" is all data associated with an experiment.
* **Experiment tracking** is the process of keeping track all the info from an ML experiment, e.g. source code, env, data, model, hyperparameters, metrics and so on.
* Why is this important? 
    * **Reproducibility**: easy to recreate same results of past experiments.
    * **Organisation**: easier to collaborate, share findings and keeping track of history.
    * **Optimisation**: different trials can be visualised which could produce insights that help to optimise the models.
* Issues with tracking experiments in excel: error prone due to manual input, no standard format to understand and compare results, lack of visibility/visualisation to understand progress and collaboration.
* **[MLflow](https://mlflow.org/)** is an open source platform for ML lifecycle. It's a Python package that can be installed with pip and contains four main modules: tracking, models, model registry, projects. tracking and model registry is covered in this course.
* **MLflow Tracking** module allows experiments to be organised into runs and to keep track of parameters, metrics, metadata (e.g. tags), artifacts (files, visualisations), models. Also logs extra info such as source code, code version, start and end time, author.

**2.2 Getting started with MLflow**
* Env setup for **Mac arm64**:
    * Create a [requirements.txt](https://github.com/viviensiu/mlops-zoomcamp/blob/main/2_experiment_tracking/requirements.txt) file like so.
    * Navigate to the folder containing ```requirements.txt``` and execute the following in terminal: 
    ```bash
    conda create --name exp-tracking-env --file requirements.txt
    ```
    * If encounter issue such as `hyperopt not found`, add ```conda-forge``` into conda channels:
    ```bash
    conda config --append channels conda-forge 
    ```
    * once done, run ```conda activate exp-tracking-env```.
    * Test that MLflow setup is successful by running ```mlflow ui```. You should see a page in localhost.
* Adding a storage at the backend: ```mlflow ui --backend-store-uri sqlite:///mlflow.db```. This tells MLflow that we want to store the artifacts and metadata using sqlite.
* Testing MLflow with [duration-prediction.ipynb](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/duration-prediction.ipynb):
    * Download the notebook from course repo unit 2 folder to working folder.
    * Add data files. 
    * Create new subfolder ```models``` to store models.
* To include MLflow tracking in notebook:
    * Setup the backend storage: ```mlflow.set_tracking_uri()```.
    * Set the ML experiment: ```mlflow.set_experiment()```.
    * Track experiment runs: ```mlflow.start_run()```.
    * Add metadata: ```mlflow.set_tag()```.
    * Log parameters: ```mlflow.log_param()```.
    * Log metric: ```mlflow.log_metric()```.
    * Log artifacts: ```mlflow.log_artifact()```.


