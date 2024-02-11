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

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='carprofile_toload', storage_type='memory', data=1)
            ]
        ),
        html.H2('Car Details'),  # Page Header
        html.Hr(),
        dbc.Alert(id='carprofile_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Car Model", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='carprofile_model',
                                placeholder="Car Model"
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
                                id='carprofile_platenumber',
                                placeholder="Car Platenumber"
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
                                id='carprofile_productionyear',
                                placeholder="Car Production Year"
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
                                    id='carprofile_carcondition',
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
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label("Wish to delete?", width=1),
                            dbc.Col(
                                dbc.Checklist(
                                    id='carprofile_removerecord',
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
                    id='carprofile_removerecord_div'
                ),
            ]
        ),
        dbc.Button(
            'Submit',
            id='carprofile_submit',
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
                    ], id='carprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/information/car',  # Clicking this would lead to a change of pages
                        id = 'carprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='carprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)



# this callback is used to make repairpartprofile_toload = 1 or 0 (this will be used later on in other callbacks)
@app.callback(
    [
        Output(component_id='carprofile_toload', component_property='data'),
        Output(component_id='carprofile_removerecord_div', component_property='style'),
        Output(component_id='carprofile_carcondition', component_property='options')
    ],
    [
        Input(component_id='url', component_property='pathname')
    ],
    [
        State(component_id='url', component_property='search')  # add this search component to the State
    ]
)

def carprofile_toloadvalue(pathname, search):
    if pathname == '/information/car/car_profile':
        # # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        carprofile_toload = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not carprofile_toload else None
    else:
        raise PreventUpdate
    return [carprofile_toload, removediv_style]

# this callback is focused on the submit button
@app.callback(
    [
        # dbc.Alert Properties
        Output(component_id='carprofile_alert', component_property='color'),
        Output(component_id='carprofile_alert', component_property='children'),
        Output(component_id='carprofile_alert', component_property='is_open'),
        # dbc.Modal Properties
        Output(component_id='carprofile_successmodal', component_property='is_open'),
        # Output(component_id='repairpartprofile_feedback_message', component_property='children'),
        # Output(component_id='repairpartprofile_btn_modal', component_property='href')
    ],
    [
        # For buttons, the property n_clicks
        Input(component_id='carprofile_submit', component_property='n_clicks')     #ok
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State(component_id='carprofile_model', component_property='value'),    
        State(component_id='carprofile_platenumber', component_property='value'),   
        State(component_id='carprofile_productionyear', component_property='value'), 
        State(component_id='carprofile_carcondition', component_property='value'),  
        State(component_id='url', component_property='search'),
        State(component_id='carprofile_removerecord', component_property='value')
    ]
)

def carprofile_saveprofile(submitbtn, carprofile_model, carprofile_platenumber, carprofile_productionyear,carprofile_carcondition, search, carprofile_removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'carprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            # We need to check inputs
            if not carprofile_model:  # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the part\'s brand name.'
            elif not carprofile_platenumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the part\'s name.'
            elif not carprofile_productionyear:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please provide the part\'s value.'
            else:  # all inputs are valid
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    sql = '''
                    INSERT INTO car (car_model, car_plate_number, car_production_year, car_purchase_condition_id, car_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
                    '''
                    values = [carprofile_model,carprofile_platenumber,carprofile_productionyear,carprofile_carcondition, False]
                    db.modifydatabase(sql, values)

                    # feedbackmessage = "Movie has been updated"
                    # okay_href='/information/repair_part_suppliers'
                    # If this is successful, we want the successmodal to show
                    modal_open = True

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    car_id = parse_qs(parsed.query)['id'][0]
                    sql = '''
                    UPDATE repair_part
                    SET
                        car_model = %s,
                        car_plate_number = %s,
                        car_production_year = %s,
                        car_delete_ind = %s,
                        car_purchase_condition_id = %s
                    WHERE
                        car_id = %s
                    '''
                    to_delete = bool(carprofile_removerecord)
                    values = [carprofile_model, carprofile_platenumber, carprofile_productionyear,carprofile_carcondition, to_delete, car_id]
                    db.modifydatabase(sql, values)
                    modal_open = True

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
        Output(component_id='carprofile_model', component_property='value'),    
        Output(component_id='carprofile_platenumber', component_property='value'),   
        Output(component_id='carprofile_productionyear', component_property='value'),
        Output(component_id='carprofile_carcondition', component_property='value'),      
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input(component_id='carprofile_toload', component_property='modified_timestamp')       # ok
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State(component_id='carprofile_toload', component_property='data'),                    # ok 
        State(component_id='url', component_property='search'),                                         # ok 
    ]
)

def carprofile_loadprofile(timestamp, carprofile_toload, search):
    if carprofile_toload:  # check if toload = 1
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        car_id = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
        SELECT car_model, car_plate_number, car_production_year,car_purchase_condition_id
        FROM car
        WHERE car_id = %s
        """
        values = [car_id]
        col = ['car_model', 'car_plate_number', 'car_production_year']
        df = db.querydatafromdatabase(sql, values, col)
        car_model = df['car_model'][0]
        car_plate_number = df['car_plate_number'][0]
        car_production_year = df['car_production_year'][0]
        car_purchase_condition_id = df['car_purchase_condition_id']
        return [car_model, car_plate_number, car_production_year, car_purchase_condition_id]
    else:
        raise PreventUpdate
    
