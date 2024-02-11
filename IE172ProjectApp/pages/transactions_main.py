# # Usual Dash dependencies
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import dash_table
# import dash
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
# import pandas as pd
# # Let us import the app object in case we need to define
# # callbacks here
# from app import app
# #for DB needs
# from apps import dbconnect as db

# # store the layout objects into a variable named layout

# layout = html.Div(
#     [
#         html.H2('Transactions'),  # Page Header
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
#                     dbc.CardBody(
#                         [
#                             html.H5("Car Purchase", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add the cars you purchase by clicking the button below.
                                
#                                 **NOTE:** Add the car supplier details to the car supplier information provision first if he is a new car supplier.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="success", className="mt-auto", href="/transactions/car_purchase"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardBody(
#                         [
#                             html.H5("Car Sale", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add the cars you sell by clicking the button below.
                                
#                                 **NOTE:** Add the customer details to the customer information provision first if he is a new customer.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="warning", className="mt-auto", href="/transactions/car_sale"
#                             ),
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardBody(
#                         [
#                             html.H5("Repair Part Purchase", className="card-title"),
#                             dcc.Markdown(
#                                 """
#                                 Add the repair parts you purchase by clicking the button below.
                                
#                                 **NOTE:** Add the repair parts details to the repair part information provision first if the order involves a new repair part.
#                                 """
#                             ),
#                             dbc.Button(
#                                 "Click here", color="danger", className="mt-auto", href="/transactions/repair_part_order"
#                             ),
#                         ]
#                     )
#                 ),
#             ],
#         )
#     ]
# )


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

layout = html.Div(
    [
        html.H2('Transactions'),  # Page Header
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
                                dcc.Markdown(
                                    """
                                    Add the cars you purchase by clicking the button below.
                                    
                                    **NOTE:** Add the car supplier details to the car supplier information provision first if he is a new car supplier.
                                    """
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/transactions/car_purchase"
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
                                dcc.Markdown(
                                    """
                                    Add the cars you sell by clicking the button below.
                                    
                                    **NOTE:** Add the customer details to the customer information provision first if he is a new customer.
                                    """
                                ),
                                dbc.Button(
                                    "Click here", color="success", className="mt-auto", href="/transactions/car_sale"
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
