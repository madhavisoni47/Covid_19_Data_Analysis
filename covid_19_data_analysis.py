#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

import warnings
import re

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format','{:.2f}'.format)


# ## TASK 1: Get a `COVID-19 pandemic` Wiki page using HTTP request

# In[2]:


url = "https://en.wikipedia.org/w/index.php?title=Template:COVID-19_testing_by_country"


# In[3]:


requests.get(url)


# In[4]:


data = requests.get(url).text


# ## TASK 2: Extract COVID-19 testing data table from the wiki HTML page

# Get the table node from the root html node
# use the `read_html` function in rvest library to get the root html node from response
# 

# In[5]:


soup = BeautifulSoup(data,"html.parser")
tables = soup.find_all('table')
len(tables)
df = pd.read_html(io=url)[1]
df


# Print the summary of the data frame

# In[43]:


df.info()


# In[7]:


df = df[0:172]


#  call `preprocess_covid_data_frame` function and assign it to a new data frame

# In[8]:


data = df.copy()


# ## TASK 3: Pre-process and export the extracted data frame
# 
# The goal of task 3 is to pre-process the extracted data frame from the previous step, and export it as a csv file

#  Print the summary of the processed data frame again

# In[9]:


data.info()


# In[20]:


data.head()


# remove noises from columns name 

# In[31]:


data.columns = data.columns.str.replace('%', '')
data.columns = data.columns.str.replace('/', '')
data.columns = data.columns.str.replace(',', '')
data.columns = data.columns.str.replace(')', '')


# In[32]:


data.head(2)


# After pre-processing, you can see the columns and columns names are simplified, and columns types are converted into correct types.

# The data frame has following columns:
# 
# - **country** - The name of the country
# - **date** - Reported date
# - **tested** - Total tested cases by the reported date
# - **confirmed** - Total confirmed cases by the reported date
# - **confirmed.tested.ratio** - The ratio of confirmed cases to the tested cases
# - **tested.population.ratio** - The ratio of tested cases to the population of the country
# - **confirmed.population.ratio** - The ratio of confirmed cases to the population of the country

# In[ ]:


# rename columns name 
data.rename(columns={
    'Country or region': 'country',
    'Date[a]': 'date',
    'Tested': 'tested',
    'Units[b]': 'units'
},inplace=True)


# In[40]:


data.rename(columns={'Confirmed cases': 'confirmed',
    'Confirmed tested': 'confirmed_tested_ratio',
    'Tested population': 'tested_population_ratio',
    'Confirmed population': 'confirmed_population_ratio'
},inplace=True)


# In[38]:


data.columns = data.columns.str.replace(' ', '')


# In[41]:


data.head(2)


# Remove The Unrelevent columns 

# In[44]:


data.drop(["units","reference"],axis =1, inplace = True)


# In[45]:


data.head(2)


# change data type of columns  

# In[46]:


from datetime import datetime
data['date'] = pd.to_datetime(data['date'])


# In[47]:


data["tested"] = data["tested"].astype('int')
data["confirmed"] = data["confirmed"].astype('int')
data["confirmed_tested_ratio"] = data["confirmed_tested_ratio"].astype('float')
data["Tested population"] = data["Tested population"].astype('float')
data["confirmed_population_ratio"] = data["confirmed_population_ratio"].astype('float')


# In[48]:


data.info()


# Export the data frame to a csv file

# In[49]:


data.to_csv("covid19_file.csv",index = False)


# ## TASK 4: Get a subset of the extracted data frame
# 
# The goal of task 4 is to get the 5th to 10th rows from the data frame with only `country` and `confirmed` columns selected

# In[50]:


# Read covid_data_frame_csv from the csv file
covid = pd.read_csv("covid19_file.csv")

# Get the 5t"covid19_file.csv")h to 10th rows, with two "country" "confirmed" columns
covid_test = covid[["country","confirmed"]]
covid_test.iloc[4:11]


# ## TASK 5: Calculate worldwide COVID testing positive ratio
# 
# The goal of task 5 is to get the total confirmed and tested cases worldwide, and try to figure the overall positive ratio using `confirmed cases / tested cases`

# In[51]:


# Get the total confirmed cases worldwide
total_tested = covid["tested"].sum()
print(total_tested)
# Get the total tested cases worldwide
total_confirmed = covid["confirmed"].sum()
print(total_confirmed)
# Get the positive ratio (confirmed / tested)
positive_ratio = (total_confirmed / total_tested )
print( positive_ratio)


# ## TASK 6: Get a country list which reported their testing data 
# 
# The goal of task 6 is to get a catalog or sorted list of countries who have reported their COVID-19 testing data

# In[52]:


country_tested_df = covid[["country","tested"]]

country_tested_df.head(5)


# In[53]:


# Conver the country column into character so that you can easily sort them
covid['country'] = covid['country'].astype(str)


# In[54]:


# Check its class (should be Factor)
print(country_tested_df['country'].dtype)


# In[55]:


# Sort the countries AtoZ
sorted_countries_AtoZ = covid["country"].sort_values(ascending=True)


# In[56]:


# Sort the countries ZtoA
sorted_countries_ZtoA = covid["country"].sort_values(ascending=False)


# In[57]:


# Print the sorted AtoZ list
print("Sorted A to Z:", sorted_countries_AtoZ)


# In[58]:


# Print the sorted ZtoA list
print("Sorted Z to A:", sorted_countries_ZtoA)


# ## TASK 7: Identify countries names with a specific pattern
# 
# The goal of task 7 is using a regular expression to find any countires start with `United`

# In[59]:


# Use a regular expression `United.+` to find matches
matches = covid['country'].str.contains('United.+', regex=True)
# Print the matched country names
matched_countries = covid[matches]['country'].tolist()
print("Matched country names:", matched_countries)


# ## TASK 8: Pick two countries you are interested, and then review their testing data
# 
# The goal of task 8 is to compare the COVID-19 test data between two countires, you will need to select two rows from the dataframe, and select `country`, `confirmed`, `confirmed-population-ratio` columns

# In[60]:


select_country1 = covid.iloc[165]
select_country1


# In[61]:


select_country2 = covid.iloc[72]
select_country2


# In[62]:


# Select a subset (should be only one row) of data frame based on a selected country name and columns
United_States = pd.DataFrame(covid.iloc[165][['country','confirmed','confirmed_population_ratio']]).T
United_States


# In[63]:


# Select a subset (should be only one row) of data frame based on a selected country name and columns
India = pd.DataFrame(covid.iloc[72][['country','confirmed','confirmed_population_ratio']]).T
India


# ## TASK 9: Compare which one of the selected countries has a larger ratio of confirmed cases to population
# 
# The goal of task 9 is to find out which country you have selected before has larger ratio of confirmed cases to population, which may indicate that country has higher COVID-19 infection risk

# In[64]:


selectedcountry_US = United_States.iloc[:,2]
selectedcountry_US


# In[65]:


selectedcountry_India = India.iloc[:,2]
selectedcountry_India


# In[66]:


ratio_US = United_States['confirmed'] / United_States['confirmed_population_ratio']
ratio_India = India['confirmed'] / India['confirmed_population_ratio']
if ratio_US.iloc[0] > ratio_India.iloc[0]:
    print("The United States has a larger ratio of confirmed cases to population.")
elif ratio_US.iloc[0] < ratio_India.iloc[0]:
    print("India has a larger ratio of confirmed cases to population.")
else:
    print("The ratios are equal.")


# ## TASK 10: Find countries with confirmed to population ratio rate less than a threshold
# 
# The goal of task 10 is to find out which countries have the confirmed to population ratio less than 1%, it may indicate the risk of those countries are relatively low

# In[67]:


# Get a subset of any countries with `confirmed.population.ratio` less than the threshold
threshold = 0.1
countries_below_threshold = covid[covid['confirmed_population_ratio'] < threshold]

# Display the result
print("Countries with confirmed to population ratio less than", threshold)
print(countries_below_threshold[['country', 'confirmed_population_ratio']])


# In[ ]:




