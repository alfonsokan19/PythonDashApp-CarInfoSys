# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
# Let us import the app object in case we need to define
# callbacks here
from app import app

#LETS USE ANOTHER STYLE
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("About Us", href="/about_us")),
        dbc.NavItem(dbc.NavLink("Frequently Asked Questions", href="/faqs")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Database Functions", header=True),
                dbc.DropdownMenuItem("Transactions", href="/transactions/transactions_main"),
                dbc.DropdownMenuItem("Reports", href="/reports/reports_main"),
                dbc.DropdownMenuItem("Information", href="/information/information_main"),
                dbc.DropdownMenuItem("Car Repairs", href="/repairs/repairs_main")
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
        dbc.NavLink("Logout", href="/logout"),
    ],
    brand="Winston's Automobiles Database",
    brand_href="/home",
    color="lightgreen",
    dark=False,
)

#FROM SIR'S CASE APP (NAVBAR STYLE)
# CSS Styling for the NavLink components
# navlink_style = {
#     'color': '#FFFFCC'
#     # #fff is white
# }
# navbar = dbc.Navbar(
#     [
#         html.A(
#             # Use row and col to control vertical alignment of logo / brand
#             dbc.Row(
#                 [
#                     dbc.Col(dbc.NavbarBrand("Winston's Automobiles Database", className="ms-2")),
#                 ],
#                 align="center",
#                 className = 'g-0' #remove gutters (i.e. horizontal space between cols)
#             ),
#             href="/home",
#         ),
        # dbc.NavLink("Home", href="/home", style=navlink_style),
        # dbc.NavLink("Movies", href="/movies", style=navlink_style),
        # dbc.NavLink("Genres", href="/genres", style=navlink_style),
#     ],
#     dark=True,
#     color='dark'
# )
