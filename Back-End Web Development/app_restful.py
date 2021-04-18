import os
from flask import Flask
import pandas as pd
from flask import render_template, jsonify, request
import json
from flask_restful import Api, Resource
from assets.assets import url_params, translation
from database import *

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello' : 'world'}

class GetData(Resource):
    def get(self):
        params = {}
        for param in url_params:  #iterate over 'accepted' params and save values in dict
            if request.args.get(param):
                params[param] = request.args.get(param)

        if params:
            jsondata = get_data_by_params(params)
        else:
            jsondata = get_all()


        return jsondata

class GetCountry(Resource):
    def get(self):
        params = {}
        for param in url_params:  #iterate over 'accepted' params and save values in dict
            if request.args.get(param):
                params[param] = request.args.get(param)

        countries = get_countries_by_params(params)

        return countries


api.add_resource(HelloWorld, '/')
api.add_resource(GetData, '/api/gapminder')
api.add_resource(GetCountry, '/api/country')


def get_countries_by_params(params):

    param_sql = get_translated_keys(params)

    countries = get_country_by_params(param_sql)
    return countries

def get_data_by_params(params):

    param_sql = get_translated_keys(params)

    data = get_selection_by_params(param_sql)
    return data


def get_translated_keys(params):
    param_sql = {}
    for key, value in params.items():
        if len(key.split("_")) > 1:
            col_name, classifier = key.split("_")
            translated = translation[col_name] 
            col = translated + "_" + classifier
        else:
            col = translation[key] 

        if value.isdigit():
            value = int(value)
        elif value.isalpha():
            value = value.capitalize()
        else:
            value = float(value)
        
        param_sql[col] = value 

    return param_sql

if __name__ == '__main__':
    create_tables()
    print(get_selection_by_params({'Year':2002}))
    print(get_country_by_params({'Year':2002, 'continent':'Asia'}))
    app.run(debug=True, host="0.0.0.0")

