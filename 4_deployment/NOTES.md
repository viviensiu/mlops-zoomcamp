**Links**
* [unit 4 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/04-deployment)

**4.1 Three ways of deploying a model**
* In previous units we talked about **Design** (requirements gathering),  **Train** (experiment tracking to save metrics, models and hyperparameters, create a training pipeline) which outputs a model, the next phase is **Operate** where a model is deployed.
* Questions to ask before deployment approach:
    * Can the deployment wait or it needs to be immediate for predictions? If yes, **batch or light deployment** where model is deployed during downtime to be applied to new data.
    * If not, it implies the model need to be up and running all the time, i.e. **online deployment**. Model is being deployed as a web service (http requests and response for predictions), or streaming (events-based when event models listen for events on the stream). 
* **Batch mode**:
    * Model is deployed at regular intervals.
    * At each interval, the model pulls the interval data from a database(e.g. last hour if it's an hourly interval), runs a scoring job to apply the model to this data and outputs the batch of predictions (maybe to another database) for processing)
    * Example: marketing-related tasks (churn prediction), 
* **Online mode (Web Service)**    
    * Example: ride duration prediction. The model is deployed as a web service, the user may initiate an app that connects to a backend which initiates a web service call to the model for duration prediction. And the user receives the info on their ride duration prediction.
* **Online mode (Streaming)**
    * In streaming settings, we have producers and consumers. A producer pushes events into event streams where consumers would read from the stream and react to them.
    * Example: media content moderation. There might be different consumers that look at different things, e.g.. NSFW, violence, copyright violation. Each of them make independent decisions if a video should be removed and you don't need all of them to reach a consensus to remove a video.
* **Web service vs Streaming**
    * Web service: 1 to 1 relationship. User-backend connection is kept alive during the whole process.
    * Streaming: 1 to many, or many to many. E.g. taxi ride may be an event containing ride information, the consumers would use these information differently such as predicting tips, duration and so on. The consumers are independent of each other. There is no explicit connection.

**4.2 Web-services: Deploying models with Flask and Docker**
* **Goal**: Take a pickle file and put into a Flask application.    
* **Note**: this is similar to what's done in ml zoomcamp deployment section. You will need some prior knowledge in Flask and Docker.
* You will also need `pipenv` preinstalled to create a virtual env for the app.
* **Reference**: `web-service` folder in unit 4.
* **Steps**:
    * Find out `sklearn` version used as it needs to be compatible with the pickle file: `pip freeze | grep scikit-learn`.
    * Create the virtual env: `pipenv install scikit-learn==<version used> flask --python==<version used>`, this should create a new `pipfile` or add these packages into an existing `pipfile`.
    * Activate virtual env: `pipenv shell`.
    * Create a script `predict.py` with Flask wrapper codes to handle the web service. It loads the pickle file, receives incoming http request for user input and returns a http response for prediction.
    * Test the web service using `test.py` in a new terminal window. Before that, service the Flask web service by doing `python predict.py`.
    * To solve the WSGI error message, setup Gunicorn: `pipenv install gunicorn`, then run `gunicorn --bind=0.0.0.0:<your port number> predict.py`.
    * To solve the `no module named 'requests' error` in development env but skip it in production, we will need to install requests only in dev using `pipenv install --dev requests`.
    * To package the app into Docker container:
        * Create a `Dockerfile`.
    * Build the Docker image with tag: `docker build -t ride-duration-prediction-service:v1 .`.
    * Start the container in interactive mode, container deleted after stopped, and map host port to container port: `docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1`.

 **4.3 Web-services: Getting the models from the model registry (MLflow)**
 * **Reference**: `web-service-mlflow` folder in unit 4.
 * **Note**: This video loads MLflow model of a specific experiment run that is stored in Amazon S3 bucket or any equivalent online source.
 * **Steps**:
    * Take the code from the previous video, i.e. `web-service`.
    * Create a pipeline that contains both the model and the vectoriser so they don't need to be downloaded separately using mlflow tracking uri and mlflow client: `from sklearn.pipeline import make_pipeline`.
    * Pipeline flow: create DictVectorizer or any vectoriser first, followed by the model.
    * Log the pipeline in `mlflow.sklearn.log_model()` to include this in the artifacts.
    * Modify `predict.py` to retrieve the logged MLflow pipeline using `run id`: `mlflow.pyfunc.load_model()`.
    * Add mlflow package into pipfile: `pipenv install mlflow boto3`.
    * We want to avoid hardcoding the tracking server inside the script because it cannot handle issues like when the server is down or we need to scale up, then another server instance needs to be created and therefore the server details will change. Hence we use env variables to pass in server info, run id and so on instead.

**4.4 Streaming: Deploying using AWS Lambda and Kinesis (Optional)**
* Refer [this video](https://youtu.be/TCqr9HNcrsI?si=kkllG4BhwKEGwgJt) for the process.

**4.5 Batch: Preparing a Scoring Script**
* **Goal**: Deploy models in batch mode (offline mode).
* **Use case**: To see how often the taxi drivers have the actual ride durations deviate from the predictions.
* **Step**:
    * Turn an experimental notebook into a notebook that applies the model. The training sections are removed since we focus on application, add unique IDs for each record using `uuid` package, parameterise the notebook to allow dynamic year month values to be passed in, put codes in functions, and save predicted results, difference between predictions and actual durations into a Parquet file. See `score.ipynb`.
    * Turn `score.ipynb` into a script `score.py`: `jupyter nbconvert --to script score.ipynb`
    * Add a main function to accept system arguments `sys.argv[.]` and clean up markdowns in `score.py`.
    * Test running `score.py`, then upload to online storage e.g. AWS S3.
* Tips for further improvement:
    * Specify all dependencies e.g. using `pipenv`.
    * Package into Docker Container. Schedule it to run in batch jobs e.g. ECS, Kubernetes or AWS Batch.

**Homework**
* [Link to questions](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2025/04-deployment/homework.md)