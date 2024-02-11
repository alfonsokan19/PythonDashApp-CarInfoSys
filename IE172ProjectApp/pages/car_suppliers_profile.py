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
                dcc.Store(id='carsupplierprofile_toload', storage_type='memory', data=1)
            ]
        ),
        html.H2('Car Supplier Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Car Supplier Page", href ='/information/car_supplier', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='carsupplierprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Car Supplier First Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carsupplierprofile_firstname',
                                placeholder="First Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                

                dbc.Row(
                    [
                        dbc.Label("Car Supplier Middle Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carsupplierprofile_middlename',
                                placeholder="Middle Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Car Supplier Last Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carsupplierprofile_lastname',
                                placeholder="Last Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Car Supplier Phone Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='carsupplierprofile_phonenumber',
                                placeholder="Phone number"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Car Supplier Address", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carsupplierprofile_address',
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
                                    id='carsupplierprofile_removerecord',
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
                    id='carsupplierprofile_removerecord_div'
                ),
            ]
        ),
        dbc.Button(
            'Submit',
            id='carsupplierprofile_submit',
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
                    ], id='carsupplierprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/information/car_supplier',  # Clicking this would lead to a change of pages
                        id = 'carsupplierprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='carsupplierprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)



# # this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
# @app.callback(
#     [
#         Output(component_id='carsupplierprofile_toload', component_property='data'),
#         Output(component_id='carsupplierprofile_removerecord_div', component_property='style')
#     ],
#     [
#         Input(component_id='url', component_property='pathname')
#     ],
#     [
#         State(component_id='url', component_property='search')  # add this search component to the State
#     ]
# )

# def carsupplierprofile_toloadvalue(pathname, search):
#     if pathname == '/information/car_suppliers/car_supplier_profile':
#         # # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         carsupplierprofile_toload = 1 if create_mode == 'edit' else 0
#         removediv_style = {'display': 'none'} if not carsupplierprofile_toload else None
#     else:
#         raise PreventUpdate
#     return [carsupplierprofile_toload, removediv_style]




# # this callback is focused on the submit button
# @app.callback(
#     [
#         # dbc.Alert Properties
#         Output(component_id='carsupplierprofile_alert', component_property='color'),
#         Output(component_id='carsupplierprofile_alert', component_property='children'),
#         Output(component_id='carsupplierprofile_alert', component_property='is_open'),
#         # dbc.Modal Properties
#         Output(component_id='carsupplierprofile_successmodal', component_property='is_open'),
#         # Output(component_id='carsupplierprofile_feedback_message', component_property='children'),
#         # Output(component_id='carsupplierprofile_btn_modal', component_property='href')
#     ],
#     [
#         # For buttons, the property n_clicks
#         Input(component_id='carsupplierprofile_submit', component_property='n_clicks')     #ok
#     ],
#     [
#         # The values of the fields are States
#         # They are required in this process but they
#         # do not trigger this callback
#         State(component_id='carsupplierprofile_firstname', component_property='value'),    #field 1 - first name
#         State(component_id='carsupplierprofile_middlename', component_property='value'),   #field 2 - middle name
#         State(component_id='carsupplierprofile_lastname', component_property='value'),      #field 3 - last name
#         State(component_id='carsupplierprofile_phonenumber', component_property='value'),   #field 4 - phone number
#         State(component_id='carsupplierprofile_address', component_property='value'),   
#         State(component_id='url', component_property='search'),
#         State(component_id='carsupplierprofile_removerecord', component_property='value')
#     ]
# )

# def carsuppliersprofile_saveprofile(submitbtn, carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, search, carsupplierprofile_removerecord):
#     ctx = dash.callback_context
#     # The ctx filter -- ensures that only a change in url will activate this callback
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'carsupplierprofile_submit' and submitbtn:
#             # the submitbtn condition checks if the callback was indeed activated by a click
#             # and not by having the submit button appear in the layout
#             # Set default outputs
#             alert_open = False
#             modal_open = False
#             alert_color = ''
#             alert_text = ''
#             # We need to check inputs
#             if not carsupplierprofile_firstname:  # If title is blank, not title = True
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s first name.'
#             elif not carsupplierprofile_middlename:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s middle name.'
#             elif not carsupplierprofile_lastname:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s last name.'
#             elif not carsupplierprofile_phonenumber:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s phone number.'
            
#             elif not carsupplierprofile_address:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s address.'
    
#             else:  # all inputs are valid
#                 # Add the data into the db
#                 parsed = urlparse(search)
#                 create_mode = parse_qs(parsed.query)['mode'][0]
#                 if create_mode == 'add':
#                     sql = '''
#                     INSERT INTO car_supplier (csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address, car_supplier_delete_ind)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     '''
#                     values = [carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, False]
#                     db.modifydatabase(sql, values)

#                     # feedbackmessage = "Movie has been updated"
#                     # okay_href='/information/car_suppliers'
#                     # If this is successful, we want the successmodal to show
#                     modal_open = True

#                 elif create_mode == 'edit':
#                     parsed = urlparse(search)
#                     csupplierid = parse_qs(parsed.query)['id'][0]
#                     sql = '''
#                     UPDATE car_supplier
#                     SET
#                         csupplier_fn = %s,
#                         csupplier_mn = %s,
#                         csupplier_ln = %s,
#                         csupplier_phone_number = %s,
#                         csupplier_address = %s,
#                         car_supplier_delete_ind = %s
#                     WHERE
#                         csupplier_id = %s
#                     '''
#                     to_delete = bool(carsupplierprofile_removerecord)
#                     values = [carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, to_delete, csupplierid]
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
#         Output(component_id='carsupplierprofile_firstname', component_property='value'),    
#         Output(component_id='carsupplierprofile_middlename', component_property='value'),   
#         Output(component_id='carsupplierprofile_lastname', component_property='value'),      
#         Output(component_id='carsupplierprofile_phonenumber', component_property='value'), 
#         Output(component_id='carsupplierprofile_address', component_property='value'),
#     ],
#     [
#         # Our trigger is if the dcc.Store object changes its value
#         # This is how you check a change in value for a dcc.Store
#         Input(component_id='carsupplierprofile_toload', component_property='modified_timestamp')       # ok
#     ],
#     [
#         # We need the following to proceed
#         # Note that the value of the dcc.Store object is in
#         # the ‘data’ property, and not in the ‘modified_timestamp’ property
#         State(component_id='carsupplierprofile_toload', component_property='data'),                    # ok 
#         State(component_id='url', component_property='search'),                                         # ok 
#     ]
# )

# def carsupplierprofile_loadprofile(timestamp, carsupplierprofile_toload, search):
#     if carsupplierprofile_toload:  # check if toload = 1
#         # Get movieid value from the search parameters
#         parsed = urlparse(search)
#         csupplier_id = parse_qs(parsed.query)['id'][0]
#         # Query from db
#         sql = """
#         SELECT csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address
#         FROM car_supplier
#         WHERE csupplier_id = %s
#         """
#         values = [csupplier_id]
#         col = ['csupplier_fn', 'csupplier_mn', 'csupplier_ln', 'csupplier_phone_number', 'csupplier_address']
#         df = db.querydatafromdatabase(sql, values, col)
#         csupplier_fn = df['csupplier_fn'][0]
#         csupplier_mn = df['csupplier_mn'][0]
#         csupplier_ln = df['csupplier_ln'][0]
#         csupplier_phone_number = df['csupplier_phone_number'][0]
#         csupplier_address = df['csupplier_address'][0]
#         return [csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address]
#     else:
#         raise PreventUpdate

# this callback is used to make carsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='carsupplierprofile_toload', component_property='data'),
        Output(component_id='carsupplierprofile_removerecord_div', component_property='style')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def carsupplierprofile_toloadvalue(pathname, search):
    if pathname == '/information/car_supplier/car_supplier_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        carsupplierprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not carsupplierprofile_toload else None
    else:
        raise PreventUpdate
    return [carsupplierprofile_toload, removediv_style]




# this callback is focused on the submit button
@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='carsupplierprofile_alert', component_property='color'),
        Output(component_id='carsupplierprofile_alert', component_property='children'),
        Output(component_id='carsupplierprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='carsupplierprofile_successmodal', component_property='is_open'),
        # Output(component_id='carsupplierprofile_feedback_message', component_property='children'),
        # Output(component_id='carsupplierprofile_btn_modal', component_property='href')
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='carsupplierprofile_submit', component_property='n_clicks')     #ok
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='carsupplierprofile_firstname', component_property='value'),    #field 1 - first name
        State(component_id='carsupplierprofile_middlename', component_property='value'),   #field 2 - middle name
        State(component_id='carsupplierprofile_lastname', component_property='value'),      #field 3 - last name
        State(component_id='carsupplierprofile_phonenumber', component_property='value'),   #field 4 - phone number
        State(component_id='carsupplierprofile_address', component_property='value'),   
        State(component_id='url', component_property='search'),
        State(component_id='carsupplierprofile_removerecord', component_property='value')
    ]
)

def carsuppliersprofile_saveprofile(submitbtn, carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, search, carsupplierprofile_removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'carsupplierprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not carsupplierprofile_firstname:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s first name.'
            elif not carsupplierprofile_middlename:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s middle name.'
            elif not carsupplierprofile_lastname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s last name.'
            elif not carsupplierprofile_phonenumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s phone number.'
            
            elif not carsupplierprofile_address:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s address.'
    
            else:  # all inputs are valid
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    try:
                        sql = '''
                        INSERT INTO car_supplier (csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address, car_supplier_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        values = [carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, False]
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
                    csupplierid = parse_qs(parsed.query)['id'][0]

                    try:
                        sql = '''
                        UPDATE car_supplier
                        SET
                            csupplier_fn = %s,
                            csupplier_mn = %s,
                            csupplier_ln = %s,
                            csupplier_phone_number = %s,
                            csupplier_address = %s,
                            car_supplier_delete_ind = %s
                        WHERE
                            csupplier_id = %s
                        '''
                        to_delete = bool(carsupplierprofile_removerecord)
                        values = [carsupplierprofile_firstname, carsupplierprofile_middlename, carsupplierprofile_lastname, carsupplierprofile_phonenumber, carsupplierprofile_address, to_delete, csupplierid]
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
        Output(component_id='carsupplierprofile_firstname', component_property='value'),    
        Output(component_id='carsupplierprofile_middlename', component_property='value'),   
        Output(component_id='carsupplierprofile_lastname', component_property='value'),      
        Output(component_id='carsupplierprofile_phonenumber', component_property='value'), 
        Output(component_id='carsupplierprofile_address', component_property='value'),
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='carsupplierprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='carsupplierprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def carsupplierprofile_loadprofile(timestamp, carsupplierprofile_toload, search):
    if carsupplierprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        csupplier_id = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
        SELECT csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address
        FROM car_supplier
        WHERE csupplier_id = %s
        """
        values = [csupplier_id]
        col = ['csupplier_fn', 'csupplier_mn', 'csupplier_ln', 'csupplier_phone_number', 'csupplier_address']
        df = db.querydatafromdatabase(sql, values, col)
        csupplier_fn = df['csupplier_fn'][0]
        csupplier_mn = df['csupplier_mn'][0]
        csupplier_ln = df['csupplier_ln'][0]
        csupplier_phone_number = df['csupplier_phone_number'][0]
        csupplier_address = df['csupplier_address'][0]
        return [csupplier_fn, csupplier_mn, csupplier_ln, csupplier_phone_number, csupplier_address]
    else:
        raise PreventUpdate