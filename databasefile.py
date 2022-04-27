from click import pass_context
import pyodbc
import pandas as pd
import sqlite3
from sqlite3 import Error
import csv

DB_NAME = 'Database.sqlite'

def create_database():
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_data1_sql = "DROP TABLE IF EXISTS 'data1'"
    drop_data2_sql = "DROP TABLE IF EXISTS 'data2'"

    create_data1_sql= '''
    CREATE TABLE IF NOT EXISTS 'data1'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'State' TEXT NOT NULL,
        'Year' INTEGER NOT NULL,
        'Household_Size' INTEGER NOT NULL,
        'Income_Level' INTEGER NOT NULL
    )
    '''

    create_data2_sql= '''
    CREATE TABLE IF NOT EXISTS 'data2'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Year' INTEGER NOT NULL,
            'State' TEXT NOT NULL,
            'Medicaid_Status' INTEGER NOT NULL,
            'Medicare_Status' INTEGER NOT NULL,
            'Poverty_Ratio' INTEGER NOT NULL,
            'Education_Level' INTEGER NOT NULL
            )
    '''
    cur.execute(drop_data1_sql)
    cur.execute(drop_data2_sql)
    cur.execute(create_data1_sql)
    cur.execute(create_data2_sql)

    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    data_data1_header = []
    data_data1_row = []

    with open('Data/guidlinesbystatebyyearCMS.csv','r') as csvfile:
        data = []
        csv_header = csv.reader(csvfile)
        for item in csv_header:
            data.append(item)
        data_data1_header.extend(data[0])
        data_data1_row.extend(data[1:])

    insert_data1_sql = '''
        INSERT INTO data1
        VALUES(NULL,?,?,?,?)
    '''

    for item in data_data1_row:
        cur.execute(insert_data1_sql,[
            item[1],
            item[2],
            item[3],
            item[4],
        ])


    data_data2_header = []
    data_data2_row = []

    with open('Data/CensusData2016-20.csv','r') as csvfile:
        data = []
        csv_header = csv.reader(csvfile)
        for item in csv_header:
            data.append(item)
        data_data2_header.extend(data[0])
        data_data2_row.extend(data[1:])

    insert_data2_sql = '''
        INSERT INTO data2
        VALUES(NULL,?,?,?,?,?,?)
    '''

    for item in data_data2_row:
        cur.execute(insert_data2_sql,[
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
            item[6],
        ])

    conn.commit()
    conn.close()

# create_database()
# populate_database()




# query = f'''
# SELECT * FROM data1 '''

# result = cur.execute(query).fetchall()
# print(result)

def data1_access(State,Year, Household_Size= None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    fetch_data1 = f''' SELECT Income_Level FROM data1 WHERE State =='{State}' AND Year == '{Year}' AND Household_Size == '{Household_Size}' '''
    print(cur.execute(fetch_data1).fetchall())
    conn.commit()
    conn.close()
#data1_access('KY',2018,7)

def data2_access(State,Year,Medicaid_Status = None,Medicare_Status =None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    fetch_data1 = f''' SELECT Medicaid_Status,Medicare_Status,Poverty_Ratio,Education_Level FROM data2 \
        WHERE State =='{State}' AND Year == '{Year}' AND Medicaid_Status == '{Medicaid_Status}' AND Medicare_Status == '{Medicare_Status}' '''
    print(cur.execute(fetch_data1).fetchall())
    conn.commit()
    conn.close()
#data2_access('WA',2020,1,1)

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
years = [2016,2017,2018,2019,2020]
prompts = ['Medicaid_Status','Medicare_Status']
Household_Size = [1,2,3,4,5,6,7,8]
tree ={}

def create_tree():
    for item1 in states:
        tree[item1] = {}
        for item2 in years:
            tree[item1][item2] = {}
            for item3 in prompts:
                pass
                for item4 in Household_Size:
                    pass