# import json
# from datetime import date
# from urllib.parse import parse_qs, urlparse

# import dash
# import dash_bootstrap_components as dbc
# import pandas as pd
# from dash import dcc, html
# from dash.dependencies import ALL, Input, Output, State
# from dash.exceptions import PreventUpdate

# from app import app
# from apps import dbconnect as db
# from pages import car_repair_utils as utils

# layout = html.Div(
#     [
#         html.Div( # This div shall contain all dcc.Store objects
#             [
#                 # if edit mode, this gets a value of 1, else 0
#                 dcc.Store(id='repairprof_toload', storage_type='memory', data=0),
                
#                 # this gets the po_id 
#                 dcc.Store(id='repairprof_repairid', storage_type='memory', data=0),
                
#                 # this gets the po_item_id to edit
#                 dcc.Store(id='repairprof_linetoedit', storage_type='memory', data=0),
#             ]
#         ),

#         html.H2("Car Repair Details"),
#         html.Hr(),
#         html.Div(
#             [
#                 dbc.Row(
#                     [
#                         dbc.Label("Repair Start Date", width=2),
#                         dbc.Col(
#                             dcc.DatePickerSingle(
#                                 id='repairprof_startdate',
#                                 date=date.today()
#                             ),
#                             width=6,
#                         ),
#                     ],
#                     className="mb-3",
#                 ),

#                 dbc.Row(
#                     [
#                         dbc.Label("Car Plate Number", width=2),
#                         dbc.Col(
#                             html.Div(
#                                 dcc.Dropdown(
#                                     id='repairprof_carbeingrepaired',
#                                     clearable=True,
#                                     searchable=True,
#                                     options=[]
#                                 ), 
#                                 className="dash-bootstrap"
#                             ),
#                             width=6,
#                         ),
#                     ],
#                     className="mb-3",
#                 ),

#                 dbc.Row(
#                     [
#                         dbc.Label("Repair Status", width=2),
#                         dbc.Col(
#                             html.Div(
#                                 dcc.Dropdown(
#                                     id='repairprof_repairstatus',
#                                     clearable=True,
#                                     searchable=True,
#                                     options=[]
#                                 ), 
#                                 className="dash-bootstrap"
#                             ),
#                             width=6,
#                         ),
#                     ],
#                     className="mb-3",
#                 ),

#                 dbc.Row(
#                     [
#                         dbc.Label("Repair Remarks", width=2),
#                         dbc.Col(
#                             dbc.Textarea(
#                                 className="mb-3",
#                                 placeholder="Add remarks",
#                                 id='repairprof_remarks'
#                             ),
#                             width=6,
#                         ),
#                     ],
#                     className="mb-3",
#                 ),
#             ]    
#         ),
#         html.Hr(),
        
#         # We don't need a div here but I like using one
#         # to signify a new section
#         html.Div(
#             [
#                 dbc.Alert("Please fill out the information above before proceeding", id='repairprof_alertmissingdata',
#                           color='danger', is_open=False),
#                 dbc.Button("Add Repair Part", id="repairprof_addlinebtn", 
#                            color='primary', n_clicks=0,
#                            style={'display':'inline-block','border-radius':'5px'}
#                 ),  
#                 html.Br(),
#                 html.Br(),
#                 html.Div(
#                     # This will contain the table of line items
#                     id='repairprof_lineitems'
#                 )
#             ]    
#         ),
        
#         dbc.Modal(
#             [
#                 dbc.ModalHeader("Add Repair Part", id='repairprof_linemodalhead'),
#                 dbc.ModalBody(
#                     [
#                         dbc.Alert(id='repairprof_linealert', color='warning', is_open=False),
#                         dbc.Row(
#                             [
#                                 dbc.Label("Repair Part", width=4),
#                                 dbc.Col(
#                                     html.Div(
#                                         dcc.Dropdown(
#                                             id='repairprof_lineitem',
#                                             clearable=True,
#                                             searchable=True,
#                                             options=[]
#                                         ), 
#                                         className="dash-bootstrap"
#                                     ),
#                                     width=6,
#                                 ),
#                             ],
#                             className="mb-3",
#                         ),

#                         dbc.Row(
#                             [
#                                 dbc.Label("Unit Price", width=4),
#                                 dbc.Col(
#                                     dbc.Input(
#                                         type="number", id="repairprof_lineunitprice", placeholder="Enter unit price"
#                                     ),
#                                     width=6,
#                                 ),
#                             ],
#                             className="mb-3"
#                         ),

#                         dbc.Row(
#                             [
#                                 dbc.Label("Qty", width=4),
#                                 dbc.Col(
#                                     dbc.Input(
#                                         type="number", id="repairprof_lineqty", placeholder="Enter qty"
#                                     ),
#                                     width=6,
#                                 ),
#                             ],
#                             className="mb-3"
#                         ),

#                         html.Div(
#                             dbc.Row(
#                                 [
#                                     dbc.Label("Wish to delete?", width=4),
#                                     dbc.Col(
#                                         dbc.Checklist(
#                                             id='repairprof_lineremove',
#                                             options=[
#                                                 {
#                                                     'label': "Mark for Deletion",
#                                                     'value': 1
#                                                 }
#                                             ],
#                                             # I want the label to be bold
#                                             style={'fontWeight':'bold'}, 
#                                         ),
#                                         width=6,
#                                         style={'margin': 'auto 0'}
#                                     ),
#                                 ],
#                                 className="mb-3",
#                             ),
#                             id='repairprof_lineremove_div'
#                         ),
#                     ]
#                 ),
#                 dbc.ModalFooter(
#                     [
#                         html.Div(
#                             [
#                                 dbc.Button('Back', id='repairprof_cancellinebtn', color='secondary'),
#                                 dbc.Button('Save Repair Part', id='repairprof_savelinebtn', color='primary'),
#                             ],
#                             # these are to separate the buttons to opposite ends
#                             className='d-flex justify-content-between',
#                             style={'flex': '1'}
#                         )
#                     ]
#                 )
#             ],
#             id='repairprof_modal',
#             backdrop='static',
#             centered=True
#         ),
        
#         # enclosing the checklist in a Div so we can
#         # hide it in Add Mode
#         html.Div(
#             dbc.Row(
#                 [
#                     dbc.Label("Wish to delete?", width=2),
#                     dbc.Col(
#                         dbc.Checklist(
#                             id='repairprof_removerecord',
#                             options=[
#                                 {
#                                     'label': "Mark for Deletion",
#                                     'value': 1
#                                 }
#                             ],
#                             # I want the label to be bold
#                             style={'fontWeight':'bold'}, 
#                         ),
#                         width=6,
#                         style={'margin': 'auto 0'}
#                     ),
#                 ],
#                 className="mb-3",
#             ),
#             id='repairprof_removerecord_div'
#         ),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader(dbc.ModalTitle("Trying to leave the page...")),
#                 dbc.ModalBody("tempmessage", id='repairprof_feedback_message'),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Okay", id="repairprof_closebtn", className="ms-auto", n_clicks=0
#                     )
#                 ),
#             ],
#             id="repairprof_modalsubmitted",
#             is_open=False,
#         ),
#         html.Hr(),
        
#         html.Div(
#             [
#                 dbc.Button('Back', id='repairprof_cancelbtn', color='secondary'),
#                 dbc.Button('Submit', color="primary", id='repairprof_savebtn'),
#             ],
#             # these are to separate the buttons to opposite ends
#             className='d-flex justify-content-between',
#             style={'flex': '1'}
#         )
#     ]
# )

# @app.callback(
#     [
#         Output('repairprof_toload', 'data'),
#         # we want to update the style of this element
#         Output('repairprof_removerecord_div', 'style'),
#         Output('repairprof_carbeingrepaired', 'options'),
#         Output('repairprof_repairstatus', 'options')
#     ],
#     [
#         Input('url', 'pathname')
#     ],
#     [
#         State('url', 'search')
#     ]
# )
# def pageLoadOperations(pathname, search):
    
#     if pathname == '/car_repair/car_repair_profile':
                
#         # are we on add or edit mode?
#         parsed = urlparse(search)
#         create_mode = parse_qs(parsed.query)['mode'][0]
#         to_load = 1 if create_mode == 'edit' else 0
        
#         # to show the remove option?

#         removediv_style = {'display': 'none'} if not to_load else None
#         # if to_load = 0, then not to_load -> not 0 -> not False -> True


#         sql_cardropdown = """ 
#         SELECT car_plate_number AS label, car.car_id AS value
#         FROM car
#         INNER JOIN car_purchase_order ON car_purchase_order.car_id=car.car_id
#         WHERE car_delete_ind =  False
#         AND car_purchase_condition_id = 1
#         """

#         values_cardropdown = []
#         cols_cardropdown = ['label', 'value']
#         df_cardropdown = db.querydatafromdatabase(sql_cardropdown, values_cardropdown, cols_cardropdown)
#         car_options = df_cardropdown.to_dict('records')


#         sql_repairstatusdropdown = """
#         SELECT repair_status_label AS label, repair_status_id AS value
#         FROM repair_status
#         where repair_status_delete_ind=False
#         """

#         values_repairstatusdropdown = []
#         cols_repairstatusdropdown = ['label', 'value']
#         df_repairstatusdropdown = db.querydatafromdatabase(sql_repairstatusdropdown, values_repairstatusdropdown, cols_repairstatusdropdown)
#         repairstatus_options = df_repairstatusdropdown.to_dict('records')

#     else:
#         raise PreventUpdate

#     return [to_load, removediv_style, car_options, repairstatus_options]

# # INCOMPLETE
# @app.callback(
#     [
#         Output('repairprof_startdate', 'date'),
#         Output('repairprof_carbeingrepaired', 'value'),
#         Output('repairprof_remarks', 'value'),
#         Output('repairprof_repairstatus', 'value'),
#     ],
#     [
#         Input('repairprof_toload', 'modified_timestamp'),
#         # toload is a dcc.store element. To use them in Input(), 
#         # property should be 'modified_timestamp'
#     ],
#     [
#         State('repairprof_toload', 'data'),
#         State('url', 'search') 
#     ]
# )
# def populateRepairData(timestamp, toload, search):
#     if toload == 1:
        
#         parsed = urlparse(search)
#         repair_id = int(parse_qs(parsed.query)['id'][0])
        
#         sql = """SELECT repair_date, car_id, repair_remarks, repair_status_id
#         FROM car_repair
#         WHERE repair_id = %s"""
#         val = [repair_id]
#         col = ['date', 'supplier', 'remarks', 'repair_status']
        
#         df = db.querydatafromdatabase(sql, val, col)
        
#         transactiondate, car, remarks, repair_status = [df[i][0] for i in col]

        
#     else:
#         raise PreventUpdate
    
#     return [transactiondate, car, remarks, repair_status]





# @app.callback(
#     [
#         Output('repairprof_modal', 'is_open'),
#         Output('repairprof_alertmissingdata', 'is_open'),
#         Output('repairprof_lineremove_div', 'className'),
#         Output('repairprof_repairid', 'data'),
        
#         Output('repairprof_lineitem', 'options'),
#         Output('repairprof_linealert', 'children'),
#         Output('repairprof_linealert', 'is_open'),
#         Output('repairprof_linetoedit', 'data'),
        
#         Output('repairprof_lineitems', 'children'),
#         Output('repairprof_linemodalhead', 'children'),
#         Output('repairprof_savelinebtn', 'children'),
#     ],
#     [
#         Input('repairprof_addlinebtn', 'n_clicks'),
#         Input('repairprof_savelinebtn', 'n_clicks'),
#         Input('repairprof_cancellinebtn', 'n_clicks'),
#         Input({'index': ALL, 'type': 'repairprof_editlinebtn'}, 'n_clicks'),
        
#         Input('repairprof_toload', 'modified_timestamp'),
        
#     ],
#     [
#         State('url', 'search'),
#         State('repairprof_startdate', 'date'), #transaction date
#         State('repairprof_remarks', 'value'),
#         State('repairprof_repairid', 'data'),
        
#         State('repairprof_lineitem', 'options'),    #10
#         State('repairprof_lineitem', 'value'),      #11

#         State('repairprof_carbeingrepaired', 'value'),          #car_id
#         State('repairprof_repairstatus', 'value'),

#         State('repairprof_lineunitprice', 'value'),
#         State('repairprof_lineqty', 'value'),
#         State('repairprof_linetoedit', 'data'),
        
#         State('repairprof_lineremove', 'value'),
#         State('repairprof_lineitems', 'children'),
#         State('repairprof_toload', 'data'),
#         State('repairprof_linemodalhead', 'children'),
        
#         State('repairprof_savelinebtn', 'children'),
#     ]
# )

# def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
#                 toload_timestamp,
#                 search, repair_startdate, remarks, repair_id,            #beginnning state
#                 item_options, itemid, 
#                 car_id, repair_status,
#                 itemprice, itemqty, linetoedit,
#                 removeitem, linetable, toload, linemodalhead,
#                 addlinebtntxt):
    
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         parsed = urlparse(search)
        
#         # some default values
#         openmodal = False
#         openalert_missingdata = False
#         lineremove_class = 'd-none' # hide the remove tickbox
        
#         linealert_message = ''
#         updatetable = False # for updating table of line items
#     else:
#         raise PreventUpdate
    
#     Repair_requireddata = [
#         repair_startdate,
#         car_id,
#         remarks
#     ]
    
#     if eventid == 'repairprof_addlinebtn' and addlinebtn and all(Repair_requireddata):
#         openmodal = True
#         item_options = utils.getItemDropdown('add', repair_id)       #MAKE NEW CALLBACK
#         linetoedit = 0
        
#         # Edit modal text (buttons, headers)
#         linemodalhead = 'Add Repair Part'
#         addlinebtntxt = 'Save Repair Part'

    
#     elif eventid == 'repairprof_addlinebtn' and addlinebtn and not all(Repair_requireddata):
#         openalert_missingdata = True
        
#     elif eventid == 'repairprof_cancellinebtn' and cancelbtn:
#         pass
    
#     elif 'repairprof_editlinebtn' in eventid and any(editlinebtn):
#         # if any of the buttons for editing si clicked
        
#         openmodal = True
#         lineremove_class = '' # show line remove option
#         linetoedit = int(json.loads(eventid)['index'])
#         item_options = utils.getItemDropdown('edit', repair_id)              #MAKE NEW CALLBACK
        
#         # Edit modal text (buttons, headers)
#         linemodalhead = 'Edit Line Item'
#         addlinebtntxt = 'Update Line Item'
        
#     elif eventid == 'repairprof_toload' and toload == 1:
#         updatetable = True
#         repair_id = int(parse_qs(parsed.query)['id'][0])

        
#     elif eventid == 'repairprof_savelinebtn' and savebtn:
#         # validate inputs
#         inputs = [
#             itemid, 
#             itemprice,
#             utils.converttoint(itemqty)>0                                    #MAKE NEW CALLBACK
#         ]
        
#         if not all(inputs):
#             linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
#         else:
#             # proceed to saving the line item
            
#             newline = {
#                 'itemid': itemid,
#                 'itemqty': int(itemqty),
#                 'unitprice': float(itemprice),
#                 'carid': car_id
#             }
            
#             # if add mode:
#             if linetoedit == 0:
#                 # if PO record not yet in db, save PO first
#                 if not repair_id:
#                     repair_id = utils.createRepairrecord(repair_startdate, remarks, car_id, repair_status)            #MAKE NEW CALLBACK
                
#                 utils.manageRepairItem(repair_id, newline)                                                   #MAKE NEW CALLBACK
            
#     #             # reflect add row entry for repair_parts_repair_parts_supplier table, delete_ind=false
#     #             util.insert_repair_parts_repair_parts_supplier(newline)
            
#             else:
#                 if removeitem:
#                     utils.removeRepairItem(linetoedit)

#     #                 if not util.check_supplier_repair_part_entries(itemid, car_id):               #MAKE NEW CALLBACK
#     #                     util.delete_repair_parts_repair_parts_supplier(itemid, car_id)            #MAKE NEW CALLBACK



#                 # reflect remove row entry for repair_parts_repair_parts_supplier table, delete_ind=True
                
#                 else:
#                 # reflect add row entry for repair_parts_repair_parts_supplier table, delete_ind=false
#                     utils.manageRepairItem(repair_id, newline)                                               #MAKE NEW CALLBACK
#                     # util.insert_repair_parts_repair_parts_supplier(newline)                                 #MAKE NEW CALLBACK
                
#             updatetable = True
    
#     else:
#         raise PreventUpdate
    
    
#     if updatetable:
#         df = utils.queryRepairItems(repair_id)                                                               #MAKE NEW CALLBACK
        
#         if df.shape[0]:
#             linetable = utils.formatRepairTable(df)          #MAKE NEW CALLBACK
#         else:
#             linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

#     # if we have an error prompt, linealert should open
#     openalert_linealert = bool(linealert_message)
    
#     return [
#         openmodal, 
#         openalert_missingdata, 
#         lineremove_class,
#         repair_id,
        
#         item_options,
#         linealert_message,
#         openalert_linealert,
#         linetoedit,
        
#         linetable,
#         linemodalhead,
#         addlinebtntxt
#     ]


# # OK
# @app.callback(
#     [
#         Output('repairprof_lineitem', 'value'),
#         Output('repairprof_lineqty', 'value'),
#         Output('repairprof_lineremove', 'value'),
#         Output('repairprof_lineunitprice', 'value')
        
#     ],
#     [
#         Input('repairprof_addlinebtn', 'n_clicks'),
#         Input('repairprof_linetoedit', 'modified_timestamp'),
#     ],
#     [
#         State('repairprof_linetoedit', 'data'),
#         State('repairprof_lineitem', 'value'),
#         State('repairprof_lineqty', 'value'),
#         State('repairprof_lineremove', 'value'),
#         State('repairprof_lineunitprice', 'value'),
    
#     ]
# )
# def clearFields(addlinebtn, line_timestamp, 
                
#                 linetoedit, itemid, itemqty, removeitem, itemprice):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#     else:
#         raise PreventUpdate
    
    
#     if eventid == 'repairprof_addlinebtn' and addlinebtn:
#         itemid, itemqty, itemprice = None, None, None
#         # itemprice = None
#         removeitem = []
        
#     elif eventid == 'repairprof_linetoedit' and linetoedit:
#         itemid, itemqty, itemprice = utils.getRepairPartLineData(linetoedit)
#         removeitem = []
        
#     else:
#         raise PreventUpdate
    
#     return [itemid, itemqty, removeitem, itemprice]



# @app.callback(
#     [
#         Output('repairprof_modalsubmitted', 'is_open'),
#         Output('repairprof_feedback_message', 'children'),
#         Output('repairprof_closebtn', 'href'),
#     ],
#     [
#         Input('repairprof_savebtn', 'n_clicks'),
#         Input('repairprof_cancelbtn', 'n_clicks'),
#         Input('repairprof_closebtn', 'n_clicks'),
#     ],
#     [
#         State('repairprof_repairid', 'data'),
#         State('repairprof_removerecord', 'value'),
#         State('repairprof_toload', 'data'),

#         State('repairprof_startdate', 'date'),
#         State('repairprof_carbeingrepaired', 'value'),
#         State('repairprof_remarks', 'value'),

#         State('repairprof_lineitem', 'value'),      #11
#         State('repairprof_carbeingrepaired', 'value'),

#         State('repairprof_repairstatus', 'value'),
        
#     ]
# )
# def finishTransaction(submitbtn, cancelbtn, closebtn,
#                       repair_id, removerecord, iseditmode,
#                       transactiondate, car, remarks,
#                       itemid, supplierid,
#                       repair_status):
    
#     ctx = dash.callback_context
#     if ctx.triggered:
#         # eventid = name of the element that caused the trigger
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         openmodal = False
#         feedbackmessage = ''
#         okay_href = None
#     else:
#         raise PreventUpdate
    
#     if eventid == 'repairprof_savebtn' and submitbtn:
#         openmodal = True
        
#         # check if we have line items
#         if not repair_id:
#             feedbackmessage = "You have not filled out the form."
            
#         elif not utils.checkRepairLineItems(repair_id):
#             feedbackmessage = "Please add line items"
            
#         elif removerecord:
#             utils.deleteRepairTransaction(repair_id)
#             utils.deleteRepair_repairpart(repair_id)

# #             itemid_list = util.retrieve_item_id(po_id)
# #             for item_id in itemid_list:
# #                 if not util.check_supplier_repair_part_entries(item_id, supplierid):
# #                     util.delete_repair_parts_repair_parts_supplier(item_id, supplierid)
                    
# #             #make function for deleting repair_parts_po_repair_part entries
            
#             feedbackmessage = "Record has been deleted. Click Okay to go back to Car Repairs Management."
#             okay_href = '/car_repair'

#         elif not transactiondate or not car or not remarks:
#             feedbackmessage = "Please fill out all required fields (date, supplier, remarks) before saving."
            
#         else: #when you are adding/subtracting line items leaving u with more than 1 line item
#             # make function for updating repair_parts_po_repair_part entries

#             sql_update = """
#                 UPDATE car_repair
#                 SET repair_date = %s, 
#                 car_id = %s, 
#                 repair_remarks = %s,
#                 repair_status_id = %s
#                 WHERE repair_id = %s
#             """

#             values_update = [transactiondate, car, remarks, repair_status, repair_id]

#             db.modifydatabase(sql_update, values_update)


#             feedbackmessage = "Car Repair is saved. Click Okay to go back to Car Repairs Management."
#             okay_href = '/car_repair'
            
#     elif eventid == 'repairprof_cancelbtn' and cancelbtn:
#         openmodal = True
        
#         if not repair_id:
#             feedbackmessage = "Click Okay to go back to Car Repairs Management."
#             okay_href = '/car_repair'

#             print(repair_id)
        
#         elif iseditmode and repair_id:
#             feedbackmessage = "Changes have been discarded. Click Okay to go back to Car Repairs Management."
#             okay_href = '/car_repair'
        
#         else:
#             feedbackmessage = "Click Okay to go back to Car Repairs Management."
#             okay_href = '/car_repair'
            
    
#     elif eventid == 'repairprof_closebtn' and closebtn:
#         pass
    
#     else:
#         raise PreventUpdate
    
#     return [openmodal, feedbackmessage, okay_href]

import json
from datetime import date
from urllib.parse import parse_qs, urlparse

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db
from pages import car_repair_utils as utils
from psycopg2 import DatabaseError

layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                # if edit mode, this gets a value of 1, else 0
                dcc.Store(id='repairprof_toload', storage_type='memory', data=0),
                
                # this gets the po_id 
                dcc.Store(id='repairprof_repairid', storage_type='memory', data=0),
                
                # this gets the po_item_id to edit
                dcc.Store(id='repairprof_linetoedit', storage_type='memory', data=0),
            ]
        ),

        html.H2("Car Repair Details"),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                html.Span(
                    "Go back to the previous page by clicking the button below! ",
                ),
                html.Br(),
                    dbc.Button("Go to Car Repair Page", href ='/car_repair', color ='success'),
                html.Br(),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("Repair Start Date", width=2),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='repairprof_startdate',
                                date=date.today()
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Label("Car Plate Number", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='repairprof_carbeingrepaired',
                                    clearable=True,
                                    searchable=True,
                                    options=[]
                                ), 
                                className="dash-bootstrap"
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Label("Repair Status", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='repairprof_repairstatus',
                                    clearable=True,
                                    searchable=True,
                                    options=[]
                                ), 
                                className="dash-bootstrap"
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Label("Repair Remarks", width=2),
                        dbc.Col(
                            dbc.Textarea(
                                className="mb-3",
                                placeholder="Add remarks",
                                id='repairprof_remarks'
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
            ]    
        ),
        html.Hr(),
        
        # We don't need a div here but I like using one
        # to signify a new section
        html.Div(
            [
                dbc.Alert("Please fill out the information above before proceeding", id='repairprof_alertmissingdata',
                          color='danger', is_open=False),
                dbc.Alert("Repeat plate number!", id='repairprof_repeatplatenumbererror',
                          color='danger', is_open=False),
                dbc.Alert("Repeat plate number!", id='repairprof_repeatplatenumbererror2',
                          color='danger', is_open=False),
                dbc.Button("Add Repair Part", id="repairprof_addlinebtn", 
                           color='primary', n_clicks=0,
                           style={'display':'inline-block','border-radius':'5px'}
                ),  
                html.Br(),
                html.Br(),
                html.Div(
                    # This will contain the table of line items
                    id='repairprof_lineitems'
                )
            ]    
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Add Repair Part", id='repairprof_linemodalhead'),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='repairprof_linealert', color='warning', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Repair Part", width=4),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            id='repairprof_lineitem',
                                            clearable=True,
                                            searchable=True,
                                            options=[]
                                        ), 
                                        className="dash-bootstrap"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Label("Unit Price", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="repairprof_lineunitprice", placeholder="Enter unit price"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3"
                        ),

                        dbc.Row(
                            [
                                dbc.Label("Qty", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="repairprof_lineqty", placeholder="Enter qty"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3"
                        ),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=4),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='repairprof_lineremove',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            # I want the label to be bold
                                            style={'fontWeight':'bold'}, 
                                        ),
                                        width=6,
                                        style={'margin': 'auto 0'}
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='repairprof_lineremove_div'
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        html.Div(
                            [
                                dbc.Button('Back', id='repairprof_cancellinebtn', color='secondary'),
                                dbc.Button('Save Repair Part', id='repairprof_savelinebtn', color='primary'),
                            ],
                            # these are to separate the buttons to opposite ends
                            className='d-flex justify-content-between',
                            style={'flex': '1'}
                        )
                    ]
                )
            ],
            id='repairprof_modal',
            backdrop='static',
            centered=True
        ),
        
        # enclosing the checklist in a Div so we can
        # hide it in Add Mode
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='repairprof_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'fontWeight':'bold'}, 
                        ),
                        width=6,
                        style={'margin': 'auto 0'}
                    ),
                ],
                className="mb-3",
            ),
            id='repairprof_removerecord_div'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Trying to leave the page...")),
                dbc.ModalBody("tempmessage", id='repairprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="repairprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="repairprof_modalsubmitted",
            is_open=False,
        ),
        html.Hr(),
        
        html.Div(
            [
                dbc.Button('Back', id='repairprof_cancelbtn', color='secondary'),
                dbc.Button('Submit', color="primary", id='repairprof_savebtn'),
            ],
            # these are to separate the buttons to opposite ends
            className='d-flex justify-content-between',
            style={'flex': '1'}
        )
    ]
)

@app.callback(
    [
        Output('repairprof_toload', 'data'),
        # we want to update the style of this element
        Output('repairprof_removerecord_div', 'style'),
        Output('repairprof_carbeingrepaired', 'options'),
        Output('repairprof_repairstatus', 'options')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def pageLoadOperations(pathname, search):
    
    if pathname == '/car_repair/car_repair_profile':
                
        # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        
        # to show the remove option?

        removediv_style = {'display': 'none'} if not to_load else None
        # if to_load = 0, then not to_load -> not 0 -> not False -> True


        sql_cardropdown = """ 
        SELECT car_plate_number AS label, car.car_id AS value
        FROM car
        INNER JOIN car_purchase_order ON car_purchase_order.car_id=car.car_id
        WHERE car_delete_ind =  False
        AND car_purchase_condition_id = 1
        """

        values_cardropdown = []
        cols_cardropdown = ['label', 'value']
        df_cardropdown = db.querydatafromdatabase(sql_cardropdown, values_cardropdown, cols_cardropdown)
        car_options = df_cardropdown.to_dict('records')


        sql_repairstatusdropdown = """
        SELECT repair_status_label AS label, repair_status_id AS value
        FROM repair_status
        where repair_status_delete_ind=False
        """

        values_repairstatusdropdown = []
        cols_repairstatusdropdown = ['label', 'value']
        df_repairstatusdropdown = db.querydatafromdatabase(sql_repairstatusdropdown, values_repairstatusdropdown, cols_repairstatusdropdown)
        repairstatus_options = df_repairstatusdropdown.to_dict('records')

    else:
        raise PreventUpdate

    return [to_load, removediv_style, car_options, repairstatus_options]

# INCOMPLETE
@app.callback(
    [
        Output('repairprof_startdate', 'date'),
        Output('repairprof_carbeingrepaired', 'value'),
        Output('repairprof_remarks', 'value'),
        Output('repairprof_repairstatus', 'value'),
    ],
    [
        Input('repairprof_toload', 'modified_timestamp'),
        # toload is a dcc.store element. To use them in Input(), 
        # property should be 'modified_timestamp'
    ],
    [
        State('repairprof_toload', 'data'),
        State('url', 'search') 
    ]
)
def populateRepairData(timestamp, toload, search):
    if toload == 1:
        
        parsed = urlparse(search)
        repair_id = int(parse_qs(parsed.query)['id'][0])
        
        sql = """SELECT repair_date, car_id, repair_remarks, repair_status_id
        FROM car_repair
        WHERE repair_id = %s"""
        val = [repair_id]
        col = ['date', 'supplier', 'remarks', 'repair_status']
        
        df = db.querydatafromdatabase(sql, val, col)
        
        transactiondate, car, remarks, repair_status = [df[i][0] for i in col]

        
    else:
        raise PreventUpdate
    
    return [transactiondate, car, remarks, repair_status]





@app.callback(
    [
        Output('repairprof_modal', 'is_open'),
        Output('repairprof_alertmissingdata', 'is_open'),
        Output('repairprof_lineremove_div', 'className'),
        Output('repairprof_repairid', 'data'),
        
        Output('repairprof_lineitem', 'options'),
        Output('repairprof_linealert', 'children'),
        Output('repairprof_linealert', 'is_open'),
        Output('repairprof_linetoedit', 'data'),
        
        Output('repairprof_lineitems', 'children'),
        Output('repairprof_linemodalhead', 'children'),
        Output('repairprof_savelinebtn', 'children'),
        Output('repairprof_repeatplatenumbererror', 'is_open')
    ],
    [
        Input('repairprof_addlinebtn', 'n_clicks'),
        Input('repairprof_savelinebtn', 'n_clicks'),
        Input('repairprof_cancellinebtn', 'n_clicks'),
        Input({'index': ALL, 'type': 'repairprof_editlinebtn'}, 'n_clicks'),
        
        Input('repairprof_toload', 'modified_timestamp'),
        
    ],
    [
        State('url', 'search'),
        State('repairprof_startdate', 'date'), #transaction date
        State('repairprof_remarks', 'value'),
        State('repairprof_repairid', 'data'),
        
        State('repairprof_lineitem', 'options'),    #10
        State('repairprof_lineitem', 'value'),      #11

        State('repairprof_carbeingrepaired', 'value'),          #car_id
        State('repairprof_repairstatus', 'value'),

        State('repairprof_lineunitprice', 'value'),
        State('repairprof_lineqty', 'value'),
        State('repairprof_linetoedit', 'data'),
        
        State('repairprof_lineremove', 'value'),
        State('repairprof_lineitems', 'children'),
        State('repairprof_toload', 'data'),
        State('repairprof_linemodalhead', 'children'),
        
        State('repairprof_savelinebtn', 'children'),
    ]
)

def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
                toload_timestamp,
                search, repair_startdate, remarks, repair_id,            #beginnning state
                item_options, itemid, 
                car_id, repair_status,
                itemprice, itemqty, linetoedit,
                removeitem, linetable, toload, linemodalhead,
                addlinebtntxt):
    
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        parsed = urlparse(search)
        
        # some default values
        openmodal = False
        openalert_missingdata = False
        openalert_platenumber = False
        lineremove_class = 'd-none' # hide the remove tickbox
        
        linealert_message = ''
        updatetable = False # for updating table of line items
    else:
        raise PreventUpdate
    
    Repair_requireddata = [
        repair_startdate,
        car_id,
        remarks
    ]
    
    if eventid == 'repairprof_addlinebtn' and addlinebtn and all(Repair_requireddata):
        openmodal = True
        item_options = utils.getItemDropdown('add', repair_id)       #MAKE NEW CALLBACK
        linetoedit = 0
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Add Repair Part'
        addlinebtntxt = 'Save Repair Part'

    
    elif eventid == 'repairprof_addlinebtn' and addlinebtn and not all(Repair_requireddata):
        openalert_missingdata = True
    
        
    elif eventid == 'repairprof_cancellinebtn' and cancelbtn:
        pass
    
    elif 'repairprof_editlinebtn' in eventid and any(editlinebtn):
        # if any of the buttons for editing si clicked
        
        openmodal = True
        lineremove_class = '' # show line remove option
        linetoedit = int(json.loads(eventid)['index'])
        item_options = utils.getItemDropdown('edit', repair_id)              #MAKE NEW CALLBACK
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Edit Line Item'
        addlinebtntxt = 'Update Line Item'
        
    elif eventid == 'repairprof_toload' and toload == 1:
        updatetable = True
        repair_id = int(parse_qs(parsed.query)['id'][0])

        
    elif eventid == 'repairprof_savelinebtn' and savebtn:
        # validate inputs
        inputs = [
            itemid, 
            itemprice,
            utils.converttoint(itemqty)>0                                    #MAKE NEW CALLBACK
        ]
        
        if not all(inputs):
            linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
        else:
            # proceed to saving the line item
            
            newline = {
                'itemid': itemid,
                'itemqty': int(itemqty),
                'unitprice': float(itemprice),
                'carid': car_id
            }
            
            # if add mode:
            if linetoedit == 0:
                # if PO record not yet in db, save PO first
                try:
                    if not repair_id:
                        repair_id = utils.createRepairrecord(repair_startdate, remarks, car_id, repair_status)
                except DatabaseError as e:
                    openalert_platenumber = True

                try:
                    utils.manageRepairItem(repair_id, newline)
                except DatabaseError as e:
                    openalert_platenumber = True                                                  #MAKE NEW CALLBACK
            
    #             # reflect add row entry for repair_parts_repair_parts_supplier table, delete_ind=false
    #             util.insert_repair_parts_repair_parts_supplier(newline)
            
            else:
                if removeitem:
                    utils.removeRepairItem(linetoedit)

    #                 if not util.check_supplier_repair_part_entries(itemid, car_id):               #MAKE NEW CALLBACK
    #                     util.delete_repair_parts_repair_parts_supplier(itemid, car_id)            #MAKE NEW CALLBACK



                # reflect remove row entry for repair_parts_repair_parts_supplier table, delete_ind=True
                
                else:
                # reflect add row entry for repair_parts_repair_parts_supplier table, delete_ind=false
                    utils.manageRepairItem(repair_id, newline)                                               #MAKE NEW CALLBACK
                    # util.insert_repair_parts_repair_parts_supplier(newline)                                 #MAKE NEW CALLBACK
                
            updatetable = True
    
    else:
        raise PreventUpdate
    
    
    if updatetable:
        df = utils.queryRepairItems(repair_id)                                                               #MAKE NEW CALLBACK
        
        if df.shape[0]:
            linetable = utils.formatRepairTable(df)          #MAKE NEW CALLBACK
        else:
            linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

    # if we have an error prompt, linealert should open
    openalert_linealert = bool(linealert_message)
    
    return [
        openmodal, 
        openalert_missingdata, 
        lineremove_class,
        repair_id,
        
        item_options,
        linealert_message,
        openalert_linealert,
        linetoedit,
        
        linetable,
        linemodalhead,
        addlinebtntxt,

        openalert_platenumber

    ]


# OK
@app.callback(
    [
        Output('repairprof_lineitem', 'value'),
        Output('repairprof_lineqty', 'value'),
        Output('repairprof_lineremove', 'value'),
        Output('repairprof_lineunitprice', 'value')
        
    ],
    [
        Input('repairprof_addlinebtn', 'n_clicks'),
        Input('repairprof_linetoedit', 'modified_timestamp'),
    ],
    [
        State('repairprof_linetoedit', 'data'),
        State('repairprof_lineitem', 'value'),
        State('repairprof_lineqty', 'value'),
        State('repairprof_lineremove', 'value'),
        State('repairprof_lineunitprice', 'value'),
    
    ]
)
def clearFields(addlinebtn, line_timestamp, 
                
                linetoedit, itemid, itemqty, removeitem, itemprice):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'repairprof_addlinebtn' and addlinebtn:
        itemid, itemqty, itemprice = None, None, None
        # itemprice = None
        removeitem = []
        
    elif eventid == 'repairprof_linetoedit' and linetoedit:
        itemid, itemqty, itemprice = utils.getRepairPartLineData(linetoedit)
        removeitem = []
        
    else:
        raise PreventUpdate
    
    return [itemid, itemqty, removeitem, itemprice]



@app.callback(
    [
        Output('repairprof_modalsubmitted', 'is_open'),
        Output('repairprof_feedback_message', 'children'),
        Output('repairprof_closebtn', 'href'),
        Output('repairprof_repeatplatenumbererror2', 'is_open')
    ],
    [
        Input('repairprof_savebtn', 'n_clicks'),
        Input('repairprof_cancelbtn', 'n_clicks'),
        Input('repairprof_closebtn', 'n_clicks'),
    ],
    [
        State('repairprof_repairid', 'data'),
        State('repairprof_removerecord', 'value'),
        State('repairprof_toload', 'data'),

        State('repairprof_startdate', 'date'),
        State('repairprof_carbeingrepaired', 'value'),
        State('repairprof_remarks', 'value'),

        State('repairprof_lineitem', 'value'),      #11
        State('repairprof_carbeingrepaired', 'value'),

        State('repairprof_repairstatus', 'value'),
        
    ]
)
def finishTransaction(submitbtn, cancelbtn, closebtn,
                      repair_id, removerecord, iseditmode,
                      transactiondate, car, remarks,
                      itemid, supplierid,
                      repair_status):
    
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
        openalert_platenumber = False
    else:
        raise PreventUpdate
    
    if eventid == 'repairprof_savebtn' and submitbtn:
        openmodal = True
        
        # check if we have line items
        if not repair_id:
            feedbackmessage = "You have not filled out the form."
            
        elif not utils.checkRepairLineItems(repair_id):
            feedbackmessage = "Please add line items"
            
        elif removerecord:
            utils.deleteRepairTransaction(repair_id)
            utils.deleteRepair_repairpart(repair_id)

#             itemid_list = util.retrieve_item_id(po_id)
#             for item_id in itemid_list:
#                 if not util.check_supplier_repair_part_entries(item_id, supplierid):
#                     util.delete_repair_parts_repair_parts_supplier(item_id, supplierid)
                    
#             #make function for deleting repair_parts_po_repair_part entries
            
            feedbackmessage = "Record has been deleted. Click Okay to go back to Car Repairs Management."
            okay_href = '/car_repair'

        elif not transactiondate or not car or not remarks:
            feedbackmessage = "Please fill out all required fields (date, supplier, remarks) before saving."
            
        else: #when you are adding/subtracting line items leaving u with more than 1 line item
            # make function for updating repair_parts_po_repair_part entries

            sql_update = """
                UPDATE car_repair
                SET repair_date = %s, 
                car_id = %s, 
                repair_remarks = %s,
                repair_status_id = %s
                WHERE repair_id = %s
            """

            values_update = [transactiondate, car, remarks, repair_status, repair_id]

            try:
                db.modifydatabase(sql_update, values_update)
                feedbackmessage = "Car Repair is saved. Click Okay to go back to Car Repairs Management."
                okay_href = '/car_repair'
            except DatabaseError:
                openalert_platenumber = True
                feedbackmessage = "Error! A repeat plate number has been entered. Only one repair entry is allowed per car."

            
    elif eventid == 'repairprof_cancelbtn' and cancelbtn:
        openmodal = True
        
        if not repair_id:
            feedbackmessage = "Click Okay to go back to Car Repairs Management."
            okay_href = '/car_repair'

            print(repair_id)
        
        elif iseditmode and repair_id:
            feedbackmessage = "Changes have been discarded. Click Okay to go back to Car Repairs Management."
            okay_href = '/car_repair'
        
        else:
            feedbackmessage = "Click Okay to go back to Car Repairs Management."
            okay_href = '/car_repair'
            
    
    elif eventid == 'repairprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href, openalert_platenumber]