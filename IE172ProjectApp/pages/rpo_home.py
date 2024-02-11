import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Purchase Orders"),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Transaction Home Page", href ='/transactions/transactions_main', color ='success'),
                html.Br(),
                html.Br(),
                html.Span(
                    "Go back to the Repair Main Page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Repair Home Page", href ='/repairs/repairs_main', color ='success'),
                html.Br()
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Repair Part Order Management")),
                dbc.CardBody(
                    [
                        dbc.Button('+ Add Repair Part Purchase Order', color="primary", href='/transactions/repair_part_order/repair_part_order_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Records", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search PO ID", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="po_filter_poid", placeholder="Enter PO ID"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "No records to show",
                                    id='po_porecords'
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
#         Output('po_porecords', 'children')
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('po_filter_poid', 'value'), # changing the text box value should update the table
#     ]
# )
# def moviehome_loadpolist(pathname, searchterm):
#     if pathname == '/transactions/repair_part_order':
        
#         sql = """ SELECT po_id, CONCAT(supplier_fn, ' ', supplier_mn, ' ', supplier_ln) AS supplier_name, supplier_phone_number, to_char(po_date, 'DD Mon YYYY')
#             FROM repair_parts_po_transaction
#             INNER JOIN repair_part_supplier ON repair_part_supplier.supplier_id=repair_parts_po_transaction.supplier_id
#             WHERE NOT po_delete_ind
#         """
#         values = [] 
#         cols = ['PO ID', 'Supplier Name', 'Phone Number', 'Date Created']
        
        
#         # Filter
#         if searchterm:
#             sql += " AND po_id = %s"
            
#             values += [searchterm]

#         df = db.querydatafromdatabase(sql, values, cols)
#         df['Phone Number'] = '+63' + df['Phone Number'].astype(str)

#         if df.shape: 
            
#             # Create the buttons as a list based on the ID
#             buttons = []
#             for po_id in df['PO ID']:
#                 buttons += [
#                     html.Div(
#                         dbc.Button('Edit', href=f'repair_part_order/repair_part_order_profile?mode=edit&id={po_id}',
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
        Output('po_porecords', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('po_filter_poid', 'value'), # changing the text box value should update the table
    ]
)
def moviehome_loadpolist(pathname, searchterm):
    if pathname == '/transactions/repair_part_order':
        
        sql = """ SELECT po_id, CONCAT(supplier_fn, ' ', supplier_mn, ' ', supplier_ln) AS supplier_name, supplier_phone_number, to_char(po_date, 'DD Mon YYYY')
            FROM repair_parts_po_transaction
            INNER JOIN repair_part_supplier ON repair_part_supplier.supplier_id=repair_parts_po_transaction.supplier_id
            WHERE NOT po_delete_ind
        """
        values = [] 
        cols = ['PO ID', 'Supplier Name', 'Phone Number', 'Date Created']
        
        
        # Filter
        if searchterm:
            sql += " AND po_id = %s"
            
            values += [searchterm]

        df = db.querydatafromdatabase(sql, values, cols)
        df['Phone Number'] = '+63' + df['Phone Number'].astype(str)

        if df.shape: 
            
            # Create the buttons as a list based on the ID
            buttons = []
            for po_id in df['PO ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'repair_part_order/repair_part_order_profile?mode=edit&id={po_id}',
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