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
from psycopg2 import DatabaseError

from urllib.parse import urlparse, parse_qs

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='customerprofile_toload', storage_type='memory', data=1)
            ]
        ),
        html.H2('Customer Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Customer Page", href ='/information/customer', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='customerprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Customer First Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='customerprofile_firstname',
                                placeholder="First Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                

                dbc.Row(
                    [
                        dbc.Label("Customer Middle Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='customerprofile_middlename',
                                placeholder="Middle Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Customer Last Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='customerprofile_lastname',
                                placeholder="Last Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Customer Phone Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='customerprofile_phonenumber',
                                placeholder="Phone number"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                
                dbc.Row(
                    [
                        dbc.Label("Customer Address", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='customerprofile_address',
                                placeholder="Address"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                html.Div(
                    dbc.Row(
                        [
                            dbc.Label("Wish to delete?", width=1),
                            dbc.Col(
                                dbc.Checklist(
                                    id='customerprofile_removerecord',
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
                    id='customerprofile_removerecord_div'
                ),
            ]
        ),
        dbc.Button(
            'Submit',
            id='customerprofile_submit',
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
                    ], id='customerprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/information/customer',  # Clicking this would lead to a change of pages
                        id = 'customerprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='customerprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)




# # this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
# @app.callback(
#     [
#         Output(component_id='customerprofile_toload', component_property='data'),
#         Output(component_id='customerprofile_removerecord_div', component_property='style')
#     ],
#     [
#         Input(component_id='url', component_property='pathname')
#     ],
#     [
#         State(component_id='url', component_property='search')  # add this search component to the State
#     ]
# )

# def customerprofile_toloadvalue(pathname, search):
#     if pathname == '/information/customer/customer_profile':
#         # # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         customerprofile_toload = 1 if create_mode == 'edit' else 0
#         removediv_style = {'display': 'none'} if not customerprofile_toload else None
#     else:
#         raise PreventUpdate
#     return [customerprofile_toload, removediv_style]




# # this callback is focused on the submit button
# @app.callback(
#     [
#         # dbc.Alert Properties
#         Output(component_id='customerprofile_alert', component_property='color'),
#         Output(component_id='customerprofile_alert', component_property='children'),
#         Output(component_id='customerprofile_alert', component_property='is_open'),
#         # dbc.Modal Properties
#         Output(component_id='customerprofile_successmodal', component_property='is_open'),
#         # Output(component_id='carsupplierprofile_feedback_message', component_property='children'),
#         # Output(component_id='carsupplierprofile_btn_modal', component_property='href')
#     ],
#     [
#         # For buttons, the property n_clicks
#         Input(component_id='customerprofile_submit', component_property='n_clicks')     #ok
#     ],
#     [
#         # The values of the fields are States
#         # They are required in this process but they
#         # do not trigger this callback
#         State(component_id='customerprofile_firstname', component_property='value'),    #field 1 - first name
#         State(component_id='customerprofile_middlename', component_property='value'),   #field 2 - middle name
#         State(component_id='customerprofile_lastname', component_property='value'),      #field 3 - last name
#         State(component_id='customerprofile_phonenumber', component_property='value'),   #field 4 - phone number
#         State(component_id='customerprofile_address', component_property='value'),       #field 5 - address
#         State(component_id='url', component_property='search'),
#         State(component_id='customerprofile_removerecord', component_property='value')
#     ]
# )

# def customerprofile_saveprofile(submitbtn, customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, search, customerprofile_removerecord):
#     ctx = dash.callback_context
#     # The ctx filter -- ensures that only a change in url will activate this callback
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'customerprofile_submit' and submitbtn:
#             # the submitbtn condition checks if the callback was indeed activated by a click
#             # and not by having the submit button appear in the layout
#             # Set default outputs
#             alert_open = False
#             modal_open = False
#             alert_color = ''
#             alert_text = ''
#             # We need to check inputs
#             if not customerprofile_firstname:  # If title is blank, not title = True
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the customer\'s first name.'
#             elif not customerprofile_middlename:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the customer\'s middle name.'
#             elif not customerprofile_lastname:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the customer\'s last name.'
#             elif not customerprofile_phonenumber:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the customer\'s phone number.'
            
#             elif not customerprofile_address:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the customer\'s address.'
    
#             else:  # all inputs are valid
#                 # Add the data into the db
#                 parsed = urlparse(search)
#                 create_mode = parse_qs(parsed.query)['mode'][0]
#                 if create_mode == 'add':
#                     sql = '''
#                     INSERT INTO customer (customer_fn, customer_mn, customer_ln, customer_phone_number, customer_address, customer_delete_ind)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     '''
#                     values = [customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, False]
#                     db.modifydatabase(sql, values)

#                     # feedbackmessage = "Movie has been updated"
#                     # okay_href='/information/car_suppliers'
#                     # If this is successful, we want the successmodal to show
#                     modal_open = True

#                 elif create_mode == 'edit':
#                     parsed = urlparse(search)
#                     customerid = parse_qs(parsed.query)['id'][0]
#                     sql = '''
#                     UPDATE customer
#                     SET
#                         customer_fn = %s,
#                         customer_mn = %s,
#                         customer_ln = %s,
#                         customer_phone_number = %s,
#                         customer_address = %s,
#                         customer_delete_ind = %s
#                     WHERE
#                         customer_id = %s
#                     '''
#                     to_delete = bool(customerprofile_removerecord)
#                     values = [customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, to_delete, customerid]
#                     db.modifydatabase(sql, values)
#                     modal_open = True

#                 else:
#                     raise PreventUpdate
#             return [alert_color, alert_text, alert_open, modal_open]
#         else:  # Callback was not triggered by desired triggers
#             raise PreventUpdate
#     else:
#         raise PreventUpdate



# # used to load exact field entries when clicking the edit button on one of the entries
# @app.callback(
#     [
#         # Our goal is to update values of these fields
#         Output(component_id='customerprofile_firstname', component_property='value'),    
#         Output(component_id='customerprofile_middlename', component_property='value'),   
#         Output(component_id='customerprofile_lastname', component_property='value'),      
#         Output(component_id='customerprofile_phonenumber', component_property='value'), 
#         Output(component_id='customerprofile_address', component_property='value')
#     ],
#     [
#         # Our trigger is if the dcc.Store object changes its value
#         # This is how you check a change in value for a dcc.Store
#         Input(component_id='customerprofile_toload', component_property='modified_timestamp')       # ok
#     ],
#     [
#         # We need the following to proceed
#         # Note that the value of the dcc.Store object is in
#         # the ‘data’ property, and not in the ‘modified_timestamp’ property
#         State(component_id='customerprofile_toload', component_property='data'),                    # ok 
#         State(component_id='url', component_property='search'),                                         # ok 
#     ]
# )

# def customerprofile_loadprofile(timestamp, customerprofile_toload, search):
#     if customerprofile_toload:  # check if toload = 1
#         # Get movieid value from the search parameters
#         parsed = urlparse(search)
#         customerid = parse_qs(parsed.query)['id'][0]
#         # Query from db
#         sql = """
#         SELECT customer_fn, customer_mn, customer_ln, customer_phone_number, customer_address
#         FROM customer
#         WHERE customer_id = %s
#         """
#         values = [customerid]
#         col = ['customerfn', 'customermn', 'customerln', 'customerphonenumber', 'customeraddress']
#         df = db.querydatafromdatabase(sql, values, col)
#         customerfn = df['customerfn'][0]
#         customermn = df['customermn'][0]
#         customerln = df['customerln'][0]
#         customerphonenumber = df['customerphonenumber'][0]
#         customeraddress = df['customeraddress'][0]
#         return [customerfn, customermn, customerln, customerphonenumber, customeraddress]
#     else:
#         raise PreventUpdate

# this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='customerprofile_toload', component_property='data'),
        Output(component_id='customerprofile_removerecord_div', component_property='style')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def customerprofile_toloadvalue(pathname, search):
    if pathname == '/information/customer/customer_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        customerprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not customerprofile_toload else None
    else:
        raise PreventUpdate
    return [customerprofile_toload, removediv_style]




# this callback is focused on the submit button
@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='customerprofile_alert', component_property='color'),
        Output(component_id='customerprofile_alert', component_property='children'),
        Output(component_id='customerprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='customerprofile_successmodal', component_property='is_open'),
        # Output(component_id='carsupplierprofile_feedback_message', component_property='children'),
        # Output(component_id='carsupplierprofile_btn_modal', component_property='href')
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='customerprofile_submit', component_property='n_clicks')     #ok
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='customerprofile_firstname', component_property='value'),    #field 1 - first name
        State(component_id='customerprofile_middlename', component_property='value'),   #field 2 - middle name
        State(component_id='customerprofile_lastname', component_property='value'),      #field 3 - last name
        State(component_id='customerprofile_phonenumber', component_property='value'),   #field 4 - phone number
        State(component_id='customerprofile_address', component_property='value'),       #field 5 - address
        State(component_id='url', component_property='search'),
        State(component_id='customerprofile_removerecord', component_property='value')
    ]
)

def customerprofile_saveprofile(submitbtn, customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, search, customerprofile_removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'customerprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not customerprofile_firstname:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer\'s first name.'
            elif not customerprofile_middlename:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer\'s middle name.'
            elif not customerprofile_lastname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer\'s last name.'
            elif not customerprofile_phonenumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer\'s phone number.'
            
            elif not customerprofile_address:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the customer\'s address.'
    
            else:  # all inputs are valid
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    try:
                        sql = '''
                        INSERT INTO customer (customer_fn, customer_mn, customer_ln, customer_phone_number, customer_address, customer_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        values = [customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, False]
                        db.modifydatabase(sql, values)

                        # feedbackmessage = "Movie has been updated"
                        # okay_href='/information/car_suppliers'
                        # If this is successful, we want the successmodal to show
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! Please enter the exact number of digits for landline (8) or mobile number (11).'
                    

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    customerid = parse_qs(parsed.query)['id'][0]

                    try:
                        sql = '''
                        UPDATE customer
                        SET
                            customer_fn = %s,
                            customer_mn = %s,
                            customer_ln = %s,
                            customer_phone_number = %s,
                            customer_address = %s,
                            customer_delete_ind = %s
                        WHERE
                            customer_id = %s
                        '''
                        to_delete = bool(customerprofile_removerecord)
                        values = [customerprofile_firstname, customerprofile_middlename, customerprofile_lastname, customerprofile_phonenumber, customerprofile_address, to_delete, customerid]
                        db.modifydatabase(sql, values)
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! Please enter the exact number of digits for landline (8) or mobile number (11).'

                else:
                    raise PreventUpdate
            return [alert_color, alert_text, alert_open, modal_open]
        else:  # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate



# used to load exact field entries when clicking the edit button on one of the entries
@app.callback(
    [
        # Our goal is to update values of these fields
        Output(component_id='customerprofile_firstname', component_property='value'),    
        Output(component_id='customerprofile_middlename', component_property='value'),   
        Output(component_id='customerprofile_lastname', component_property='value'),      
        Output(component_id='customerprofile_phonenumber', component_property='value'), 
        Output(component_id='customerprofile_address', component_property='value')
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='customerprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='customerprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def customerprofile_loadprofile(timestamp, customerprofile_toload, search):
    if customerprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        customerid = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
        SELECT customer_fn, customer_mn, customer_ln, customer_phone_number, customer_address
        FROM customer
        WHERE customer_id = %s
        """
        values = [customerid]
        col = ['customerfn', 'customermn', 'customerln', 'customerphonenumber', 'customeraddress']
        df = db.querydatafromdatabase(sql, values, col)
        customerfn = df['customerfn'][0]
        customermn = df['customermn'][0]
        customerln = df['customerln'][0]
        customerphonenumber = df['customerphonenumber'][0]
        customeraddress = df['customeraddress'][0]
        return [customerfn, customermn, customerln, customerphonenumber, customeraddress]
    else:
        raise PreventUpdate