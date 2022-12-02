import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# import data
ds = pd.read_csv('Data_Cleaned(10.28).csv')
ds.head()

# PREPROCESSING
# Drop unneeded columns
ds.drop(ds.columns[[0, 1, 2, 3, 5]], axis=1, inplace=True)
ds.head()
# scale features
scaler = MinMaxScaler()
ds[['CO2 Emissions', 'CH4 Emissions', 'N2O Emissions']] = scaler.fit_transform(
    ds[['CO2 Emissions', 'CH4 Emissions', 'N2O Emissions']])

# convert Category data to Numerical
ds['Category'] = ds['Category'].map({'low emitter' : 0, 'high emitter' : 1})

# perform KMeans
k_mean = KMeans(random_state=42, n_init=5, max_iter=100, n_clusters=5)
k_mean.fit(ds)

# Insert new column to store cluster info
identified_clusters = k_mean.fit_predict(ds)
ds['Cluster_int'] = identified_clusters

# kmeans predict to determine CO2 emissions based on zip code and methane
X = ds.iloc[:,[0,1,2]].values

y = k_mean.fit_predict(X)

# plot
plt.scatter(ds['Zip Code Region'], ds['CO2 Emissions'], c=ds['Cluster_int'])
plt.title('CO2 Emissions & Zip Code Region (Clustered)')
plt.xlabel('Zip Code Region')
plt.ylabel('CO2 Emissions')
plt.show()

# fig = plt.figure(figsize = (10,10))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X[y == 0,0],X[y == 0,1],X[y == 0,2], s = 40 , color = 'red', label = "cluster 1")
# ax.scatter(X[y == 1,0],X[y == 1,1],X[y == 1,2], s = 40 , color = 'blue', label = "cluster 2")
# ax.scatter(X[y == 2,0],X[y == 2,1],X[y == 2,2], s = 40 , color = 'green', label = "cluster 3")
# ax.scatter(X[y == 3,0],X[y == 3,1],X[y == 3,2], s = 40 , color = 'yellow', label = "cluster 4")
# ax.scatter(X[y == 4,0],X[y == 4,1],X[y == 4,2], s = 40 , color = 'purple', label = "cluster 5")
# ax.set_xlabel('Zip Code Region-->')
# ax.set_ylabel('Carbon Emissions-->')
# ax.set_zlabel('Methane Emissions-->')
# ax.legend()
# plt.show()
