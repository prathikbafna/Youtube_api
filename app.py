from bson import json_util
from flask import Flask , jsonify
import pymongo
import json
from pymongo import MongoClient
import urllib.parse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
#import pandas as pd
#import dns
import datetime
#from sentiment import *
from dateutil.parser import parse
#from ner import *
import threading
import time

#username and password to connect to database(mongodb)
username = urllib.parse.quote_plus('prathikbafna0')
password = urllib.parse.quote_plus("Pbabc0821@@@###")
url = "mongodb+srv://{}:{}@youtubedatafech.6f81l.mongodb.net/<dbname>?retryWrites=true&w=majority".format(username, password)
cluster = pymongo.MongoClient(url)
db = cluster['ytData']['real_time_data']
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is my first API call!'


#@app.route('/fetch')
def youtube_search(q='mobile', max_results = 5,order="date", token=None, location=None, location_radius=None):

    #here we are fetching the data for the predefined query using youtube api

    #DEVELOPER_KEY = "AIzaSyBkV83GKSoqmxxPxB1h7KrVvu8Kj6d7RWE"
    DEVELOPER_KEY = "AIzaSyBA9aUzGcJzRH4nJii10Gydf0EqE_P9nm0"
    print('working..............')

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    while(True):
        try:
            search_response = youtube.search().list(
            q=q,
            type="video",
            pageToken=token,
            order = order,
            part="id,snippet", # Part signifies the different types of data you want
            maxResults=max_results,
            location=location,
            locationRadius=location_radius).execute()

            for search_result in search_response.get("items", []):
                publish_datetime = search_result['snippet']['publishedAt']
                title = search_result['snippet']['title']
                desc = search_result['snippet']['description']
                thumbnail_urls = search_result['snippet']['thumbnails']
                flag = True


                #checking if the record is already present in the database
                for i in db.find({'tag':q}):
                    if i['title'] == title:
                        flag = False
                        break
                if flag:
                    db.insert_one({ 'tag':q,
                               'title':title,
                               'publish_datetime':publish_datetime,
                               'description' : desc,
                               'urls':[ j['url'] for i,j in thumbnail_urls.items()]
                               })

                '''else:
                    db.update_one({ 'tag':q,
                               'title':title,
                               'publish_datetime':publish_datetime,
                               'description' : desc,
                               'urls':[ j['url'] for i,j in thumbnail_urls.items()]
                               })'''
        except:
            print("limit reached")
            break

        time.sleep(10)
    #return 'Data added to database'


@app.route('/search/<string:title>/<string:desc>')
def find_by_title_and_desc(title,desc):

    #fetch data based on title and description

    result ={}
    key =0
    for responses in db.find({'title': title , 'description': desc },{'_id':0}):
        result[key] = responses
        key+=1
    return result


@app.route('/get/<string:q>')
#query can be set as a constant to 'mobile'
def get_data(q):

    #returning data for the predefined query in reverse chronological order of their publishing date-time

    result = {}
    key = 0
    x = list(db.find({'tag': q},{'_id':0}))
    x.sort(key = lambda x: x['publish_datetime'],reverse=True)
    for data in x:
        result[key] = data
        key+=1
    return result


if __name__ == '__main__':
    t1 = threading.Thread(target=youtube_search)
    t1.start()
    app.run(host = '0.0.0.0',port = 5000,debug=True)
