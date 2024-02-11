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

# store the layout objects into a variable named layout
# layout = html.Div(
#     [
#         html.H2('Report Generation'), # Page Header
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
#             dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Car Purchase", className="card-title"),
#                     html.P(
#                         "See critical car-purchase-related data "
#                         "by clicking the button below.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="success", className="mt-auto", href="/report/car_purchase"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Car Sale", className="card-title"),
#                     html.P(
#                         "See critical car-sale-related data "
#                         "by clicking the button below.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="warning", className="mt-auto", href="/report/car_sale"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Repair Part Purchase", className="card-title"),
#                     html.P(
#                         "See critical repair-part-purchase related data "
#                         "by clicking the button below. ",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/report/repair_purchase"
#                     ),
#                 ]
#             )
#         ),
#         dbc.Card(
#             dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
#             dbc.CardBody(
#                 [
#                     html.H5("Car Repair", className="card-title"),
#                     html.P(
#                         "See critical car-repair-related data "
#                         "by clicking the button below.",
#                         className="card-text",
#                     ),
#                     dbc.Button(
#                         "Click here", color="danger", className="mt-auto",href="/report/car_repair"
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
        html.H2('Report Generation'),  # Page Header
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
                        dbc.CardImg(src="/assets/6.png", top=True),  # Image above the card
                        dbc.CardBody(
                            [
                                html.H5("Car Purchase", className="card-title"),
                                html.P(
                                    "See critical car-purchase-related data "
                                    "by clicking the button below.",
                                    className="card-text",
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/report/car_purchase"
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Card(
                    [
                        dbc.CardImg(src="/assets/4.png", top=True),  # Image above the card
                        dbc.CardBody(
                            [
                                html.H5("Car Sale", className="card-title"),
                                html.P(
                                    "See critical car-sale-related data "
                                    "by clicking the button below.",
                                    className="card-text",
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/report/car_sale"
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
                                html.P(
                                    "See critical repair-part-purchase related data "
                                    "by clicking the button below. ",
                                    className="card-text",
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/report/repair_purchase"
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
                                html.P(
                                    "See critical car-repair-related data "
                                    "by clicking the button below.",
                                    className="card-text",
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/report/car_repair"
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)