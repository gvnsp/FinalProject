from ast import While
from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import matplotlib
import matplotlib.pyplot
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import json
from databaseandtree import *

f = open('tree.json')
tree = json.load(f)


def run_program():
    states = userinputforstate
    years = userinputforyear
    prompt1 = userinputformedicareormedicaid
    prompts = userinputformedicareormedicaidstatus
    Household_Size = userinputforhouseholdsize
    user = tree[states][years][prompt1][prompts][Household_Size]
    return states, years, user

#-------------- INTERACTION 1 ----------------------#

def interaction1(thelist):
    emptylist = []
    for item in thelist:
        item = item[1:]
    for item in thelist[1:]:
        emptylist.append(item[1])

    matplotlib.pyplot.hist(emptylist)
    matplotlib.pyplot.show()


# #-------------- INTERACTION 2 ---------------------- #

def interaction2(year, thelist):
    userinput = year
    Highestincomelevel = {2016: 51120, 2017: 51670, 2018: 52980, 2019: 54310, 2020: 55150}

    er = thelist[0]
    s = [str(integer) for integer in er]
    a_string = "".join(s)
    res = int(a_string)

    x = [0]
    y = [res,Highestincomelevel[int(userinput)]]
    fig, ax = plt.subplots()
    width = 0.75
    ind = np.arange(len(y))
    ax.barh(ind, y, width, color = "green")
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v),
                color = 'blue', fontweight = 'bold')
    plt.show()

# #--------------INTERACTION 3 ---------------------- #

def interaction3(state, year):
    state = state
    answer = data1_access(state,int(year))
    listyui  =[]
    for itemx in answer:
        for item1 in itemx:
            t = item1
            listyui.append(t)

    # print(listyui)
    x = [0]
    y = listyui
    fig, ax = plt.subplots()
    width = 0.50
    ind = np.arange(1, len(y)+1)
    #print(ind)
    ax.barh(ind, y, width, color = "yellow")
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v),
                color = 'blue', fontweight = 'bold')
    plt.show()

# #------------------------------------- #

flag = True
while flag == True:
    print('We will check the poverty ratio and income levels based on state,year and medicare or medicaid status:  ')

    time.sleep(1)

    state_list = ['MI', 'CA', 'WA']
    state_flag = True
    while state_flag == True:
        userinputforstate = input('Please type the State name in abrrevaited form:  ')
        if userinputforstate in state_list:
            state_flag=False
        else:
            print('Please select a valid input')
            continue

    time.sleep(1)

    year_list = ['2016','2017','2018','2019','2020']
    year_flag = True
    while year_flag == True:
        userinputforyear = input('Please select an year between 2016 - 2020:  ')
        if userinputforyear in year_list:
            year_flag=False
        else:
            print('Please select a valid input')
            continue

    time.sleep(1)

    medicareormedicaid_list = ['Medicare', 'Medicaid']
    medicareormedicaidflag = True
    while medicareormedicaidflag == True:
        userinputformedicareormedicaid = input('Please select Medicaid or Medicare:  ')
        if userinputformedicareormedicaid in medicareormedicaid_list:
            medicareormedicaidflag = False
        else:
            print('Please select a valid input')
            continue

    time.sleep(1)


    medicareormedicaidstatus_list = ['1','2']
    medicareormedicaidstatus_flag = True
    while medicareormedicaidstatus_flag == True:
        userinputformedicareormedicaidstatus = input('Please enter 1 or 2, where 1 is yes,and 2 is no:  ')
        if userinputformedicareormedicaidstatus in medicareormedicaidstatus_list:
            medicareormedicaidstatus_flag=False
        else:
            print('Please select a valid input')
            continue

    time.sleep(1)


    householdsize_list = ['1','2','3','4','5','6','7','8']
    householdsize_flag = True
    while householdsize_flag == True:
        userinputforhouseholdsize = input('Please select a number between 1 -8  based on householdsize:  ')
        if userinputforhouseholdsize in householdsize_list:
            householdsize_flag = False
        else:
            print('Please select a valid input')
            continue

    time.sleep(1)

    state,year,thelist = run_program()


    time.sleep(2)

    userinput1 = input(f'Do you want to see the poverty ratio for {state} in the year{year} type y for yes or n for no?: ')
    if userinput1 == 'y':

        time.sleep(1)
        print("Povert Ratio: 4: 150 percent and above the low-income level")
        time.sleep(1)
        print("Povert Ratio: 3: 125 - 149 percent of the low-income level")
        time.sleep(1)
        print("Povert Ratio: 2: 100 - 124 percent of the low-income level")
        time.sleep(1)
        print("Povert Ratio: 1: Below low-income level")
        time.sleep(1)

        interaction1(thelist)
    else:

        pass

    time.sleep(2)

    userinput2 = input(f'Do you want to see the difference between highest income level in the U.S to income level in {state} in {year} ?: type y for yes or n for no')

    if userinput2 == 'y':
        time.sleep(1)
        print("Graphs are based on data in the dataset and your inputs")
        interaction2(year,thelist)

    else:
        pass

    time.sleep(2)

    userinput3 = input(f'Do you want to see income levels based on family size for {state} in {year}?: type y for yes or n for no ')
    if userinput3 == 'y':
        interaction3(state,year)
    else:
        pass

    userinput4 = input('Do you want to continue or exit? please type continue to continue or exit to exit:')

    time.sleep(2)

    if userinput4 == 'exit':
        print('Thank you!')
        flag = False
    else:
        continue



# print(user)


