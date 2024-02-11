import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
from app import app
from apps import dbconnect as db



layout = html.Div(
    [
        html.H2('Repair Order Reports'),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to Report Generation Home Page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Report Generation Home Page", href ='/reports/reports_main', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('View Repair Part Purchase Reports')
                    ]
                ),
                dbc.CardBody( 
                    [
                        html.Div(
                            [
                                html.Div(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Repair Order Date", width=1),
                                                    dbc.Col(
                                                       dcc.DatePickerRange(
                                                            id='report_repairpurchasedatefilter',
                                                            display_format='YYYY-MM-DD',
                                                            start_date='',
                                                            end_date='',
                                                            start_date_placeholder_text='Select start date',
                                                            end_date_placeholder_text='Select end date',
                                                       ),
                                                        width=5
                                                    )
                                                ], className = 'mb-3'
                                                
                                            ),
                                        ],
                                    )
                                ),
                                html.Div([
                                    dcc.Loading(
                                        id="reportrepairpurchaseload",
                                        children=[
                                        dcc.Graph(id='reportrepairpurchasereceipts',)
                                      ],type="circle")
                                ],style={'width':'100%',"border": "3px #5c5c5c solid",} ),
                                html.Hr(),
                                html.H5('Repair Parts Purchase History'),
                                html.Div(
                                    id='report_repairpurchaselist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


#callback to populate dropdown options
@app.callback(
    [
        Output('report_repairpurchasedatefilter', 'options'),
        
    ],
    [
        Input('url', 'pathname'),
    ]
)
def moviehome_loadmovielist(pathname):
    if pathname == '/report/repair_purchase':
        sql = """ SELECT po_date as label, 
                    po_id as value
                FROM repair_parts_po_transaction
                WHERE po_delete_ind = %s
            """
        columns = ['label', 'value']
        values = [False]
        dfsql = db.querydatafromdatabase(sql, values, columns)
        return [dfsql.to_dict('records')]
    
    else:
        raise PreventUpdate


#callback for figure and table
@app.callback(
    [
        Output('report_repairpurchaselist', 'children'),
        Output('reportrepairpurchasereceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('report_repairpurchasedatefilter', 'start_date'),
        Input('report_repairpurchasedatefilter', 'end_date')
    ]
)
def moviehome_loadmovielist(pathname, start_date,end_date):
    if pathname == '/report/repair_purchase':
        sql = """ SELECT c.supplier_id,count(po_id),po_date, CONCAT(supplier_fn, ' ', supplier_mn, ' ', supplier_ln), po_created_date
                FROM repair_parts_po_transaction d
                    INNER JOIN repair_part_supplier c ON d.supplier_id = c.supplier_id
                WHERE po_delete_ind = false
            """
        values = []
        
        if start_date and end_date:
            sql += " AND po_date BETWEEN %s AND %s"
            values += [start_date, end_date]
        
        sql += """ Group By c.supplier_id, CONCAT(supplier_fn, ' ', supplier_mn, ' ', supplier_ln), po_date, po_created_date
                    Order By po_date, CONCAT(supplier_fn, ' ', supplier_mn, ' ', supplier_ln), po_created_date
        """

        cols = ['ID', 'Number of Orders','Purchase Date', 'Repair Parts Supplier Name', 'PO Created Date']

        df = db.querydatafromdatabase(sql, values, cols)

        
        df = df[['Purchase Date','PO Created Date','Repair Parts Supplier Name','Number of Orders']]

        listofgenre = df["Repair Parts Supplier Name"].unique().tolist()

    
        traces={}
        #setting up the values of the x-axis and y-axis of the Bar graph
        for repairpartssuppliername in listofgenre:
            # traces['tracebar_' + repairpartssuppliername]=go.Bar(y=df[df["Repair Parts Supplier Name"]==repairpartssuppliername]["Number of Orders"],
            #                         x=df[df["Repair Parts Supplier Name"]==repairpartssuppliername]["Repair Parts Supplier Name"],
            #                         # orientation = 'h', #try to uncomment this line
            #                         name=repairpartssuppliername)
            traces['tracebar_' + repairpartssuppliername] = go.Bar(
            y=df[df["Repair Parts Supplier Name"] == repairpartssuppliername]["Number of Orders"],
            x=df[df["Repair Parts Supplier Name"] == repairpartssuppliername]["Repair Parts Supplier Name"],
            marker=dict(color='lightgreen'),  # Set your desired color here
)
        #setting up the values of the x-axis and y-axis of the line chart
        # for repairpartssuppliername in listofgenre:
        #     traces['traceline_' + repairpartssuppliername] = go.Scatter(y=df[df["Repair Parts Supplier Name"]==repairpartssuppliername]["Number of Orders"],
        #                             x=df[df["Repair Parts Supplier Name"]==repairpartssuppliername]["Repair Parts Supplier Name"],
        #                             # orientation = 'h', #try to uncomment this line
        #                             mode = 'lines+markers',
        #                             name=repairpartssuppliername,
        #                             yaxis='y2')
        
        #you can add more traces if you want!

        data=list(traces.values())

        #layout of the chart/graph
        layout = go.Layout(
                yaxis1={'categoryorder':'total ascending', 'title':"Number of Orders (y-axis for bar)",'range':[0,10]},
                yaxis2={'categoryorder':'total ascending', 'title':"Number of Orders (y-axis for line)",'overlaying':'y','side':'right', 'range':[0,10]},
                xaxis={'title':"Repair Parts Supplier Name", "mirror":False, "zeroline":True },
                height=500,
                width = 2000,
                margin={'b': 50,'t':20, 'l':175},
                hovermode='closest',
                autosize= False,
                dragmode = 'zoom',
                #bar graph
                barmode='stack', #try other barmodes (e.g. group)
                boxmode= "overlay",
                )


        figure3 = {'data':data, 'layout':layout }
        # df['Purchase Amount'] = df['Purchase Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        # df['Sale Amount'] = df['Sale Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        # df['Repair Part Cost'] = df['Repair Part Cost'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        # df['Overall Profit'] = df['Overall Profit'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm', style={'text-align': 'center'})
        sql_result_text = html.Div([
            html.H5("Filter Results:"),
            dcc.Markdown(f"Total Number of Records: {len(df)}"),
            # You can add more information here based on your needs
        ])

        # Combine the table and additional SQL query information
        table_and_sql_result = [sql_result_text, table]
        if df.shape[0]:
            return [table_and_sql_result, figure3]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate