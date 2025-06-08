**Links**
* [unit 3 repo]()
* [2023 repo for Prefect](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/cohorts/2023/03-orchestration/prefect)

**3.1 ML Pipeline**
* Pipeline: sequence of steps, e.g. training pipeline would be a sequence of steps to train a model.
* **ML Pipeline a.k.a Workflow Orchestration** organise the ML steps to work in order.
* Example of steps in a ML Pipeline:
    * **Ingestion**: data download.
    * **Transformation**: feature preprocessing, e.g. changing data types, filtering, removing outliers, aggregation.
    * **Preparing data for ML**: feature engineering, creating features and target sets.
    * **Hyperparameter tuning**: see `hyperopt` examples used in previous unit.
    * **Train the final model**.
    * **Save model to model registry**.
* One example to orchestrate is to convert a notebook into a Python script. However there are some caveats:
    * How do we schedule this?
    * How do we manage multiple sccripts?
    * Where could we deploy/host this?
    * How to make it accessible for collaboration?
    * How do we version control?
    * How do we manage scalability?
    * How do we retry automatically when there is maintenance or other issues?
    * What about dependency management?
* The answer is to use a tool for orchestration. Example tools (can be general purpose or ML-specific):
    * Airflow.
    * Prefect.
    * Mage.
    * Kubeflow pipelines.
    * MLflow pipelines.

**3.2 Turning notebook into python script**
* Preparation:
    * Start jupyter notebook instance to bring up the experimental notebook to be converted.
    * Start `mlflow server`.
* Steps in notebook:
    * Remove visualisation libraries.
    * change URI instance from `sqlite://...` to `localhost...`, refer to started MLflow server for the localhost port.
    * Remove redundant codes, e.g. experimental codes, experimenting with multiple models.
    * Keep the hyperparameter tuning codes.
    * Adjust the number of training rounds if it's too long/short.
    * Adjust paths to make it dynamic or auto-create new folders if folder is missing.
    * Ensure the adjusted notebook works by running it end to end.
* Convert notebook into script: 
    ```bash 
    jupyter nbconvert --to=script <notebook name>
    ```
    if it runs properly you should get a `.py` file that follows the notebook name without `.ipynb` extension.
* Clean and organise the script code:
    * Organise all imports together.
    * Remove redundant comments.
    * Organise codes into functions. They should reflect the steps intended for orchestration.
    * Adjust the parameters in functions to make it more dynamic, e.g. allow pass in year and month, create a `DictVectorizer` if none is provided.
    * In `main()` function, organise the functions into the orchestration steps. You may include parameters in `main()` to allow users to pass in values.
    * To allow users to pass in parameters outside of script, use `argparse.ArgumentParser()`.
* Ensure script is working by end-to-end test.

**The following notes are based on 2023 Prefect videos**
**3.1 Intro to Workflow Orchestration**
* [Prefect](https://www.prefect.io/) allows you to orchestrate & observe your Python workflows at scale.
* [Prefect](https://www.prefect.io/) provides tools to work with complex systems so you can stop wondering about your workflows.
* Goal: Learn how to use [Prefect](https://www.prefect.io/) to orchestrate & observe your ML workflows.

**3.2 Intro to Prefect**
* Goal:
    * Clone github repo.
    * Setup conda env.
    * Start a Prefect server.
    * Run a Prefect flow.
    * Checkout Prefect UI.
* Why use [Prefect](https://www.prefect.io/): Flexible, open source framework to turn standard pipelines into fault-tolerant dataflows.
* Installation:
    ```bash
        pip install -U prefect
    ```
    also refer [Install Prefect](https://docs.prefect.io/v3/get-started/install).
* Self-hosting a [Prefect](https://www.prefect.io/) server:
    * Orchestration API: Rest API used by server to work with workflow metadata.
    * Database: local sqlite db that stores workflow metadata.
    * UI: visualises workflows.
    * Also refer [Hosting Prefect](https://docs.prefect.io/v3/how-to-guides/self-hosted/server-cli).
* Terminology:
    * Task: A discrete unit of work in a Prefect workflow. just like a regular Python function.
    * Flow: Container for workflow logic. Can be leveraged as parent functions to call tasks, define state and data dependencies.
    * Subflow: flow called by another flow.
* In a Prefect workflow, you'll require task and flow decorators to convert existing scripts into workflows. Arguments are accepted for these decorators.
* Environment setup: 
    * Download the `requirements.txt` in this folder.
    ```bash
    conda create -n prefect-ops python==3.9.12
    conda activate prefect-ops
    pip install -r requirements.txt
    ```
    * Alternatively to reuse the `exp-tracking-env` that was setup since Unit 2, you could just:
    ```bash
    conda activate exp-tracking-env
    conda install prefect
    ```
* Once installed, start Prefect server using `prefect server start`. 

