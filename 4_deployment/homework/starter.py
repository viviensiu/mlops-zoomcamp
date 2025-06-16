#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import argparse

categorical = ['PULocationID', 'DOLocationID']

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
        return dv, model
    
def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def get_prediction(df, dv, model):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="year of Yellow taxi data")
    parser.add_argument("month", help="month of Yellow taxi data")
    args = parser.parse_args()

    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{args.year}-{args.month}.parquet')
    dv, model = load_model()
    pred = get_prediction(df, dv, model)
    print(f'Mean duration: {pred.mean():.2f}')
