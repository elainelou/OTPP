#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:44:03 2024

@author: yilinlou
"""


import pandas as pd

# Example time series data
ts1_data = {'Date': ['2019-12-31', '2020-01-02', '2020-01-03', '2020-01-04'],
            'Value': [3230.78, 3257.85, 3234.85, 3246.28]}
ts2_data = {'Date': ['2019-12-31','2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04'],
            'Value': [1.30606, 1.3002, 1.2973, 1.2983,1.29866]}

# Convert data to pandas DataFrames
ts1_df = pd.DataFrame(ts1_data)
ts2_df = pd.DataFrame(ts2_data)

# Convert 'Date' columns to datetime objects
ts1_df['Date'] = pd.to_datetime(ts1_df['Date'])
ts2_df['Date'] = pd.to_datetime(ts2_df['Date'])

# Step 1: Identify common dates (intersection of date indices)
common_dates = pd.Index(ts1_df['Date']).intersection(ts2_df['Date'])

# Step 2: Filter time series to include only common dates
ts1_common = ts1_df[ts1_df['Date'].isin(common_dates)]
ts2_common = ts2_df[ts2_df['Date'].isin(common_dates)]

# Step 3: Resample or interpolate (if needed)
# Example using forward fill to fill missing values in ts2_common
ts2_common['Value'] = ts2_common['Value'].fillna(method='ffill')

# Step 4: Align data
# Now ts1_common and ts2_common have the same dates and lengths

# Output the aligned time series
print("Time Series 1 (Aligned):")
print(ts1_common)
print("\nTime Series 2 (Aligned):")
print(ts2_common)
