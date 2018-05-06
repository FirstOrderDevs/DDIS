import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as ax
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pandas as pd
import statsmodels.api as sm
from copy import deepcopy

def naive_forecast(train_data):
    return [train_data[-1],train_data[-1]];

def simple_average_forecast(train_data):
    mean = np.mean(train_data);
    return  [mean, mean];

def order_calculator(array):
    order=1;
    for i in range(0,len(array)-2):
        if(((array[i+1]-array[i])*(array[i+2]-array[i+1]))<0):
            order = order+1;

    return order;

def auto_regressive_plot(train_data):

    poly = PolynomialFeatures(degree=order_calculator(train_data));
    poly_train = poly.fit_transform([[0],[1],[2],[3],[4],[5],[6]]);
    poly_test = poly.fit_transform([[0],[1],[2],[3],[4],[5],[6],[7],[8]]);

    poly_regr = linear_model.LinearRegression();
    poly_regr.fit(poly_train, train_data);
    return poly_regr.predict(poly_test);

def auto_regressive_forecast(train_data):

    poly = PolynomialFeatures(degree=order_calculator(train_data));
    poly_train = poly.fit_transform([[0],[1],[2],[3],[4],[5],[6]]);
    poly_test = poly.fit_transform([[7],[8]]);

    poly_regr = linear_model.LinearRegression();
    poly_regr.fit(poly_train, train_data);
    return poly_regr.predict(poly_test)[0:2];

def moving_average_forecast(input_data, window):
    return pd.rolling_mean(input_data, window)[7:9]

def ewma_calculator(data, window):

    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha

    scale = 1/alpha_rev
    n = data.shape[0]

    r = np.arange(n)
    scale_arr = scale**r
    offset = data[0]*alpha_rev**(r+1)
    pw0 = alpha*alpha_rev**(n-1)

    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out

def ewma_forecast(data, window):
    input_data = deepcopy(data);
    input_data[-2] = ewma_calculator(input_data, window)[-2];
    input_data[-1] = ewma_calculator(input_data, window)[-1];
    return input_data[7:9];

csv_file_1 = "Southland - Performance.csv";
csv_file_2 = "Sirisaman - Perfomance.csv";

subject = "Science"

# reading the csv file and selecting subject columns
df1 = pd.read_csv(csv_file_1, header=1, usecols=["Index No.",subject, subject + ".1", subject + ".2", subject + ".3", subject + ".4", subject + ".5", subject + ".6", subject + ".7", subject + ".8"]);
df1.fillna(0, inplace=True);
df1.replace('ab', 0, inplace=True);

df2 = pd.read_csv(csv_file_2, header=1, usecols=["Index No.",subject, subject + ".1", subject + ".2", subject + ".3", subject + ".4", subject + ".5", subject + ".6", subject + ".7", subject + ".8"]);
df2.fillna(0, inplace=True);
df2.replace('ab', 0, inplace=True);

# add data to numpy array
np_marks_array_1 = df1.as_matrix().astype(float);
np_marks_array_2 = df2.as_matrix().astype(float);

input_marks = np.append(np_marks_array_1, np_marks_array_2, axis=0);

index = 321;

train_data = input_marks[index][1:8];
test_data = input_marks[index][8:10];

#change forecasting algorithm here
#forecast_data = auto_regressive_forecast(train_data)
#forecast_data = moving_average_forecast(input_marks[index][1:], 3);
forecast_data = ewma_forecast(input_marks[index][1:], 3);

# plotting
plt.plot([1,2,3,4,5,6,7], train_data, color='blue',label='Train Data');

plt.plot([7,8], [train_data[-1],test_data[0]], color='red', dashes=[6, 2]);
plt.plot([8,9], input_marks[index][8:10], color='red',label='Test Data');

plt.plot([7,8], [train_data[-1],forecast_data[0]], color='green',dashes=[6, 2]);
plt.plot([8,9], forecast_data, color='green',label='Forecast Data');

plt.xlabel("Index "+ str(int(input_marks[index][0])));
plt.ylabel(subject+" Marks");

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show();

#error calculation
print("MSE :", mean_squared_error(test_data, forecast_data));