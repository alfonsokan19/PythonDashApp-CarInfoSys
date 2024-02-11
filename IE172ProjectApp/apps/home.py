# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
# Let us import the app object in case we need to define
# callbacks here
from app import app
from dash import html
# store the layout objects into a variable named layout

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

#try this
# transaction_jumbotron = dbc.Col(
#     html.Div(
#         [
#             html.H2("Car Details and Transactions", className="display-3"),
#             html.Hr(className="my-2"),
#             html.P(
#                 "Add a car, car purchase, or car sale "
#                 "by clicking the button below!"
#             ),
#             dbc.Button("Add or Edit a Transaction", color="light", outline=True, href="/transactions/transactions_main"),
#         ],
#         className="h-100 p-5 text-white bg-dark rounded-3",
#     ),
#     md=6,
# )
        
# information_jumbotron = dbc.Col(
#     html.Div(
#         [
#             html.H2("Information", className="display-3"),
#             html.Hr(className="my-2"),
#             html.P(
#                 "Add or Edit the information of your car suppliers, car buyers, and repair part suppliers "
#                 "by clicking the button below!"
#             ),
#             dbc.Button("Add or Edit Information", color="secondary", outline=True, href="/information/information_main"),
#         ],
#         className="h-100 p-5 bg-light border rounded-3",
#     ),
#     md=6,
# )

# reports_jumbotron = dbc.Col(
#     html.Div(
#         [
#             html.H2("Report Generation", className="display-3"),
#             html.Hr(className="my-2"),
#             html.P(
#                 "Check your financial reports "
#                 "by clicking the button below!"
#             ),
#             dbc.Button("Check Financial Reports", color="secondary", outline=True, href="/reports/reports_main"),
#         ],
#         className="h-100 p-5 bg-light border rounded-3",
#     ),
#     md=6,
# )

# repair_jumbotron = dbc.Col(
#     html.Div(
#         [
#             html.H2("Repair Part Details and Tracking Repair", className="display-3"),
#             html.Hr(className="my-2"),
#             html.P(
#                 "Add repair parts details or track car repairs "
#                 "by clicking the button below!"
#             ),
#             dbc.Button("Track Car Repairs", color="light", outline=True, href="/repairs/repairs_main"),
#         ],
#         className="h-100 p-5 text-white bg-dark rounded-3",
#     ),
#     md=6,
# )
# jumbotron = dbc.Row(
#     [transaction_jumbotron,information_jumbotron,reports_jumbotron,repair_jumbotron],
#     className="align-items-md-stretch",
# )
 
#Sir's case app layout
layout = html.Div(
    [
        html.H2('Welcome to our app!'),
        html.Hr(),
        dbc.Carousel(
    items=[
        {
            "key": "1",
            "src": "assets/1.png",
            "header": "Manage your business with this app! ",
            "caption": "Scroll down to see functionalities!",
        },
        {
            "key": "2",
            "src": "/assets/2.png",
            "header": "With header only",
            "caption": "",
        },
        {
            "key": "3",
            "src": "/assets/3.png",
            "header": "",
            "caption": "This slide has a caption only",
        },
    ]
),
        dbc.CardGroup(
            [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Transaction Provision", className="card-title"),
                        html.Hr(),
                        html.P(
                            "Manage transactions such as car purchase, car sale, and repair parts purchase "
                            "by clicking the button below!",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="success", className="mt-auto", href="/transactions/transactions_main"
                        ),
                ]
            ),
            style={"width": "75%"},
            className="mb-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Information Provision", className="card-title"),
                        html.Hr(),
                        html.P(
                            "Manage information of cars, car suppliers, car buyers, employees, repair parts, and repair part suppliers "
                            "by clicking the button below!",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="success", className="mt-auto", href="/information/information_main"
                        ),
                ]
            ),
            style={"width": "75%"},
            className="mb-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Report Generation", className="card-title"),
                        html.Hr(),
                        html.P(
                            "Manage financial and other data "
                            "by clicking the button below!",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="success", className="mt-auto", href="/reports/reports_main"
                        ),
                ]
            ),
            style={"width": "75%"},
            className="mb-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Repair-Related Information", className="card-title"),
                        html.Hr(),
                        html.P(
                            "Manage repair-related information such as repair parts, repair part purchase, or car repair "
                            "by clicking the button below!",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Click here", color="success", className="mt-auto", href="/repairs/repairs_main"
                        ),
                ]
            ),
            style={"width": "75%"},
            className="mb-3",
        )
    ]
),
    ]
)


# #THIS IS THE MAIN CODE
# layout = html.Div(
#     [
#         html.H2('Welcome to our app!'),
#         html.Hr(),
#         # Container for the cards
#         dbc.Carousel(
#     items=[
#         {
#             "key": "1",
#             "src": "assets/1.png",
#             "header": "With header ",
#             "caption": "and caption",
#         },
#         {
#             "key": "2",
#             "src": "/assets/2.png",
#             "header": "With header only",
#             "caption": "",
#         },
#         {
#             "key": "3",
#             "src": "/static/images/slide3.svg",
#             "header": "",
#             "caption": "This slide has a caption only",
#         },
#     ]
# ),
#         html.Div(
#             [
#                 # Card 1
#                 html.Div(
#                     [
#                         html.H5("Transaction Provision", className="card-title"),
#                         html.Hr(),
#                         html.P(
#                             "Manage transactions such as car purchase, car sale, and repair parts purchase "
#                             "by clicking the button below!",
#                             className="card-text",
#                         ),
#                         dbc.Button(
#                             "Click here", color="success", className="mt-auto", href="/transactions/transactions_main"
#                         ),
#                     ],
#                     className="card mb-3",
#                 ),

#                 # Card 2
#                 html.Div(
#                     [
#                         html.H5("Information Provision", className="card-title"),
#                         html.Hr(),
#                         html.P(
#                             "Manage information of cars, car suppliers, car buyers, employees, repair parts, and repair part suppliers "
#                             "by clicking the button below!",
#                             className="card-text",
#                         ),
#                         dbc.Button(
#                             "Click here", color="warning", className="mt-auto", href="/information/information_main"
#                         ),
#                     ],
#                     className="card mb-3",
#                 ),

#                 # Card 3
#                 html.Div(
#                     [
#                         html.H5("Report Generation", className="card-title"),
#                         html.Hr(),
#                         html.P(
#                             "Manage financial and other data "
#                             "by clicking the button below!",
#                             className="card-text",
#                         ),
#                         dbc.Button(
#                             "Click here", color="danger", className="mt-auto", href="/reports/reports_main"
#                         ),
#                     ],
#                     className="card mb-3",
#                 ),

#                 # Card 4
#                 html.Div(
#                     [
#                         html.H5("Repair-Related Information", className="card-title"),
#                         html.Hr(),
#                         html.P(
#                             "Manage repair-related information such as repair parts, repair part purchase, or car repair "
#                             "by clicking the button below!",
#                             className="card-text",
#                         ),
#                         dbc.Button(
#                             "Click here", color="info", className="mt-auto", href="/repairs/repairs_main"
#                         ),
#                     ],
#                     className="card mb-3",
#                 ),
#             ],
#             className="container",
#         ),
#         # Container for buttons
#     ]
# )
# # Callback for toggling the offcanvas
# @app.callback(
#     Output("offcanvas", "is_open"),
#     Input("open-offcanvas", "n_clicks"),
#     [State("offcanvas", "is_open")],
# )
# def toggle_offcanvas(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open


