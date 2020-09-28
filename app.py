import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#!/usr/bin/env python
# coding: utf-8


#import sys
#import sys
#!{sys.executable} -m pip install jupyter_plotly_dash
#!{sys.executable} -m pip install pandas
#!{sys.executable} -m pip install plotly
#!{sys.executable} -m pip install dash
#!{sys.executable} -m pip install gunicorn


#from jupyter_plotly_dash import JupyterDash
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_excel('FILLEDStateResults18ED-2018-0616.xls', sheet_name = 'ALL STATES')

allSubindeces=['Final Index', 'Government And Fiscal  Policy Subindex', 'Security Subindex', 
            'Infrastructure Subindex', 'Human Resources Subindex', 'Technology Subindex', 
            'Business Incubation Subindex', 'Openness Subindex',
            'Environmental Policy Subindex']

us_states= {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

stateAbbrev = list(us_states.values())

stateNames = list(us_states.keys())
stateNamesUpper = list(x.upper() for x in stateNames)

#df_NoRanks is a dataframe that contains only the normalized values for the 50 U.S. states
df_NoRanks = df[stateNamesUpper]


#df_Ranks is a dataframe that contains only the rankings of each state for their subindeces
df_Ranks = df.filter(regex='Unnamed')
del df_Ranks['Unnamed: 0']
for x in df_Ranks.columns:
    df_Ranks.columns = stateNamesUpper

#stateIndices populates a dictionary of state names and their column numbers
stateIndices=dict()
column=0
for v in stateNames:
    stateIndices[v]=column
    column+=1


#df_vars is the first column in the dataframe which contains the names of the variables
df_vars = df['Unnamed: 0'] 
varNames = df_vars.values.tolist()
varNames
varNamesCapitalized = list(x.title() for x in varNames)

#variables populates a dictionary of variable names and their row numbers
variables=dict()
row=0
for x in varNamesCapitalized:
    variables[x]=row
    row+=1
variableNames = list(variables.keys())

#----------------------------------------------------------

df2 = pd.read_csv('BHI-SCI-2006-2018Topline.csv',skiprows=[0,1])

dates=['x',2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006]
df2_Ranks=df2.filter(regex='Unnamed')
for x in df2_Ranks.columns:
    df2_Ranks.columns = dates
df2_Ranks=df2_Ranks.iloc[1:]
del df2_Ranks['x']
dates.pop(0)

df2_NoRanks=df2[df2.columns[1::2]]
df2_NoRanks=df2_NoRanks.iloc[1:]
    

#----------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

image_filename = 'TEST3-4-2019.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

colorList = ['darkred','indianred','#F59905','#FEC477','dimgrey','grey']

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'display':'block','margin-left': 'auto','margin-right':'auto'}),
                html.Br()
            ],
        ),

        html.Div(
            id = 'heading',
            children =[
                html.H1(children='2018 U.S. State Competitiveness Index'),
                html.H4(children = 'Benjamin Magid (Benny) 2020'),
                html.Br()
            ],
            style = {'text-align':'center'}
        ),
        
        html.Div(
            id='top',
            children=[
                html.Div(
                    id='dropdownMenu',
                    children=[
                        html.Div(
                            children=[
                                html.P(children='Select a Variable or Subindex to view below:')
                            ],
                            style={'margin-left':'20%'}
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id='firstVarsDropdown',
                                    options=[{'label': s,'value':s} for s in varNamesCapitalized],
                                    multi=False,
                                    placeholder = 'Start typing to select a variable',
                                    value='Final Index'
                                )
                            ],
                            style={'width':'60%','text-align':'center', 'margin-left': 'auto','margin-right':'auto'}
                        )
                    ],
                    style={'padding':'2px'}
                ),
                html.Div(
                    id='nationwide-visuals',
                    children=[
                        html.Div(
                            id='top-left-map',
                            children=[
                                html.Div(id='output-map'),
                            ],
                            style = {'width':'50%','margin-left':'0', 'margin-right':'auto','display':'inline-block'}
                        ),
                        html.Div(
                            id='top-right-table',
                            children=[
                                html.Div(id='output-table')
                            ],
                            style = {'width': '43%', 'margin-left':'auto', 'margin-right':'0','display':'inline-block'}
                        ),
                    ]
                )
            ]
        ),
        
        html.Div(
            id = 'mid',
            children = [
                html.Div(
                    id = 'comparativeDropdownMenus',
                    children = [
                        html.Div(
                            children=[
                                html.P(children='Pick the State(s) to compare on the two graphs below:')
                            ],
                            style={'margin-left':'20%'}
                        ),
                        html.Div(
                            children = [
                                dcc.Dropdown(
                                    id = 'stateDropdown',
                                    options=[{'label': s, 'value': s} for s in stateNames],
                                    multi=True,
                                    placeholder = 'Start typing to select a state',
                                    value=stateNames[0:4]
                                )
                            ],
                            style = {'width':'60%','margin-left': 'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            id='middle-graph',
                            children= [
                                html.Div(id='timeseries')
                            ]
                        ),
                        html.Div(
                            children = [
                                html.P(children='Pick the Subindeces / Variables to compare on the graph below: '+
                                        '(The Final Index and 8 Subindeces are selected by default)'),
                                html.P(children=''),
                                dcc.Dropdown(
                                    id = 'variableDropdown',
                                    options=[{'label': s, 'value': s} for s in varNamesCapitalized],
                                    multi=True,
                                    placeholder = 'Start typing to select a variable',
                                    value=allSubindeces
                                )
                            ],
                            style = {'width': '75%','margin-left': 'auto','margin-right':'auto'}
                        )
                    ]
                ),
                html.Div(
                    id = 'bottom-graph',
                    children=[
                        html.Div(id='output-graph')
                    ]
                )
            ]
        ),
   ],
    style = {'font-family':'Arial, Helvetica, sans-serif'}
)

#----------------------------------------------------------


#Multi State Graph
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='stateDropdown', component_property='value'),
     Input(component_id='variableDropdown', component_property='value')]
)
def update_graph(listOfSelectedStates, listOfSelectedVariables):
    listOfRows = [variables.get(x) for x in listOfSelectedVariables]
    listOfStates = [stateIndices.get(x) for x in listOfSelectedStates]
    colorCount=-1
    stateCount=0
    
    fig = go.Figure()
    for s in listOfSelectedStates:
        currColumn = listOfStates[stateCount]
        if (colorCount==len(colorList)-1):
            colorCount=0
        else:
            colorCount+=1
        fig.add_trace(
            go.Bar(
                x=listOfSelectedVariables,
                y=df_NoRanks.iloc[listOfRows,currColumn],
                marker_color=colorList[colorCount],
                customdata=df_Ranks.iloc[listOfRows,currColumn],
                name = s,
                hovertemplate =
                'Index: <b>%{x}</b>'+
                '<br>Rank: %{customdata}'+
                '<br>Index: %{y:.2f}'
            )
        )
        stateCount+=1
    fig.update_layout(
        yaxis_title = 'Normalized Values',
        title = "U.S. States vs. 2018 Competitiveness Normalized Indeces",
        font = {'family': 'Arial, Helvetica, sans-serif'}
    )
    return dcc.Graph(figure = fig)

#Choropleth map
@app.callback(
    Output(component_id='output-map', component_property='children'),
    [Input(component_id='firstVarsDropdown', component_property='value')]
)
def update_map(selectedVar):
    currSubindex = selectedVar
    currRow = variables.get(currSubindex)
    fig = go.Figure(data = go.Choropleth(
        locations = stateAbbrev,
        z = df_NoRanks.iloc[currRow], # z = list of normalized values for the first row in given range of rows,
        locationmode = 'USA-states',
        colorscale = [[0.0,"#FFF"],[1.0,"#F59905"]],
        customdata = df_Ranks.iloc[currRow],
        text = ['{}'.format(stateNames[i]) for i in range(50)],
        hovertemplate =
        'State: <b>%{text}</b>'+
        '<br>Rank: %{customdata}'+
        '<br>Index: %{z:.2f}'+
        '<extra></extra>'
    ))
    fig.update_layout(
        geo_scope='usa',
        font = {'family': 'Arial, Helvetica, sans-serif'},
    )
    return dcc.Graph(figure = fig)

#DataTable output
@app.callback(
    Output(component_id='output-table', component_property='children'),
    [Input(component_id='firstVarsDropdown', component_property='value')]
)
def update_table(selectedSubindex):
    currSubindex = selectedSubindex
    currRow = variables.get(currSubindex)

    croppedData = pd.DataFrame(list(zip(df_Ranks.iloc[currRow],stateNames,df_NoRanks.iloc[currRow])),
                 columns=['Rank','State','Value'])

    sortedCropped = croppedData.sort_values(by=['Rank'])

    dataTable= go.Figure(data=[go.Table(
        columnwidth=[1,4,2],
        header=dict(values=list(sortedCropped.columns),
                   align='left',
                   fill_color = '#840029',
                   font_color='white'),
        cells=dict(values=[sortedCropped.Rank, sortedCropped.State, sortedCropped.Value],
                  align=['center','left','left'],
                  format = [[None],[None],['.2f']])
    )])
    
    return dcc.Graph(figure=dataTable)

#Timeseries
@app.callback(
    Output(component_id='timeseries', component_property='children'),
    [Input(component_id='stateDropdown', component_property='value')]
)

def update_timeseries(listOfSelectedStates):
    listOfRows = [stateIndices.get(x) for x in listOfSelectedStates]
    fig = go.Figure()
    colorCount=-1
    stateCount = 0
    
    for s in listOfSelectedStates:
        currRow = listOfRows[stateCount]
        if (colorCount==len(colorList)-1):
            colorCount=0
        else:
            colorCount+=1
        name = s
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=df2_NoRanks.iloc[currRow],
                mode='markers+lines',
                customdata = df2_Ranks.iloc[currRow],
                name = name,
                meta=[name],
                hovertemplate =
                '%{meta}'+
                '<br>Rank: %{customdata}'+
                '<br>Overall Index: %{y:.2f}'+
                '<extra></extra>',
            marker_color= colorList[colorCount]
        ))
        stateCount+=1

    fig.update_layout(
        title={
             'text': "State Overall Ranking from 2006-2018"
        },
        xaxis_title = "Year",
        hovermode="x",
        font = {'family': 'Arial, Helvetica, sans-serif'},
        yaxis_title = "Overall Index"
    )
        
        
    return dcc.Graph(figure = fig)

if __name__ == '__main__':
    app.run_server(debug=True)