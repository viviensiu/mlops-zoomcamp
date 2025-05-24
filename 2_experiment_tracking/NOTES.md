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

**2.3 Experiment tracking with MLflow**
* Using `hyperopt` to use Bayesian method to find an optimal set of hyperparameters.
* How to define hyperopt search spaces: [hyperopt documentation](https://hyperopt.github.io/hyperopt/getting-started/search_spaces/).
* After executing the hyperopt, one could view the experiment results at MLflow UI. There is also scatter plot and contour plot to show the correlation of the hyperparameters with chosen metric.
* To select the best model from experiment runs, you could sort results by metrics in MLflow and view the hyperparameters used there.
* Note that the best model may not be suitable for you due to resource constraints (requires larger space, more CPU-demanding) so you need to decide base on your own use cases.
* After selecting the best model, you could train a final model with those hyperparameters.
* Depending on the model framework, MLflow allows [autologging](https://mlflow.org/docs/latest/tracking/autolog). E.g. with XGBoost ```mlflow.xgboost.autolog()```. It not only logs a more complete set of hyperparameters but also feature importances, packages version used, the conda env, and the MLflow model. The `.model` file provides info on how to run this model based on `flavors`, e.g. you can it as a python function or an xgboost for this module's sample code. If you click on `model` folder inside MLflow UI, you can see sample codes on how to make predictions using the logged model.

**2.4 Model Management**
* Covers experiment tracking, model versioning, model deployment and scaling of hardware.
* This helps to ensure that different models resulted from experiment runs are tracked and managed accordingly, as different models may cater to different scenarios, e.g. more or less resource-intensive (scaling), model versions may rely on different dependencies, and so on.
* ```mlflow.set_tracking_uri()```: sets the database URI for saving tracking info. **This needs to be done first**.
* ```mlflow.log_artifact()```: Logs and saves the model by passing in local path and artifact path, saved artifacts could be found under ```Artifacts > model``` in MLflow.
* ```mlflow.<framework>.log_model()```: Logs and saves the model by passing in model object and artifact path, which could be found under ```Artifacts > (artifact path)``` in MLflow.
* When saved using ```log_model()```, the model contains .yaml file, requirements.txt and the model itself. .yaml provides info on the model environment, which may include packages not called by the experiment but from the conda env it ran in.
* Note that you could also use MLflow to save feature transformation model (e.g. DictVectorizer model) using the methods above.
* As in 2.3, you could deploy the logged model in either Python or the framework flavor under the ```Make Predictions``` section that's available when scroll further down within ```Artifacts```.

**2.5 Model Registry**
* A model registry in MLflow is useful for tracking models that are ready for different stages. E.g. when models are ready for production deployment, this could be marked by the experimentation team like so, and the deployment team could just look at the registry and deploy them as indicated.
* Models could also be registered depending on different stages such as staging, production and archive, which helps to manage models.
* Note: Model registry is not used for deployment but for labelling purposes only.
* Registering models in MLflow:
    * Under ```Artifacts```, click on ```Register Model```.
    * Either ```Create New Model``` > key in new model name > register.
    * Or select an existing model name and register under that name.
* Under ```Models``` tab, you can find the registered models and the different versions it has. You could even add a description and tags.
* Click on different model version provide you the ```source run``` it's linked to, which then shows you the logged info associated with this version. Each version could have its own description and tags as well.
* You could also change the ```Stage``` transition to staging, production and archived.
* To interact with the MLflow tracking server **outside of a run context**, you use **MLflow Client** instead. It is a lower-level API helps you to do things such as 
    * Querying past experiments
    * Creates and manages registered models
    * Managing model stages
    * Getting run details without being inside a with ```mlflow.start_run()```: block.
* Note: always set tracking URI beforehand.    
* Useful functions via **MLflow Client** object:
    * ```list_experiments()```: list past experiments done.
    * ```create_experiment()```: create new experiment.
    * ```search_runs()```: query and filter past runs.
    * ```register_model()```: register new model.
    * ```list_registered_models()```: list all registered models in registry.
    * ```get_latest_versions()```: returns a list of model versions and metadata such as status.
    * ```transition_model_version_stage()```: transition model stage.
    * ```update_model_version()```: update version and add optional description.




**Other Resources**
* [Neptune.ai: Why ML Experiment Tracking matters](https://www.linkedin.com/pulse/ml-experiment-tracking-what-why-matters-how-implement-jakub-czakon/)

