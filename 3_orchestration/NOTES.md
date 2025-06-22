**Links**
* [unit 3 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/03-orchestration)
* [2023 repo for Prefect](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/cohorts/2023/03-orchestration/prefect)
* [Prefect Python SDK API Documentation](https://reference.prefect.io/prefect/)

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

## The following notes are based on 2023 Prefect videos
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
    * **Note**: I have post-setup issues if setup using the original `requirements.txt`. Different post-setup issues if I use `conda install prefect` in conda env `exp-tracking-env` setup since Unit 2.
    * The issues surface when I try to run `prefect server start`.
    * The issues resolved when I run the following on my Mac arm64:
    ```bash
    conda create -n prefect-env python==3.12
    conda activate prefect-env
    pip install -U prefect --pre
    ```
    * Reference for the setup that works: [Getting started with Prefect part 1 - Nate from Prefect](https://youtu.be/Y1eDm50BDIU?si=ckRR2Ku2kd1hEbxI)
    * **Note**: I could also run `pip install -U prefect` in conda env `exp-tracking-env`. Starting prefect server after this would create some IO exceptions that is ignored by the Prefect server.
* Start Prefect server: `prefect server start`.
* Copy and run the Prefect API url in a new terminal window (env activated) to ensure we send our server metadata to the server's UI:
    `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`
* Test sample codes `cat_facts.py` and `cat_dog_facts.py` by running it with python in terminal. You should see a new flow run record captured in `Prefect UI > Runs`.
* You could view a timeline and logs of this flow run by clicking on the flow run record in UI.
* Prefect functions:
    * `@task`: configurable for retries, logging and so on. Make sure to set `log_prints=True` to enable logging to the UI.
    * `@flow`: decorator to execute a Prefect flow. Make sure to set `log_prints=True` to enable logging to the UI.
    
**3.3 Prefect Workflow**
* Explains how to convert a jupyter notebook `duration_prediction_explore.ipynb` to `orchestrate_pre_prefect.py`. **Note**: The codes are outdated since 2023 and some codes would need to be updated, e.g. sklearn mean_squared_error.
* The basic notebook clean up is similar to the 2025 run of unit 3.2, refer those notes.
* To add observability and orchestration with Prefect, the following is used:
    * `@task(retries=..., retry_delay_seconds=..., caching=...)`: To set retries, delays between retries and caching for saving.
    * `@task(log_print=True)`: log print outs.
    * `@flow`: to run tasks.
* Refer `orchestrate.py` for the Prefect codes.

**3.4 Deploying Your Workflow**
* We use `prefect project` for deployment. Here we assume that our script is already wrapped with Prefect decorators.
* Step 1 `prefect project init`: initialise the files for deployment. Creates:
    * `.prefectignore`
    * `prefect.yaml`: file to configure deployment build, push and pull steps.
    * `deployment.yaml`:
* Step 2 login to Prefect cloud `prefect cloud login` or start local server `prefect server start`.
* Step 3 start a worker that polls your workpool `prefect worker start -p <pool name> -t process` or via the UI:
    * `Work Pools > Create`: enter name, type=`Process`. Click create.
* Step 4 Deploy your flow `prefect deploy <script name>`:<flow decorated function to start within the script> -n <flow name> -p <work pool created in step 3>'
* Step 5 start a run of the deployed flow from terminal `prefect deployment run <flow name from step 4>` or inside UI:
    * `Flows --> <flow decorated function to start within the script> --> <flow name> --> (...) menu --> quick run`.
    * You should see the completed run, logs and etc under UI > `Flow Runs`.
* ![image of Prefect create run deployment](https://github.com/viviensiu/mlops-zoomcamp/blob/main/3_orchestration/Prefect/Activity-create-run-deployment.png)

**Homework**
* [Link to questions](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2025/03-orchestration/homework.md)

