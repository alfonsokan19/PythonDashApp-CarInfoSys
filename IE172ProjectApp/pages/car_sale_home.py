# Importing necessary libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# Importing app object and database functions
from app import app
from apps import dbconnect as db

# Defining the layout
layout = html.Div(
    [
        html.H2('Car Sale'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Transaction Home Page", href ='/transactions/transactions_main', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(
            [  # Card Container
                dbc.CardHeader(
                    [  # Define Card Header
                        html.H3('Manage Car Sale')
                    ]
                ),
                dbc.CardBody(
                    [  # Define Card Contents
                        html.Div(
                            [  # Add Car Sale Btn
                                dbc.Button(
                                    "Add Car Sale",
                                    href='/transactions/car_sale/car_sale_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [  # Create section to show list of car sales
                                html.H4('Find Car Sale'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Plate Number", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='carsalehome_titlefilter',
                                                        placeholder='Plate Number'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    id='carsalehome_carsalelist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# # Callback to update car sale list based on URL and search term
# @app.callback(
#     Output('carsalehome_carsalelist', 'children'),
#     [Input('url', 'pathname')],
#     [Input('carsalehome_titlefilter', 'value')]
# )
# def carsalehome_loadcarsalelist(pathname, searchterm):
#     if pathname == '/transactions/car_sale':
#         # Query data from the database
#         sql = """ SELECT sale_date, car_model, car_plate_number, car_production_year, concat(customer_fn, ' ' ,customer_mn, ' ', customer_ln) AS customer_name, sale_amount, sale_id
#                  FROM car_sale
#                  INNER JOIN car ON car.car_id=car_sale.car_id
#                  INNER JOIN customer ON customer.customer_id=car_sale.customer_id
#                  WHERE NOT car_sale_delete_ind
#               """
#         values = []

#         # Add search term condition to SQL query
#         if searchterm:
#             sql += " AND car_plate_number ILIKE %s"
#             values += [f"%{searchterm}%"]

#         # Execute query and get dataframe
#         cols = ['Sale Date', 'Car Model', 'Car Plate Number', 'Car Production Year','Customer Name', 'Sale Amount', 'ID']
#         df = db.querydatafromdatabase(sql, values, cols)

#         if not df.empty:
#             # Create "Edit" buttons for each record
#             buttons = [
#                 html.Div(
#                     dbc.Button('Edit',
#                                href=f'car_sale/car_sale_profile?mode=edit&id={sale_id}',
#                                size='sm', color='warning'),
#                     style={'text-align': 'center'}
#                 ) for sale_id in df['ID']
#             ]

#             # Add "Action" column to dataframe
#             df['Action'] = buttons
#             # Remove the column 'ID' before turning into a table
#             df = df[['Sale Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Customer Name', 'Sale Amount', 'Action']]

#             df['Sale Amount'] = df['Sale Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}"))

#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
#                                             hover=True, size='sm', style={'text-align': 'right'})
#             return [table]
#         else:
#             return ["No records to display"]
#     else:
#         raise PreventUpdate

# Callback to update car sale list based on URL and search term
@app.callback(
    Output('carsalehome_carsalelist', 'children'),
    [Input('url', 'pathname')],
    [Input('carsalehome_titlefilter', 'value')]
)
def carsalehome_loadcarsalelist(pathname, searchterm):
    if pathname == '/transactions/car_sale':
        # Query data from the database
        sql = """ SELECT sale_date, car_model, car_plate_number, car_production_year, concat(customer_fn, ' ' ,customer_mn, ' ', customer_ln) AS customer_name, sale_amount, sale_id
                 FROM car_sale
                 INNER JOIN car ON car.car_id=car_sale.car_id
                 INNER JOIN customer ON customer.customer_id=car_sale.customer_id
                 WHERE NOT car_sale_delete_ind
              """
        values = []

        # Add search term condition to SQL query
        if searchterm:
            sql += " AND car_plate_number ILIKE %s"
            values += [f"%{searchterm}%"]

        # Execute query and get dataframe
        cols = ['Sale Date', 'Car Model', 'Car Plate Number', 'Car Production Year','Customer Name', 'Sale Amount', 'ID']
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            # Create "Edit" buttons for each record
            buttons = [
                html.Div(
                    dbc.Button('Edit',
                               href=f'car_sale/car_sale_profile?mode=edit&id={sale_id}',
                               size='sm', color='warning'),
                    style={'text-align': 'center'}
                ) for sale_id in df['ID']
            ]

            # Add "Action" column to dataframe
            df['Action'] = buttons
            # Remove the column 'ID' before turning into a table
            df = df[['Sale Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Customer Name', 'Sale Amount', 'Action']]

            df['Sale Amount'] = df['Sale Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                            hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate