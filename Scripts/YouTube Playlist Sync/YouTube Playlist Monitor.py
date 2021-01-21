#!/usr/bin/env python
# coding: utf-8

# #  YouTube Playlist Monitoring

# <!-- wp:paragraph -->
# <p>There are many different workflow and automation suites/platforms (some of which include IFTTT, Power Automate and Tonkean) available out there that allow users to interact with their YouTube connector. Most of these workflows classify the functions within the connectors as either a <strong>Trigger </strong>or an <strong>Action</strong>. A trigger would be seen as an event that "kicks off" the workflow/process, whereas an action would be an event (or a set of events) that should be executed once the workflow/process has been triggered. </p>
# <!-- /wp:paragraph -->
# 
# <!-- wp:paragraph -->
# <p>Many of these workflows make use of APIs to get their triggers and actions functioning. There is one small problem though... They don't always have the predefined triggers or actions that we might be looking to use. Platforms like IFTTT and Power Automate do not have a "When an item is added to a Playlist" trigger. Not a train smash though... In this post, we work through how to monitor a YouTube playlist for the addition of new items using Python.</p>
# <!-- /wp:paragraph -->

# ## Install Libraries

# In[ ]:


get_ipython().system('pip install google-api-python-client')
get_ipython().system('pip install google_auth_oauthlib')


# ## Import Libraries

# In[ ]:


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from datetime import datetime

import pandas as pd
import numpy as np
import requests
import json


# ## Gather Variable Values

# In[ ]:


DEVELOPER_KEY = '<insert key>'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

playlist_id = '<insert id>'


# ## Query Playlist Items

# In[ ]:


# Get all items in specified playlist
def get_playlist_items(page_token):
    # Auth with YouTube service
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the playlistItems.list method to retrieve results matching the specified query term.
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        pageToken=page_token,
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    
    return response


# ## Process New Items

# In[ ]:


# process any items that were not found in the previous set of results
def process_new(df_old, df_new):
    
    df_diff = df_new.set_index('title').drop(df_old['title'], errors='ignore').reset_index(drop=False)
    
    print(len(df_diff))
    
    for index, element in df_diff.iterrows():
    
        print("New Item Added: " + str(element['title']).encode('utf-8'))


# ## Main Method Snippet

# In[ ]:


isEnd = False
page_token = None
df = pd.DataFrame() # instantiate blank dataframe
df_history = pd.read_excel('items.xlsx', headers=False) # read history before querying new results so that the new records may be identified

while not isEnd:

    playlist_items = get_playlist_items(page_token)
    
    current_count = playlist_items['pageInfo']['totalResults']
    
    # if there is a page token, use it for the next call or assign it back to None
    if 'nextPageToken' in playlist_items.keys():
        
        page_token = playlist_items['nextPageToken']
                            
    else:
        
        isEnd = True
        
        page_token = None
    
    # write playlist item information to the dataframe
    for item in playlist_items['items']:

        temp_df = pd.DataFrame.from_dict(item)
        temp_df = temp_df[['snippet']].transpose()

        df = df.append(temp_df)
            
df.to_excel('items.xlsx') # write the dataframe to excel

process_new(df_history, df) # process the new items

