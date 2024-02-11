# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

import urllib.parse
# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Car'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Information Home Page", href ='/information/information_main', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Cars')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        # html.Div(  # Add Movie Btn
                        #     [
                        #         # Add movie button will work like a
                        #         # hyperlink that leads to another page
                        #         dbc.Button(
                        #             "Add Car",
                        #             href='/information/car/car_profile?mode=add'
                        #         )
                        #     ]
                        # ),
                        html.Hr(),
                        html.Div(  # Create section to show list of movies
                            [
                                html.H4('Find Car'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Car", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='carhome_namefilter',
                                                        placeholder='Car Plate Number'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with car will go here.",
                                    id='carhome_carlist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# the callback is used to load the list of suppliers in the main car suppliers page
@app.callback(
    [
        Output(component_id='carhome_carlist', component_property='children')
    ],
    [
        Input(component_id='url', component_property='pathname'),
        Input(component_id='carhome_namefilter', component_property='value'),  # changing the text box value should update the table
    ]
)
def repairparthome_loadpartlist(pathname, searchterm):
    if pathname == '/information/car':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT car_model, car_plate_number, car_production_year
                FROM car
                WHERE NOT car_delete_ind
              """
        values = []  # blank since I do not have placeholders in my SQL
        cols = ['Car Model', 'Car Plate Number', 'Car Production Year']
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND car_plate_number ILIKE %s"
            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape:  # check if query returned anything

            # # add the new column
            # # 2. Create the buttons as a list based on the ID
            # buttons = []
            # for car_id in df['ID']:
            #     buttons += [
            #         html.Div(
            #             dbc.Button('Edit',
            #                     href=f'car/car_profile?mode=edit&id={car_id}',
            #                     size='sm', color='warning'),
            #             style={'text-align': 'center'}
            #         )
            #     ]
            # df['Action'] = buttons
            # # remove the column ID before turning into a table
            df = df[['Car Model', 'Car Plate Number', "Car Production Year"]]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
