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
from dash import Dash, dcc, html, Input, Output

app = Flask(__name__)


@app.route('/')
def landing():
    return current_app.redirect("home.html")


@app.route('/home.html')
def home():  # put application's code here
    df = pd.read_csv("Data_Scaled.csv")
    # de = pd.read_csv("highEmitter.csv")
    df.head()

    # CO2 Analysis
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

    print("\n")

    # CH4 Analysis
    CH4List = df.CH4_Emissions.tolist()
    df['er'] = (df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std()))

    graphCH4 = px.bar(df, title="CH4 Emissions by Facility", x="Facility", y="CH4_Emissions", error_y="er")
    chartCH4 = json.dumps(graphCH4, cls=plotly.utils.PlotlyJSONEncoder)

    for i in range(len(df)):
        if CH4List[i] > (df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std() * 2)):
            print(facList[i])
            print(CH4List[i])

    graphCH4_2 = px.bar(df, title="CH4 High Emitters", x=facList, y=CH4List)
    chartCh4_2 = json.dumps(graphCH4_2, cls=plotly.utils.PlotlyJSONEncoder)

    print("\n")

    # N2O Analysis
    N2OList = df.N2O_Emissions.tolist()
    df['err'] = (df['N2O_Emissions'].mean() + (df['N2O_Emissions'].std()))

    graphN2O = px.bar(df, title="N2O Emissions by Facility", x="Facility", y="N2O_Emissions", error_y="err")
    chartN2O = json.dumps(graphN2O, cls=plotly.utils.PlotlyJSONEncoder)

    for i in range(len(df)):
        if N2OList[i] > (df['N2O_Emissions'].mean() + (df['N2O_Emissions'].std() * 2)):
            print(facList[i])
            print(N2OList[i])

    graphN2O_2 = px.bar(df, title="N2O High Emitters", x=facList, y=N2OList)
    chartN2O_2 = json.dumps(graphN2O_2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("home.html", chart=chart, chart2=chart2, chartCH4=chartCH4, chartCH4_2=chartCh4_2,
                           chartN2O=chartN2O, chartN2O_2=chartN2O_2)


@app.route('/map.html')
def map_page():
    return render_template("map.html")


if __name__ == '__main__':
    app.run()
