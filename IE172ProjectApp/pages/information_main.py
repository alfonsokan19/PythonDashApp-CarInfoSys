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

# layout = html.Div(
#     [
#         html.H2('Information'), # Page Header
#         html.Hr(),
#         html.Br(),
#         html.Div(
#             [
#                 html.Span(
#                     "Go back to the Home Page by clicking the button below! ",
#                 ),
#                 html.Br(),
#                     dbc.Button("Go to Home Page", href ='/home'),
#                 html.Br(),
#             ]
#         ),
#         html.Br(),
#         html.Br(),
#         dbc.CardGroup(
#             [
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Car Suppliers", className="card-title"),
#                     html.P(
#                         "Add details of new car suppliers "
#                         "by clicking the button below."
#                         "NOTE: Make sure there are no duplicate entries "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="success", className="mt-auto", href="/information/car_suppliers"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Customers", className="card-title"),
#                     html.P(
#                         "Add details of new customers "
#                         "by clicking the button below."
#                         "NOTE: Make sure there are no duplicate entries "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="warning", className="mt-auto", href="/information/customer"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Repair Part Suppliers", className="card-title"),
#                     html.P(
#                         "Add details of new repair part suppliers "
#                         "by clicking the button below. "
#                         "NOTE: Make sure there are no duplicate entries "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/information/repair_part_supplier"
#                     ),
#                 ]
#             )
#         ),
#     ]
# ),
#     html.Hr(),
#         dbc.CardGroup(
#             [
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Car", className="card-title"),
#                     html.P(
#                         "Add details of new car "
#                         "by clicking the button below."
#                         "NOTE: Make sure there are no duplicate entries "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="success", className="mt-auto", href="/information/car"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Employee", className="card-title"),
#                     html.P(
#                         "Add details of employees or new employees "
#                         "by clicking the button below."
#                         "NOTE: Make sure there are no duplicate entries "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="warning", className="mt-auto", href="/information/car_repair_staff"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardBody(
#                 [
#                     html.H5("Repair Part", className="card-title"),
#                     html.P(
#                         "Add details of new repair part "
#                         "by clicking the button below."
#                         "NOTE: Make sure there are no duplicates "
#                         "to ensure that records are not doubled.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/information/repair_part"
#                     ),
#                 ]
#             )
#         ),
#     ]
# )
    
#     ]
# )

# layout = html.Div(
#     [
#         html.H2('Information'),  # Page Header
#         html.Hr(),
#         html.Br(),
#         html.Div(
#             [
#                 html.Span(
#                     "Go back to the Home Page by clicking the button below! ",
#                 ),
#                 html.Br(),
#                 dbc.Button("Go to Home Page", href='/home'),
#                 html.Br(),
#             ]
#         ),
#         html.Br(),
#         html.Br(),
#         dbc.CardGroup(
#             [
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Car Suppliers", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of new car suppliers by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="success", className="mt-auto", href="/information/car_suppliers"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Customers", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of new customers by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="warning", className="mt-auto", href="/information/customer"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Repair Part Suppliers", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of new repair part suppliers by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="danger", className="mt-auto", href="/information/repair_part_supplier"
#                             ),
#                         ]
#                     )
#                 ),
#             ]
#         ),
#         html.Hr(),
#         dbc.CardGroup(
#             [
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Car", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of new car by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="success", className="mt-auto", href="/information/car"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Employee", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of employees or new employees by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="warning", className="mt-auto", href="/information/car_repair_staff"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#                     dbc.CardBody(
#                         [
#                             html.H5("Repair Part", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add details of new repair part by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicates to ensure that records are not doubled.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="danger", className="mt-auto", href="/information/repair_part"
#                             ),
#                         ]
#                     )
#                 ),
#             ]
#         )
#     ]
# )



# Common note message for all cards
common_note_message = """
**NOTE:** Make sure there are no duplicate entries to ensure that records are not doubled.
"""

layout = html.Div(
    [
        html.H2('Information'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the Home Page by clicking the button below! ",
                ),
                html.Br(),
                dbc.Button("Go to Home Page", href='/home', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.CardGroup(
            [
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/7.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Car Suppliers", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new car suppliers by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/car_supplier"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/8.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Customers", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new customers by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/customer"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/9.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Repair Part Suppliers", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new repair part suppliers by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/repair_part_supplier"
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        html.Hr(),
        dbc.CardGroup(
            [
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/10.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Car", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new cars by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/car"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/11.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Employee", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of employees or new employees by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/car_repair_staff"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/12.png", top=True),
                        dbc.CardBody(
                            [
                                html.H5("Repair Part", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new repair parts by clicking the button below.
                                    """ + common_note_message
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/repair_part"
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)