from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

df = pd.read_csv('whalesWithClusters.csv')

app = Dash(__name__)
server = app.server #for render.com

app.layout = html.Div([
    html.H1(children='Cetaceans of the Azores', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content'),
    dcc.Dropdown(np.append(df.scientificname.unique(), 'None'), 'None', id='dropdown-selection'),
    dcc.Dropdown(np.append(df.year.unique(), 'None'), 'None', id='test'),

])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('test', 'value'),
)
def update_graph(species, year):
    print(species)


    dff = df.sort_values('year')
    dff.loc[:, 'cluster_str']  = dff.loc[:,'cluster'].astype(str)
    dff.loc[:, 'year_str']  = dff.loc[:,'year'].astype(str)

    if species != 'None':
        dff = dff[dff.scientificname==species]

    if year != 'None':
        print(year, dff.year.unique())
        dff = dff[df.year==int(year)]
    print(dff.shape)
    #dff.loc[:, 'cluster_str']  = dff.loc[:,'cluster'].astype(str)

    fig = px.scatter_mapbox(dff,
                            lat='decimallatitude', lon='decimallongitude',
                            color='cluster_str',
                            color_discrete_sequence=px.colors.qualitative.Alphabet,
                            #animation_frame='year',
                            size='depht_positive',
                            zoom=5,
                            height=800,
                            #width=1650
                            )


    #fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)
    fig.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=TOKEN)
    #fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)

    # fig.update_layout(
    #     legend=dict(
    #         x=0,
    #         y=1,
    #         traceorder="reversed",
    #         title_font_family="Times New Roman",
    #         font=dict(
    #             family="Courier",
    #             size=12,
    #             color="black"
    #         ),
    #         bgcolor="LightSteelBlue",
    #         bordercolor="Black",
    #         borderwidth=2
    #     )
    # )

    return fig
   # return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)