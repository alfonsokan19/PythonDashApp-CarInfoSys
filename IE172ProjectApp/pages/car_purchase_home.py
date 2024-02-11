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
        html.H2('Car Purchase'),  # Page Header
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
                        html.H3('Manage Car Purchase')
                    ]
                ),
                dbc.CardBody(
                    [  # Define Card Contents
                        html.Div(
                            [  # Add Movie Btn
                                # Add movie button will work like a hyperlink that leads to another page
                                dbc.Button(
                                    "Add Car Purchase",
                                    href='/transactions/car_purchase/car_purchase_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [  # Create section to show list of movies
                                html.H4('Find Car Purchase'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Plate Number", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='carpurchasehome_titlefilter',
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
                                    "Table with car purchase will go here.",
                                    id='carpurchasehome_carpurchaselist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


# @app.callback(
#     [
#         Output(component_id='carpurchasehome_carpurchaselist', component_property='children')
#     ],
#     [
#         Input(component_id='url', component_property='pathname'),
#         Input(component_id='carpurchasehome_titlefilter', component_property='value'),  # changing the text box value should update the table
#     ]
# )
# def carpurchasehome_loadcarpurchaselist(pathname, searchterm):
#     if pathname == '/transactions/car_purchase':
#         # 1. Obtain records from the DB via SQL
#         # 2. Create the html element to return to the Div
#         sql = """ 
#         SELECT purchase_date, car_model, car_plate_number, car_production_year, car_purchase_condition_label, concat(csupplier_fn, ' ' ,csupplier_mn, ' ', csupplier_ln) AS supplier_name, purchase_amount, purchase_id
#         FROM car_purchase_order
#         INNER JOIN car ON car.car_id=car_purchase_order.car_id
#         INNER JOIN car_supplier ON car_supplier.csupplier_id=car_purchase_order.csupplier_id
#         INNER JOIN car_purchase_condition ON car_purchase_condition.car_purchase_condition_id = car_purchase_order.car_purchase_condition_id
#         WHERE car_purchase_order_delete_ind = False
#         """
#         values = []  # blank since I do not have placeholders in my SQL
#         cols = ['Purchase Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Purchase Condition', 'Supplier Name', 'Purchase Amount', 'ID']

#         ### ADD THIS IF BLOCK
#         if searchterm:
#             # We use the operator ILIKE for pattern-matching
#             sql += " AND car_plate_number ILIKE %s"
#             # The % before and after the term means that
#             # there can be text before and after
#             # the search term
#             values += [f"%{searchterm}%"]
        
#         df = db.querydatafromdatabase(sql, values, cols)


#         if df.shape:  # check if query returned anything
#             # add the new column
#             # 2. Create the buttons as a list based on the ID
#             buttons = []
#             for purchase_id in df['ID']:
#                 buttons += [
#                     html.Div(
#                         dbc.Button('Edit',
#                                 href=f'/transactions/car_purchase/car_purchase_profile?mode=edit&id={purchase_id}',
#                                 size='sm', color='warning'),
#                         style={'text-align': 'center'}
#                     )
#                 ]
#             df['Action'] = buttons
#             # remove the column ID before turning into a table
#             df = df[['Purchase Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Purchase Condition', 'Supplier Name', 'Purchase Amount', 'Action']]

#             df['Purchase Amount'] = df['Purchase Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}"))

#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
#                                             hover=True, size='sm', style={'text-align': 'right'})
#             return [table]
#         else:
#             return ["No records to display"]

#     else:
#         raise PreventUpdate

@app.callback(
    [
        Output(component_id='carpurchasehome_carpurchaselist', component_property='children')
    ],
    [
        Input(component_id='url', component_property='pathname'),
        Input(component_id='carpurchasehome_titlefilter', component_property='value'),  # changing the text box value should update the table
    ]
)
def carpurchasehome_loadcarpurchaselist(pathname, searchterm):
    if pathname == '/transactions/car_purchase':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ 
        SELECT purchase_date, car_model, car_plate_number, car_production_year, car_purchase_condition_label, concat(csupplier_fn, ' ' ,csupplier_mn, ' ', csupplier_ln) AS supplier_name, purchase_amount, purchase_id
        FROM car_purchase_order
        INNER JOIN car ON car.car_id=car_purchase_order.car_id
        INNER JOIN car_supplier ON car_supplier.csupplier_id=car_purchase_order.csupplier_id
        INNER JOIN car_purchase_condition ON car_purchase_condition.car_purchase_condition_id = car_purchase_order.car_purchase_condition_id
        WHERE car_purchase_order_delete_ind = False
        """
        values = []  # blank since I do not have placeholders in my SQL
        cols = ['Purchase Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Purchase Condition', 'Supplier Name', 'Purchase Amount', 'ID']

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
            # add the new column
            # 2. Create the buttons as a list based on the ID
            buttons = []
            for purchase_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                href=f'/transactions/car_purchase/car_purchase_profile?mode=edit&id={purchase_id}',
                                size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            # remove the column ID before turning into a table
            df = df[['Purchase Date', 'Car Model', 'Car Plate Number', 'Car Production Year', 'Purchase Condition', 'Supplier Name', 'Purchase Amount', 'Action']]

            df['Purchase Amount'] = df['Purchase Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                            hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to display"]

    else:
        raise PreventUpdate