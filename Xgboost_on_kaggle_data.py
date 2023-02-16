#importing libraries
import os
if not os.path.exists("../input/train.csv"):
    os.symlink("../input/home-data-for-ml-course/train.csv", "../input/train.csv")  
    os.symlink("../input/home-data-for-ml-course/test.csv", "../input/test.csv") 
from learntools.core import binder
binder.bind(globals())
from learntools.ml_intermediate.ex6 import *
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error


# Reading the data
X = pd.read_csv('../input/train.csv', index_col='Id')
X_test_full = pd.read_csv('../input/test.csv', index_col='Id')

# Removing rows with missing target, separate target from predictors
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice              
X.drop(['SalePrice'], axis=1, inplace=True)

# Breaking off validation set from training data
X_train_full, X_valid_full, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                                random_state=0)

# "Cardinality" means the number of unique values in a column
# Selecting categorical columns with relatively low cardinality (convenient but arbitrary)
low_cardinality_cols = [cname for cname in X_train_full.columns if X_train_full[cname].nunique() < 10 and 
                        X_train_full[cname].dtype == "object"]

# Selecting numeric columns
numeric_cols = [cname for cname in X_train_full.columns if X_train_full[cname].dtype in ['int64', 'float64']]

# Keeping selected columns only
my_cols = low_cardinality_cols + numeric_cols
X_train = X_train_full[my_cols].copy()
X_valid = X_valid_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()

# One-hot encoding the data (to shorten the code, we use pandas)
X_train = pd.get_dummies(X_train)
X_valid = pd.get_dummies(X_valid)
X_test = pd.get_dummies(X_test)
X_train, X_valid = X_train.align(X_valid, join='left', axis=1)
X_train, X_test = X_train.align(X_test, join='left', axis=1)

# Defining the model
my_model_1 = XGBRegressor()
my_model_1.fit(X_train, y_train)

predictions_1 = my_model_1.predict(X_valid)

# Calculating MAE
mae_1 = mean_absolute_error(predictions_1, y_valid)

print("Mean Absolute Error: " + str(mae_1))

# Defining the model
my_model_2 = XGBRegressor(n_estimators=1000, learning_rate=0.05)

# Fitting the model
my_model_2.fit(X_train, y_train, 
             early_stopping_rounds=5, 
             eval_set=[(X_valid, y_valid)], 
             verbose=False)

# Getting predictions
predictions_2 = my_model_2.predict(X_valid)

# Calculating MAE
mae_2 = mean_absolute_error(predictions_2, y_valid)

# Printing MAE
print("Mean Absolute Error: " + str(mae_2))

# Defining the model
my_model_3 = XGBRegressor(n_estimators=500, learning_rate=3e-4)

# Fitting the model
my_model_3.fit(X_train, y_train, 
             early_stopping_rounds=2, 
             eval_set=[(X_valid, y_valid)], 
             verbose=False)

# Getting predictions
predictions_3 = my_model_3.predict(X_valid)

# Calculating MAE
mae_3 = mean_absolute_error(predictions_3, y_valid)

# Printing MAE
print("Mean Absolute Error: " + str(mae_3))



