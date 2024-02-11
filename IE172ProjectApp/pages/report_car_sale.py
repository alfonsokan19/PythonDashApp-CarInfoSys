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

# Layout of the app

layout = html.Div(
    [
        html.H2('Car Sale Reports'),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to Report Generation Home Page by clicking the button below! ",
                ),
                html.Br(),
                dbc.Button("Go to Report Generation Home Page", href='/reports/reports_main', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('View Car Sale Reports')
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
                                                    dbc.Label("Sale Date", width=1),
                                                    dbc.Col(
                                                        dcc.DatePickerRange(
                                                            id='report_saledatefilter',
                                                            display_format='YYYY-MM-DD',
                                                            start_date='',
                                                            end_date='',
                                                            start_date_placeholder_text='Select start date',
                                                            end_date_placeholder_text='Select end date',
                                                        ),
                                                        width=5
                                                    )
                                                ], className='mb-3'
                                            ),
                                        ],
                                    )
                                ),
                                html.Div([
                                    dcc.Loading(
                                        id="reportsaleload",
                                        children=[
                                            dcc.Graph(id='reportsalereceipts',)
                                        ], type="circle")
                                ], style={'width': '100%', "border": "3px #5c5c5c solid", }),
                                html.Hr(),
                                html.H5('Cars Sale History'),
                                html.Div(
                                    id='report_carsalelist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback to populate dropdown options
@app.callback(
    Output('report_saledatefilter', 'options'),
    Input('url', 'pathname')
)
def load_sale_dates(pathname):
    if pathname == '/report/car_sale':
        sql = """ SELECT sale_date as label, 
                    sale_id as value
                FROM car_sale
                WHERE car_sale_delete_ind = %s
            """
        columns = ['label', 'value']
        values = [False]
        dfsql = db.querydatafromdatabase(sql, values, columns)
        return [dfsql.to_dict('records')]
    else:
        raise PreventUpdate

# Callback for figure and table
@app.callback(
    [
        Output('report_carsalelist', 'children'),
        Output('reportsalereceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('report_saledatefilter', 'start_date'),
        Input('report_saledatefilter', 'end_date')
    ]
)
def load_car_sale_data(pathname, start_date, end_date):
    if pathname == '/report/car_sale':
        # sql = """  SELECT c.car_id, count(car_model), car_sale.sale_date, 
        #                 CONCAT(customer_fn, ' ', customer_mn, ' ', customer_ln) AS customer_name, 
        #                 car_model, d.sale_amount, 
        #                 car_purchase_order.purchase_amount, 
		#    SUM(repair_part_price * repair_part_used_quantity) AS repair_part_cost, 
		#    d.sale_amount - car_purchase_order.purchase_amount - SUM(repair_part_price * repair_part_used_quantity) AS result
        #         FROM car_sale d
        #             INNER JOIN car c ON d.car_id = c.car_id
        #             INNER JOIN customer a ON d.customer_id = a.customer_id
        #             INNER JOIN car_repair ON c.car_id=car_repair.car_id
        #             INNER JOIN car_repair_repair_part ON car_repair.repair_id=car_repair_repair_part.repair_id
        #             INNER JOIN car_sale ON c.car_id=car_sale.car_id
        #             INNER JOIN car_purchase_order ON car_purchase_order.car_id = car_sale.car_id
        #             WHERE car_sale.car_sale_delete_ind = false
                
        #     """

        sql = """ 
        SELECT * FROM (SELECT car_plate_number, COUNT(DISTINCT car.car_id), sale_date, CONCAT(customer_fn, ' ',customer_mn, ' ', customer_ln) AS customer_name, car_model, sale_amount, purchase_amount,  SUM(repair_part_price*repair_part_used_quantity) AS repair_cost, sale_amount - purchase_amount - SUM(repair_part_price*repair_part_used_quantity) AS profit
        FROM car
        INNER JOIN car_purchase_order ON car.car_id=car_purchase_order.car_id
        INNER JOIN car_repair ON car_repair.car_id=car.car_id
        INNER JOIN car_sale ON car.car_id = car_sale.car_id
        INNER JOIN car_repair_repair_part ON car_repair.repair_id=car_repair_repair_part.repair_id
        INNER JOIN customer ON customer.customer_id = car_sale.customer_id
        WHERE car_sale_delete_ind = False
        AND car_repair_delete_ind = False
        GROUP BY car_model, car_plate_number, purchase_amount, sale_amount, sale_date, customer_name, car_plate_number

        UNION

        SELECT car_plate_number, COUNT(DISTINCT car.car_id), sale_date, CONCAT(customer_fn, ' ',customer_mn, ' ', customer_ln) AS customer_name, car_model, sale_amount, purchase_amount, 0 as repair_cost, sale_amount - purchase_amount AS profit 
        FROM car
        INNER JOIN car_purchase_order ON car.car_id=car_purchase_order.car_id
        INNER JOIN car_sale ON car.car_id = car_sale.car_id
        INNER JOIN customer ON customer.customer_id = car_sale.customer_id
        WHERE car_sale_delete_ind = False
        AND NOT EXISTS (
            SELECT 1
            FROM car_repair
            WHERE car_repair.car_id = car.car_id
        )
        GROUP BY car_model, car_plate_number, purchase_amount, sale_amount, sale_date, customer_name, car_plate_number) AS RESULT
        """
        values = []

        if start_date and end_date:
            sql += " WHERE sale_date BETWEEN %s AND %s"
            values += [start_date, end_date]

        # sql += """ GROUP BY c.car_id, sale_date, customer_name, car_model, sale_amount, purchase_amount, repair_part_cost, result 
        #            ORDER BY customer_name, car_model, sale_amount, purchase_amount, repair_part_cost, sale_date, result 
        #         """
        sql += """ORDER BY sale_date, profit """
        
        cols = ['Plate Number', 'Number of Cars', 'Sale Date', 'Customer Name', 'Car Model', 'Sale Amount', 'Purchase Amount', 'Repair Part Cost', 'Overall Profit']

        df = db.querydatafromdatabase(sql, values, cols)

        df = df[['Number of Cars','Sale Date', 'Customer Name', 'Car Model', 'Plate Number','Sale Amount','Purchase Amount','Repair Part Cost', 'Overall Profit']]

        list_of_models = df["Car Model"].unique().tolist()

        traces = {}
        for carmodel in list_of_models:
            # traces['tracebar_' + car_model] = go.Bar(
            #     y=df[df["Car Model"] == car_model]["Number of Cars"],
            #     x=df[df["Car Model"] == car_model]["Customer Name"],
            #     name=car_model
            # )
            traces['tracebar_' + carmodel] = go.Bar(
            y=df[df["Car Model"] == carmodel]["Number of Cars"],
            x=df[df["Car Model"] == carmodel]["Customer Name"],
            marker=dict(color='lightgreen'),  # Set your desired color here
)

            # traces['traceline_' + car_model] = go.Scatter(
            #     y=df[df["Car Model"] == car_model]["Number of Cars"],
            #     x=df[df["Car Model"] == car_model]["Customer Name"],
            #     mode='lines+markers',
            #     name=car_model,
            #     yaxis='y2'
            # )

        data = list(traces.values())

        layout = go.Layout(
            yaxis1={'categoryorder': 'total ascending', 'title': "Number of Cars (y-axis for bar)", 'range': [0, 10]},
            yaxis2={'categoryorder': 'total ascending', 'title': "Cost of Car (y-axis for line)", 'overlaying': 'y',
                    'side': 'right', 'range': [0, 10]},
            xaxis={'title': "Customer Name", "mirror": False, "zeroline": True},
            height=500,
            width=2000,
            margin={'b': 50, 't': 20, 'l': 175},
            hovermode='closest',
            autosize=False,
            dragmode='zoom',
            barmode='stack',
            boxmode="overlay",
        )

        figure = {'data': data, 'layout': layout}
        df['Purchase Amount'] = df['Purchase Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        df['Sale Amount'] = df['Sale Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        df['Repair Part Cost'] = df['Repair Part Cost'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        df['Overall Profit'] = df['Overall Profit'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
  # If you want to include the SQL query values above the table, you can add a new div
        
        sql_result_text = html.Div([
            html.H5("Filter Results:"),
            dcc.Markdown(f"Total Number of Records: {len(df)}"),
            # You can add more information here based on your needs
        ])

        # Combine the table and additional SQL query information
        table_and_sql_result = [sql_result_text, table]
        if df.shape[0]:
            return [table_and_sql_result, figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate