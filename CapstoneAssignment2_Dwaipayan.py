#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries
# import requests # library to handle requests
# import pandas as pd # library for data analsysis
# import numpy as np # library to handle data in a vectorized manner
# import random # library for random number generation
# from geopy.geocoders import Nominatim 
# from IPython.display import Image 
# from IPython.core.display import HTML 
# from IPython.display import display_html
# import pandas as pd
# import numpy as np
# from pandas.io.json import json_normalize
# import folium 
# from bs4 import BeautifulSoup
# from sklearn.cluster import KMeans
# import matplotlib.cm as cm
# import matplotlib.colors as colors
# 
# print('Libraries imported.')

# # Scraping, cleaning and arranging data
# source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
# soup=BeautifulSoup(source,'lxml')
# print(soup.title)
# from IPython.display import display_html
# tab = str(soup.table)
# display_html(tab,raw=True)

# In[3]:


dfs = pd.read_html(tab)
df=dfs[0]
df.head()


# In[10]:


df1 = df.dropna()

df2 = df1.groupby(['Postal code','Borough'], sort=False).agg(', '.join)
df2.reset_index(inplace=True)

# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
df2['Neighborhood'] = np.where(df2['Neighborhood'] == 'Not assigned',df2['Borough'], df2['Neighborhood'])

df2


# In[20]:


lat_lon = pd.read_csv('https://cocl.us/Geospatial_data')
lat_lon


# In[32]:


lat_lon.columns=['Postalcode','Latitude','Longitude']

df2.rename(columns={'Postal code':'Postalcode'},inplace=True)
df3=pd.merge(df2,lat_lon[['Postalcode','Latitude', 'Longitude']],on='Postalcode')
df3.head()


# In[33]:


## Getting Latitude and Longitude 
df4 = df3[df3['Borough'].str.contains('Toronto',regex=False)]
df4


# 

# In[49]:





# In[ ]:




