# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# To open browser upon running your app
import webbrowser
# Importing your app definition from app.py so we can use it
from app import app

#apps is the folder name
from apps import commonmodules as cm
from apps import home


#pages is the folder name 
from pages import login
from pages import signup
from pages import transactions_main
from pages import information_main
from pages import car_suppliers_home 
from pages import car_suppliers_profile
from pages import car_purchase_home
from pages import car_purchase_profile
from pages import customer_home 
from pages import customer_profile
from pages import repairs_main
from pages import reportsgeneration_main
from pages import car_repair_staff_home
from pages import car_repair_staff_profile
from pages import repair_parts_supplier_home
from pages import repair_parts_supplier_profile
from pages import repair_part_home
from pages import repair_part_profile
from pages import car_home
from pages import car_profile
from pages import rpo_home
from pages import rpo_profile
from pages import car_sale_home
from pages import car_sale_profile
from pages import report_car_sale
from pages import faqs
from pages import report_car_purchase
from pages import report_repair_purchase
from pages import report_car_repair
from pages import car_repair_home
from pages import car_repair_profile
from pages import about_us
CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}
app.layout = html.Div(
    [
         # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),

        # Adding the navbar
        html.Div(cm.navbar, id = 'navbar_div'),

        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        # If the path (i.e. part after the website name;
        # in url = youtube.com/watch, path = '/watch') changes,
        # the callback is triggered
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage (pathname,sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if userid < 0: # if logged out
                if pathname == '/':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = signup.layout
                else:
                    returnlayout = '404: request not found'
            else:    
                if pathname == '/logout':
                    returnlayout = login.layout
                    sessionlogout = True
                elif pathname == '/' or pathname == '/home':
                    returnlayout = home.layout
                elif pathname == '/transactions/transactions_main':
                    returnlayout = transactions_main.layout
                elif pathname == '/information/information_main':
                    returnlayout = information_main.layout
                elif pathname == '/repairs/repairs_main':
                    returnlayout = repairs_main.layout
                elif pathname == '/reports/reports_main':
                    returnlayout = reportsgeneration_main.layout
                elif pathname == '/information/car_supplier':
                    returnlayout = car_suppliers_home.layout
                elif pathname == '/information/car_supplier/car_supplier_profile':
                    returnlayout = car_suppliers_profile.layout
                elif pathname == '/transactions/car_purchase':
                    returnlayout = car_purchase_home.layout
                elif pathname == '/transactions/car_purchase/car_purchase_profile':
                    returnlayout = car_purchase_profile.layout
                elif pathname == '/information/customer':
                    returnlayout = customer_home.layout
                elif pathname == '/information/customer/customer_profile':
                    returnlayout = customer_profile.layout
                elif pathname == '/information/repair_part_supplier':
                    returnlayout = repair_parts_supplier_home.layout
                elif pathname == '/information/repair_part_supplier/repair_part_supplier_profile':
                    returnlayout = repair_parts_supplier_profile.layout
                elif pathname == '/information/car_repair_staff':
                    returnlayout = car_repair_staff_home.layout
                elif pathname == '/information/car_repair_staff/car_repair_staff_profile':
                    returnlayout = car_repair_staff_profile.layout
                elif pathname == '/information/repair_part':
                    returnlayout = repair_part_home.layout
                elif pathname ==  '/information/repair_part/repair_part_profile':
                    returnlayout = repair_part_profile.layout
                elif pathname == '/information/car':
                    returnlayout = car_home.layout
                elif pathname == '/information/car/car_profile':
                    returnlayout = car_profile.layout
                elif pathname == '/transactions/repair_part_order':
                    returnlayout = rpo_home.layout
                elif pathname == '/transactions/repair_part_order/repair_part_order_profile':
                    returnlayout = rpo_profile.layout
                elif pathname == '/transactions/car_sale':
                    returnlayout = car_sale_home.layout
                elif pathname == '/transactions/car_sale/car_sale_profile':
                    returnlayout = car_sale_profile.layout
                elif pathname == '/report/car_sale':
                    returnlayout = report_car_sale.layout
                elif pathname == '/faqs':
                    returnlayout = faqs.layout
                elif pathname == '/report/car_purchase':
                    returnlayout = report_car_purchase.layout
                elif pathname == '/report/repair_purchase':
                    returnlayout = report_repair_purchase.layout
                elif pathname == '/report/car_repair':
                    returnlayout = report_car_repair.layout
                elif pathname == '/car_repair':
                    returnlayout = car_repair_home.layout
                elif pathname == '/car_repair/car_repair_profile':
                    returnlayout = car_repair_profile.layout
                elif pathname == '/about_us':
                    returnlayout = about_us.layout
                else:
                    returnlayout = 'Testing123'
            
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
            
            # hide navbar if logged-out; else, set class/style to default
            navbar_classname = 'd-none' if sessionlogout else ''
        else:
            raise PreventUpdate
        
        return [returnlayout , sessionlogout, navbar_classname]
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
