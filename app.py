import csv
import json
import math
import os
import sys
import dash
import dash_core_components as dcc
import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, render_template, current_app, request
import plotly.graph_objects as go
def figure():
    df = pd.read_csv('Data_Cleaned_updated.csv')
    fig = go.Figure(data=go.Choropleth(
        locations=df['State'],
        z=df['CO2_Emissions'].astype(float),
        locationmode='USA-states',
        colorscale='Blues',
        colorbar_title='CO2_Emissions',
    ))

    fig.update_layout(
        title_text='CO2 Emissions by State',
        geo_scope='usa',
    )

    return fig

app = Flask(__name__)


@app.route('/')
def landing():
    return current_app.redirect("home.html")

@app.route('/graph.html')
def return_graph():
    return render_template('graph.html')
@app.route('/CO2_high.html')
def return_graph2():
    return render_template('CO2_high.html')
@app.route('/graphCH4.html')
def return_graphCH4():
    return render_template('graphCH4.html')
@app.route('/graphCH4_2.html')
def return_graphCH4_2():
    return render_template('graphCH4_2.html')
@app.route('/graphN2O.html')
def return_graphN2O():
    return render_template('graphN2O.html')
@app.route('/graphN2O_2.html')
def return_graphN2O_2():
    return render_template('graphN2O_2.html')
@app.route('/home.html', methods=["GET", "POST"])
def home():  # put application's code here

    if request.method == "POST":
        Year = request.form["Year"]
        Facility = request.form["Facility"]
        City = request.form["City"]
        State = request.form["State"]
        Zipcode = request.form["Zipcode"]
        Address = request.form["Address"]
        CO2_Emissions = request.form["CO2_Emissions"]
        CH4_Emissions = request.form["CH4_Emissions"]
        N2O_Emissions = request.form["N2O_Emissions"]

        fieldnames = ['Year', 'Facility', 'City', 'State', 'Zip Code Region', 'Address', 'CO2_Emissions',
                      'CH4_Emissions', 'N2O_Emissions']
        with open('Data_Cleaned_updated.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(
                {'Year': Year, 'Facility': Facility, 'City': City, 'State': State, 'Zip Code Region': Zipcode,
                 'Address': Address, 'CO2_Emissions': CO2_Emissions, 'CH4_Emissions': CH4_Emissions, 'N2O_Emissions':
                     N2O_Emissions})

    df = pd.read_csv("Data_Cleaned_updated.csv")
    # CO2 Analysis
    df.Facility.tolist()
    data = df.groupby(by='Facility')['CO2_Emissions'].sum()
    data.to_csv('grouped.csv')
    groups = pd.read_csv('grouped.csv')
    groups['err'] = (groups['CO2_Emissions'].mean() + (groups['CO2_Emissions'].std()))

    graph = px.bar(groups, title="CO2 Emissions by Facility", x='Facility', y='CO2_Emissions', error_y='err')
    # chart = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    graph.write_html("graph.html")


    highresult = df[df['CO2_Emissions'] > df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std() * 2)]
    highresult.to_csv("highEmitter.csv")
    highCO2 = pd.read_csv('highEmitter.csv')

    if request.method == "POST":
        highresult = df[df['CO2_Emissions'] > df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std() * 2)]
        highresult.to_csv("highEmitter.csv")
        highCO2 = pd.read_csv('highEmitter.csv')

    graph2 = px.bar(highCO2, title="CO2 High Emitters", x="Facility", y="CO2_Emissions")
    # chart2 = json.dumps(graph2, cls=plotly.utils.PlotlyJSONEncoder)

    graph2.write_html('templates/CO2_high.html')

    print("\n")

    # CH4 Analysis
    CH4List = df.CH4_Emissions.tolist()
    df['er'] = (df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std()))
    dataCH4 = df.groupby(by='Facility')['CH4_Emissions'].sum()
    dataCH4.to_csv('groupedCH4.csv')
    groupsCH4 = pd.read_csv('groupedCH4.csv')
    groupsCH4['err'] = (groupsCH4['CH4_Emissions'].mean() + (groupsCH4['CH4_Emissions'].std()))

    meanCH4 = groupsCH4['CH4_Emissions'].mean()
    filterCH4 = groupsCH4[groupsCH4['CH4_Emissions'] > meanCH4]
    filterCH4['errr'] = (filterCH4['CH4_Emissions'].mean() + (filterCH4['CH4_Emissions'].std()))

    graphCH4 = px.bar(filterCH4, title="CH4 Emissions by Facility", x="Facility", y="CH4_Emissions", error_y="errr")
    # chartCH4 = json.dumps(graphCH4, cls=plotly.utils.PlotlyJSONEncoder)

    graphCH4.write_html('templates/graphCH4.html')

    highresultCH4 = filterCH4[
        filterCH4['CH4_Emissions'] > filterCH4['CH4_Emissions'].mean() + (filterCH4['CH4_Emissions'].std())]
    highresultCH4.to_csv("highCH4.csv")
    highCH4 = pd.read_csv('highCH4.csv')

    graphCH4_2 = px.bar(highCH4, title="CH4 High Emitters", x="Facility", y="CH4_Emissions")
    # chartCh4_2 = json.dumps(graphCH4_2, cls=plotly.utils.PlotlyJSONEncoder)

    graphCH4_2.write_html('templates/graphCH4_2.html')

    print("\n")

    # N2O Analysis
    N2OList = df.N2O_Emissions.tolist()
    dataN2O = df.groupby(by='Facility')['N2O_Emissions'].sum()
    dataN2O.to_csv('groupedN2O.csv')
    groupsN2O = pd.read_csv('groupedN2O.csv')
    groupsN2O['err'] = (groupsN2O['N2O_Emissions'].mean() + (groupsN2O['N2O_Emissions'].std()))

    graphN2O = px.bar(groupsN2O, title="N2O Emissions by Facility", x="Facility", y="N2O_Emissions", error_y="err")
    # chartN2O = json.dumps(graphN2O, cls=plotly.utils.PlotlyJSONEncoder)

    graphN2O.write_html('templates/graphN2O.html')

    highresultN2O = df[df['N2O_Emissions'] > df['N2O_Emissions'].mean() + (df['N2O_Emissions'].std() * 2)]
    highresultN2O.to_csv("highN2O.csv")
    highN2O = pd.read_csv('highN2O.csv')

    graphN2O_2 = px.bar(highN2O, title="N2O High Emitters", x="Facility", y="N2O_Emissions")
    # chartN2O_2 = json.dumps(graphN2O_2, cls=plotly.utils.PlotlyJSONEncoder)

    graphN2O_2.write_html('templates/graphN2O_2.html')

    return render_template("home.html")


@app.route('/map.html')
def map_page():
    # df = pd.read_csv('Data_Cleaned_updated.csv')
    # fig = go.Figure(data=go.Choropleth(
    #     locations=df['State'],
    #     z=df['CO2_Emissions'].astype(float),
    #     locationmode='USA-states',
    #     colorscale='Blues',
    #     colorbar_title='CO2_Emissions',
    # ))
    #
    # fig.update_layout(
    #     title_text='CO2 Emissions by State',
    #     geo_scope='usa',
    # )
    #
    # fig.show()

    # mapus = px.choropleth(locations=df['State'], locationmode='USA-states', color_continuous_scale='Blues',
    #                       title='CO2 test', )
    # mapusjson = json.dumps(mapus, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("map.html")

server = dash.Dash(server=app, routes_pathname_prefix="/figure/")
server.layout = dcc.Graph(figure=figure(), style={"width": "100%", "height": "1000px"})



if __name__ == '__main__':
    server.run_server()
