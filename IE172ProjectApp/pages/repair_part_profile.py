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
                dcc.Store(id='repairpartprofile_toload', storage_type='memory', data=1)
            ]
        ),
        html.H2('Repair Part Details'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Repair Part Page", href ='/information/repair_part', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Alert(id='repairpartprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                # dbc.Row(
                #     [
                #         dbc.Label("Field 1", width=1),
                #         dbc.Col(
                #             dbc.Input(
                #                 type='text',
                #                 id='repairpartprofile_brandname',
                #                 placeholder="Brand of Part"
                #             ),
                #             width=5
                #         )
                #     ],
                #     className='mb-3'
                # ),
                dbc.Row(
                    [
                        dbc.Label("Name of Part", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='repairpartprofile_partname',
                                placeholder="Name of Part"
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
                                    id='repairpartprofile_removerecord',
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
                    id='repairpartprofile_removerecord_div'
                ),
            ]
        ),
        dbc.Button(
            'Submit',
            id='repairpartprofile_submit',
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
                    ], id='repairpartprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/information/repair_part',  # Clicking this would lead to a change of pages
                        id = 'repairpartprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='repairpartprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)



# # this callback is used to make repairpartprofile_toload = 1 or 0 (this will be used later on in other callbacks)
# @app.callback(
#     [
#         Output(component_id='repairpartprofile_toload', component_property='data'),
#         Output(component_id='repairpartprofile_removerecord_div', component_property='style')
#     ],
#     [
#         Input(component_id='url', component_property='pathname')
#     ],
#     [
#         State(component_id='url', component_property='search')  # add this search component to the State
#     ]
# )

# def repairpartprofile_toloadvalue(pathname, search):
#     if pathname == '/information/repair_part/repair_part_profile':
#         # # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         repairpartprofile_toload = 1 if create_mode == 'edit' else 0
#         removediv_style = {'display': 'none'} if not repairpartprofile_toload else None
#     else:
#         raise PreventUpdate
#     return [repairpartprofile_toload, removediv_style]

# # this callback is focused on the submit button
# @app.callback(
#     [
#         # dbc.Alert Properties
#         Output(component_id='repairpartprofile_alert', component_property='color'),
#         Output(component_id='repairpartprofile_alert', component_property='children'),
#         Output(component_id='repairpartprofile_alert', component_property='is_open'),
#         # dbc.Modal Properties
#         Output(component_id='repairpartprofile_successmodal', component_property='is_open'),
#         # Output(component_id='repairpartprofile_feedback_message', component_property='children'),
#         # Output(component_id='repairpartprofile_btn_modal', component_property='href')
#     ],
#     [
#         # For buttons, the property n_clicks
#         Input(component_id='repairpartprofile_submit', component_property='n_clicks')     #ok
#     ],
#     [
#         # The values of the fields are States
#         # They are required in this process but they
#         # do not trigger this callback
#         # State(component_id='repairpartprofile_brandname', component_property='value'),    
#         State(component_id='repairpartprofile_partname', component_property='value'),   
#         State(component_id='url', component_property='search'),
#         State(component_id='repairpartprofile_removerecord', component_property='value')
#     ]
# )

# def repairpartprofile_saveprofile(submitbtn, repairpartprofile_partname, search, repairpartprofile_removerecord):
#     ctx = dash.callback_context
#     # The ctx filter -- ensures that only a change in url will activate this callback
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'repairpartprofile_submit' and submitbtn:
#             # the submitbtn condition checks if the callback was indeed activated by a click
#             # and not by having the submit button appear in the layout
#             # Set default outputs
#             alert_open = False
#             modal_open = False
#             alert_color = ''
#             alert_text = ''
#             # We need to check inputs
#             # if not repairpartprofile_brandname:  # If title is blank, not title = True
#             #     alert_open = True
#             #     alert_color = 'danger'
#             #     alert_text = 'Check your inputs. Please provide the part\'s brand name.'
#             if not repairpartprofile_partname:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = 'Check your inputs. Please provide the part\'s name.'
#             else:  # all inputs are valid
#                 # Add the data into the db
#                 parsed = urlparse(search)
#                 create_mode = parse_qs(parsed.query)['mode'][0]
#                 if create_mode == 'add':
#                     sql = '''
#                     INSERT INTO repair_part (item_name, item_delete_ind)
#                     VALUES (%s, %s)
#                     '''
#                     values = [repairpartprofile_partname, False]
#                     db.modifydatabase(sql, values)

#                     # feedbackmessage = "Movie has been updated"
#                     # okay_href='/information/repair_part_suppliers'
#                     # If this is successful, we want the successmodal to show
#                     modal_open = True

#                 elif create_mode == 'edit':
#                     parsed = urlparse(search)
#                     item_id = parse_qs(parsed.query)['id'][0]
#                     sql = '''
#                     UPDATE repair_part
#                     SET
#                         item_name = %s,
#                         item_delete_ind = %s
#                     WHERE
#                         item_id = %s
#                     '''
#                     to_delete = bool(repairpartprofile_removerecord)
#                     values = [repairpartprofile_partname, to_delete, item_id]
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
#         Output(component_id='repairpartprofile_brandname', component_property='value'),    
#         Output(component_id='repairpartprofile_partname', component_property='value'),   
#         Output(component_id='repairpartprofile_value', component_property='value'),      
#     ],
#     [
#         # Our trigger is if the dcc.Store object changes its value
#         # This is how you check a change in value for a dcc.Store
#         Input(component_id='repairpartprofile_toload', component_property='modified_timestamp')       # ok
#     ],
#     [
#         # We need the following to proceed
#         # Note that the value of the dcc.Store object is in
#         # the ‘data’ property, and not in the ‘modified_timestamp’ property
#         State(component_id='repairpartprofile_toload', component_property='data'),                    # ok 
#         State(component_id='url', component_property='search'),                                         # ok 
#     ]
# )

# def repairpartprofile_loadprofile(timestamp, repairpartprofile_toload, search):
#     if repairpartprofile_toload:  # check if toload = 1
#         # Get movieid value from the search parameters
#         parsed = urlparse(search)
#         item_id = parse_qs(parsed.query)['id'][0]
#         # Query from db
#         sql = """
#         SELECT item_name
#         FROM repair_part
#         WHERE item_id = %s
#         """
#         values = [item_id]
#         col = [ 'part_name']
#         df = db.querydatafromdatabase(sql, values, col)
#         item_name = df['item_name'][0]
#         return [item_name]
#     else:
#         raise PreventUpdate

# this callback is used to make repairpartprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='repairpartprofile_toload', component_property='data'),
        Output(component_id='repairpartprofile_removerecord_div', component_property='style')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def repairpartprofile_toloadvalue(pathname, search):
    if pathname == '/information/repair_part/repair_part_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        repairpartprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not repairpartprofile_toload else None
    else:
        raise PreventUpdate
    return [repairpartprofile_toload, removediv_style]

# this callback is focused on the submit button
@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='repairpartprofile_alert', component_property='color'),
        Output(component_id='repairpartprofile_alert', component_property='children'),
        Output(component_id='repairpartprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='repairpartprofile_successmodal', component_property='is_open'),
        # Output(component_id='repairpartprofile_feedback_message', component_property='children'),
        # Output(component_id='repairpartprofile_btn_modal', component_property='href')
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='repairpartprofile_submit', component_property='n_clicks')     #ok
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback 
        State(component_id='repairpartprofile_partname', component_property='value'),   
        State(component_id='url', component_property='search'),
        State(component_id='repairpartprofile_removerecord', component_property='value')
    ]
)

def repairpartprofile_saveprofile(submitbtn, repairpartprofile_partname, search, repairpartprofile_removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'repairpartprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs

            if not repairpartprofile_partname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the part\'s name.'
            else:  # all inputs are valid
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    try:
                        sql = '''
                            INSERT INTO repair_part (item_name, item_delete_ind)
                            VALUES (%s, %s)
                            '''
                        values = [repairpartprofile_partname, False]
                        db.modifydatabase(sql, values)

                        # feedbackmessage = "Movie has been updated"
                        # okay_href='/information/repair_part_suppliers'
                        # If this is successful, we want the successmodal to show
                        modal_open = True

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! You already listed this repair part before.'

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    item_id = parse_qs(parsed.query)['id'][0]

                    try:
                        sql = '''
                        UPDATE repair_part
                        SET
                            item_name = %s,
                            item_delete_ind = %s
                        WHERE
                            item_id = %s
                        '''
                        to_delete = bool(repairpartprofile_removerecord)
                        values = [repairpartprofile_partname, to_delete, item_id]
                        db.modifydatabase(sql, values)
                        modal_open = True
                    

                    except DatabaseError as e:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Error! You already listed this repair part before.'

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
        Output(component_id='repairpartprofile_partname', component_property='value'),     
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='repairpartprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='repairpartprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def repairpartprofile_loadprofile(timestamp, repairpartprofile_toload, search):
    if repairpartprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        item_id = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
        SELECT item_name
        FROM repair_part
        WHERE item_id = %s
        """
        values = [item_id]
        col = ['item_name']
        df = db.querydatafromdatabase(sql, values, col)
        item_name = df['item_name'][0]
        return [item_name]
    else:
        raise PreventUpdate