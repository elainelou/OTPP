
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import csv


##### Section 1 #####
####  Question 1 ####

# Generate two independent and identically distributed variables of length 5000
length = 5000
X = np.random.normal(0, 1, length)
Y = np.random.normal(0, 1, length)

### Now we impose a corr = 0.5 between X & Y using linear tranformation ###
### If X and Y are independent and identically distributed, then their covariance is zero $$$

# Define desired correlation
desired_correlation = 0.5

# Calculate the covariance of X and Y
covariance_xy = np.cov(X, Y)[0, 1]

# Calculate the scaling factor for Y to achieve the desired correlation
scaling_factor = desired_correlation * np.std(X) / np.std(Y)

# Apply the scaling to Y
Y_correlated = Y * scaling_factor


#### Question 2 ####
# apply linear tranformation while preserving their marginal distributions
# Import data

##### Please use Section 1 data #######
file_path1 = '/Users/yilinlou/JOB/2024Package/JD/USDCAD.csv'
usd_cad =pd.read_csv(file_path1)

file_path2 = '/Users/yilinlou/JOB/2024Package/JD/SP500.xlsx'
sp500=pd.read_excel(file_path2)

dates = usd_cad["Date"]
usd_cad_rates = usd_cad["Adj Close"]
usd_cad = pd.DataFrame({'Date': dates, 'USD_CAD': usd_cad_rates})
usd_cad.set_index('Date', inplace=True)

dates2=sp500["Date"]
sp500_price = sp500['Adj Close']
sp500_df = pd.DataFrame({'Date': dates, 'index_price': sp500_price})
sp500_df.set_index('Date', inplace=True)

# Merge the two datasets based on date
data = pd.merge(sp500_df['index_price'], usd_cad, left_index=True, right_index=True)
data.columns = ['SP500', 'USD_CAD']
# Interpolate missing values using linear interpolation
data = data.interpolate(method='linear')

# Forward fill any remaining missing values
data = data.ffill()
#print(data)


# Compute empirical correlation coefficient
empirical_corr = data['SP500'].corr(data['USD_CAD'])
print("Empirical correlation coefficient:", empirical_corr)

# Apply transformation to achieve correlation of 0.5
desired_corr = 0.5
scaling_factor = desired_corr / empirical_corr
data['USD_CAD_transformed'] = data['USD_CAD'] * scaling_factor


### Lastly, let's validate if the corr coefficient is close to 0.5 ###
# Calculate correlation coefficient
correlation = data['SP500'].corr(data['USD_CAD_transformed'])

# Print the correlation coefficient
print("Correlation coefficient between SP500 and USD_CAD_transformed:", correlation)


#### Question 3 ####

#### Extending the bivariate framework to multivariate distributions involves considering more than two variables simultaneously. The key concepts remain similar, but the computations become more complex as we need to consider correlations among all pairs of variables
