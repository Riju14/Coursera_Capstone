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


df4 = df3[df3['Borough'].str.contains('Toronto',regex=False)]
df4


# # Clustering and putting on Map
# 
# k=5
# toronto_clustering = df4.drop(['Postalcode','Borough','Neighborhood'],1)
# kmeans = KMeans(n_clusters = k,random_state=0).fit(toronto_clustering)
# kmeans.labels_
# df4
# #df4.insert(0, 'Cluster Labels', kmeans.labels_)

# In[49]:


# Map showing the Clusters
map_clusters = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

# set color scheme for the clusters
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, neighborhood, cluster in zip(df4['Latitude'], df4['Longitude'], df4['Neighborhood'], df4['Cluster Labels']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[ ]:




