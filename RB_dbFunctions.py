import json
import pandas as pd
import pymysql
import pymongo
import sqlalchemy
from sqlalchemy import create_engine

import os

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
else:
    # use the config.py file if IS_HEROKU is not detected
    from config import mongoConn, remote_db_endpoint, remote_db_port, remote_db_name, remote_db_user, remote_db_pwd

#connect to mySQL
conn = pymysql.connect(host=f'{remote_db_endpoint}',
                       user=remote_db_user,
                       password=remote_db_pwd,
                       db=remote_db_name)

mycursor = conn.cursor()


pymysql.install_as_MySQLdb()
engine = create_engine(
    f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")


#inserts user profile
def insert_user(profile_dict):
    sql = """
    INSERT INTO 
        user_profile(User_Name, First_Name, Last_Name, Age, Gender, Frequency_ID, Zip_Code, Audit)
    VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    val = (profile_dict['User_Name'], profile_dict['First_Name'], profile_dict['Last_Name'], profile_dict['Age'],
           profile_dict['Gender'], profile_dict['Frequency_ID'], profile_dict['Zip_Code'], profile_dict['Audit'])
    mycursor.execute(sql, val)
    conn.commit()
    userid = mycursor.lastrowid
    map_services(userid, profile_dict['Services'])
    return ''

#insert into table that maps services to user
def map_services(user_id, serviceList):
    sql = """
        DELETE FROM user_profile_services
        WHERE User_ID = %s;
    """
    val = (user_id)
    mycursor.execute(sql, val)
    conn.commit()

    sql = """
    INSERT INTO 
        user_profile_services(User_ID, Service_ID)
    VALUES 
        (%s, %s);
        """
    for service_id in serviceList:
        val = (user_id, service_id)
        mycursor.execute(sql, val)
        conn.commit()


def view_exists(db_view_name):
    conn = engine.connect()
    sql = '''
    SELECT TABLE_NAME DB_VIEW FROM (
        SELECT TABLE_NAME  FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = 'ripe_bananas' 
        UNION
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'ripe_bananas' 
    ) DB_VIEWS  
    '''
    df = pd.read_sql(sql, con=conn)
    df = df.loc[df.DB_VIEW == db_view_name]
    conn.close()
    return len(df) > 0


def get_dataframe_from_db(db_view_name):
    conn = engine.connect()
    if not view_exists(db_view_name):
        return 'db view object not found / invalid' 
    sql = f''' SELECT * FROM {db_view_name}'''
    df = pd.read_sql(sql, con=conn)
    conn.close()
    return df

