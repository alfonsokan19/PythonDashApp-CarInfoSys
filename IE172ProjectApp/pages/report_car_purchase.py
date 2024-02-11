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
        html.H2('Car Purchase Reports'),
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
                        html.H3('View Car Purchase Reports')
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
                                                    dbc.Label("Purchase Date", width=1),
                                                    dbc.Col(
                                                       dcc.DatePickerRange(
                                                            id='report_purchasedatefilter',
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
                                        id="reportpurchaseload",
                                        children=[
                                        dcc.Graph(id='reportpurchasereceipts',)
                                      ],type="circle")
                                ],style={'width':'100%',"border": "3px #5c5c5c solid",} ),
                                html.Hr(),
                                html.H5('Cars Purchased History'),
                                html.Div(
                                    id='report_carpurchaselist'
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
        Output('report_purchasedatefilter', 'options'),
        
    ],
    [
        Input('url', 'pathname'),
    ]
)
def moviehome_loadmovielist(pathname):
    if pathname == '/report/car_purchase':
        sql = """ SELECT purchase_date as label, 
                    purchase_id as value
                FROM car_purchase_order
                WHERE car_purchase_order_delete_ind = %s
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
        Output('report_carpurchaselist', 'children'),
        Output('reportpurchasereceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('report_purchasedatefilter', 'start_date'),
        Input('report_purchasedatefilter', 'end_date')
    ]
)
def moviehome_loadmovielist(pathname, start_date,end_date):
    if pathname == '/report/car_purchase':
        sql = """ SELECT c.car_id,count(car_model),purchase_date, CONCAT(csupplier_fn, ' ', csupplier_mn, ' ', csupplier_ln), car_model, purchase_amount
                FROM car_purchase_order d
                    INNER JOIN car c ON d.car_id = c.car_id
                    INNER JOIN car_supplier a ON d.csupplier_id = a.csupplier_id
                WHERE car_purchase_order_delete_ind = false
            """
        values = []
        
        if start_date and end_date:
            sql += " AND purchase_date BETWEEN %s AND %s"
            values += [start_date, end_date]
        
        sql += """ Group By c.car_id, CONCAT(csupplier_fn, ' ', csupplier_mn, ' ', csupplier_ln), car_model, purchase_amount, purchase_date
                    Order By CONCAT(csupplier_fn, ' ', csupplier_mn, ' ', csupplier_ln), car_model, purchase_amount, purchase_date
        """

        cols = ['ID', 'Number of Cars','Purchase Date', 'Car Supplier Name', 'Car Model', 'Purchase Amount']

        df = db.querydatafromdatabase(sql, values, cols)

        
        df = df[['Car Model','Purchase Amount','Car Supplier Name','Purchase Date','Number of Cars']]

        listofgenre = df["Car Model"].unique().tolist()

    
        traces={}
        #setting up the values of the x-axis and y-axis of the Bar graph
        for carmodel in listofgenre:
            # traces['tracebar_' + carmodel]=go.Bar(y=df[df["Car Model"]==carmodel]["Number of Cars"],
            #                         x=df[df["Car Model"]==carmodel]["Car Supplier Name"],
            #                         # orientation = 'h', #try to uncomment this line
            #                         name=carmodel)
#             traces['tracebar_' + carmodel] = go.Bar(
#             y=df[df["Car Model"] == carmodel]["Number of Cars"],
#             x=df[df["Car Model"] == carmodel]["Car Supplier Name"],
# )
            traces['tracebar_' + carmodel] = go.Bar(
            y=df[df["Car Model"] == carmodel]["Number of Cars"],
            x=df[df["Car Model"] == carmodel]["Car Supplier Name"],
            marker=dict(color='lightgreen'),  # Set your desired color here
)
        #setting up the values of the x-axis and y-axis of the line chart
        # for carmodel in listofgenre:
        #     traces['traceline_' + carmodel] = go.Scatter(y=df[df["Number of Cars"]==carmodel]["Number of Cars"],
        #                             x=df[df["Number of Cars"]==carmodel]["Car Supplier Name"],
        #                             # orientation = 'h', #try to uncomment this line
        #                             mode = 'lines+markers',
        #                             name=carmodel,
        #                             yaxis='y2')
        
        #you can add more traces if you want!

        data=list(traces.values())

        #layout of the chart/graph
        layout = go.Layout(
                yaxis1={'categoryorder':'total ascending', 'title':"Number of Cars (y-axis for bar)",'range':[0,10]},
                yaxis2={'categoryorder':'total ascending', 'title':"Cost of Car (y-axis for line)",'overlaying':'y','side':'right', 'range':[0,10]},
                xaxis={'title':"Car Supplier Name", "mirror":False, "zeroline":True },
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
        
        df['Purchase Amount'] = df['Purchase Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm', style={'text-align': 'Center'})
        
        sql_result_text = html.Div([
            html.H5("Filter Results:"),
            dcc.Markdown(f"Total Number of Records: {len(df)}"),
            # You can add more information here based on your needs
        ])
        table_and_sql_result = [sql_result_text, table]
        if df.shape[0]:
            return [table_and_sql_result, figure3]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate