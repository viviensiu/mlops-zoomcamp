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
