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
                dcc.Store(id='repairpartsupplierprofile_toload', storage_type='memory', data=1)
            ]
        ),
        html.H2('Repair Part Supplier Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Repair Part Supplier Page", href ='/information/repair_part_supplier', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='repairpartsupplierprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Repair Parts Supplier First Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='repairpartsupplierprofile_firstname',
                                placeholder="First Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                

                dbc.Row(
                    [
                        dbc.Label("Repair Parts Supplier Middle Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='repairpartsupplierprofile_middlename',
                                placeholder="Middle Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Repair Parts Supplier Last Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='repairpartsupplierprofile_lastname',
                                placeholder="Last Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Repair Parts Supplier Phone Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='repairpartsupplierprofile_phonenumber',
                                placeholder="Phone number"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Label("Repair Parts Supplier Address", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='repairpartsupplierprofile_address',
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
                                    id='repairpartsupplierprofile_removerecord',
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
                    id='repairpartsupplierprofile_removerecord_div'
                ),
            ]
        ),
        dbc.Button(
            'Submit',
            id='repairpartsupplierprofile_submit',
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
                    ], id='repairpartsupplierprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/information/repair_part_supplier',  # Clicking this would lead to a change of pages
                        id = 'repairpartsupplierprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='repairpartsupplierprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)



# # this callback is used to make repairpartsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
# @app.callback(
#     [
#         Output(component_id='repairpartsupplierprofile_toload', component_property='data'),
#         Output(component_id='repairpartsupplierprofile_removerecord_div', component_property='style')
#     ],
#     [
#         Input(component_id='url', component_property='pathname')
#     ],
#     [
#         State(component_id='url', component_property='search')  # add this search component to the State
#     ]
# )

# def repairpartsupplierprofile_toloadvalue(pathname, search):
#     if pathname == '/information/repair_part_supplier/repair_part_supplier_profile':
#         # # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         repairpartsupplierprofile_toload = 1 if create_mode == 'edit' else 0
#         removediv_style = {'display': 'none'} if not repairpartsupplierprofile_toload else None
#     else:
#         raise PreventUpdate
#     return [repairpartsupplierprofile_toload, removediv_style]




# # this callback is focused on the submit button
# @app.callback(
#     [
#         # dbc.Alert Properties
#         Output(component_id='repairpartsupplierprofile_alert', component_property='color'),
#         Output(component_id='repairpartsupplierprofile_alert', component_property='children'),
#         Output(component_id='repairpartsupplierprofile_alert', component_property='is_open'),
#         # dbc.Modal Properties
#         Output(component_id='repairpartsupplierprofile_successmodal', component_property='is_open'),
#         # Output(component_id='repairpartsupplierprofile_feedback_message', component_property='children'),
#         # Output(component_id='repairpartsupplierprofile_btn_modal', component_property='href')
#     ],
#     [
#         # For buttons, the property n_clicks
#         Input(component_id='repairpartsupplierprofile_submit', component_property='n_clicks')     #ok
#     ],
#     [
#         # The values of the fields are States
#         # They are required in this process but they
#         # do not trigger this callback
#         State(component_id='repairpartsupplierprofile_firstname', component_property='value'),    #field 1 - first name
#         State(component_id='repairpartsupplierprofile_middlename', component_property='value'),   #field 2 - middle name
#         State(component_id='repairpartsupplierprofile_lastname', component_property='value'),      #field 3 - last name
#         State(component_id='repairpartsupplierprofile_phonenumber', component_property='value'),   #field 4 - phone number
#         State(component_id='repairpartsupplierprofile_address', component_property='value'),   
#         State(component_id='url', component_property='search'),
#         State(component_id='repairpartsupplierprofile_removerecord', component_property='value')
#     ]
# )

# def repairpartsuppliersprofile_saveprofile(submitbtn, repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, search, repairpartsupplierprofile_removerecord):
#     ctx = dash.callback_context
#     # The ctx filter -- ensures that only a change in url will activate this callback
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'repairpartsupplierprofile_submit' and submitbtn:
#             # the submitbtn condition checks if the callback was indeed activated by a click
#             # and not by having the submit button appear in the layout
#             # Set default outputs
#             alert_open = False
#             modal_open = False
#             alert_color = ''
#             alert_text = ''
#             # We need to check inputs
#             if not repairpartsupplierprofile_firstname:  # If title is blank, not title = True
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s first name.'
#             elif not repairpartsupplierprofile_middlename:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s middle name.'
#             elif not repairpartsupplierprofile_lastname:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s last name.'
#             elif not repairpartsupplierprofile_phonenumber:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s phone number.'
#             elif not repairpartsupplierprofile_address:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the supplier\'s address.'
    
#             else:  # all inputs are valid
#                 # Add the data into the db
#                 parsed = urlparse(search)
#                 create_mode = parse_qs(parsed.query)['mode'][0]
#                 if create_mode == 'add':
#                     sql = '''
#                     INSERT INTO repair_part_supplier (supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address, supplier_delete_ind)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     '''
#                     values = [repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, False]
#                     db.modifydatabase(sql, values)

#                     # feedbackmessage = "Movie has been updated"
#                     # okay_href='/information/repair_part_suppliers'
#                     # If this is successful, we want the successmodal to show
#                     modal_open = True

#                 elif create_mode == 'edit':
#                     parsed = urlparse(search)
#                     supplierid = parse_qs(parsed.query)['id'][0]
#                     sql = '''
#                     UPDATE repair_part_supplier
#                     SET
#                         supplier_fn = %s,
#                         supplier_mn = %s,
#                         supplier_ln = %s,
#                         supplier_phone_number = %s,
#                         supplier_address = %s,
#                         supplier_delete_ind = %s
#                     WHERE
#                         supplier_id = %s
#                     '''
#                     to_delete = bool(repairpartsupplierprofile_removerecord)
#                     values = [repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, to_delete, supplierid]
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
#         Output(component_id='repairpartsupplierprofile_firstname', component_property='value'),    
#         Output(component_id='repairpartsupplierprofile_middlename', component_property='value'),   
#         Output(component_id='repairpartsupplierprofile_lastname', component_property='value'),      
#         Output(component_id='repairpartsupplierprofile_phonenumber', component_property='value'), 
#         Output(component_id='repairpartsupplierprofile_address', component_property='value'),
#     ],
#     [
#         # Our trigger is if the dcc.Store object changes its value
#         # This is how you check a change in value for a dcc.Store
#         Input(component_id='repairpartsupplierprofile_toload', component_property='modified_timestamp')       # ok
#     ],
#     [
#         # We need the following to proceed
#         # Note that the value of the dcc.Store object is in
#         # the ‘data’ property, and not in the ‘modified_timestamp’ property
#         State(component_id='repairpartsupplierprofile_toload', component_property='data'),                    # ok 
#         State(component_id='url', component_property='search'),                                         # ok 
#     ]
# )

# def repairpartsupplierprofile_loadprofile(timestamp, repairpartsupplierprofile_toload, search):
#     if repairpartsupplierprofile_toload:  # check if toload = 1
#         # Get movieid value from the search parameters
#         parsed = urlparse(search)
#         supplier_id = parse_qs(parsed.query)['id'][0]
#         # Query from db
#         sql = """
#         SELECT supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address
#         FROM repair_part_supplier
#         WHERE supplier_id = %s
#         """
#         values = [supplier_id]
#         col = ['supplier_fn', 'supplier_mn', 'supplier_ln', 'supplier_phone_number', 'supplier_address']
#         df = db.querydatafromdatabase(sql, values, col)
#         supplier_fn = df['supplier_fn'][0]
#         supplier_mn = df['supplier_mn'][0]
#         supplier_ln = df['supplier_ln'][0]
#         supplier_phone_number = df['supplier_phone_number'][0]
#         supplier_address = df['supplier_address'][0]
#         return [supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address]
#     else:
#         raise PreventUpdate

# this callback is used to make repairpartsuppliersprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='repairpartsupplierprofile_toload', component_property='data'),
        Output(component_id='repairpartsupplierprofile_removerecord_div', component_property='style')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def repairpartsupplierprofile_toloadvalue(pathname, search):
    if pathname == '/information/repair_part_supplier/repair_part_supplier_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        repairpartsupplierprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not repairpartsupplierprofile_toload else None
    else:
        raise PreventUpdate
    return [repairpartsupplierprofile_toload, removediv_style]




# this callback is focused on the submit button
@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='repairpartsupplierprofile_alert', component_property='color'),
        Output(component_id='repairpartsupplierprofile_alert', component_property='children'),
        Output(component_id='repairpartsupplierprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='repairpartsupplierprofile_successmodal', component_property='is_open'),
        # Output(component_id='repairpartsupplierprofile_feedback_message', component_property='children'),
        # Output(component_id='repairpartsupplierprofile_btn_modal', component_property='href')
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='repairpartsupplierprofile_submit', component_property='n_clicks')     #ok
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='repairpartsupplierprofile_firstname', component_property='value'),    #field 1 - first name
        State(component_id='repairpartsupplierprofile_middlename', component_property='value'),   #field 2 - middle name
        State(component_id='repairpartsupplierprofile_lastname', component_property='value'),      #field 3 - last name
        State(component_id='repairpartsupplierprofile_phonenumber', component_property='value'),   #field 4 - phone number
        State(component_id='repairpartsupplierprofile_address', component_property='value'),   
        State(component_id='url', component_property='search'),
        State(component_id='repairpartsupplierprofile_removerecord', component_property='value')
    ]
)

def repairpartsuppliersprofile_saveprofile(submitbtn, repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, search, repairpartsupplierprofile_removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'repairpartsupplierprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not repairpartsupplierprofile_firstname:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s first name.'
            elif not repairpartsupplierprofile_middlename:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s middle name.'
            elif not repairpartsupplierprofile_lastname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s last name.'
            elif not repairpartsupplierprofile_phonenumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the supplier\'s phone number.'
            elif not repairpartsupplierprofile_address:
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
                        INSERT INTO repair_part_supplier (supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address, supplier_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        values = [repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, False]
                        db.modifydatabase(sql, values)

                        # feedbackmessage = "Movie has been updated"
                        # okay_href='/information/repair_part_suppliers'
                        # If this is successful, we want the successmodal to show
                        modal_open = True
                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! Please enter the exact number of digits for landline (8) or mobile number (11).'

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    supplierid = parse_qs(parsed.query)['id'][0]

                    try:
                        sql = '''
                        UPDATE repair_part_supplier
                        SET
                            supplier_fn = %s,
                            supplier_mn = %s,
                            supplier_ln = %s,
                            supplier_phone_number = %s,
                            supplier_address = %s,
                            supplier_delete_ind = %s
                        WHERE
                            supplier_id = %s
                        '''
                        to_delete = bool(repairpartsupplierprofile_removerecord)
                        values = [repairpartsupplierprofile_firstname, repairpartsupplierprofile_middlename, repairpartsupplierprofile_lastname, repairpartsupplierprofile_phonenumber, repairpartsupplierprofile_address, to_delete, supplierid]
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
        Output(component_id='repairpartsupplierprofile_firstname', component_property='value'),    
        Output(component_id='repairpartsupplierprofile_middlename', component_property='value'),   
        Output(component_id='repairpartsupplierprofile_lastname', component_property='value'),      
        Output(component_id='repairpartsupplierprofile_phonenumber', component_property='value'), 
        Output(component_id='repairpartsupplierprofile_address', component_property='value'),
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='repairpartsupplierprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='repairpartsupplierprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def repairpartsupplierprofile_loadprofile(timestamp, repairpartsupplierprofile_toload, search):
    if repairpartsupplierprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        supplier_id = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
        SELECT supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address
        FROM repair_part_supplier
        WHERE supplier_id = %s
        """
        values = [supplier_id]
        col = ['supplier_fn', 'supplier_mn', 'supplier_ln', 'supplier_phone_number', 'supplier_address']
        df = db.querydatafromdatabase(sql, values, col)
        supplier_fn = df['supplier_fn'][0]
        supplier_mn = df['supplier_mn'][0]
        supplier_ln = df['supplier_ln'][0]
        supplier_phone_number = df['supplier_phone_number'][0]
        supplier_address = df['supplier_address'][0]
        return [supplier_fn, supplier_mn, supplier_ln, supplier_phone_number, supplier_address]
    else:
        raise PreventUpdate