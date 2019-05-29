import pandas as pd
import numpy as np
import re
import csv
import openpyxl
from urllib.request import urlopen
from bs4 import BeautifulSoup

url= "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"        #url to open wikipedia of US cities by population
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
type(soup)

title = soup.title                                                                     #Webpage title
#print(title)

text = soup.get_text()               
#print(soup.text)

all_tables = soup.find_all("table")                                                    #Find tables in the webpage
#print(all_tables)

links = soup.find_all('a')                                                             #Find links in the webpage
#print(links)

rows = soup.find_all('tr')                                                             #Find table rows in webage
#print(rows[:2])

#for row in rows:                                                                       #Iterate through row and print cells(Uncomment to view)
    #row_td = row.find_all('td')
    #print(row_td)
    #type(row_td)

    #str_cells = str(row_td) 
    #cleantext = BeautifulSoup(str_cells,"lxml").get_text()
    #print(cleantext)

list_rows = []

#####Cleaning of data
for row in rows:                                                                        #Iterate through rows and extract text without HTML tags 
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '', str_cells))
    list_rows.append(clean2)                                                            #Append to list

    #print(clean2)
    #type(clean2)

df = pd.DataFrame(list_rows)                                                            #Convert to DataFrame
first_100 = df.head(100)
#print(first_100)

df1 = df[0].str.split('\n,',expand=True)
first_100_1 = df1.head(100)
#print(first_100_1)

df1[0] = df1[0].str.strip('[')
first_100_2 = df1.head(100)
#print(first_100_2)
#print(df1.iloc[20:334])
df1 =  df1.iloc[20:334]
col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str,"lxml").get_text()
all_header.append(cleantext2)
#print(all_header)

df2 = pd.DataFrame(all_header)
all_header = df2.head()
#print(all_header)

df3 = df2[0].str.split('\n,',expand = True)
all_header = df3.head()
#print(all_header)
#print(df3.iloc[:,1:9])
df3 = df3.iloc[0:,1:10]


frames = [df3, df1]
df4 = pd.concat(frames)                                                                 #Concatenate header and rest of the data

df4 = df4.iloc[0:,0:9]
df5 = df4.rename(columns=df4.iloc[0])
df5.drop(df5.head(1).index, inplace=True)

final = df5.head()
#print(final)

list_url = []

# Clean city name data and add url of cities to table
for i in range(0,314):
    regex = '\[.*?\]'
    df5.iloc[i,1] = re.sub(regex,'',df5.iloc[i,1])
    df5.iloc[i,1] = re.sub('[^A-Za-z0-9]+', '_', df5.iloc[i,1])
    df5.iloc[i,1] = (df5.iloc[i,1])[1:]
    #print(df5.iloc[i,1])
    if((df5.iloc[i,1]) == "Washington_D_C_"):
       (df5.iloc[i,1]) = "Washington,_D.C."
    url2 = "https://en.wikipedia.org/wiki/"+(df5.iloc[i,1])                             #Create URL for cities
    list_url.append(url2)

df5.insert(9,"URL",list_url,True)

for i in range(0,314):
    regex = '\[.*?\]'
    df5.iloc[i,2] = re.sub(regex,'',df5.iloc[i,2])
    df5.iloc[i,2] = re.sub('[^A-Za-z0-9]+', '', df5.iloc[i,2])
    
for i in range(0,314):
    df5.iloc[i,5] = df5.iloc[i,5].replace(" âˆ’","")
        
    
    
export_csv = df5.to_csv('out.csv',index = False)                                        #Save csv file
export_excel = df5.to_excel('out.xlsx',index = False)                                   #Save Excel file

df10 = pd.read_csv('out.csv')
#print(df10)

