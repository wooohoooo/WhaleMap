from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')


app = Dash(__name__)
server = app.server #for render.com

df = pd.read_csv('whalesWithClusters.csv')
df_tuna = pd.read_csv('Tuna.csv')

app.layout = html.Div([
    html.H1(children='Cetaceans of the Azores', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content'),
    html.H3(children='Genus', style={'textAlign': 'left'}),
    dcc.Dropdown(np.append(df.scientificname.unique(), 'None'), 'None', id='dropdown-selection'),
    html.H3(children='year', style={'textAlign': 'left'}),
    dcc.Dropdown(np.append(df.year.unique(), 'None'), 'None', id='test'),
    html.H3(children='Show Tuna', style={'textAlign': 'left'}),
    dcc.Dropdown(['True','False'],'True', id='tuna'),

])




@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('test', 'value'),
    Input('tuna', 'value'),
)



def update_graph(species, year, tuna):#, df_tuna=df_tuna):
    global df_tuna
    print(species)


    dff = df.sort_values('year')
    dff_tuna = df_tuna.sort_values('year')

    dff.loc[:, 'cluster_str']  = dff.loc[:,'cluster'].astype(str)
    dff.loc[:, 'year_str']  = dff.loc[:,'year'].astype(str)

    if species != 'None':
        dff = dff[dff.scientificname==species]
    if year != 'None':

        print(year, dff.year.unique())
        dff = dff[dff.year==int(year)]
        dff_tuna = df_tuna[df_tuna.year==int(year)]
        print(dff_tuna.shape)


    print(dff.shape)

    fig = px.scatter_mapbox(dff,
                            lat='decimallatitude', lon='decimallongitude',
                            color='cluster_str',
                            color_discrete_sequence=px.colors.qualitative.G10,
                            #animation_frame='year',
                            size='depht_positive',
                            zoom=4,
                            height=700,
                            #width=1650
                            hover_data=['scientificname','year']
                            )


    print('tuna',tuna)
    if tuna == 'True':
        # if year != 'None':
        #     df_tuna = df_tuna[df_tuna.year == int(year)]

        # if year != 'None':
        #     df_tuna = df_tuna[df_tuna.year == int(year)]
        #     print('test')


        fig2 = px.scatter_mapbox(dff_tuna,
                                 lat='decimallatitude', lon='decimallongitude',
                                 zoom=4,
                                 opacity=.25,
                                 color='scientificname',
                                 color_discrete_sequence=px.colors.qualitative.G10[6:])
        fig.add_trace(fig2.data[0])  # adds the line trace to the first figure

    fig.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=TOKEN)
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)

    return fig

if __name__ == '__main__':
    app.run(debug=True)
