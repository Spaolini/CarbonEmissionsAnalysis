import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('Data_Cleaned(10.28).csv')

# feature scaling
scaler = MinMaxScaler()
df[['CO2 Emissions', 'CH4 Emissions', 'N2O Emissions']] = scaler.fit_transform(
    df[['CO2 Emissions', 'CH4 Emissions', 'N2O Emissions']])

y = df['CO2 Emissions']
X = df[['Zip Code Region', 'CH4 Emissions']]

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
support_vector_indices = regr.support_
print(support_vector_indices)

# Creating 3d figure
fig = plt.figure()
ax = plt.axes(projection='3d')

# Injecting data from previously defined x and y variables into
# 3d figure
xdata = X.loc[:, 'Zip Code Region']
ydata = y
zdata = X.loc[:, 'CH4 Emissions']

ax.scatter3D(xdata, zdata, ydata, c=xdata, cmap='viridis')
# ax.scatter3D(support_vector_indices[X.loc[:, 'Zip Code Region']],
#              support_vector_indices[X.loc[:, 'CH4 Emissions']],
#              ydata)
# labels
ax.set_title('CO2 Emissions based on Zip Code Region and Methane')
ax.set_xlabel('Zip Code Region-->')
ax.set_zlabel('Carbon Emissions-->')
ax.set_ylabel('Methane Emissions-->')
plt.show()
