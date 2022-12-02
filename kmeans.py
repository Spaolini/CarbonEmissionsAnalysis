import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go


# import data
ds = pd.read_csv('Data_Cleaned(10.28).csv')
ds.head()

# PREPROCESSING
# Drop unneeded columns
ds.drop(ds.columns[[0, 1, 2, 3, 5]], axis=1, inplace=True)
ds.head()
# scale features
scaler = MinMaxScaler()
ds[['CO2_Emissions', 'CH4_Emissions', 'N2O_Emissions']] = scaler.fit_transform(
    ds[['CO2_Emissions', 'CH4_Emissions', 'N2O_Emissions']])

# convert Category data to Numerical
ds['Category'] = ds['Category'].map({'low emitter' : 0, 'high emitter' : 1})

# kmeans predict to determine CO2 emissions based on zip code and methane
# perform KMeans
k_mean = KMeans(random_state=42, n_init=5, max_iter=100, n_clusters=5)
k_mean.fit(ds)

# Insert new column to store cluster info
identified_clusters = k_mean.fit_predict(ds)
ds['Cluster_int'] = identified_clusters

# define variable to run kmeans analysis on
X = ds.iloc[:,[0,1,2]].values

y = k_mean.fit_predict(X)



xdata = ds.loc[:, 'Zip Code Region']
ydata = ds['CO2_Emissions']
zdata = ds.loc[:, 'CH4_Emissions']

# Visualize kmeans clusters with Plotly

fig = go.Figure(data=[go.Scatter3d(x=xdata,
    y=ydata,
    z=zdata,
    mode='markers', marker=dict(size=8,
                                color=ds['Cluster_int'],
                                opacity=0.7)
)])

fig.update_layout(title='Kmeans Clustering of Emissions and Zip Code Region',
scene = dict(
    xaxis_title='ZIP CODE REGION',
    yaxis_title='CO2 EMISSIONS',
    zaxis_title='CH4 EMISSIONS'),
)
fig.show()
