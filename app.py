import json
import pandas as pd
import pymysql
import pymongo
import sqlalchemy
from sqlalchemy import create_engine 
from flask import Flask, request, render_template, jsonify, make_response, redirect
import os 
import re
from RB_dbFunctions import insert_user, view_exists, get_dataframe_from_db
from RB_Scrape import scrape_title
from collections import Counter
import plotly.express as px
from plotly import graph_objects as go

app = Flask(__name__)  

# # # # # # # # # # # # # # # #   
# Heroku check 
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True  

if is_heroku == True:
    # if IS_HEROKU is found in the environment variables, then use the rest
    # NOTE: you still need to set up the IS_HEROKU environment variable on Heroku (it is not there by default)
    mongoConn = os.environ.get('mongoConn')
    remote_db_endpoint = os.environ.get('remote_db_endpoint')
    remote_db_port = os.environ.get('remote_db_port')
    remote_db_name = os.environ.get('remote_db_name')
    remote_db_user = os.environ.get('remote_db_user')
    remote_db_pwd = os.environ.get('remote_db_pwd')
    accessToken = os.environ.get('accessToken')
    
else:
    # use the config.py file if IS_HEROKU is not detected
    from config import mongoConn, remote_db_endpoint, remote_db_port, remote_db_name, remote_db_user, remote_db_pwd, accessToken
# # # # # # # # # # # # # # # #   
## MY SQL CONN 
pymysql.install_as_MySQLdb() 
engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# # # # # # # # # # # # # # # #  
## ROUTES   


@app.route("/", methods=['GET', 'POST'])
def index(): 
    tab = ''
    df_titles = pd.DataFrame()
    if request.method == 'POST':
        query = request.form['media_title']
        if query != '':
            df_titles = lookup(query)
            tab = 'search'
    streaming_services = get_dataframe_from_db('VW_ServiceByPopularity')
    return render_template("index.html", titles=df_titles.to_dict(orient='records'), streaming_services=streaming_services.to_dict(orient='records'), accessToken=accessToken, tab=tab)

@app.route("/search")
def search(): 
    return render_template("search.html") 

@app.route("/maps")
def maps():
    return render_template("maps.html", accessToken=accessToken)

@app.route("/map")
def map():
    return render_template("maps.html", accessToken=accessToken)

@app.route("/thankyou")
def thankyou():
    streaming_services = get_dataframe_from_db('VW_ServiceByPopularity')
    return render_template("thankyou.html", streaming_services=streaming_services.to_dict(orient='records'))


@app.route("/lookup_result", methods=['GET', 'POST'])
def plots():
    #query = request.form['media_title'] 
    df_titles = pd.DataFrame()
    if request.method == 'POST': 
        query = request.form['media_title']
        if query != '':
            df_titles = lookup(query)
            print(df_titles.to_dict(orient='records'))
  
    return render_template("lookup_result.html", titles=df_titles.to_dict(orient='records'))
 
########################
## FIND A TITLE 
#Look up by 'Post' (a request)
@app.route("/api/lookup", methods=['POST'])
def post_title():
    query = request.form['media_title']  
    if query == '': 
        query="nothing"
    df = lookup(query)
    return render_template("index.html", titles=df.to_dict(orient='records'))

#Look up - 
@app.route("/api/lookup/<query>")
def get_title(query):
    if query == '':
        query = "nothing"
    df = lookup(query)
    _json = df.to_json(orient='records', default_handler=str) 
    #print(_json) 
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json'
    return resp
 
def lookup(query): 
    #MONGO DB CONNECTION FOR CACHED TITLES
    client = pymongo.MongoClient(mongoConn) 
    db = client.shows_db
    collection = db.items
    
    query = re.sub(r'[^a-zA-Z0-9_\s]', '', query)
  
  # TRY EXACT MATCH : With Exact Regular Expression
    title_filter = {  
        "title": {"$regex": f'^{query}', "$options": 'i'}
    }
    #FIND TITLE IN MONGO CACHE
    dict_title = collection.find(title_filter, {'_id': False})
    df_title = pd.DataFrame(dict_title)
  
    if len(df_title) < 1:  #IF NO EXACT MATCH
        title_filter = { 
            # TRY LIKE * MATCH : Regular Expression w/broader search capacity
            "title": {"$regex": f'.*{query}.*', "$options": 'i'}
        }
        #FIND TITLE IN MONGO CACHE
        dict_title = collection.find(title_filter, {'_id': False})
        df_title = pd.DataFrame(dict_title)

    print(title_filter)
    if len(df_title) < 1:  # NO RESULT FOUND IN CACHE 
        dict_title = scrape_title(query)  # SCRAPE TITLE 
        df_title = pd.DataFrame([dict_title])  # LOAD TITLE 
        collection.insert_one(dict_title)  # CACHE TITLE
    df_title = df_title.drop_duplicates(subset='title', keep='last', inplace=False) #Drop any duplicate search results
    try:# TO MAP SERVICE(from mySQL) INFO TO MONGO DATA
        df_StreamingServices = get_dataframe_from_db('streamingservices') #calls function from RB_dbFunctions.py bring in mySQL services table data

        #For Line 135: Had issues with columns returning with numbers instead of column names. May not need this line need to test      
        df_StreamingServices.rename(columns={0: 'Service_ID', 1: 'Service_Name',
                            2: 'Service_Type', 3: 'Service_Img', 4: 'Service_Url'}, inplace=True)
 
        dic_titles = df_title.to_dict(orient='records')#Turn title data frame into dictionary

        #Loop 
        for title in dic_titles: #for each title in list
            title['services_info'] = [] #create empty list for service info
            for service in title['services']: #Loop through service for each title
                try:
                    df_services_info = df_StreamingServices.loc[df_StreamingServices['Service_Name'] == service] #Filter to match up service name to record in mySQL services
                    dict_services_info = df_services_info.to_dict(orient='records')[0] #turn data frame into dictionary
                    print(f'StreamingServices Record : {dict_services_info}') #debug
                    title['services_info'].append(dict_services_info) #appends dictionary to list
                    print(f'Scraped Service : {service} ')
                except:
                    print(f'{service} meta not found')
                    #raise
        df_title = pd.DataFrame(dic_titles)

    except:
        print(f' Services Failed to Map') 
        #raise
         
    return df_title
    

########################
## GET DATA FROM DB RETURN JSON
@app.route("/api/view/<db_view_name>") #set up for testing need to SECCURE!!!!!
def get_db_view(db_view_name): 
 
    df = get_dataframe_from_db(db_view_name)
    _json = df.to_json(orient='records')
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json'  
    return resp
 

########################
## INSERT USER DATA
@app.route("/create_user", methods=['GET', 'POST'])
def create_user(): 
    if request.method == "POST":
        try:
            user_name = request.form["userName"]
            age = request.form["userAge"]
            zips = request.form["userZip"]
            frequency = request.form["userFreq"] 
            service = request.form.getlist('userServ')
            stream_dict = {
                "User_Name": user_name,
                "First_Name":'',
                "Last_Name":'',
                'Age': age,
                'Gender':'',
                'Frequency_ID': frequency,
                'Zip_Code': zips,
                'Audit':'TEST',
                'Services': service
            }  
            user_id = insert_user(stream_dict) 
            print(f'{str(user_id)}{stream_dict}')
        except:
            print(f'create user fail')
        return redirect("/thankyou", code=302)
    return render_template("create_user.html")


########################
## SERVICES DATA ENDPOINT
@app.route("/services-data/")
def services_data(): 

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()
    service_list = []

    services = db.items.find({},{"_id":0, "services":1})
    for service in services:
        if (len(list(service.values())) != 0):
            for opt in list(service.values())[0]:
                service_list.append(opt)

    service_dict = dict(Counter(service_list))
    service_df = pd.DataFrame.from_dict(service_dict, orient='index')
    sds = service_df.sort_values(by=0, ascending=False)
    sds.reset_index(inplace=True)
    sds.rename(columns={'index':'service preferred by user', 0:'count'}, inplace=True)
    sds.drop(sds.loc[sds['service preferred by user']=='Rent or Buy'].index, inplace=True)

    sds_short = sds[0:30]
    
    sds_short_json = sds_short.to_json(orient='records')

    return sds_short_json

########################
## RECOMMENDATIONS DATA ENDPOINT
@app.route("/recommendations-data/")
def recommendations_data():

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()

    rec_list = []
    recs = db.items.find({},{"_id":0, "recommended":1});
    for rec in recs:
        if (len(list(rec.values()))!= 0):
            for opt in list(rec.values())[0]:
                if isinstance(opt, str):
                    rec_list.append(opt)

    rec_dict = dict(Counter(rec_list))
    rec_df = pd.DataFrame.from_dict(rec_dict, orient='index')
    rds = rec_df.sort_values(by=0, ascending=False)
    rds.reset_index(inplace=True)
    rds.rename(columns={'index':'recommendation', 0:'count'}, inplace=True)

    rds_short = rds[0:30]

    rds_short_json = rds_short.to_json(orient='records')

    return rds_short_json

########################
## SUBSCRIBER DATA ENDPOINT
@app.route("/subscriber-data/")
def subscriber_data():

    mySQLConn = ''
    pymysql.install_as_MySQLdb() 
    engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")
    conn = engine.connect()

    sql = f''' 

        SELECT 
            p.User_Name AS username,
            t.Service_Name as services,
            z.Latitude AS lat,
            z.Longitude AS lng
        FROM
            user_profile p
        INNER JOIN user_profile_services s
            ON s.User_ID = p.User_ID
        INNER JOIN streamingservices t
            ON t.Service_ID = s.Service_ID
        INNER JOIN zips z
            ON z.Zip = p.Zip_Code
        
    '''
    df = pd.read_sql(sql, con=conn)
    user_services = df.groupby(['username'])['services'].apply(', '.join).to_frame()
    user_location = df.drop_duplicates(subset=['username'])[['username', 'lat','lng']]
    user_data = pd.merge(user_location, user_services, how='left', on='username')

    user_data_json = user_data.to_json(orient='records')

    return user_data_json

########################
## BAR CHART OF SERVICES
@app.route("/services-viz/")
def services_viz():

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()
    service_list = []

    services = db.items.find({}, {"_id": 0, "services": 1})
    for service in services:
        if (len(list(service.values())) != 0):
            for opt in list(service.values())[0]:
                service_list.append(opt)

    service_dict = dict(Counter(service_list))
    service_df = pd.DataFrame.from_dict(service_dict, orient='index')
    sds = service_df.sort_values(by=0, ascending=False)
    sds.reset_index(inplace=True)
    sds.rename(
        columns={'index': 'service preferred by user', 0: 'count'}, inplace=True)
    sds.drop(sds.loc[sds['service preferred by user']=='Rent or Buy'].index, inplace=True)

    sds_short = sds[0:30]
    fig = px.bar(sds_short, x="service preferred by user",
                 y="count", color="count", title="SERVICES USERS PREFER")
    fig.write_html("templates/services-viz.html")

    return render_template("services-viz.html")

########################
## BAR CHART OF RECOMMENDATIONS


@app.route("/recommendations-viz/")
def recommendations_viz():

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()

    rec_list = []
    recs = db.items.find({}, {"_id": 0, "recommended": 1})
    for rec in recs:
        if (len(list(rec.values())) != 0):
            for opt in list(rec.values())[0]:
                if isinstance(opt, str):
                    rec_list.append(opt)

    rec_dict = dict(Counter(rec_list))
    rec_df = pd.DataFrame.from_dict(rec_dict, orient='index')
    rds = rec_df.sort_values(by=0, ascending=False)
    rds.reset_index(inplace=True)
    rds.rename(columns={'index': 'recommendation', 0: 'count'}, inplace=True)

    rds_short = rds[0:30]
    fig = px.bar(rds_short, x="recommendation", y="count", color="count", title="USER RECOMMENDATIONS")
    fig.write_html("templates/recommendations-viz.html")

    return render_template("recommendations-viz.html")


@app.route("/services-cost-viz")
def services_cost_viz():
   
    fig = go.Figure()

    fig.add_trace(go.Funnel(
        name='Netflix',
        y=["Premium", "Standard", "Basic"],
        x=[17.99,  13.99, 8.99],
        textinfo="value+percent initial"))

    fig.add_trace(go.Funnel(
        name='Hulu',
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[70.99, 11.99, 5.99],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Youtube Premium",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[64.99, 11.99, 0.00],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Sling TV",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[50.00, 35.00, 0.00],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Disney Plus",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[69.99, 6.99, 0.00],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Peacock TV",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[9.99, 4.99, 0.00],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Amazon Prime Video",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[12.99, 8.99, 6.99],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Crunchyroll",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[14.99, 9.99, 7.99],
        textposition="inside",
        textinfo="value+percent previous"))

    fig.add_trace(go.Funnel(
        name="Funimation",
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[99.99, 7.99, 5.99],
        textposition="inside",
        textinfo="value+percent previous"))


    fig.add_trace(go.Funnel(
        name='Apple One',
        orientation="h",
        y=["Premium", "Standard", "Basic"],
        x=[29.95, 19.95, 4.99],
        textposition="outside",
        textinfo="value+percent total"))

    #fig.show()
    #fig.write_html("templates/services_cost_viz.html")

    return render_template("services_cost_viz.html")


@app.route("/ripe-rating-viz")
def ripe_rating_viz():


    return render_template("ripe_rating_viz.html")




# run the app in debug mode
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)

#     ____                           ___
#    |  _ \  ___              _   _.' _ `.
# _  | [_) )' _ `._   _  ___ ! \ | | (_) |    _
#|:;.|  _ <| (_) | \ | |' _ `|  \| |  _  |  .:;|
#|   `.[_) )  _  |  \| | (_) |     | | | |.',..|
#':.   `. /| | | |     |  _  | |\  | | |.' :;::'
# !::,   `-!_| | | |\  | | | | | \ !_!.'   ':;!
# !::;       ":;:!.!.\_!_!_!.!-'-':;:''    '''!
# ';:'        `::;::;'             ''     .,  .
#   `:     .,.    `'    .::... .      .::;::;'
#     `..:;::;:..      ::;::;:;:;,    :;::;'
#       "-:;::;:;:      ':;::;:''     ;.-'
#           ""`---...________...---'""
#------------------------------------------------
