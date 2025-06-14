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
* **Steps**:
    * Find out `sklearn` version used as it needs to be compatible with the pickle file: `pip freeze | grep scikit-learn`.
    * Create the virtual env: `pipenv install scikit-learn==<version used> flask --python==<version used>`, this should create a new `pipfile` or add these packages into an existing `pipfile`.
    * Activate virtual env: `pipenv shell`.
    * Create a script `predict.py` to run the web service codes. It loads the pickle file, receives incoming http request for user input and returns a http response for prediction.
