# -*- coding: utf-8 -*-
"""Final Project.PRATAP
"""

#PIP INSTALL CODE CHUNK

from multiprocessing import AuthenticationError
from turtle import title
import requests
import webbrowser
import time
import datetime
import json
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import plotly.graph_objs as go
import plotly.figure_factory as ff
import csv
import sqlite3
import pandas as pd
import http.client
#import xmltodict
# Using BeautifulSoup to Scrap CMS Website
url = 'https://developer.cms.gov/marketplace-api/'
# html = urlopen(url) 
# soup = BeautifulSoup(html, 'html.parser')
# #tables = soup.find_all('table')
# #print(tables)
# empty_list =[]
# for div in soup.find_all('table'):
#         #empty_list.append(div)
#         path = div.get('table')
#         empty_list.append(path)
# empty_list
response1 = requests.get(url)
soup = BeautifulSoup(response1.text, 'html.parser')
print(soup)
datasets = []
for link in soup.find_all('a'):
  path = link.get('href')
  datasets.append(path)
print(datasets)

# Retrieving Income Guidelines for state over 5 years using API from CMS website

import http.client
conn = http.client.HTTPSConnection("marketplace.api.healthcare.gov")
headers = { 'accept': "application/json" }
API_KEY = "PnpazgEspJ5X17MDvspgPRMmjAuuUlFT"

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
years = [2016,2017,2018,2019,2020]
data1frame = []
d = {}
d['State'] = []
d['Year'] = []
d['Household_Size'] = []
d['Income_Level'] = []
while True:
  for item1 in states:
    for item2 in years: 
      user_input_State = item1
      user_input_Year = item2 
      conn.request("GET", "/api/v1/states/{}/poverty-guidelines?year={}&apikey={}".format(user_input_State,user_input_Year,API_KEY), headers=headers)
      res = conn.getresponse()
      data = ((res.read()).decode("utf-8"))
      data = json.loads(data)
      x = data.get("guidelines")
      for val in x:
        d['State'].append(user_input_State)
        d['Year'].append(user_input_Year)
        d['Household_Size'].append(val['household_size'])
        d['Income_Level'].append(val['guideline'])
  break
data = pd.DataFrame.from_dict(d)

data

data.to_csv("guidlinesbystatebyyearCMS.csv")

# Retrieving Census data using API

"""Data Variables explanation:

CAID = Health insurance, covered by Medicaid / local name ["2": "No", "1": "Yes", "0": "Niu"]

CARE = 	Health insurance, covered by Medicare ["2": "No", "1": "Yes", "0": "Niu"]

FAMLIS= Poverty - ratio family income/low-income level 
["4": "150 percent and above the low-income level","3": "125 - 149 percent of the low-income level","2": "100 - 124 percent of the low-income level", "1": "Below low-income level"] 

A_HGA = Demographics, Educational attainment 
["0": "Children",
"31": "Less Than 1st Grade",
"32": "1st,2nd,3rd,or 4th grade",
"33": "5th Or 6th Grade",
"34": "7th and 8th grade",
"35": "9th Grade",
"36": "10th Grade",
"37": "11th Grade",
"38": "12th Grade No Diploma",
"39": "High school graduate-high school diploma",
"40": "Some College But No Degree",
"41": "Assc degree-occupation/vocation",
"42": "Assc degree-academic program"
"44": "Master's degree (MA,MS,MENG,MED,MSW,MBA)",
"43": "Bachelor's degree (BA,AB,BS)",
"45": "Professional school degree (MD,DDS,DVM,L)",
"46": "Doctorate degree (PHD,EDD)"]
"""

years = [2016,2017,2018,2019,2020]
data_census = []
for item in years:
  censusdata= requests.get('https://api.census.gov/data/{item}/cps/asec/mar?get=CAID,CARE,FAMLIS,A_HGA&for=state:*&key=8591815c57eeadba524bd90eeebc51bd2c120349')
  data_census.append(requests.Response.json())

df_census = pd.DataFrame()
state = []
medicaid_status = []
medicare_status = []
poverty_ratio = []
education_level = []
Year = []
for x,y in zip(years, data_census):
  for item in y[1:]:
    Year.append(x)
    state.append(item[-1])
    medicaid_status.append(item[0])
    medicare_status.append(item[1])
    poverty_ratio.append(item[2])
    education_level.append(item[3])
df_census['Year'] = Year
df_census['State'] = state
df_census['Medicaid_Status'] = medicaid_status
df_census['Medicare_Status'] = medicare_status
df_census['Poverty_Ratio'] = poverty_ratio
df_census['Education_Level'] = education_level

state_dict = { "51": "VA",
      "21": "KY",
      "15": "HI",
      "45": "SC",
      "44": "RI",
      "36": "NY",
      "55": "WI",
      "26": "MI",
      "22": "LA",
      "30": "MT",
      "41": "OR",
      "47": "TN",
      "25": "MA",
      "27": "MN",
      "31": "NE",
      "42": "PA",
      "53": "WA",
      "18": "IN",
      "46": "SD",
      "10": "DE",
      "16": "ID",
      "1": "AL",
      "50": "VT",
      "56": "WY",
      "9": "CT",
      "35": "NM",
      "6": "CA",
      "23": "ME",
      "33": "NH",
      "40": "OK",
      "49": "UT",
      "13": "GA",
      "20": "KS",
      "32": "NV",
      "37": "NC",
      "8": "CO",
      "19": "IA",
      "34": "NJ",
      "28": "MS",
      "38": "ND",
      "5": "AR",
      "54": "WV",
      "11": "DC",
      "12": "FL",
      "29": "MO",
      "2": "AK",
      "39": "OH",
      "4": "AZ",
      "48": "TX",
      "17": "IL",
      "24": "MD"
    }

df_census['State'] = df_census.State.replace(state_dict)

df_census
df_census.to_csv("CensusData2016-20.csv")

