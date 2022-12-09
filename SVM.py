import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from mlxtend.plotting import plot_decision_regions
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('Data_Cleaned(10.28).csv')

# feature scaling
scaler = MinMaxScaler()
df[['CO2_Emissions', 'CH4_Emissions', 'N2O_Emissions']] = scaler.fit_transform(
    df[['CO2_Emissions', 'CH4_Emissions', 'N2O_Emissions']])

y = df['CO2_Emissions']
X = df[['Zip Code Region', 'CH4_Emissions']]

# split the dataset into training and testing, allocating the majority of data to training
x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

# most important SVR parameter is Kernel type. It can be #linear,polynomial or gaussian SVR.
# We have a non-linear condition, so we can select polynomial or gaussian
# The SVR tries to find an optimal hyper-plane as a decision function in
# high-dimensional space.
regr = svm.SVR(kernel='rbf')
regr.fit(x_train,y_train)

# Now predict the output by passing the x_test variable.
regr.predict(x_test)
accuracy=regr.score(x_test,y_test)
print(accuracy)

# Visualising the Support Vector Regression result
support_vector = regr.support_vectors_
print(support_vector)

# Injecting data from previously defined x and y variables into
# # 3d figure
xdata = x_train.loc[:, 'Zip Code Region']
ydata = y_train
zdata = x_train.loc[:, 'CH4_Emissions']

# Visualize support vectors with Plotly
fig = go.Figure(data=[go.Scatter3d(x=xdata,
    y=ydata,
    z=zdata,
    mode='markers', marker=dict(size=8,
                                color='blue',
                                opacity=0.7)
)])

fig.update_layout(title='Support Vector Regression For Prediction',
scene = dict(
    xaxis_title='ZIP CODE REGION',
    yaxis_title='CO2 EMISSIONS',
    zaxis_title='CH4 EMISSIONS'),
)
fig.add_trace(go.Scatter3d(x=support_vector[:,0],
                           y=support_vector[:,1],
                           z=X['CH4_Emissions'],
                           mode='markers', marker=dict(color='red')
                           ))
fig.update_traces(name='')
fig.write_html('templates/SVM.html')
