
# coding: utf-8

# ### Welcome to getting started with Pyhton!
# 
# This notebook's goal is not just teach the basics of the python language but instead to show what you can do with it!
# We will be covering some of the language basics as we move along the project.
# 
# Tha project at hand is to parse data from [www.coloradobrewerylist.com](www.coloradobrewerylist.com) and perform some basic analysis, including spatial analysis!

# Fist let's import the libraries we need.
# 
# The `import` method is used to load external libraries into your code. You can also provide aliases to a given library by using the `as` argument, like were are doing with the `pandas` library.

# In[ ]:

import pip

# Install Follium since it doesn't come with Anaconda
pip.main(['install', 'folium'])


# In[1]:

import pip
import urllib2
import json
import pandas as pd
import bokeh
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic(u'matplotlib inline')

import folium
from folium.plugins import MarkerCluster


# In[2]:

# This is the base URL that we will be using to get the data from the API. Note the {page} argument.
base_url = 'https://www.coloradobrewerylist.com/wp-json/wp/v2/brewery/?filter%5Bbrewery_visitors%5D=visitors-welcome&location-type_exclude=404,405&page={page}&per_page=100'

# An empty list that we will use to hold the parsed data
breweries = []

# The API has a limit of 100 results per page, so we need to receive 4 pages to get the full dataset.
page_numbers = [1, 2, 3, 4]

# A for loop that will iterate over the page_numbers list and update the base_url with each page number.
for page_number in page_numbers :
    # A new URL is built for each page_number. The format method replaces the {page} argument in the base_url string
    # with the current page_number
    new_base_url = base_url.format(page=page_number)
    print new_base_url
    
    # Using the urllib2 library we query the new_base_url url which returns the JSON data.
    response = urllib2.urlopen(new_base_url)
    # Using the JSON library we parse the JSON data into a Python object (a list composed by dictionaries).
    data = json.load(response)
    
    # The parsed data is a list composed by dictionaries holding the data we want. 
    for el in data:
        # grab name, coordinates, and open date
        name = el['title']['rendered']
        lon = float(el['meta']['brewery_lon'][0])
        lat = float(el['meta']['brewery_lat'][0])
        open_date = el['meta']['brewery_open_date'][0]
        # in case the open_data is missing we set it as a string 'None'
        if open_date == None:
            open_date = np.nan
    

        # Build a dictionary with the current brewery data
        brewery = {'name': name, 'lng': lon, 'lat': lat, 'open_date': open_date}
        
        # Add disctionary to main breweries list
        breweries.append(brewery) 


# In[ ]:

# Let's look at the final list
print breweries


# In[5]:

# Using the Pandas library (loaded as pd) we transform our dictionary into a Dataframe.
# Dataframes is one the basic data formats provided by Pandas.
# It is essentialy a table that support a number of different data analysis methods.
df = pd.DataFrame.from_dict(breweries)
# Convert data column from string to datatime type
df.open_date = pd.to_datetime(df.open_date)
print df
df.to_csv('./colorado_breweries.csv', encoding='utf-8')
print 'Number of breweries is: {}'.format(df.shape[0])


# In[ ]:

# Let's see when the first brewery was open
# df[(df['open_date'] != np.nan)].min()
df[df.open_date == df.open_date.min()]


# In[ ]:

# Let's see when the first brewery was open
df[df.open_date == df.open_date.max()]


# In[ ]:

# Let's create a new column with the year the brewery was open
df['open_year'] = df['open_date'].astype('str').str[:4]

# And now we count how many breweries were open on each year
year_counts = df.groupby(['open_year']).size()


# In[ ]:

# let's plot a histogran for the open_year column
plt.subplots(figsize=(15,8))
sns.countplot(x="open_year", data=df[df['open_year'] != 'NaT'], palette="Greens_d")


# In[ ]:

# This is maptime, so let's create a map!
map = folium.Map(location=[39.7, -104.9])
marker_cluster = MarkerCluster().add_to(map)

# add a marker for every record in the filtered data, use a clustered view
for brewery in df.iterrows():
    folium.Marker(
        location = [brewery[1]['lat'],brewery[1]['lng']], popup=brewery[1]['name']).add_to(marker_cluster)

map


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



