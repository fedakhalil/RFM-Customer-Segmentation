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

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings("ignore")


# In[2]:


retail = pd.read_excel("retail_dataset.xlsx")
df = retail.copy()
df.head()


# # Data Preprocessing

# In[3]:


df.isnull().sum()


# ## Missing value fix

# In[4]:


df = df.dropna()


# In[5]:


df.info()


# In[6]:


df.reset_index(drop = True, inplace=True)
df.index


# ## Outliers fix

# In[7]:


df.describe().T


# In[8]:


plt.figure(figsize = (7,5))
sns.boxplot(df["Quantity"]);


# In[9]:


df = df[(df["Quantity"] > 0) & (df["Quantity"] < 10000)]


# In[10]:


df.describe().T


# In[11]:


plt.figure(figsize = (7,5))
sns.boxplot(df["UnitPrice"]);


# In[12]:


df = df[(df["UnitPrice"] > 0) & (df["UnitPrice"] < 3000)]


# In[13]:


df.describe().T


# In[ ]:





# # RFM Analysis

# In[14]:


df.head()


# In[15]:


# Creating Total Price column

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]


# In[16]:


df.head()


# In[ ]:





# ## Recency

# In[17]:


import datetime as dt


# In[18]:


df["InvoiceDate"].max()


# In[19]:


last_date = df["InvoiceDate"].max() + dt.timedelta(days = 1)


# In[20]:


last_date


# In[21]:


recency = df.groupby("CustomerID")["InvoiceDate"].apply(lambda x : (last_date - x.max()).days)


# In[22]:


recency


# In[ ]:





# ## Frequency

# In[23]:


frequency = df.groupby("CustomerID")["InvoiceNo"].count()


# In[24]:


frequency


# In[ ]:





# # Monetary

# In[25]:


monetary = df.groupby("CustomerID")["TotalPrice"].sum()


# In[26]:


monetary


# In[ ]:





# In[27]:


rfm_data = pd.concat([recency, frequency, monetary], axis = 1)


# In[28]:


rfm_data


# In[29]:


# rename columns
rfm_data.rename(columns= {"InvoiceDate" : "Recency",
                          "InvoiceNo" : "Frequency", 
                          "TotalPrice" : "Monetary"}, inplace=True)


# In[30]:


rfm_data.head()


# In[ ]:





# ## Cut values with labels
# - Customers with the lowest recency, highest frequency and monetary amounts considered as top customers

# In[31]:


r_labels = range(5,0,-1)
f_labels = range(1,6)
m_labels = range(1,6)


# In[32]:


r_groups = pd.qcut(rfm_data["Recency"],q = 5, labels=r_labels)
f_groups = pd.qcut(rfm_data["Frequency"], q = 5, labels = f_labels)
m_groups = pd.qcut(rfm_data["Monetary"], q = 5, labels = m_labels)


# In[33]:


rfm_data["R"] = r_groups.values
rfm_data["F"] = f_groups.values
rfm_data["M"] = m_groups.values


# In[34]:


rfm_data


# In[35]:


# combine labels for score
def join_func(x):
    return str(x["R"]) + str(x["F"]) + str(x["M"])


# In[36]:


rfm_data["RFM_Score"] = rfm_data.apply(join_func, axis = 1)


# In[37]:


rfm_data.head()


# In[38]:


# sort by Top/Best customers
rfm_data.sort_values(by = "RFM_Score", ascending = False)


# In[ ]:





# In[ ]:


get_ipython().system(' jupyter nbconvert -- to script rfm_analysis.ipynb')


# In[ ]:




