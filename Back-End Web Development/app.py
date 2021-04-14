import os
from flask import Flask
import pandas as pd
from flask import render_template, jsonify, request
import json
from flask_restful import Api
from assets.assets import url_params, translation

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/gapminder', methods=["GET"])
def read_data():
    if request.method == "GET":
        df = pd.read_csv("gapminder_clean.csv")
        jsondata = json.loads(df.to_json(orient='records'))
        return render_template('index.html', ctrsuccess=jsondata)

@app.route('/api/country', methods=["GET"])
def get_country(url_params=url_params):
    if request.method == "GET":

        df = pd.read_csv("gapminder_clean.csv")  #load data

        params = {}
        # print(request.args)  #gte all passed params
        for param in url_params:  #iterate over 'accepted' params and save values in dict
            if request.args.get(param):
                # request.args.get(param).split("_")
                params[param] = request.args.get(param)
        # jsondata = json.loads(df.to_json(orient='records'))

        countries = get_countries_by_params(params, df)


        return render_template('url_params.html', ctrsuccess=countries)

def get_countries_by_params(params, df):
    subset_df = df.copy()
    for key, value in params.items():
        if len(key.split("_")) > 1:
            key = key.split("_")    
            col = translation[key[0]]
            if value.isdigit():
                value = int(value)
            else:
                value = float(value)
            if key[1] == 'gt':
                subset = df[col] > value
            elif key[1] == 'st':
                subset = df[col] < value
        else:
            col = translation[key] 
            try:
                value = int(value)
                subset = df[col] == value
            except ValueError:
                value = value.capitalize()
                subset = df[col] == value

        subset_df = subset_df[subset]
    
    countries = list(subset_df['Country Name'].unique())
    return countries

def get_data_by_params(params, df):
    subset_df = df.copy()
    for key, value in params.items():
        if len(key.split("_")) > 1:
            key = key.split("_")    
            col = translation[key[0]]
            if value.isdigit():
                value = int(value)
            else:
                value = float(value)
            if key[1] == 'gt':
                subset = df[col] > value
            elif key[1] == 'st':
                subset = df[col] < value
        else:
            col = translation[key] 
            try:
                value = int(value)
                subset = df[col] == value
            except ValueError:
                value = value.capitalize()
                subset = df[col] == value

        subset_df = subset_df[subset]
    
    return subset_df

if __name__ == '__main__':
    app.run(debug=True)

