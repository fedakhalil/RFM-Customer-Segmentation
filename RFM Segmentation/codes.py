#!/usr/bin/env python
# coding: utf-8

# # The scores are creating using:
# 
# - R = days since last transaction at the end of each month
# - F = Number of transactions in the time period
# - M = Money spent in the time period (Revenue would be a better parameter)
# 
# 
# 
# 
# - RFM_Score = Quality score of Customers


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings("ignore")



retail = pd.read_excel("retail_dataset.xlsx")
df = retail.copy()
df.head()


# Data Preprocessing




df.isnull().sum()


# Missing value fix


df = df.dropna()

df.info()
df.reset_index(drop = True, inplace=True)
df.index


# Outliers fix


df.describe().T


plt.figure(figsize = (7,5))
sns.boxplot(df["Quantity"]);



df = df[(df["Quantity"] > 0) & (df["Quantity"] < 10000)]

df.describe().T


plt.figure(figsize = (7,5))
sns.boxplot(df["UnitPrice"]);


df = df[(df["UnitPrice"] > 0) & (df["UnitPrice"] < 3000)]


df.describe().T



# RFM Analysis


df.head()

# Creating Total Price column

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
df.head()



# ## Recency


import datetime as dt


df["InvoiceDate"].max()

last_date = df["InvoiceDate"].max() + dt.timedelta(days = 1)
last_date

recency = df.groupby("CustomerID")["InvoiceDate"].apply(lambda x : (last_date - x.max()).days)
recency


# ## Frequency

frequency = df.groupby("CustomerID")["InvoiceNo"].count()
frequency


# ## Monetary

monetary = df.groupby("CustomerID")["TotalPrice"].sum()
monetary


rfm_data = pd.concat([recency, frequency, monetary], axis = 1)
rfm_data


# rename columns
rfm_data.rename(columns= {"InvoiceDate" : "Recency",
                          "InvoiceNo" : "Frequency", 
                          "TotalPrice" : "Monetary"}, inplace=True)


rfm_data.head()


# ## Cut values with labels
# - Customers with the lowest recency, highest frequency and monetary amounts considered as top customers

r_labels = range(5,0,-1)
f_labels = range(1,6)
m_labels = range(1,6)


r_groups = pd.qcut(rfm_data["Recency"],q = 5, labels=r_labels)
f_groups = pd.qcut(rfm_data["Frequency"], q = 5, labels = f_labels)
m_groups = pd.qcut(rfm_data["Monetary"], q = 5, labels = m_labels)


rfm_data["R"] = r_groups.values
rfm_data["F"] = f_groups.values
rfm_data["M"] = m_groups.values


rfm_data


# combine labels for score
def join_func(x):
    return str(x["R"]) + str(x["F"]) + str(x["M"])


rfm_data["RFM_Score"] = rfm_data.apply(join_func, axis = 1)
rfm_data.head()


# sort by Top/Best customers
rfm_data.sort_values(by = "RFM_Score", ascending = False)