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
                dcc.Store(id='carsaleprofile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('Car Sale Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Car Sale Page", href ='/transactions/car_sale', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='carsaleprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                html.H3("Car Details"),
                dbc.Row(
                    [
                        dbc.Label("Sale Date", width=2),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='carsaleprofile_purchasedate',
                                placeholder='Sale Date',
                                month_format='MMM DD YY',
                            ),
                            width=6
                        )
                    ],
                    className='mb-3'
                ),

             dbc.Row(
                    [
                        dbc.Label("Plate Number", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='carsaleprofile_car',
                                    placeholder='Plate Number',
                                    clearable=True,
                                    searchable=True,
                                    options=[]
                                ), 
                                className="dash-bootstrap"
                            ),
                            width=6,
                        ),
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Sale Amount", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carsaleprofile_purchaseamount',
                                placeholder='Sale Amount'
                            ),
                            width=6
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
    [
        dbc.Label("Customer Name", width=2),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='carsaleprofile_customer',
                    placeholder='Customer Name',
                    clearable=True,
                    searchable=True,
                    options=[]
                ),
                className="dash-bootstrap"
            ),
            width=4,
        ),
    ],
    className="mb-3",
                ),
                dbc.Row(
                    [
        dbc.Col(
            dbc.Button(
                'Proceed here if customer is not listed',
                id='carsaleprofile_redirectcustomer',
                n_clicks=0,
                href='/information/customer/customer_profile?mode=add'
            ),
            width=5,
        ),
    ],
    className='mb-3'
),

                html.Div(
                    dbc.Row(
                        [
                            dbc.Label("Wish to delete?", width=1),
                            dbc.Col(
                                dbc.Checklist(
                                    id='carsaleprofile_removerecord',
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
                    id='carsaleprofile_removerecord_div'
                ),

            ]
        ),
        dbc.Button(
            'Submit',
            id='carsaleprofile_submit',
            n_clicks=0  # Initialize number of clicks
        ),
        dbc.Modal(  # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    [
                        'Action completed successfully.'
                    ], id = 'carsaleprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/transactions/car_sale',
                        id = 'carsaleprofile_btn_modal'  # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='carsaleprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

# DONE
# this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='carsaleprofile_toload', component_property='data'),
        Output(component_id='carsaleprofile_removerecord_div', component_property='style'),
        Output(component_id='carsaleprofile_customer', component_property='options'),
        Output(component_id='carsaleprofile_car', component_property='options'),
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def carsaleprofile_toloadvalue_customerandcardropdown(pathname, search):
    if pathname == '/transactions/car_sale/car_sale_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        carsaleprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not carsaleprofile_toload else None

        sql_customer = """
        SELECT CONCAT(customer_fn, ' ', customer_mn, ' ', customer_ln) AS customer_name, customer_id
        FROM customer
        WHERE customer_delete_ind = False
        """

        values_customer = []
        cols_customer = ['label', 'value']

        df_customer = db.querydatafromdatabase(sql_customer, values_customer, cols_customer)

        customer_options = df_customer.to_dict('records')

        sql_cars = """
        SELECT car_plate_number, car.car_id
        FROM car_repair
		INNER JOIN repair_status ON repair_status.repair_status_id=car_repair.repair_status_id
        INNER JOIN car ON car.car_id = car_repair.car_id
        INNER JOIN CAR_purchase_order ON CAR_purchase_order.car_id=car.car_id
        WHERE car_purchase_condition_id = 1 		
        AND repair_status.repair_status_id = 3					
        AND car_delete_ind = False
		AND car_repair_delete_ind = False

        UNION
        
        SELECT car_plate_number, car_purchase_order.car_id
        FROM car_purchase_order
        INNER JOIN car ON car_purchase_order.car_id = car.car_id
        WHERE car_purchase_condition_id = 2 
        AND car_delete_ind = False 
        """

        values_cars = []
        cols_cars = ['label', 'value']
        df_cars = db.querydatafromdatabase(sql_cars, values_cars, cols_cars)
        cars_options = df_cars.to_dict('records')


    else:
        raise PreventUpdate
    
    return [carsaleprofile_toload, removediv_style, customer_options, cars_options]






@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='carsaleprofile_alert', component_property='color'),
        Output(component_id='carsaleprofile_alert', component_property='children'),
        Output(component_id='carsaleprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='carsaleprofile_successmodal', component_property='is_open'),
        # Output(component_id='carsaleprofile_feedback_message', component_property='children'),
        # Output(component_id='carsaleprofile_btn_modal', component_property='href'),
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='carsaleprofile_submit', component_property='n_clicks'),
        # Input(component_id='carsaleprofile_btn_modal', component_property='n_clicks'),
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='carsaleprofile_purchasedate', component_property='date'),                           #1
        State(component_id='carsaleprofile_purchaseamount', component_property='value'),
        State(component_id='url', component_property='search'),
        State(component_id='carsaleprofile_removerecord', component_property='value'),

        State(component_id='carsaleprofile_customer', component_property='value'), 
        State(component_id='carsaleprofile_car', component_property='value'),
        
    ]
)


# done
def carsaleprofile_saveprofile(submitbtn, 
                               carsaleprofile_purchasedate, carsaleprofile_purchaseamount, search, carsaleprofile_removerecord,
                               customer, chosen_car):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'carsaleprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not carsaleprofile_purchasedate:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the purchase date.'

            elif not carsaleprofile_purchaseamount:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the purchase amount.'

            elif not customer:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer name.'

            else:  # all inputs are valid
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    # Add the data into the db

                    try:
                        sql_carsaleorder = '''
                        INSERT INTO car_sale (sale_date, sale_amount, customer_id, car_id, car_sale_delete_ind)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        values_carsaleorder = [carsaleprofile_purchasedate, carsaleprofile_purchaseamount, customer, chosen_car, False]
                        db.modifydatabase(sql_carsaleorder, values_carsaleorder)

                        # If this is successful, we want the successmodal to show
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! This car has either been already sold to someone else or this is a duplicate entry.'

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    sale_id = parse_qs(parsed.query)['id'][0]

                    try:
                        sql_carsaleorder = '''
                        UPDATE car_sale
                        SET
                            sale_date = %s,
                            sale_amount = %s,
                            car_sale_delete_ind = %s,
                            customer_id = %s,
                            car_id = %s
                        WHERE sale_id = %s
                        '''


                        to_delete_carsaleorder = bool(carsaleprofile_removerecord)
                        values_carsaleorder = [carsaleprofile_purchasedate, carsaleprofile_purchaseamount, to_delete_carsaleorder, customer, chosen_car, sale_id]

                        db.modifydatabase(sql_carsaleorder, values_carsaleorder)
                        modal_open = True

                    except DatabaseError as e:
                            alert_open = True
                            alert_color = 'danger'
                            alert_text = 'Error! This car has either been already sold to someone else or this is a duplicate entry.'

            return [alert_color, alert_text, alert_open, modal_open]
        else:  # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate



# done just delete old car fields
# used to load exact field entries when clicking the edit button on one of the entries
@app.callback(
    [
        # Our goal is to update values of these fields
        Output(component_id='carsaleprofile_purchasedate', component_property='date'),                           #1
        Output(component_id='carsaleprofile_purchaseamount', component_property='value'),
        Output(component_id='carsaleprofile_customer', component_property='value'),
        Output(component_id='carsaleprofile_car', component_property='value'),

    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='carsaleprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='carsaleprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def carsaleprofile_loadprofile(timestamp, carsaleprofile_toload, search):
    if carsaleprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        sale_id = parse_qs(parsed.query)['id'][0]

        # Query from db
        sql = """ SELECT sale_date, car_sale.customer_id, sale_amount, car_sale.car_id
        FROM car_sale
        INNER JOIN car ON car.car_id=car_sale.car_id
        INNER JOIN customer ON customer.customer_id=car_sale.customer_id
        WHERE sale_id = %s
        """
        values = [sale_id]
        col = ['sale_date', 'customer', 'sale_amount', 'car']
        
        df = db.querydatafromdatabase(sql, values, col)

        sale_date = df['sale_date'][0]
        customer = int(df['customer'][0])
        sale_amount = (df['sale_amount'][0])
        car = int(df['car'][0])

        return [sale_date, sale_amount, customer, car]
    else:
        raise PreventUpdate