from flask import Flask, render_template, redirect, url_for, flash, request
import numpy as np
import pandas as pd
import plotly.express as px
from flask_bootstrap import Bootstrap
from GraphClass import Graphs,graphs_toshow_list
#import matplotlib.pyplot as plt
#import seaborn as sns

app = Flask(__name__)
Bootstrap(app)
graph= Graphs()


pd.options.display.float_format = '{:,.2f}'.format
df_data = pd.read_csv('./static/mission_launches_country.csv')
df_data['Price'] = df_data['Price'].fillna(0, inplace=False)
df_data['Year']  = pd.to_datetime(df_data['Date'],utc=True).dt.year

# Preparing DataFrames GRAPH-001
df_failures_bycountry = df_data[df_data['Mission_Status'].str.find('Failure') >-1]
df_failures_bycountry = df_failures_bycountry.groupby(['Country'])['Country'].count()
df_failures_bycountry = pd.DataFrame(df_failures_bycountry)
df_failures_bycountry = df_failures_bycountry.rename(columns={'Country':'Failure_Count'})
df_failures_bycountry = df_failures_bycountry.reset_index()

# Preparin DataFrame GRAPH-002
df_launches_Success  = df_data[(df_data['Mission_Status']=='Success')].groupby(['Year'])['Year'].count()
df_launches_Failures = df_data[(df_data['Mission_Status']!='Success')].groupby(['Year'])['Year'].count()

# Preparing DataFrame GRAPH-003
df_sunburst = df_data.groupby(['Country','Organisation','Mission_Status'])['Mission_Status'].count()
df_sunburst = pd.DataFrame(df_sunburst)
df_sunburst = df_sunburst.rename(columns={'Mission_Status':'Mission_Status_Count'})
df_sunburst = df_sunburst.reset_index()

df_data['Price'] = df_data['Price'].fillna(0,inplace=False)
df_data['Price'] = pd.to_numeric(df_data['Price'],errors='coerce')

df_data_price = df_data.groupby(['Year'])['Price'].mean()
df_data_price = pd.DataFrame(df_data_price)
df_data_price = df_data_price.reset_index()
df_data_price = df_data_price.sort_values(by=['Year'], ascending=True)

df_data_usa_ussr = df_data[df_data['Country'].isin(['USA','RUS'])] #df_data[df_data['Country'] == 'USA']
df_data_usa_ussr = df_data_usa_ussr.groupby(['Year','Country'])['Country'].count()
df_data_usa_ussr = pd.DataFrame(df_data_usa_ussr)
df_data_usa_ussr = df_data_usa_ussr.rename(columns={'Country':'Count_Launches'})
df_data_usa_ussr = df_data_usa_ussr.reset_index()

df_launches_by_country = df_data.groupby(['Country'])['Country'].count()
df_launches_by_country = pd.DataFrame(df_launches_by_country)
df_launches_by_country = df_launches_by_country.rename(columns={'Country':'Launches number'})
df_launches_by_country = df_launches_by_country.reset_index()


#print(df_data_usa_ussr.head(4))

## Building Graphs
graph.mth_graph_donuts(pLabels      =df_failures_bycountry['Failure_Count'].index
                        ,pValues    =df_failures_bycountry.Failure_Count
                        ,pNames     =df_failures_bycountry['Country']
                        ,pHole      =0.6
                        ,pWidth     =900
                       ,pHeight    =500
                        ,pTitle     ="Missions Failures"
                        ,pFilename  ='graph-001.html'
                        )

graph.mth_graph_compare_two_variables(pDf_data01   = df_launches_Success
                                      ,pDf_data02  = df_launches_Failures
                                      ,pFilename   ='graph-002.png'
                                      ,pWidth      =900
                                      ,pHeight     =500
                                     )

graph.mth_graph_sunburst(pDf_sunburst   =df_sunburst
                         ,pFilename     ='graph-003.html'
                         ,pWidth        =900
                         ,pHeight       =500
                         ,pPath         =['Country', 'Organisation', 'Mission_Status']
                         ,pValues       ='Mission_Status_Count'
                         ,pHover_data   =['Country']
                         )

graph.mth_graph_line(pDf_data   =df_data_price
                     ,pX_collumn='Year'
                     ,pY_collumn='Price'
                     ,pWidth    =900
                     ,pHeight   =500
                     ,pFilename ='graph-004.html'
                     ,pTitle    ='Variation in the cost of space launches over time'
                     ,pColor    =''
                     )

graph.mth_graph_line(pDf_data   =df_data_usa_ussr
                     ,pX_collumn='Year'
                     ,pY_collumn='Count_Launches'
                     ,pWidth    =900
                     ,pHeight   =500
                     ,pFilename ='graph-005.html'
                     ,pTitle    ='Cold War Space Race: USA vs USSR'
                     ,pColor    ='Country'
                     )

graph.mth_graph_choropleth(pDf_data         =df_launches_by_country
                           ,pLocations      ='Country'
                           ,pColor          ='Launches number'
                           ,pFilename       ='graph-006.html'
                           ,pWidth          =900
                           ,pHeight         =500
                           ,pTitle          ='Number of Launches by Country'
                           )
#print(graphs_toshow_list)
#print(graphs_toshow_list[2]['graphname'])
#print(graphs_toshow_list[2]['dimention'][0])

@app.route("/")
def fn_home():
    return render_template("index.html"
                           ,graphs_web_list =graphs_toshow_list
                           ,width_web        =450
                           ,height_web       =450
                           )

if __name__ == '__main__':
    app.run(debug=True,port=5001)
