# mlops-zoomcamp
My learning notes for DataTalks.Club ML Ops zoomcamp

## Environment setup
* Done using conda. Environment can be recreated using the `environment.yml` file with following command.
```bash
conda create --name <env name> --file environment.txt
```

## Update environment.yml
```bash
conda env export --from-history > environment.yml
```
