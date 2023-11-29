import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash_extensions.javascript import assign

from dash.dependencies import Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx

#import plotly.express as px
from plotly import graph_objs as go
#from plotly.tools import make_subplots
from plotly.subplots import make_subplots
#from datetime import datetime as dt

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Tripadvisor restaurants NI"
server = app.server

df = pd.read_csv('csv_old_clean/NI_joined.csv')
#filter out records with coordinates outside NI
df = df.loc[(df['latitude'] > 54) & (df['longitude'] < -5.4) ]

df['color'] = df['status'].map({'in rating':'green', 'closed':'red', 'redirect':'yellow'})

restaurants = []
for i in range(len(df)):
    restaurants.append(dict(popup=df['restaurant_name'].iloc[i], color=df['color'].iloc[i],
                            lat=df['latitude'].iloc[i], lon=df['longitude'].iloc[i]))

geo_data = dlx.dicts_to_geojson(restaurants)
color_options = [{"label": "Color by Tripadvisor Status", "value": "status"},
                 {"label": "Color by Claimed status", "value": "claimed"},
                 {"label": "Color by Review Activity", "value": "is_active"},
                 {"label": "Color by Price Level", "value": "price_level"}]

status_options = [{"label": "In Rating", "value": "in rating"},
                  {"label": "Redirect", "value": "redirect"},
                  {"label": "Closed", "value": "closed"},
                  {"label": "Any Status", "value": "All"},]

'''
claimed_options = [{"label": "Claimed", "value": 1},
                   {"label": "Unclaimed", "value": 0},
                   {"label": "Both Claimed and Unclaimed", "value": -1}]

active_options = [{"label": "Long Inactive", "value": 0},
                  {"label": "Recently Inactive", "value": 1},
                  {"label": "Active", "value": 2},
                  {"label": "Both Active and Inactive", "value": -1}]

price_level_options = [{"label": "€", "value": 0},
                       {"label": "€€-€€€", "value": 1},
                       {"label": "€€€€", "value": 2},
                       {"label": "All Price Levels", "value": -1}]
'''
claimed_options = [{"label": "Claimed", "value": "Claimed"},
                   {"label": "Unclaimed", "value": "Unclaimed"},
                   {"label": "Both Claimed and Unclaimed", "value": "All"}]

active_options = [{"label": "Long Inactive", "value": "long_inactive"},
                  {"label": "Recently Inactive", "value": "recently_inactive"},
                  {"label": "Active", "value": "active"},
                  {"label": "Both Active and Inactive", "value": "All"}]

price_level_options = [{"label": "No data", "value": "No data"},
                       {"label": "€", "value": "€"},
                       {"label": "€€-€€€", "value": "€€-€€€"},
                       {"label": "€€€€", "value": "€€€€"},
                       {"label": "All Price Levels", "value": "All"}]

vegetarian_options = [{"label": "Vegetarian Options", "value": 'Y'},
                       {"label": "No Vegetarian Options", "value": 'N'},
                       {"label": "All Restraunts by Vegetarian Options", "value": 'All'}]

vegan_options = [{"label": "Vegan Options", "value": 'Y'},
                 {"label": "No Vegan Options", "value": 'N'},
                 {"label": "All Restraunts by Vegan Options", "value": 'All'}]

gluten_free_options = [{"label": "Gluten Free Options", "value": 'Y'},
                       {"label": "No Gluten Free Options", "value": 'N'},
                       {"label": "All Restraunts by Gluten Free Options", "value": 'All'}]

point_to_layer = assign("""function(feature, latlng, context){
    const {circleOptions, color} = context.hideout;
    circleOptions.fillColor = feature.properties.color;  // set color based on color prop
    return L.circleMarker(latlng, circleOptions);  // render a simple circle marker
}""")


#fig_bar = go.Figure()
#fig_bar.add_trace(go.Bar(
#    x=df_agg["status"],
#    y=df_agg["count"],
#    name="status_count",
#    marker_color='#0d0887'
#))
#, marker_color='#0d0887'

'''
df_agg = df['status'].value_counts().reset_index()
df_agg['precent'] = df_agg['count']/df_agg['count'].sum()

df_agg2 = df['is_active'].value_counts().reset_index()
df_agg2['precent'] = df_agg2['count']/df_agg2['count'].sum()

#fig_bar = go.Figure()
fig_bar = make_subplots(rows=1, cols=2, shared_yaxes=True)
trace_rm1 = go.Bar(x = df_agg['status'])
trace_rm2 = go.Bar(x = df_agg['precent'])
fig_bar.append_trace(go.Bar(
    x=df_agg['status'],
    y=df_agg['precent'] ,
    name='All Restaurants',
    marker_color='#0d0887'
),1,1)
fig_bar.append_trace(go.Bar(
    x=df_agg['status'],
    y=df_agg['precent'],
    name='Filtered Restaurants',
    marker_color='lightsalmon'
),1,1)
fig_bar.append_trace(go.Bar(
    x=df_agg2['is_active'],
    y=df_agg2['precent'] ,
    showlegend=False,
    marker_color='#0d0887'
),1,2)
fig_bar.append_trace(go.Bar(
    x=df_agg2['is_active'],
    y=df_agg2['precent'],
    showlegend=False,
    marker_color='lightsalmon'
),1,2)
'''
def generate_bar_charts(df_all, df_sel):
    def generate_bar(df_to_agg, col_to_agg, color, legend=None):
        df_agg = df_to_agg[col_to_agg].value_counts().reset_index()
        df_agg['precent'] = df_agg['count'] / df_agg['count'].sum()
        if legend:
            g_bar = go.Bar(
                x=df_agg[col_to_agg],
                y=df_agg['precent'] ,
                name=legend,
                marker_color=color
                )
        else:
            g_bar = go.Bar(
                x=df_agg[col_to_agg],
                y=df_agg['precent'] ,
                showlegend=False,
                marker_color=color
                )
        return g_bar

    fig = make_subplots(rows=1, cols=4, shared_yaxes=True)
    fig.append_trace(generate_bar(df_all, 'status', '#0d0887', 'All Restaurants'), 1, 1)
    fig.append_trace(generate_bar(df_sel, 'status', 'lightsalmon', 'Filtered Restaurants'), 1, 1)
    fig.append_trace(generate_bar(df_all, 'is_active', '#0d0887'), 1, 2)
    fig.append_trace(generate_bar(df_sel, 'is_active', 'lightsalmon'), 1, 2)
    fig.append_trace(generate_bar(df_all, 'claimed', '#0d0887'), 1, 3)
    fig.append_trace(generate_bar(df_sel, 'claimed', 'lightsalmon'), 1, 3)
    fig.append_trace(generate_bar(df_all, 'price_level', '#0d0887'), 1, 4)
    fig.append_trace(generate_bar(df_sel, 'price_level', 'lightsalmon'), 1, 4)

    #fig.layout.update(go.Layout(barmode='group', xaxis_tickangle=-45))
    #fig.update_scenes(barmode='group')
    fig.layout.update(go.Layout(plot_bgcolor='#323130', paper_bgcolor='#323130', font=dict(color='white')))
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(showgrid=False, linecolor='white')

    return fig

fig_bar = generate_bar_charts(df, df)


def scale_value(x):
    if x <  0:
        return 0
    else:
        return 10**x

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("DASH - Tripadvisor restraunts NI"),
                        html.P(
                            """Select restaurant type."""
                        ),

                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="color-dropdown",
                                            options=color_options,
                                            value='status',
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="status-dropdown",
                                            options=status_options,
                                            value="All",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="claimed-dropdown",
                                            options=claimed_options,
                                            value="All",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="active-dropdown",
                                            options=active_options,
                                            value="All",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="price-level-dropdown",
                                            options=price_level_options,
                                            value="All",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Checklist(['Also show restaurants without rating'],
                                                      ['Also show restaurants without rating'],
                                                      id = 'checkbox-rating-na'),

                                        # Dropdown to select times
                                        dcc.RangeSlider(1, 5, 0.5, value=[1, 5],
                                                        id='user-rating-slider'
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        #dcc.RangeSlider(0, 1000, 200, value=[0, 1000],
                                        #                id='total-reviews-slider'
                                        #                ),
                                        dcc.RangeSlider(-0.1, 3,
                                                        id='total-reviews-slider',
                                                        marks={
                                                            -0.1: '0',
                                                            0: '1',
                                                            1: '10',
                                                            2: '100',
                                                            3: '1000+'
                                                        },
                                                        value=[-0.1, 3],
                                                        dots=False,
                                                        step=0.1,
                                                        updatemode='drag'
                                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="vegetarian-dropdown",
                                            options=vegetarian_options,
                                            value="All",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="vegan-dropdown",
                                            options=vegan_options,
                                            value="All",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="gluten-free-dropdown",
                                            options=gluten_free_options,
                                            value="All",
                                        )
                                    ],
                                ),
                            ], 
                        ),
                        html.P("Total Restaurants: " + str(len(df))),
                        html.P(id="total-restraunts-selection"),
                        #html.P(id="date-value"),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dl.Map(children=[dl.TileLayer(url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png')]
                                        + [dl.GeoJSON(data=geo_data,
                                                      id='map_points',
                                                      pointToLayer=point_to_layer,
                                                      hideout=dict(circleOptions=dict(fillOpacity=1, stroke=False, radius=4),
                                                                   color='red'))],
                               style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"},
                               center=[54.7, -6],
                               zoom=8,
                               id="map"),
                        html.Div(
                            className="row",
                            children=[
                                html.Div([dcc.Graph(id="bar_chart", figure=fig_bar)],
                                         #className="one-third column"
                                         ),
                                #html.Div([dcc.Graph(id="bar_chart2", figure=fig_bar)],
                                #         className="column bg-grey"),
                                ],

                        ),
                    ],
                ),

            ],
        )
    ]
)

#Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map_points", "data"),
    Output("total-restraunts-selection", "children"),
    Output("bar_chart", "figure"),

    [
        Input("color-dropdown", "value"),
        Input("status-dropdown", "value"),
        Input("claimed-dropdown", "value"),
        Input("active-dropdown", "value"),
        Input("price-level-dropdown", "value"),
        Input("checkbox-rating-na", "value"),
        Input("user-rating-slider", "value"),
        Input("total-reviews-slider", "value"),
        Input("vegetarian-dropdown", "value"),
        Input("vegan-dropdown", "value"),
        Input("gluten-free-dropdown", "value"),
    ],
)
def filter_df(color_by, status, claimed, is_active, price_level, rating_checkbox, user_rating, total_reviews,
              vegetarian, vegan, gluten_free):
    if claimed != 'All':
        df_selected = df.loc[df['claimed'] == claimed]
    else:
        df_selected = df.copy()

    if status != 'All':
        df_selected = df_selected.loc[df_selected['status'] == status]

    if is_active != 'All':
        df_selected = df_selected.loc[df_selected['is_active'] == is_active]

    if price_level != 'All':
        df_selected = df_selected.loc[df_selected['price_level'] == price_level]

    if vegetarian != 'All':
        df_selected = df_selected.loc[df_selected['vegetarian_friendly'] == vegetarian]

    if vegan != 'All':
        df_selected = df_selected.loc[df_selected['vegan_options'] == vegan]

    if gluten_free != 'All':
        df_selected = df_selected.loc[df_selected['gluten_free'] == gluten_free]

    if rating_checkbox:
        df_selected = df_selected.loc[(df_selected['avg_rating'] >= user_rating[0]) | (df_selected['avg_rating'].isnull())]
        df_selected = df_selected.loc[(df_selected['avg_rating'] <= user_rating[1]) | (df_selected['avg_rating'].isnull())]
    else:
        df_selected = df_selected.loc[df_selected['avg_rating'] >= user_rating[0]]
        df_selected = df_selected.loc[df_selected['avg_rating'] <= user_rating[1]]

    #if total_reviews[1] == 1000:
    #    df_selected = df_selected.loc[df_selected['total_reviews_count'] >= total_reviews[0]]
    #else:
    #    df_selected = df_selected.loc[df_selected['total_reviews_count'] >= total_reviews[0]]
    #    df_selected = df_selected.loc[df_selected['total_reviews_count'] <= total_reviews[1]]

    if total_reviews[1] == 3:
        df_selected = df_selected.loc[df_selected['total_reviews_count'] >= scale_value(total_reviews[0])]
    else:
        df_selected = df_selected.loc[df_selected['total_reviews_count'] >= scale_value(total_reviews[0])]
        df_selected = df_selected.loc[df_selected['total_reviews_count'] <= scale_value(total_reviews[1])]

    if color_by == 'status':
        df_selected['color'] = df_selected['status'].map({'in rating': 'green', 'closed': 'red', 'redirect': 'yellow'})
    elif color_by == 'is_active':
        df_selected['color'] = df_selected['is_active'].map({'long_inactive': 'red', 'recently_inactive': 'yellow', 'active': 'green'})
    elif color_by == 'claimed':
        df_selected['color'] = df_selected['claimed'].map({'Unclaimed': 'red', 'Claimed': 'green'})
    elif color_by =='price_level':
        df_selected['color'] = df_selected['price_level'].map({'€': 'red', '€€-€€€': 'yellow', '€€€€': 'green', 'No data':'grey'})

    fig_bar = generate_bar_charts(df, df_selected)

    restaurants = []
    for i in range(len(df_selected)):
        restaurants.append(dict(popup=df_selected['restaurant_name'].iloc[i], color=df_selected['color'].iloc[i],
                                lat=df_selected['latitude'].iloc[i], lon=df_selected['longitude'].iloc[i]))

    geo_data = dlx.dicts_to_geojson(restaurants)
    selected_restraunt_string = "Restaurants Selected: {:,d}".format(
        len(df_selected) )
    return geo_data, selected_restraunt_string, fig_bar


if __name__ == '__main__':
    app.run_server()