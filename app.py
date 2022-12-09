import csv
import json
import math
import os
import sys
import dash
from dash import dcc
import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, render_template, current_app, request
import plotly.graph_objects as go

# app initiation
app = Flask(__name__)


# all routes are assigned here for home and map page along with iframe pages
@app.route('/')
def landing():
    return current_app.redirect("home.html")


@app.route('/graph_CO2.html')
def return_graph():
    return render_template('graph_CO2.html')


@app.route('/CO2_high.html')
def return_graph2():
    return render_template('CO2_high.html')


@app.route('/CO2_low.html')
def return_graphlow():
    return render_template('CO2_low.html')


@app.route('/CO2_table.html')
def return_CO2Table():
    return render_template('CO2_table.html')


@app.route('/CO2_high_table.html')
def return_CO2_high_Table():
    return render_template('CO2_high_table.html')


@app.route('/CO2_low_table.html')
def return_CO2_low_Table():
    return render_template('CO2_low_table.html')


@app.route('/graphCH4.html')
def return_graphCH4():
    return render_template('graphCH4.html')


@app.route('/graphCH4_2.html')
def return_graphCH4_2():
    return render_template('graphCH4_2.html')


@app.route('/CH4_low.html')
def return_graphCH4_low():
    return render_template('graphCH4_low.html')


@app.route('/CH4_table.html')
def return_CH4Table():
    return render_template('CH4_table.html')


@app.route('/CH4_high_table.html')
def return_CH4_high_Table():
    return render_template('CH4_high_table.html')


@app.route('/CH4_low_table.html')
def return_CH4_low_Table():
    return render_template('low_CH4_table.html')


@app.route('/graphN2O.html')
def return_graphN2O():
    return render_template('graphN2O.html')


@app.route('/graphN2O_2.html')
def return_graphN2O_2():
    return render_template('graphN2O_2.html')


@app.route('/graphN2O_low.html')
def return_graphN2O_low():
    return render_template('graphN2O_low.html')


@app.route('/N2O_table.html')
def return_N2OTable():
    return render_template('N2O_table.html')


@app.route('/high_N2O_table.html')
def return_high_N2O_Table():
    return render_template('high_N2O_table.html')


@app.route('/low_N2O_table.html')
def return_low_N2O_Table():
    return render_template('lowN20_table.html')


@app.route('/Select_view.html')
def return_Select_view():
    return render_template('Select_view.html')


@app.route('/SVM.html')
def return_SVM():
    return render_template('SVM.html')


@app.route('/kmeans.html')
def return_kmeans():
    return render_template('kmeans.html')


@app.route('/about.html')
def return_about():
    return render_template('about.html')

@app.route('/map_us.html')
def return_figtest():
    return render_template('map_us.html')


@app.route('/home.html', methods=["GET", "POST"])
# Home page contained within home function
def home():
    # User input handling
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
        # Writing to csv's
        # First csv is for classification and second is for Kmeans and SVM
        with open('Data_Cleaned_updated.csv', 'a', newline='') as file, \
                open('Data_Cleaned(10.28).csv', 'a', newline='') as fileB:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(
                {'Facility': Facility, 'Year': Year, 'City': City, 'State': State, 'Zip Code Region': Zipcode,
                 'Address': Address, 'CO2_Emissions': CO2_Emissions, 'CH4_Emissions': CH4_Emissions, 'N2O_Emissions':
                     N2O_Emissions})
            writer = csv.DictWriter(fileB, fieldnames=fieldnames)
            writer.writerow(
                {'Facility': Facility, 'Year': Year, 'City': City, 'State': State, 'Zip Code Region': Zipcode,
                 'Address': Address, 'CO2_Emissions': CO2_Emissions, 'CH4_Emissions': CH4_Emissions, 'N2O_Emissions':
                     N2O_Emissions})
        df = pd.read_csv("Data_Cleaned_updated.csv")
        print(df)
        data = df.groupby(by='Facility')['CO2_Emissions'].sum()
        data.to_csv('grouped.csv')
        groups = pd.read_csv('grouped.csv')
        print(groups)
        groups['err'] = (groups['CO2_Emissions'].mean() + (groups['CO2_Emissions'].std()))
        graphCo2 = px.bar(groups, title="CO2 Emissions by Facility", x='Facility', y='CO2_Emissions', error_y='err')
        graphCo2.write_html("templates/graph_CO2.html")

        return render_template('confirmation.html')

    # CO2 Analysis
    df = pd.read_csv("Data_Cleaned_updated.csv")
    data = df.groupby(by='Facility')['CO2_Emissions'].sum()
    groups = pd.read_csv('grouped.csv')
    data.to_csv('grouped.csv')
    groups['err'] = (groups['CO2_Emissions'].mean() + (groups['CO2_Emissions'].std()))

    graph = px.bar(groups, title="CO2 Emissions by Facility", x='Facility', y='CO2_Emissions', error_y='err')

    # writes graph and table to html documents for iframing
    graph.write_html("templates/graph_CO2.html")
    groups.to_html("templates/CO2_table.html")

    # Doing calculation for high emitter
    highresult = df[df['CO2_Emissions'] > df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std() * 2)]
    highresult.to_csv("highEmitter.csv")
    highCO2 = pd.read_csv('highEmitter.csv')

    # looks for user input
    if request.method == "POST":
        highresult = df[df['CO2_Emissions'] > df['CO2_Emissions'].mean() + (df['CO2_Emissions'].std() * 2)]
        highresult.to_csv("highEmitter.csv")
        highCO2 = pd.read_csv('highEmitter.csv')

    # High emitter graph
    graph2 = px.bar(highCO2, title="CO2 High Emitters", x="Facility", y="CO2_Emissions")

    graph2.write_html('templates/CO2_high.html')
    highCO2.to_html("templates/CO2_high_table.html")

    # Low emitter calculation
    lowresult = df[df['CO2_Emissions'] < df['CO2_Emissions'].mean() - (df['CO2_Emissions'].std())]
    lowresult.to_csv("lowEmitter.csv")
    lowCO2 = pd.read_csv('lowEmitter.csv')

    if request.method == "POST":
        lowresult = df[df['CO2_Emissions'] < df['CO2_Emissions'].mean() - (df['CO2_Emissions'].std() * 2)]
        lowresult.to_csv("lowEmitter.csv")
        lowCO2 = pd.read_csv('lowEmitter.csv')

    graphLow = px.bar(lowCO2, title="CO2 Low Emitters", x="Facility", y="CO2_Emissions")

    graphLow.write_html('templates/CO2_low.html')
    lowCO2.to_html("templates/CO2_low_table.html")

    print("\n")

    # Process is repeated for CH4 and N2O

    # CH4 Analysis
    df.CH4_Emissions.tolist()
    df['er'] = (df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std()))
    dataCH4 = df.groupby(by='Facility')['CH4_Emissions'].sum()
    dataCH4.to_csv('groupedCH4.csv')
    groupsCH4 = pd.read_csv('groupedCH4.csv')

    meanCH4 = groupsCH4['CH4_Emissions'].mean()
    filterCH4 = groupsCH4[groupsCH4['CH4_Emissions'] > meanCH4]
    filterCH4['errr'] = (filterCH4['CH4_Emissions'].mean() + (filterCH4['CH4_Emissions'].std()))

    graphCH4 = px.bar(filterCH4, title="CH4 Emissions by Facility", x="Facility", y="CH4_Emissions", error_y="errr")
    graphCH4.write_html('templates/graphCH4.html')
    groupsCH4.to_html("templates/CH4_table.html")

    highresultCH4 = df[
        df['CH4_Emissions'] > df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std())]
    highresultCH4.to_csv("highCH4.csv")
    highCH4 = pd.read_csv('highCH4.csv')

    graphCH4_2 = px.bar(highCH4, title="CH4 High Emitters", x="Facility", y="CH4_Emissions")

    graphCH4_2.write_html('templates/graphCH4_2.html')
    highCH4.to_html("templates/CH4_high_table.html")

    if request.method == "POST":
        df['er'] = (df['CH4_Emissions'].mean() + (df['CH4_Emissions'].std()))
        dataCH4 = df.groupby(by='Facility')['CH4_Emissions'].sum()
        dataCH4.to_csv('groupedCH4.csv')
        groupsCH4 = pd.read_csv('groupedCH4.csv')
        # groupsCH4['err'] = (groupsCH4['CH4_Emissions'].mean() + (groupsCH4['CH4_Emissions'].std()))

        meanCH4 = groupsCH4['CH4_Emissions'].mean()
        filterCH4 = groupsCH4[groupsCH4['CH4_Emissions'] > meanCH4]
        filterCH4['errr'] = (filterCH4['CH4_Emissions'].mean() + (filterCH4['CH4_Emissions'].std()))

        graphCH4 = px.bar(filterCH4, title="CH4 Emissions by Facility", x="Facility", y="CH4_Emissions", error_y="errr")
        graphCH4.write_html('templates/graphCH4.html')
        groupsCH4.to_html("templates/CH4_table.html")
        pd.read_csv('highCH4.csv')
        graphCH4_2 = px.bar(highCH4, title="CH4 High Emitters", x="Facility", y="CH4_Emissions")
        graphCH4_2.write_html('templates/graphCH4_2.html')
        highCH4.to_html("templates/CH4_high_table.html")

    lowresultCH4 = filterCH4[
        filterCH4['CH4_Emissions'] < filterCH4['CH4_Emissions'].mean() - (filterCH4['CH4_Emissions'].std())]
    lowresultCH4.to_csv("lowCH4.csv")
    lowCH4 = pd.read_csv('lowCH4.csv')

    graphCH4_low = px.bar(lowCH4, title="CH4 Low Emitters", x="Facility", y="CH4_Emissions")

    graphCH4_low.write_html('templates/graphCH4_low.html')
    lowCH4.to_html('templates/low_CH4_table.html')

    print("\n")

    # N2O Analysis
    df.N2O_Emissions.tolist()
    dataN2O = df.groupby(by='Facility')['N2O_Emissions'].sum()
    dataN2O.to_csv('groupedN2O.csv')
    groupsN2O = pd.read_csv('groupedN2O.csv')
    groupsN2O['err'] = (groupsN2O['N2O_Emissions'].mean() + (groupsN2O['N2O_Emissions'].std()))

    graphN2O = px.bar(groupsN2O, title="N2O Emissions by Facility", x="Facility", y="N2O_Emissions", error_y="err")

    graphN2O.write_html('templates/graphN2O.html')
    groupsN2O.to_html('templates/N2O_table.html')

    highresultN2O = df[df['N2O_Emissions'] > df['N2O_Emissions'].mean() + (df['N2O_Emissions'].std() * 3)]
    highresultN2O.to_csv("highN2O.csv")
    highN2O = pd.read_csv('highN2O.csv')

    graphN2O_2 = px.bar(highN2O, title="N2O High Emitters", x="Facility", y="N2O_Emissions")

    graphN2O_2.write_html('templates/graphN2O_2.html')
    highN2O.to_html('templates/high_N2O_table.html')

    lowresultN2O = df[df['N2O_Emissions'] < (df['N2O_Emissions'].std() - df['N2O_Emissions'].mean())]
    lowresultN2O.to_csv("lowN2O.csv")
    lowN2O = pd.read_csv('lowN2O.csv')

    graphN2O_low = px.bar(lowN2O, title="N2O Low Emitters", x="Facility", y="N2O_Emissions")

    graphN2O_low.write_html('templates/graphN2O_low.html')
    lowN2O.to_html('templates/lowN20_table.html')





    return render_template("home.html")


@app.route('/map.html', methods=["GET", "POST"])
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

    fig.write_html("templates/map_us.html")

    if request.method == 'POST':
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

        fig.write_html("templates/map_us.html")
    return render_template('map.html')


if __name__ == '__main__':
    app.run_server()
