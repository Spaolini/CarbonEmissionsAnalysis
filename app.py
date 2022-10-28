import csv
import json
import math
import pandas as pd
import plotly
import plotly.express as px
from csv import writer
import sqlite3
from flask import Flask, render_template, current_app
from plotly.offline import plot
import plotly.graph_objs as go

app = Flask(__name__)


@app.route('/')
def landing():
    return current_app.redirect("home.html")


@app.route('/home.html')
def home():  # put application's code here
    df = pd.read_csv("Data_Scaled.csv")
    de = pd.read_csv("highEmitter.csv")
    df.head()
    meanco2 = df['CO2_Emissions'].mean()
    stdco2 = df['CO2_Emissions'].std()
    above = meanco2 + (stdco2 * 2)
    CO2List = df.CO2_Emissions.tolist()
    facList = df.Facility.tolist()
    df['e'] = (df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std()))

    graph = px.bar(df, title="CO2 Emissions by Facility", x="Facility", y="CO2_Emissions", error_y="e")
    chart = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    for i in range(len(df)):
        if CO2List[i] > (df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std() * 2)):
            print(facList[i])
            print(CO2List[i])

    graph2 = px.bar(df, title="CO2 High Emitters", x=facList, y=CO2List)
    chart2 = json.dumps(graph2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("home.html", chart=chart, chart2=chart2)


@app.route('/map.html')
def map_page():
    return render_template("map.html")


if __name__ == '__main__':
    app.run()
