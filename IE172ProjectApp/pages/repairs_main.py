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
#         html.H2('Repair Parts Details and Tracking Car Repairs'), # Page Header
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
#             dbc.CardImg(src="/assets/5.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Repair Part", className="card-title"),
#                     dcc.Markdown(
#                                 """
#                                 Add details of new repair part by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicates to ensure that records are not doubled.
#                                 """
#                             ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/information/repair_part"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardImg(src="/assets/5.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Car Repair", className="card-title"),
#                     dcc.Markdown(
#                                 """
#                                 Add details of new repair part by clicking the button below.
                                
#                                 **NOTE:** Make sure there are no duplicates to ensure that records are not doubled.
#                                 """
#                             ),
#                     dbc.Button(
#                         "Click here", color="warning", className="mt-auto", href="/car_repair"
#                     ),
#                 ]
#             )
#         ),
#      dbc.Card(
#          dbc.CardImg(src="/assets/5.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Repair Part Purchase", className="card-title"),
#                     dcc.Markdown(
#                                 """
#                                 Add the repair parts you purchase by clicking the button below.
                                
#                                 **NOTE:** Add the repair parts details to the repair part information provision first if the order involves a new repair part.
#                                 """
#                             ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/transactions/repair_part_order"
#                     ),
#                 ]
#             )
#         ),
       
#     ]
# )
#     ]
# )


layout = html.Div(
    [
        html.H2('Repair Parts Details and Tracking Car Repairs'),  # Page Header
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
                        dbc.CardImg(src="/assets/12.png", top=True),  # Image above the card
                        dbc.CardBody(
                            [
                                html.H5("Repair Part", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new repair part by clicking the button below.
                                    
                                    **NOTE:** Make sure there are no duplicates to ensure that records are not doubled.
                                    """
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/information/repair_part"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/13.png", top=True),  # Image above the card
                        dbc.CardBody(
                            [
                                html.H5("Car Repair", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add details of new car repair by clicking the button below.
                                    
                                    **NOTE:** Make sure there are no duplicates to ensure that records are not doubled.
                                    """
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/car_repair"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/5.png", top=True),  # Image above the card
                        dbc.CardBody(
                            [
                                html.H5("Repair Part Purchase", className="card-title"),
                                dcc.Markdown(
                                    """
                                    Add the repair parts you purchase by clicking the button below.
                                    
                                    **NOTE:** Add the repair parts details to the repair part information provision first if the order involves a new repair part.
                                    """
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/transactions/repair_part_order"
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)