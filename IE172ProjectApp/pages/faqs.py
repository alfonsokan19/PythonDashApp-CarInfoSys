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

faq_content = [
    {
        'question': 'Why does the submit button not work?',
        'answer': 'This may be due to incorrect data type inputs. Please make sure to place numeric inputs for years, phone number, and amounts.'
    },
    {
        'question': 'How do I logout?',
        'answer': 'You can logout by clicking the logout button on the upper right portion of the navigation bar.'
    },
    {
        'question': 'How do I use the report generation?',
        'answer': 'Without inputting a range of dates, the page will show the entire history for that specific transaction. If you input a date range, the page will only show you the transactions that occurred during the specified dat range.'
    },
    {
        'question': 'How do I use the search bars in information provision?',
        'answer': 'To use the search bars, you have to type the information that is specified in the search bar itself. An example is for Customers Information Provision, the search bar says "customer name"; thus, you have to type a customer name for the search bar to work.'
    },
    {
        'question': 'Why is the customer/ car supplier/ repair parts supplier not showing in the dropdown in car sale/ car purchase/ repair parts purchase?',
        'answer': 'Make sure to input their details first in the information provision.'
    },
    # Add more FAQs as needed
]
layout = html.Div(
    [
        html.H2('Frequently Asked Questions'),  # Page Header
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the Home Page by clicking the button below! ",
                ),
                html.Br(),
                dbc.Button("Go to Home Page", href='/home'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Row(
                    [
                        html.H4(f"Q: {faq['question']}"),
                        html.P(f"A: {faq['answer']}"),
                        html.Hr(),
                    ],
                    className="mb-4",
                )
                for faq in faq_content
            ]
        ),
    ],
     className="container",
) 