**Links**
* [unit 5 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/05-monitoring)

**5.1 Intro to Monitoring**
* Often in production, model performance starts to degrade after some time and we need to account for it through monitoring.
* Monitoring accounts for data health, service health and model health.
* Basic set of monitoring:
    * Service health: To make sure it works.
    * Model performance: Ensure performance quality and minimise breakage.
    * Data quality and integrity: To identify the source of breakage/issues, missing values.
    * Data and concept drift: To identify if the model is robust/relevant.
* Others: performance by segment, model bias/fairness, outliers, explainability.
* Batch vs Online serving model influences how we could do monitoring. If your company has existing production services deployed it's likely there's already monitoring in place. Hence you could reuse those.
* Batch mode data quality can be evaluated based on past data:
    * Expected data quality.
    * Data distribution.
    * Statistics e.g. mean, median, quantiles, min-max for individual features. Point estimates, or statistical tests to get confidence interval.
* Non-batch mode:
    * Metrics are calculated continuously or incrementally, e.g. using moving windows, or in real-time.
* Monitoring scheme: Starting from software service (batch/online mode), we build our monitoring on top of logged predictions. We have monitoring jobs to read the prediction logs by batch, analyse them, calculate some metrics and store them. These metrics are later on visualised on dashboards for monitoring.

**5.2 Env Setup**
* Create new folder `mkdir taxi_monitoring`.
* In `taxi_monitoring` folder:
    * `conda create -n py11 python=3.11`
    * `conda activate py11`.
* Create `requirements.txt`:
    ```
    prefect
    tqdm
    requests
    joblib
    pyarrow
    psycopg
    psycopg_binary
    evidently==0.6.7
    pandas
    numpy
    scikit-learn
    jupyter
    matplotlib
    ```
* Run `pip install -r requirements.txt` to install packages in this virtual env.
* Create [`docker-compose.yml`](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/docker-compose.yml).
* Create sub-folder `config` to store Grafana configurations. Inside, create `grafana_datasources.yaml` and `grafana_dashboards.yaml`.
* Bring up the containers using `docker compose up --build`.
* Try to access Grafana using `localhost:3000` with username and password equals `admin`. Grafana will ask you to change the password afterwards. Personal note: local Grafana password is changed to `.....1234`.
* Also try to access Adminer at `localhost:8080`.
* If all the above works, the env setup is completed.
* To bring down the containers, in a new terminal, execute `docker-compose down`.

**5.3 Prepare reference and model**
* Create two sub-folders: `models` and `data`.
* Create a baseline model [`baseline_model_nyc_taxi_data.ipynb`](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/baseline_model_nyc_taxi_data.ipynb) which will:
    * Download NYC taxi datasets for Jan and Feb 2022.
    * Preprocess data and split into training and validation sets.
    * Train a baseline model using `LinearRegression` model.
    * Evaluate model on validation data using MAE metric.
    * **Save model and reference data for monitoring**: The reference data provides a baseline data distribution to be compared against latest data to identify data drifts which causes performance drop.

**5.4 Evidently metrics calculation**
* [Evidently](https://www.evidentlyai.com/) provides the convenience of computing various metrics for different ML aspects which is useful for monitoring.
* We begin by: 
    * Define column mappings of target, prediction, numerical and categorical columns in `ColumnMapping`.
    * Define reporting metrics with `Report`.
    * Run report generation with `report.run(reference_data=..., current_data=..., column_mapping=...)`.
* The generated report can be viewed in Notebook using `report.show(mode='inline')`, or converted to dictionary to pull out the metrics for further use `report.as_dict()`.

**5.5 Evidently Monitoring Dashboard**
* **Goal**: We will be using [Evidently](https://www.evidentlyai.com/) to build a monitoring dashboard.
* **Steps**:
    * Import `DataDriftPreset`: A base for data quality monitoring.
    * Import `Workspace`: A base to store our data.
    * Import `DashboardPanelCounter, DashboardPanelPlot, CounterAgg, PanelValue, PlotType, ReportFilter, WidgetSize`: Configure the dashboard.
    * Create the local workspace with `Workspace`.
    * Create the project in this workspace `ws.create_project()`, add a project description `project.description` and save it (`project.save()`).
    * Build a report `Report` and add it to the workspace to track the project progress. You could add a specific `timestamp` in the report to track plots for this specific date.
    * Calculate the report `report.run()`, preview it by invoking the report object itself, if you like it then you can add it to the workspace: `ws.add_report(project.id, report)`.
* We could view the report directly in :
    * To view all Evidently commands: `evidently ui --help`
    * Start UI service: `evidently ui`.
    * To view the report as per preview, first click on the correct project, go to `Reports`, navigate to the right report ID, then click on `View`.
* Steps for adding a dashboard into the project:
    * `project.dashboard.add_panel(DashboardPanelCounter(...))`.
    * The panels could be made up of different plots as well using `DashboardPanelPlot` and specify the plot type, e.g. bar plot: `plot_type=PlotType.BAR`.
    * The displayed values are configured under `values=[PanelValue(...)]`.
    * Don't forget to save your project! `project.save()`.
    * Refresh your Evidently UI and you should be able to see the dashboard under the project's `Dashboard` tab.

**5.6 Dummy Monitoring**
* **Goal**: We will attempt to calculate some dummy metrics, save into database and try to access it via Grafana.
* We will run [dummy_metrics_calculation.py](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/dummy_metrics_calculation.py) to generate dummy metrics.
* **Steps**:
    * Make sure Grafana and Adminer is up by `docker-compose up --build`.
    * Once the containers are up, execute `python dummy_metrics_calculation.py`.
    * Once a few iterations have passed, we can login to Adminer via `localhost:8080` with the same username, password and database `test` specified in [dummy_metrics_calculation.py](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/dummy_metrics_calculation.py) to see the random data that was created.
* Add a new Grafana dashboard:
    * Login to Grafana. Note that if the previous Docker containers are removed then login with the default `admin` username and password.
    * `Add new dashboard` > `New Panel` > under `Query` >  toggle from Builder to Code, and copy paste the following:
    ```sql
    SELECT
    $__time(timestamp),
    value1
    FROM dummy_metrics 
    WHERE $__timeFilter(timestamp)
    ORDER BY timestamp
    ```
    * Click `Run Query` and toggle the time range to see the different visualisations displayed on the dashboard.   

**5.7 Data Quality Monitoring**
* We modify the script from 5.6 to incorporate Evidently monitoring as in Section 5.5.
* See [evidently_metrics_calculation.py](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/evidently_metrics_calculation.py).
* The script will:
    * Read daily data from Feb 2022 onwards to simulate production usage by batch. In reality there will be data pipeline for reading data.
    * Create column mapping and pass it into report object as in Section 5.5. 
    * Extract current data and generate predictions.
    * With historical and current data, run the report object to generate monitoring metrics. 
    * The metrics are inserted into Postgresql database table.
    * Finally, use Prefect to orchestrate the pipeline of all above. Refer [unit 3 notes](https://github.com/viviensiu/mlops-zoomcamp/blob/main/3_orchestration/NOTES.md) on Prefect.
        * The main pipeline is `batch_monitoring_backfill` as it has the `@flow` decorator.
        * The pipeline contains 2 steps: `prep_db()` and `calculate_metrics_postgresql()` to ensure the database and tables are ready, and to generate the Evidently monitoring metrics.
* In virtual env `py11`, bring up Prefect server `prefect server start`.
* Execute `python evidently_metrics_calculation.py`. There would be some hashing error flagged by Prefect but Adminer will reflect that the monitoring metrics are captured without issues.
* You can build a new dashboard with multiple plots in Grafana using:
```sql
    SELECT
    $__time(timestamp),
    prediction_drift
    FROM dummy_metrics 
    WHERE $__timeFilter(timestamp)
    ORDER BY timestamp

    SELECT
    $__time(timestamp),
    num_drifted_columns
    FROM dummy_metrics 
    WHERE $__timeFilter(timestamp)
    ORDER BY timestamp

    SELECT
    $__time(timestamp),
    share_missing_values
    FROM dummy_metrics 
    WHERE $__timeFilter(timestamp)
    ORDER BY timestamp
```
* Adjust the timestamps to between Feb 1, 2022 to Feb 28, 2022 to reflect the timestamps used by the sample data, so you could view the predictions plotted.
* Adjust the colors (click on the color in legend) and plot types (right panel > `Visualizations`) as you wish.

**5.8 Save Grafana Dashboard**
* **Goal**: Saving and reusing the dashboard.
* Create a sub folder `dashboards` under `taxi_monitoring`.
* In `docker-compose.yml`, specify the volumes under Grafana so it knows to load from `dashboards`.
* In `dashboards`, create `data_drift.json`.
* Go to the Grafana dashboard you wanted to save, click `Settings > JSON Model`, copy paste into `data_drift.json`. This allows you to load the same dashboard even after stopping docker compose.
* To prove this works:
    * `docker compose down`
    * `docker-compose up --build`, you could access Grafana at this step and see that the dashboard is still here but without data. Run the next step to repopulate Postgresql with data.
    * `python evidently_metrics_calculation.py`.
    * You should now be able to view data in Grafana.

**5.9 Debugging with test suites and reports**
* Monitoring helps us detect the time something went wrong and rectify issues on time.
* **Goal**: Drift detection and debugging support using Evidently test suites and reports.
* We setup a new notebook [`debugging_nyc_taxi_data.ipynb`](https://github.com/viviensiu/mlops-zoomcamp/blob/main/5_model_monitoring/taxi_monitoring/debugging_nyc_taxi_data.ipynb):
    * Import `DataDriftPreset` from `evidently.metric_preset` to help build visual boards and address specific parts of the pipeline. This preset is for data creation moments.
    * `TestSuite` helps to compare metric values against threshold.
    * `DataDriftTestPreset` helps to tackle specific data-related problems using a predefined set of **data drift statistical tests**.
    * First we specify a reference set of data as a baseline for comparison. We also load a specific data as problematic sample (difers greatly from reference set).
    * We specify a `TestSuite(tests=[DataDriftTestPreset])` to calculate data drift tests. More tests can be specified.
    * Run predictions on the loaded sample problematic data and fill missing values.
    * `test_suite.run()` to run tests. Then visualise the test results using `test_suite.show(mode='inline')`. The results can also be shown in other formats e.g. HTML and JSON.
    * We could also run reports with test suites to support analysis and debugging: `Report(metrics = [DataDriftPreset()])`. The report can either be shown in notebook or exported as HTML format.
    * Notice that when the problematic data's distribution differs greatly from reference set, data drift is flagged by the predefined tests and can be viewed in the report. This helps with monitoring the issue and pinpoint where we need to do some debugging.

**References**
* [Evidently documentation](https://docs.evidentlyai.com/introduction).
