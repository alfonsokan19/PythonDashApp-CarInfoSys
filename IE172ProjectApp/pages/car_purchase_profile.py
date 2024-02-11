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

from urllib.parse import urlparse, parse_qs
from psycopg2 import DatabaseError

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='carpurchaseprofile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('Car Purchase Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Car Purchase Page", href ='/transactions/car_purchase', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='carpurchaseprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                html.H3("Car Details"),
                dbc.Row(
                    [
                        dbc.Label("Purchase Date", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='carpurchaseprofile_purchasedate',
                                placeholder='Purchase Date',
                                month_format='MMM DD YY',
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Car Model", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carpurchaseprofile_carmodel',
                                placeholder='Car Model'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),


                dbc.Row(
                    [
                        dbc.Label("Car Plate Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carpurchaseprofile_carplatenumber',
                                placeholder='Car Plate Number'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Car Production Year", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='carpurchaseprofile_carproductionyear',
                                placeholder='Production Year'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Purchase Amount", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='carpurchaseprofile_purchaseamount',
                                placeholder='Purchase Amount'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),


                dbc.Row(
                    [
                        dbc.Label("Car Condition", width=1),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='carpurchaseprof_carcondition',
                                    clearable=True,
                                    searchable=True,
                                    options=[],
                                    placeholder='Condition'
                                ), 
                                className="dash-bootstrap"
                            ),
                            width=5,
                        ),
                    ],
                    className="mb-3",
                ),

               # Existing code for Field 7
dbc.Row(
    [
        dbc.Label("Car Supplier Name", width=1),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='carpurchaseprofile_supplier',
                    placeholder='Supplier Name',
                    clearable=True,
                    searchable=True,
                    options=[]
                ), 
                className="dash-bootstrap"
            ),
            width=3,
        ),
    ],
    className="mb-3",
),

# Button beside Field 7
dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                'Proceed here if supplier is not listed',
                id='carpurchaseprofile_redirectsupplier',
                n_clicks=0,
                href='/information/car_supplier/car_supplier_profile?mode=add'
            ),
            width=5,
        ),
    ],
    className="mb-3",
),


                html.Div(
                    dbc.Row(
                        [
                            dbc.Label("Wish to delete?", width=1),
                            dbc.Col(
                                dbc.Checklist(
                                    id='carpurchaseprofile_removerecord',
                                    options=[
                                        {
                                            'label': "Mark for Deletion",
                                            'value': 1
                                        }
                                    ],
                                    # I want the label to be bold
                                    style={'fontWeight':'bold'},
                                ),
                                width=5,
                            ),
                        ],
                        className="mb-3",
                    ),
                    id='carpurchaseprofile_removerecord_div'
                ),

            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Submit',
            id='carpurchaseprofile_submit',
            n_clicks=0  # Initialize number of clicks
        ),
        dbc.Modal(  # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    [
                        'Purchase Transaction has been saved!'
                    ], id = 'carpurchaseprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/transactions/car_purchase',
                        id = 'carpurchaseprofile_btn_modal'  # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='carpurchaseprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

# # DONE
# @app.callback(
#         [
#             Output(component_id='carpurchaseprofile_supplier', component_property='options'),
#             Output(component_id='carpurchaseprof_carcondition', component_property='options')
#         ],
#         [
#             Input(component_id='url', component_property='pathname')
#         ]
# )

# def carpurchaseprofile_populatedropdowns(pathname):
#     if pathname == '/transactions/car_purchase/car_purchase_profile':
#         sql_supplier = """
#         SELECT CONCAT(csupplier_fn, ' ', csupplier_mn, ' ', csupplier_ln) AS csupplier_name, csupplier_id
#         FROM car_supplier
#         WHERE car_supplier_delete_ind = False
#         """

#         values_supplier = []
#         cols_supplier = ['label', 'value']

#         df_supplier = db.querydatafromdatabase(sql_supplier, values_supplier, cols_supplier)

#         csupplier_options = df_supplier.to_dict('records')


#         sql_carpurchasecondition = """
#         SELECT car_purchase_condition_label, car_purchase_condition_id
#         FROM car_purchase_condition
#         WHERE car_purchase_condition_delete_ind = False
#         """

#         values_carpurchasecondition = []
#         cols_carpurchasecondition = ['label', 'value']
#         df_condition = db.querydatafromdatabase(sql_carpurchasecondition, values_carpurchasecondition, cols_carpurchasecondition)
#         carcondition_options = df_condition.to_dict('records')

#         return [csupplier_options, carcondition_options]
#     else:
#         raise PreventUpdate


# # DONE
# # this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
# @app.callback(
#     [
#         Output(component_id='carpurchaseprofile_toload', component_property='data'),
#         Output(component_id='carpurchaseprofile_removerecord_div', component_property='style')
#     ],
#     [
#         Input(component_id='url', component_property='pathname')
#     ],
#     [
#         State(component_id='url', component_property='search')  # add this search component to the State
#     ]
# )

# def carpurchaseprofile_toloadvalue(pathname, search):
#     if pathname == '/transactions/car_purchase/car_purchase_profile':
#         # # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         carpurchaseprofile_toload = 1 if create_mode == 'edit' else 0
#         removediv_style = {'display': 'none'} if not carpurchaseprofile_toload else None
#     else:
#         raise PreventUpdate
#     return [carpurchaseprofile_toload, removediv_style]



# @app.callback(
#     [
#         # dbc.Alert Properties
#         Output(component_id='carpurchaseprofile_alert', component_property='color'),
#         Output(component_id='carpurchaseprofile_alert', component_property='children'),
#         Output(component_id='carpurchaseprofile_alert', component_property='is_open'),
#         # dbc.Modal Properties
#         Output(component_id='carpurchaseprofile_successmodal', component_property='is_open'),
#         # Output(component_id='carpurchaseprofile_feedback_message', component_property='children'),
#         # Output(component_id='carpurchaseprofile_btn_modal', component_property='href'),
#     ],
#     [
#         # For buttons, the property n_clicks
#         Input(component_id='carpurchaseprofile_submit', component_property='n_clicks'),
#         # Input(component_id='carpurchaseprofile_btn_modal', component_property='n_clicks'),
#     ],
#     [
#         # The values of the fields are States
#         # They are required in this process but they
#         # do not trigger this callback
#         State(component_id='carpurchaseprofile_purchasedate', component_property='date'),                           #1
#         State(component_id='carpurchaseprofile_carmodel', component_property='value'),                              #2
#         State(component_id='carpurchaseprofile_carplatenumber', component_property='value'),
#         State(component_id='carpurchaseprofile_carproductionyear', component_property='value'),

#         State(component_id='carpurchaseprofile_purchaseamount', component_property='value'),
#         State(component_id='url', component_property='search'),
#         State(component_id='carpurchaseprofile_removerecord', component_property='value'),
#         State(component_id='carpurchaseprofile_toload', component_property='modified_timestamp'),

#         State(component_id='carpurchaseprofile_supplier', component_property='value'),
#         State(component_id='carpurchaseprof_carcondition', component_property='value')
#     ]
# )
# def carpurchaseprofile_saveprofile(submitbtn, 
#                                    carpurchaseprofile_purchasedate, carpurchaseprofile_carmodel,carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear,
#                                    carpurchaseprofile_purchaseamount, search, carpurchaseprofile_removerecord, modified_date,
#                                    carpurchaseprofile_supplierid, car_condition_id):
#     ctx = dash.callback_context
#     # The ctx filter -- ensures that only a change in url will activate this callback
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'carpurchaseprofile_submit' and submitbtn:
#             # the submitbtn condition checks if the callback was indeed activated by a click
#             # and not by having the submit button appear in the layout
#             # Set default outputs
#             alert_open = False
#             modal_open = False
#             alert_color = ''
#             alert_text = ''
#             # We need to check inputs
#             if not carpurchaseprofile_purchasedate:  # If title is blank, not title = True
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the purchase date.'

#             elif not carpurchaseprofile_carmodel:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the car model.'

#             elif not carpurchaseprofile_carplatenumber:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the plate number.'

#             elif not carpurchaseprofile_carproductionyear:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the production year.'


#             elif not carpurchaseprofile_purchaseamount:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the purchase amount.'

#             elif not carpurchaseprofile_supplierid:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s name.'

#             elif not car_condition_id:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the car condition.'

#             else:  # all inputs are valid
#                 parsed = urlparse(search)
#                 create_mode = parse_qs(parsed.query)['mode'][0]
#                 if create_mode == 'add':

#                     try: 
#                         # Add the data into the db
#                         sql_insertcar = '''
#                         INSERT INTO car (car_model, car_plate_number, car_production_year, car_delete_ind)
#                         VALUES (%s, %s, %s, %s)
#                         '''
#                         values_insertcar = [carpurchaseprofile_carmodel, carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear, False]
#                         db.modifydatabase(sql_insertcar, values_insertcar)


#                         sql_car_id = """
#                         SELECT MAX(car_id) FROM car
#                         """
#                         values = []
#                         column = ['car_id']
#                         car_id = db.querydatafromdatabase(sql_car_id, values, column)
#                         car_id_value = int(car_id.iloc[0])
#                         print(car_id_value)


#                         sql_carpurchaseorder = '''
#                         INSERT INTO car_purchase_order (purchase_date, purchase_amount, car_purchase_order_delete_ind, car_id, csupplier_id, car_purchase_condition_id)
#                         VALUES (%s, %s, %s, %s, %s, %s)
#                         '''
#                         values_carpurchaseorder = [carpurchaseprofile_purchasedate, carpurchaseprofile_purchaseamount, False, car_id_value, carpurchaseprofile_supplierid, car_condition_id]
#                         db.modifydatabase(sql_carpurchaseorder, values_carpurchaseorder)

#                         # If this is successful, we want the successmodal to show
#                         modal_open = True

#                     except DatabaseError as e:
#                         alert_open = True
#                         alert_color = 'danger'
#                         alert_text = 'Error! You already made a car purchase entry for this plate number.'

#                 elif create_mode == 'edit':
#                     parsed = urlparse(search)
#                     purchase_id = parse_qs(parsed.query)['id'][0]

#                     try:
#                         sql_car = '''
#                         UPDATE car 
#                         SET
#                             car_model = %s,
#                             car_plate_number = %s,
#                             car_production_year = %s,
#                             car_delete_ind = %s
#                         FROM car_purchase_order cpo
#                         WHERE cpo.car_id=car.car_id
#                         AND cpo.purchase_id = %s
#                         '''
#                         to_delete_car = bool(carpurchaseprofile_removerecord)
#                         values_car = [carpurchaseprofile_carmodel, carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear, to_delete_car, purchase_id]

#                         db.modifydatabase(sql_car, values_car)

#                         # NOT SURE
#                         sql_carpurchaseorder = '''
#                         UPDATE car_purchase_order
#                         SET
#                             purchase_date = %s,
#                             purchase_amount = %s,
#                             car_purchase_order_delete_ind = %s,
#                             csupplier_id = %s,
#                             car_purchase_condition_id = %s
#                         WHERE purchase_id = %s
#                         '''

#                         to_delete_carpurchaseorder = bool(carpurchaseprofile_removerecord)
#                         values_carpurchaseorder = [carpurchaseprofile_purchasedate, carpurchaseprofile_purchaseamount, to_delete_carpurchaseorder, carpurchaseprofile_supplierid, car_condition_id, purchase_id]

#                         db.modifydatabase(sql_carpurchaseorder, values_carpurchaseorder)
#                         modal_open = True

#                     except DatabaseError as e:
#                         alert_open = True
#                         alert_color = 'danger'
#                         alert_text = 'Error! You already made a car purchase entry for this plate number.'

#             return [alert_color, alert_text, alert_open, modal_open]
#         else:  # Callback was not triggered by desired triggers
#             raise PreventUpdate
#     else:
#         raise PreventUpdate




# # used to load exact field entries when clicking the edit button on one of the entries
# @app.callback(
#     [
#         # Our goal is to update values of these fields
#         Output(component_id='carpurchaseprofile_purchasedate', component_property='date'),                           #1
#         Output(component_id='carpurchaseprofile_carmodel', component_property='value'),                              #2
#         Output(component_id='carpurchaseprofile_carplatenumber', component_property='value'),
#         Output(component_id='carpurchaseprofile_carproductionyear', component_property='value'),
#         Output(component_id='carpurchaseprofile_purchaseamount', component_property='value'),
#         Output(component_id='carpurchaseprofile_supplier', component_property='value'),
#         Output(component_id='carpurchaseprof_carcondition', component_property='value')

#     ],
#     [
#         # Our trigger is if the dcc.Store object changes its value
#         # This is how you check a change in value for a dcc.Store
#         Input(component_id='carpurchaseprofile_toload', component_property='modified_timestamp')       # ok
#     ],
#     [
#         # We need the following to proceed
#         # Note that the value of the dcc.Store object is in
#         # the ‘data’ property, and not in the ‘modified_timestamp’ property
#         State(component_id='carpurchaseprofile_toload', component_property='data'),                    # ok 
#         State(component_id='url', component_property='search'),                                         # ok 
#     ]
# )

# def carpurchaseprofile_loadprofile(timestamp, carpurchaseprofile_toload, search):
#     if carpurchaseprofile_toload:  # check if toload = 1
#         # Get movieid value from the search parameters
#         parsed = urlparse(search)
#         purchase_id = parse_qs(parsed.query)['id'][0]

#         # Query from db
#         sql = """ 
#         SELECT purchase_date, car_model, car_plate_number, car_production_year, purchase_amount, car_purchase_order.csupplier_id, car_purchase_order.car_purchase_condition_id
#         FROM car_purchase_order
#         INNER JOIN car ON car.car_id=car_purchase_order.car_id
#         INNER JOIN car_supplier ON car_supplier.csupplier_id=car_purchase_order.csupplier_id
#         INNER JOIN car_purchase_condition ON car_purchase_condition.car_purchase_condition_id=car_purchase_order.car_purchase_condition_id
#         WHERE purchase_id = %s
#         """
#         values = [purchase_id]
#         col = ['purchase_date', 'car_model', 'car_plate_number', 'car_production_year', 'purchase_amount', 'csupplier_id', 'car_condition']
        
#         df = db.querydatafromdatabase(sql, values, col)

#         purchase_date = df['purchase_date'][0]
#         car_model = df['car_model'][0]
#         car_plate_number = df['car_plate_number'][0]
#         car_production_year = df['car_production_year'][0]
#         purchase_amount = df['purchase_amount'][0]
#         csupplier_id = int(df['csupplier_id'][0])
#         car_condition = int(df['car_condition'][0])


#         return [purchase_date, car_model, car_plate_number, car_production_year, purchase_amount, csupplier_id, car_condition]
#     else:
#         raise PreventUpdate

# DONE
@app.callback(
        [
            Output(component_id='carpurchaseprofile_supplier', component_property='options'),
            Output(component_id='carpurchaseprof_carcondition', component_property='options')
        ],
        [
            Input(component_id='url', component_property='pathname')
        ]
)

def carpurchaseprofile_populatedropdowns(pathname):
    if pathname == '/transactions/car_purchase/car_purchase_profile':
        sql_supplier = """
        SELECT CONCAT(csupplier_fn, ' ', csupplier_mn, ' ', csupplier_ln) AS csupplier_name, csupplier_id
        FROM car_supplier
        WHERE car_supplier_delete_ind = False
        """

        values_supplier = []
        cols_supplier = ['label', 'value']

        df_supplier = db.querydatafromdatabase(sql_supplier, values_supplier, cols_supplier)

        csupplier_options = df_supplier.to_dict('records')


        sql_carpurchasecondition = """
        SELECT car_purchase_condition_label, car_purchase_condition_id
        FROM car_purchase_condition
        WHERE car_purchase_condition_delete_ind = False
        """

        values_carpurchasecondition = []
        cols_carpurchasecondition = ['label', 'value']
        df_condition = db.querydatafromdatabase(sql_carpurchasecondition, values_carpurchasecondition, cols_carpurchasecondition)
        carcondition_options = df_condition.to_dict('records')

        return [csupplier_options, carcondition_options]
    else:
        raise PreventUpdate


# DONE
# this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='carpurchaseprofile_toload', component_property='data'),
        Output(component_id='carpurchaseprofile_removerecord_div', component_property='style')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def carpurchaseprofile_toloadvalue(pathname, search):
    if pathname == '/transactions/car_purchase/car_purchase_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        carpurchaseprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not carpurchaseprofile_toload else None
    else:
        raise PreventUpdate
    return [carpurchaseprofile_toload, removediv_style]



@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='carpurchaseprofile_alert', component_property='color'),
        Output(component_id='carpurchaseprofile_alert', component_property='children'),
        Output(component_id='carpurchaseprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='carpurchaseprofile_successmodal', component_property='is_open'),
        # Output(component_id='carpurchaseprofile_feedback_message', component_property='children'),
        # Output(component_id='carpurchaseprofile_btn_modal', component_property='href'),
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='carpurchaseprofile_submit', component_property='n_clicks'),
        # Input(component_id='carpurchaseprofile_btn_modal', component_property='n_clicks'),
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='carpurchaseprofile_purchasedate', component_property='date'),                           #1
        State(component_id='carpurchaseprofile_carmodel', component_property='value'),                              #2
        State(component_id='carpurchaseprofile_carplatenumber', component_property='value'),
        State(component_id='carpurchaseprofile_carproductionyear', component_property='value'),

        State(component_id='carpurchaseprofile_purchaseamount', component_property='value'),
        State(component_id='url', component_property='search'),
        State(component_id='carpurchaseprofile_removerecord', component_property='value'),
        State(component_id='carpurchaseprofile_toload', component_property='modified_timestamp'),

        State(component_id='carpurchaseprofile_supplier', component_property='value'),
        State(component_id='carpurchaseprof_carcondition', component_property='value')
    ]
)
def carpurchaseprofile_saveprofile(submitbtn, 
                                   carpurchaseprofile_purchasedate, carpurchaseprofile_carmodel,carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear,
                                   carpurchaseprofile_purchaseamount, search, carpurchaseprofile_removerecord, modified_date,
                                   carpurchaseprofile_supplierid, car_condition_id):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'carpurchaseprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not carpurchaseprofile_purchasedate:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the purchase date.'

            elif not carpurchaseprofile_carmodel:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the car model.'

            elif not carpurchaseprofile_carplatenumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the plate number.'

            elif not carpurchaseprofile_carproductionyear:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the production year.'


            elif not carpurchaseprofile_purchaseamount:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the purchase amount.'

            elif not carpurchaseprofile_supplierid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s name.'

            elif not car_condition_id:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the car condition.'

            else:  # all inputs are valid
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':

                    try: 
                        # Add the data into the db
                        sql_insertcar = '''
                        INSERT INTO car (car_model, car_plate_number, car_production_year, car_delete_ind)
                        VALUES (%s, %s, %s, %s)
                        '''
                        values_insertcar = [carpurchaseprofile_carmodel, carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear, False]
                        db.modifydatabase(sql_insertcar, values_insertcar)


                        sql_car_id = """
                        SELECT MAX(car_id) FROM car
                        """
                        values = []
                        column = ['car_id']
                        car_id = db.querydatafromdatabase(sql_car_id, values, column)
                        car_id_value = int(car_id.iloc[0])
                        print(car_id_value)


                        sql_carpurchaseorder = '''
                        INSERT INTO car_purchase_order (purchase_date, purchase_amount, car_purchase_order_delete_ind, car_id, csupplier_id, car_purchase_condition_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        values_carpurchaseorder = [carpurchaseprofile_purchasedate, carpurchaseprofile_purchaseamount, False, car_id_value, carpurchaseprofile_supplierid, car_condition_id]
                        db.modifydatabase(sql_carpurchaseorder, values_carpurchaseorder)

                        # If this is successful, we want the successmodal to show
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! You already made a car purchase entry for this plate number.'

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    purchase_id = parse_qs(parsed.query)['id'][0]

                    try:
                        sql_car = '''
                        UPDATE car 
                        SET
                            car_model = %s,
                            car_plate_number = %s,
                            car_production_year = %s,
                            car_delete_ind = %s
                        FROM car_purchase_order cpo
                        WHERE cpo.car_id=car.car_id
                        AND cpo.purchase_id = %s
                        '''
                        to_delete_car = bool(carpurchaseprofile_removerecord)
                        values_car = [carpurchaseprofile_carmodel, carpurchaseprofile_carplatenumber, carpurchaseprofile_carproductionyear, to_delete_car, purchase_id]

                        db.modifydatabase(sql_car, values_car)

                        # NOT SURE
                        sql_carpurchaseorder = '''
                        UPDATE car_purchase_order
                        SET
                            purchase_date = %s,
                            purchase_amount = %s,
                            car_purchase_order_delete_ind = %s,
                            csupplier_id = %s,
                            car_purchase_condition_id = %s
                        WHERE purchase_id = %s
                        '''

                        to_delete_carpurchaseorder = bool(carpurchaseprofile_removerecord)
                        values_carpurchaseorder = [carpurchaseprofile_purchasedate, carpurchaseprofile_purchaseamount, to_delete_carpurchaseorder, carpurchaseprofile_supplierid, car_condition_id, purchase_id]

                        db.modifydatabase(sql_carpurchaseorder, values_carpurchaseorder)
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! You already made a car purchase entry for this plate number.'

            return [alert_color, alert_text, alert_open, modal_open]
        else:  # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate




# used to load exact field entries when clicking the edit button on one of the entries
@app.callback(
    [
        # Our goal is to update values of these fields
        Output(component_id='carpurchaseprofile_purchasedate', component_property='date'),                           #1
        Output(component_id='carpurchaseprofile_carmodel', component_property='value'),                              #2
        Output(component_id='carpurchaseprofile_carplatenumber', component_property='value'),
        Output(component_id='carpurchaseprofile_carproductionyear', component_property='value'),
        Output(component_id='carpurchaseprofile_purchaseamount', component_property='value'),
        Output(component_id='carpurchaseprofile_supplier', component_property='value'),
        Output(component_id='carpurchaseprof_carcondition', component_property='value')

    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='carpurchaseprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='carpurchaseprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def carpurchaseprofile_loadprofile(timestamp, carpurchaseprofile_toload, search):
    if carpurchaseprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        purchase_id = parse_qs(parsed.query)['id'][0]

        # Query from db
        sql = """ 
        SELECT purchase_date, car_model, car_plate_number, car_production_year, purchase_amount, car_purchase_order.csupplier_id, car_purchase_order.car_purchase_condition_id
        FROM car_purchase_order
        INNER JOIN car ON car.car_id=car_purchase_order.car_id
        INNER JOIN car_supplier ON car_supplier.csupplier_id=car_purchase_order.csupplier_id
        INNER JOIN car_purchase_condition ON car_purchase_condition.car_purchase_condition_id=car_purchase_order.car_purchase_condition_id
        WHERE purchase_id = %s
        """
        values = [purchase_id]
        col = ['purchase_date', 'car_model', 'car_plate_number', 'car_production_year', 'purchase_amount', 'csupplier_id', 'car_condition']
        
        df = db.querydatafromdatabase(sql, values, col)

        purchase_date = df['purchase_date'][0]
        car_model = df['car_model'][0]
        car_plate_number = df['car_plate_number'][0]
        car_production_year = df['car_production_year'][0]
        purchase_amount = df['purchase_amount'][0]
        csupplier_id = int(df['csupplier_id'][0])
        car_condition = int(df['car_condition'][0])


        return [purchase_date, car_model, car_plate_number, car_production_year, purchase_amount, csupplier_id, car_condition]
    else:
        raise PreventUpdate