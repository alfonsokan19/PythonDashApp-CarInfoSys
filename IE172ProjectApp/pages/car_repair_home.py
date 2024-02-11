import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Car Repairs"),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Repair Home Page", href ='/repairs/repairs_main', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Car Repairs Management")),
                dbc.CardBody(
                    [
                        dbc.Button('+ Add Car Repair', color="primary", href='/car_repair/car_repair_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Records", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search PO ID", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="repair_filter_repairid", placeholder="Enter Repair ID"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "No records to show",
                                    id='repair_records'
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)


# @app.callback(
#     [
#         Output('repair_records', 'children')
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('repair_filter_repairid', 'value'), # changing the text box value should update the table
#     ]
# )
# def moviehome_loadpolist(pathname, searchterm):
#     if pathname == '/car_repair':
        
#         # 1. SQL Query to get the records
#         # added the movie_id for the query since we need it
#         # to generate the hyperlinks
#         sql = """ 
#         SELECT repair_id, car_model, car_plate_number, repair_status_label, to_char(repair_date, 'DD Mon YYYY')
#         FROM car_repair cr
#         INNER JOIN car c ON c.car_id = cr.car_id
#         INNER JOIN repair_status rs ON cr.repair_status_id = rs.repair_status_id
#         WHERE NOT car_repair_delete_ind
#         """
#         values = [] 
#         cols = ['Repair ID', 'Car Model', 'Car Plate Number', 'Repair Status', 'Date Created']
        
        
#         # Filter
#         if searchterm:
#             sql += " AND repair_id = %s"
            
#             values += [searchterm]

#         df = db.querydatafromdatabase(sql, values, cols)
        
#         if df.shape: 
            
#             # Create the buttons as a list based on the ID
#             buttons = []
#             for repair_id in df['Repair ID']:
#                 buttons += [
#                     html.Div(
#                         dbc.Button('Edit', href=f'car_repair/car_repair_profile?mode=edit&id={repair_id}',
#                                    size='sm', color='warning'),
#                         style={'text-align': 'center'}
#                     )
#                 ]
            
#             df['Action'] = buttons
            
#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
#                     hover=True, size='sm', style={'text-align': 'right'})
#             return [table]
#         else:
#             return ["No records to show"]
        
#     else:
#         raise PreventUpdate

@app.callback(
    [
        Output('repair_records', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('repair_filter_repairid', 'value'), # changing the text box value should update the table
    ]
)
def moviehome_loadpolist(pathname, searchterm):
    if pathname == '/car_repair':
        
        # 1. SQL Query to get the records
        # added the movie_id for the query since we need it
        # to generate the hyperlinks
        sql = """ 
        SELECT repair_id, car_model, car_plate_number, repair_status_label, to_char(repair_date, 'DD Mon YYYY')
        FROM car_repair cr
        INNER JOIN car c ON c.car_id = cr.car_id
        INNER JOIN repair_status rs ON cr.repair_status_id = rs.repair_status_id
        WHERE NOT car_repair_delete_ind
        """
        values = [] 
        cols = ['Repair ID', 'Car Model', 'Car Plate Number', 'Repair Status', 'Date Created']
        
        
        # Filter
        if searchterm:
            sql += " AND repair_id = %s"
            
            values += [searchterm]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            # Create the buttons as a list based on the ID
            buttons = []
            for repair_id in df['Repair ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'car_repair/car_repair_profile?mode=edit&id={repair_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm', style={'text-align': 'center'})
            return [table]
        else:
            return ["No records to show"]
        
    else:
        raise PreventUpdate