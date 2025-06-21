**Links**
* [unit 5 repo]()

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
* Create a baseline model [`baseline_model_nyc_taxi_data.ipynb`]() which will:
    * Download NYC taxi datasets for Jan and Feb 2022.
    * Preprocess data and split into training and validation sets.
    * Train a baseline model using `LinearRegression` model.


