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
        html.H2('Employees'),  # Page Header
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
                        html.H3('Manage Employee')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  # Add Movie Btn
                            [
                                # Add movie button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Employee",
                                    href='/information/car_repair_staff/car_repair_staff_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of movies
                            [
                                html.H4('Find Employee'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Employee", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='carrepairstaffhome_namefilter',
                                                        placeholder='Employee'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with Employees will go here.",
                                    id='carrepairstaffhome_carrepairstafflist'
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
#         Output(component_id='carrepairstaffhome_carrepairstafflist', component_property='children')
#     ],
#     [
#         Input(component_id='url', component_property='pathname'),
#         Input(component_id='carrepairstaffhome_namefilter', component_property='value'),  # changing the text box value should update the table
#     ]
# )
# def employeehome_loadsupplierlist(pathname, searchterm):
#     if pathname == '/information/car_repair_staff':
#         # 1. Obtain records from the DB via SQL
#         # 2. Create the html element to return to the Div
#         sql = """ SELECT concat(staff_fn, ' ', staff_mn, ' ', staff_ln), staff_phone_number, car_repair_staff_address, staff_id
#                   FROM car_repair_staff
#                   WHERE NOT staff_delete_ind
#               """
#         values = []  # blank since I do not have placeholders in my SQL
#         cols = ['Car Repair Staff name', 'Phone number', 'Address', 'ID']
#         ### ADD THIS IF BLOCK
#         if searchterm:
#             # We use the operator ILIKE for pattern-matching
#             sql += " AND concat(staff_fn, ' ', staff_mn, ' ', staff_ln) ILIKE %s"
#             # The % before and after the term means that
#             # there can be text before and after
#             # the search term
#             values += [f"%{searchterm}%"]
#         df = db.querydatafromdatabase(sql, values, cols)
#         if df.shape:  # check if query returned anything

#             # add the new column
#             # 2. Create the buttons as a list based on the ID
#             buttons = []
#             for staff_id in df['ID']:
#                 buttons += [
#                     html.Div(
#                         dbc.Button('Edit',
#                                 href=f'car_repair_staff/car_repair_staff_profile?mode=edit&id={staff_id}',
#                                 size='sm', color='warning'),
#                         style={'text-align': 'center'}
#                     )
#                 ]
#             df['Action'] = buttons
#             # remove the column ID before turning into a table
#             df = df[['Car Repair Staff name', 'Phone number', "Address", "Action"]]

#             df['Phone number'] = '+63' + df['Phone number'].astype(str)
#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'right'})
#             return [table]
#         else:
#             return ["No records to display"]
#     else:
#         raise PreventUpdate

# the callback is used to load the list of suppliers in the main car suppliers page
@app.callback(
    [
        Output(component_id='carrepairstaffhome_carrepairstafflist', component_property='children')
    ],
    [
        Input(component_id='url', component_property='pathname'),
        Input(component_id='carrepairstaffhome_namefilter', component_property='value'),  # changing the text box value should update the table
    ]
)
def employeehome_loadsupplierlist(pathname, searchterm):
    if pathname == '/information/car_repair_staff':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT concat(staff_fn, ' ', staff_mn, ' ', staff_ln), staff_phone_number, car_repair_staff_address, staff_id
                  FROM car_repair_staff
                  WHERE NOT staff_delete_ind
              """
        values = []  # blank since I do not have placeholders in my SQL
        cols = ['Car Repair Staff name', 'Phone number', 'Address', 'ID']
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND concat(staff_fn, ' ', staff_mn, ' ', staff_ln) ILIKE %s"
            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape:  # check if query returned anything

            # add the new column
            # 2. Create the buttons as a list based on the ID
            buttons = []
            for staff_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                href=f'car_repair_staff/car_repair_staff_profile?mode=edit&id={staff_id}',
                                size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            # remove the column ID before turning into a table
            df = df[['Car Repair Staff name', 'Phone number', "Address", "Action"]]

            def add_country_code(phone_number):
                if len(str(phone_number)) == 10:
                    return '(+63) ' + str(phone_number)
                if len(str(phone_number)) == 8:
                    return '(02) ' + str(phone_number)
                else:
                    return str(phone_number)

            # df['Phone number'] = '+63' + df['Phone number'].astype(str)
            df['Phone number'] = df['Phone number'].apply(add_country_code)

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate