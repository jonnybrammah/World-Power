#!/usr/bin/env python
# coding: utf-8

# In[76]:


# Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy import stats


# In[77]:


#Data taken from 2020 census but as a csv
#Read the csv

aqi_data = "C:/Users/emanu/repos/Data Project Github/World-Power/Resources/AQI data from EPA.csv"
ppbycounty = "C:/Users/emanu/repos/Data Project Github/World-Power/Output/powerplants_by_county.csv"


# In[78]:


#Read the CSV for all the state powerplants

#Select only useful columns

aqidf = pd.read_csv(aqi_data)
ppbycountydf = pd.read_csv(ppbycounty)

aqidf.head()


# In[79]:


#inserting state and county data merged into one column

aqidf.insert(2,"County, State","")

aqidf


# In[80]:


aqidf.head()


# In[81]:


#created a new column for county/state for the AQI data

aqidf["County, State"] = aqidf["County"]  + " County, "+ aqidf["State"]


aqidf


# In[ ]:





# In[82]:


# creating new column for AQ percentage
aqidf.insert(5, "% Poor Air Quality","")

aqidf


# In[83]:


#checking if we can combine bad air quality days as integers
aqidf.dtypes


# In[84]:


# Figured percentage of Poor Air Quality Days

aqidf["% Poor Air Quality"] = (aqidf["Hazardous Days"] + aqidf["Unhealthy Days"] + aqidf["Very Unhealthy Days"] + aqidf["Unhealthy for Sensitive Groups Days"])/aqidf["Days with AQI"] *100

aqidf.tail()


# In[85]:


#renamed column in new df

ppbycountydf = ppbycountydf.rename(columns={"County":"County, State"})





# In[90]:


#merging dfs

mergedaqippdf = pd.merge(aqidf,ppbycountydf, on="County, State", how="left")



mergedaqippdf

mergedaqippdf = mergedaqippdf.dropna(axis=0, how="any")

mergedaqippdf.columns


# In[93]:




mergedaqippdf["num_combustible"] = mergedaqippdf["num_gas"] + mergedaqippdf["num_oil"] + mergedaqippdf["num_coal"] + mergedaqippdf["num_petcoke"] + mergedaqippdf["num_biomass"]

mergedaqippdf.head()


# In[99]:


#Plotting

x_values = mergedaqippdf["num_combustible"]
y_values = mergedaqippdf["% Poor Air Quality"]

(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = f"y = {str(round(slope,2))}x + {str(round(intercept,2))}"
rvalue_string = f"r-value = {str(round(rvalue,2))}"

plt.scatter(x_values, y_values)
plt.plot(x_values,regress_values)
plt.annotate(line_eq,(35,28),fontsize=12.5,color="red")
plt.annotate(rvalue_string, (35,23), fontsize = 12.5, color = "red")
plt.xlabel("Number of Combustion Power Plants")
plt.ylabel("% of Poor Air Quality Days")
plt.title("% of Poor Air Quality Days by Number of Combustion Power Plants")
print(f"The r-value for this is {rvalue}")


plt.show


# In[101]:


#Determing outliers
quartiles = mergedaqippdf["num_combustible"].quantile([.25, .5, .75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq
lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
outliers_df = mergedaqippdf.loc[(mergedaqippdf["num_combustible"] < lower_bound) | (mergedaqippdf["num_combustible"] > upper_bound)]

outliers_df
#print(outliers_df["State"])
#print(f"The upper bound is {upper_bound}")


# In[102]:


#Removing the Outliers
mergedaqippdf = mergedaqippdf.loc[(mergedaqippdf["num_combustible"] < upper_bound) & (mergedaqippdf["num_combustible"] > lower_bound)]
mergedaqippdf


# In[103]:



x_values_no_outs = mergedaqippdf["num_combustible"]
y_values_no_outs = mergedaqippdf["% Poor Air Quality"]

(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values_no_outs, y_values_no_outs)
regress_values_no_outs = x_values_no_outs * slope + intercept

line_eq = f"y = {str(round(slope,2))}x + {str(round(intercept,2))}"
rvalue_string = f"r-value = {str(round(rvalue,2))}"

plt.scatter(x_values_no_outs, y_values_no_outs)
plt.plot(x_values_no_outs,regress_values_no_outs)
plt.xlabel("Number of Combustion Power Plants")
plt.ylabel("% of Poor Air Quality Days")

plt.title("% of Poor Air Quality Days by Number of Combustion Power Plants")

plt.annotate(line_eq,(15,10.75),fontsize=12.5,color="red")
plt.annotate(rvalue_string, (15, 9.75), fontsize = 12.5, color = "red")


plt.show
print(f"The r-value for this is {rvalue}")

