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


# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H2('Repair Part'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the Information Main Page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Information Home Page", href ='/information/information_main', color ='success'),
                html.Br(),
                html.Br(),
                html.Span(
                    "Go back to the Repair Main Page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Repair Home Page", href ='/repairs/repairs_main', color ='success'),
                html.Br()
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Repair Parts')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  # Add Movie Btn
                            [
                                # Add movie button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Repair Part",
                                    href='/information/repair_part/repair_part_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of movies
                            [
                                html.H4('Find Repair Part'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Repair Part", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='repairparthome_namefilter',
                                                        placeholder='Repair Part'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with car repair parts will go here.",
                                    id='repairparthome_repairpartlist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# # the callback is used to load the list of suppliers in the main car suppliers page
# @app.callback(
#     [
#         Output(component_id='repairparthome_repairpartlist', component_property='children')
#     ],
#     [
#         Input(component_id='url', component_property='pathname'),
#         Input(component_id='repairparthome_namefilter', component_property='value'),  # changing the text box value should update the table
#     ]
# )
# def repairparthome_loadpartlist(pathname, searchterm):
#     if pathname == '/information/repair_part':
#         # 1. Obtain records from the DB via SQL
#         # 2. Create the html element to return to the Div
#         sql = """ SELECT item_brand, item_name, item_id
#                   FROM repair_part
#                   WHERE NOT item_delete_ind
#               """
#         values = []  # blank since I do not have placeholders in my SQL
#         cols = ['Part Brand Name', 'Part Name', 'ID']
#         ### ADD THIS IF BLOCK
#         if searchterm:
#             # # We use the operator ILIKE for pattern-matching
#             sql += " AND item_name ILIKE %s"
#             # # The % before and after the term means that
#             # # there can be text before and after
#             # # the search term
#             values += [f"%{searchterm}%"]
#             # # We use the operator ILIKE for pattern-matching
#             # sql += " AND (part_name ILIKE %s OR part_brand ILIKE %s OR part_value ILIKE %s)"
#             # # The % before and after the term means that
#             # # there can be text before and after
#             # # the search term
#             # values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
#         df = db.querydatafromdatabase(sql, values, cols)
#         if df.shape:  # check if query returned anything

#             # add the new column
#             # 2. Create the buttons as a list based on the ID
#             buttons = []
#             for item_id in df['ID']:
#                 buttons += [
#                     html.Div(
#                         dbc.Button('Edit',
#                                 href=f'repair_part/repair_part_profile?mode=edit&id={item_id}',
#                                 size='sm', color='warning'),
#                         style={'text-align': 'center'}
#                     )
#                 ]
#             df['Action'] = buttons
#             # remove the column ID before turning into a table
#             df = df[['Part Brand Name', 'Part Name', "Action"]]

#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'right'})
#             return [table]
#         else:
#             return ["No records to display"]
#     else:
#         raise PreventUpdate

# the callback is used to load the list of suppliers in the main car suppliers page
@app.callback(
    [
        Output(component_id='repairparthome_repairpartlist', component_property='children')
    ],
    [
        Input(component_id='url', component_property='pathname'),
        Input(component_id='repairparthome_namefilter', component_property='value'),  # changing the text box value should update the table
    ]
)
def repairparthome_loadpartlist(pathname, searchterm):
    if pathname == '/information/repair_part':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT item_name, item_id
                  FROM repair_part
                  WHERE NOT item_delete_ind
              """
        values = []  # blank since I do not have placeholders in my SQL
        cols = ['Part Name', 'ID']
        ### ADD THIS IF BLOCK
        if searchterm:
            # # We use the operator ILIKE for pattern-matching
            sql += " AND item_name ILIKE %s"
            # # The % before and after the term means that
            # # there can be text before and after
            # # the search term
            values += [f"%{searchterm}%"]
            # # We use the operator ILIKE for pattern-matching
            # sql += " AND (part_name ILIKE %s OR part_brand ILIKE %s OR part_value ILIKE %s)"
            # # The % before and after the term means that
            # # there can be text before and after
            # # the search term
            # values += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape:  # check if query returned anything

            # add the new column
            # 2. Create the buttons as a list based on the ID
            buttons = []
            for item_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                href=f'repair_part/repair_part_profile?mode=edit&id={item_id}',
                                size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            # remove the column ID before turning into a table
            df = df[['Part Name', "Action"]]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate