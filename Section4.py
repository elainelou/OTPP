#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:51:16 2024

@author: yilinlou
"""


import cvxpy as cp

import numpy as np
import pandas as pd
import csv
import os
from scipy.stats import norm

####### Please use Section 4data ######
# Example usage:
directory = '/Users/yilinlou/JOB/2024Package/JD/Case/s4data/'  # Directory containing CSV files

####### I. Import Data ##########
def import_csvs(directory):
    all_dataframes = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            # Extract the first and fifth columns
            first_column = df.iloc[:, 0]
            fifth_column = df.iloc[:, 5]
            # Store them in separate DataFrames
            first_df = pd.DataFrame({f"{filename}_first_column": first_column})
            
            returns_col_name = f"{filename}_returns"
            returns = fifth_column.pct_change()
            returns_df = pd.DataFrame({returns_col_name: returns})
            
            # Concatenate first column DataFrame with returns DataFrame
            combined_df = pd.concat([first_df, returns_df], axis=1)
            
            all_dataframes[f"{filename}_combined"] = combined_df

            # Store the combined DataFrame
    return all_dataframes

def compute_stats(dataframes):
    # Combine all returns into a single DataFrame
    all_returns = pd.concat([df.iloc[:, 1] for df in dataframes.values()], axis=1)
    
    # Rename columns to match the DataFrame names
    all_returns.columns = [name for name in dataframes.keys()]
    
    # Compute expected return for each DataFrame
    expected_returns = all_returns.mean()
    
    # Compute covariance matrix across different asset classes
    cov_matrix = all_returns.cov()
    
    return expected_returns, cov_matrix
'''
def compute_annual_returns(expected_returns):
    # Assuming 252 trading days in a year
    annual_returns = expected_returns * 252
    return annual_returns
'''


# Import CSV files as separate DataFrames with meaningful names
dataframes = import_csvs(directory)
# Access and print each new DataFrame
for name, df in dataframes.items():
    print(f"DataFrame '{name}':")
 

# Compute expected returns and covariance matrix across different asset classes
expected_returns, cov_matrix = compute_stats(dataframes)


# Print expected returns for each DataFrame
print("Expected Returns:")



# Print covariance matrix across different asset classes
print("Covariance Matrix:")
print(cov_matrix)


####### II. Portfoilo construction - mean Variance ################
# Define the expected returns and covariance matrix for the assets
exoected_returns = expected_returns.values
covariance_matrix = cov_matrix.values
print("Returns (array):")
print(exoected_returns)
print()

print("Covariance Matrix (array):")
print(covariance_matrix)

# Number of assets
n_assets = len(expected_returns)

# Define the variables
weights = cp.Variable(n_assets)

# Define the objective function (minimize portfolio risk)
portfolio_variance = cp.quad_form(weights, covariance_matrix)
objective = cp.Minimize(portfolio_variance)

# Define the constraints (all weights sum to 1)
constraints = [cp.sum(weights) == 1]

# Solve the problem
problem = cp.Problem(objective, constraints)
problem.solve()

# Obtain optimal portfolio weights
optimal_weights = weights.value

# Calculate portfolio standard deviation
portfolio_std_dev = np.sqrt(portfolio_variance.value)

# Calculate portfolio 1-day VaR at 99% confidence level
confidence_level = 0.99
z_score = norm.ppf(confidence_level)
portfolio_var = z_score * portfolio_std_dev

# Calculate contributional VaR's
contributional_vars = optimal_weights * portfolio_var

# Calculate incremental VaR's
incremental_vars = []
for i in range(n_assets):
    new_weights = np.zeros(n_assets)
    new_weights[i] = 1  # Add only one asset at a time
    incremental_var = z_score * np.sqrt(np.dot(new_weights, np.dot(covariance_matrix, new_weights)))
    incremental_vars.append(incremental_var)

# Display results
print("Optimal Portfolio Weights:")
for i, asset in enumerate(["S&P GSCI", "TSX", "S&P 500", "Gold", "US 10Y Treasuries", "CA 10Y Treasuries"]):
    print(f"{asset}: {optimal_weights[i]*100:.2f}%")
print("Portfolio 1-day VaR:", portfolio_var)
print("Contributional VaR's:", contributional_vars)
print("Incremental VaR's:")
for i, asset in enumerate(["S&P GSCI", "TSX", "S&P 500", "Gold", "US 10Y Treasuries", "CA 10Y Treasuries"]):
    print(f"{asset}: {incremental_vars[i]}")