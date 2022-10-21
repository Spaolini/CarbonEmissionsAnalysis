import math
import os
import flask
from flask import Flask, render_template, redirect, current_app, url_for, request
import csv
import json
import plotly
import plotly.express as px
import pandas as pd
import sqlite3

app = Flask(__name__)


@app.route('/')
def landing():
    return current_app.redirect("home.html")


@app.route('/home.html')
def home():  # put application's code here
    df = pd.read_csv("Data_Scaled.csv")
    avgCO2 = math.floor(df['CO2_Emissions'].mean() * 100)
    stdCO2 = df['CO2_Emissions'].std()
    print(stdCO2)
    CO2List = df.CO2_Emissions.tolist()

    # avgCH4 = math.floor(df['CH4_Emissions'].mean() * 100)
    # CH4LIst = df.CH4_Emissions.toList()

    for i in range(len(CO2List)):
        # CO2List[i] = math.floor(CO2List[i] * 100)
        if CO2List[i] < stdCO2 * 3:
            CO2List[i] = 'low emitter'

        elif CO2List[i] > stdCO2 * 3:
            CO2List[i] = 'high emitter'
    print(CO2List)

    graph = px.pie(df, title='High Emitters vs Low Emitters', values='CO2_Emissions', names="Category")
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("home.html", graphJSON=graphJSON)


@app.route('/map.html')
def map_page():
    return render_template("map.html")


if __name__ == '__main__':
    app.run()
#test
