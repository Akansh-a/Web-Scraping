#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:54:58 2020

@author: akansha
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
url = "http://forem.co.in/members.html"
# Make a GET request to fetch the raw HTML content
html_content = uReq(url)

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
#print(soup.prettify()) # print the parsed data of html

from collections import defaultdict
data = {}
table1 = soup.find("table", attrs={"class": "table"})
table_data = table1.findAll("tr")  # contains 71 rows
table_data[1]
# Get all the headings of Lists
headings = []
for th in table_data[0].findAll("th"):
    # remove any newlines and extra spaces from left and right
    headings.append(th.text.replace('\n', ' '))

t_headers = []

for i in range(len(table_data)):
    for th in table_data[i].findAll("td"):
        # remove any newlines and extra spaces from left and right
        t_headers.append(th.text.replace('\n', ' ').strip())
        
res=[]
for i in range(0,len(t_headers),len(headings)):
    res.append(t_headers[i:i+5])
temp = defaultdict(list)
for i in range(len(res)):
    class_list = headings
    id_list = res[i]
    for key, value in zip(class_list, id_list):
        temp[key].append(value)

# print the contents using zip format. 
res=[]
for each_row in zip(*([i] + (j) for i, j in temp.items())): 
      res.append((*each_row,))
    
# Using pandas to clean data    
import pandas as pd
df=pd.DataFrame(res)
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header

data=df
# dropping null value columns to avoid errors 
data.dropna(inplace = True) 
#Renaming old column names
data["Organization Name"]=data["Event Company"]
data["Contact Person Name"]=data["Name of Member"]
# Dropping old columns 
data.drop(columns =["Event Company"], inplace = True) 
data.drop(columns =["Name of Member"], inplace = True) 
# new data frame with split value columns 
newphone = data["Contact No."].str.split("/", n = 1, expand = True)  
# making separate column from new data frame 
data["Phone - Mobile"]= newphone[0] 
data["Phone 2- Mobile"]= newphone[1] 
# Dropping old Contact No. column 
data.drop(columns =["Contact No."], inplace = True) 

# new data frame with split value columns 
newEmail = data["Email ID"].str.split(",", n = 1, expand = True)  
# making separate column from new data frame 
data["E-mail 1"]= newEmail[0] 
data["E-mail 2"]= newEmail[1] 
# Dropping old Email ID columns 
data.drop(columns =["Email ID"], inplace = True) 
# Data frame to excel  
df.to_excel('Members.xlsx', index = False, header=True) 
