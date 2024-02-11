# # This file contains the functions used in po_profile.py
# import dash_bootstrap_components as dbc
# from dash import html

# from apps import dbconnect as db


# def getItemDropdown(mode='add', repair_id=0, car_repair_repair_part_id=None): #OK
#     sql = """ SELECT item_id as value,
#         item_name as label
#     FROM repair_part
#     WHERE
#         TRUE
#     """
#     # we put true so we can add additional constraints below
#     val = []
    
#     if mode == 'add' and not repair_id:
#         # if po is not yet in db
#         pass
    
#     elif mode == 'add' and repair_id:
#         # if po already in db
#         # exclude the items already in the PO
        
#         sql += """ AND item_id NOT IN (
#             SELECT item_id 
#             FROM car_repair_repair_part 
#             WHERE repair_id = %s
#                 AND NOT car_repair_repair_part_delete_ind
#         )"""
#         val += [repair_id]
        
#     else:
#         # if edit mode, add the current item_id in the options
#         # so it appears on the dropdown
#         sql += """ AND item_id NOT IN (
#             SELECT item_id 
#             FROM car_repair_repair_part 
#             WHERE repair_id = %s
#                 AND car_repair_repair_part_id <> %s
#                 AND NOT car_repair_repair_part_delete_ind
#         )"""
#         val += [repair_id, car_repair_repair_part_id]
    
#     df = db.querydatafromdatabase(sql, val, ['value', 'label'])
    
#     return df.to_dict('records')


# def converttoint(num):
#     try:
#         num = int(num)
#         if num > 0:
#             return num
#         else:
#             return 0
#     except:
#         return 0
    

# def createRepairrecord(date, remarks, car, repair_status):
#     sql = """INSERT INTO car_repair(repair_date, repair_remarks, car_id, repair_status_id)
#     VALUES (%s, %s, %s, %s) 
#     RETURNING repair_id"""
#     values = [date, remarks, car, repair_status]
#     repair_id = db.modifydatabasereturnid(sql, values)
#     return repair_id



# # def updatePOrecord(date, remarks, supplier, po_id):
# #     sql = """UPDATE repair_parts_po_transaction
# #     SET po_date = %s, 
# #     po_remarks = %s, 
# #     supplier_id = %s
# #     WHERE po_id = %s"""
# #     values = [date, remarks, supplier, po_id]
# #     db.modifydatabase(sql, values)


    
# def manageRepairItem(repair_id, newline):
    
#     # note that the table has restrictions 
#     # on having unique(po_id, item_id).
#     # If we insert a duplicate row, this sql command 
#     # updates the existing record instead.
#     sql = """INSERT INTO car_repair_repair_part(repair_id, item_id, repair_part_used_quantity, repair_part_price)
#     VALUES (%(repairid)s, %(itemid)s, %(qty)s, %(unit_price)s) 
#     ON CONFLICT (repair_id, item_id) DO 
#     UPDATE 
#         SET 
#             car_repair_repair_part_delete_ind = false,
#             repair_part_used_quantity = %(qty)s,
#             repair_part_price = %(unit_price)s"""
#     values = {
#         'repairid': repair_id,
#         'itemid': newline['itemid'],
#         'qty': newline['itemqty'],
#         'unit_price': newline['unitprice']
#     }
#     db.modifydatabase(sql, values)


# def removeRepairItem(car_repair_repair_part_id):
#     sql = """UPDATE car_repair_repair_part
#     SET car_repair_repair_part_delete_ind = true
#     WHERE car_repair_repair_part_id = %s"""
    
#     val = [car_repair_repair_part_id]
#     db.modifydatabase(sql, val)
    

# def queryRepairItems(repair_id):
#     sql = """SELECT
#     item_name,
#     repair_part_used_quantity,
#     repair_part_price,
#     (repair_part_used_quantity * repair_part_price) AS total_amount,
#     car_repair_repair_part_id
# FROM
#     car_repair_repair_part pi
# INNER JOIN
#     repair_part i ON i.item_id = pi.item_id
# WHERE 
#     NOT car_repair_repair_part_delete_ind AND
#     repair_id = %s
# """

#     val = [repair_id]
#     cols = ['Item', 'Qty', 'Unit Price', 'Total Amount', 'id']
    
#     return db.querydatafromdatabase(sql, val, cols)


# def formatRepairTable(df):
#     # align numbers to the right
#     df['Qty'] = df['Qty'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))
#     df['Unit Price'] = df['Unit Price'].apply(lambda num: html.Div(f"₱{num:,.2f}"))
#     df['Total Amount'] = df['Total Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}"))
            
#     # add the Edit buttons
#     buttons = []
#     for id in df['id']:
#         buttons += [
#             html.Div(
#                 dbc.Button('Edit', id={'index':id, 'type': 'repairprof_editlinebtn'},
#                             size='sm', color='warning'),
#                 style={'text-align': 'center'}
#             )
#         ]
    
#     df['Action'] = buttons
    
#     # add an item# column
#     df.insert(
#         loc=0, 
#         column='Item #', 
#         value=[html.Div(i+1, style={'text-align': 'right'}) for i in range(len(df.index))]
#     )
    
#     # remove the id column
#     df.drop('id', axis=1, inplace=True)
    
#     return dbc.Table.from_dataframe(df, striped=True, bordered=True,
#             hover=True, size='sm', style={'text-align': 'right'})
    
    


# def getRepairPartLineData(lineid):
#     sql = """SELECT
#         item_id, 
#         repair_part_used_quantity,
#         repair_part_price
#     FROM car_repair_repair_part
#     WHERE 
#         car_repair_repair_part_id = %s
#     """
#     val = [lineid]
#     cols = ['item', 'qty', 'amount']
    
#     df = db.querydatafromdatabase(sql, val, cols)
    
#     return [df[i][0] for i in cols]



# def checkRepairLineItems(repair_id):
#     sql = """SELECT COUNT(*)
#     FROM car_repair_repair_part
#     WHERE NOT car_repair_repair_part_delete_ind
#         AND repair_id = %s"""
#     val = [repair_id]
#     col = ['count']
    
#     df = db.querydatafromdatabase(sql, val, col)
    
#     return df['count'][0]


# def deleteRepairTransaction(repair_id):
#     sql = """UPDATE car_repair
#     SET car_repair_delete_ind = true
#     WHERE repair_id = %s"""
    
#     val = [repair_id]
#     db.modifydatabase(sql, val)



# def deletePO_repairpart(po_id):
#     sql = """UPDATE repair_parts_po_repair_part
#     SET po_item_delete_ind = true
#     WHERE po_id = %s"""

#     val = [po_id]
#     db.modifydatabase(sql, val)


# def deleteRepair_repairpart(repair_id):
#     sql = """UPDATE car_repair_repair_part
#     SET car_repair_repair_part_delete_ind = true
#     WHERE repair_id = %s"""

#     val = [repair_id]
#     db.modifydatabase(sql, val)



# # # functions for repair_parts_repair_parts_supplier table
# # def insert_repair_parts_repair_parts_supplier(newline):
# #     # Prepare SQL query
# #     sql = """
# #     INSERT INTO repair_parts_repair_parts_supplier(item_id, supplier_id, repair_parts_repair_parts_supplier_delete_ind)
# #     VALUES (%(itemid)s, %(supplier_id)s, false) 
# #     ON CONFLICT (item_id, supplier_id) DO UPDATE
# #     SET
# #         repair_parts_repair_parts_supplier_delete_ind = false
# #     """
    
# #     # Prepare values for the SQL query
# #     values = {
# #         'itemid': newline['itemid'],
# #         'supplier_id': newline['supplierid']
# #     }
    
# #     # Execute SQL query using db.modifydatabase
# #     db.modifydatabase(sql, values)


# # def check_supplier_repair_part_entries(item_id, supplier_id):
# #     sql = """SELECT COUNT(*)
# #     FROM repair_parts_po_transaction
# #     INNER JOIN repair_part_supplier ON repair_parts_po_transaction.supplier_id=repair_part_supplier.supplier_id
# #     INNER JOIN repair_parts_po_repair_part ON repair_parts_po_repair_part.po_id = repair_parts_po_transaction.po_id
# #     WHERE NOT po_item_delete_ind 
# #     AND item_id = %s
# #     AND repair_part_supplier.supplier_id = %s"""
# #     val = [item_id, supplier_id]
# #     col = ['count']
# #     df = db.querydatafromdatabase(sql, val, col)
# #     print(item_id)
# #     print(supplier_id)
# #     print("check suppplier entry function")
# #     return df['count'][0]


# # def delete_repair_parts_repair_parts_supplier(item_id, supplier_id):
# #     # Prepare SQL query
# #     sql = """
# #     UPDATE repair_parts_repair_parts_supplier
# #     SET repair_parts_repair_parts_supplier_delete_ind = true
# #     WHERE item_id =%s AND supplier_id = %s"""
    
# #     # Prepare values for the SQL query
# #     values = [item_id, supplier_id]
# #     db.modifydatabase(sql, values)
# #     print(item_id)
# #     print(supplier_id)
# #     print("hello")



# # def retrieve_item_id(po_id):
# #     sql = """SELECT repair_parts_po_repair_part.item_id FROM repair_parts_po_repair_part
# #     INNER JOIN repair_part ON repair_part.item_id=repair_parts_po_repair_part.item_id
# #     WHERE po_id = %s"""

# #     value = [po_id]
# #     col = ['item_id']
# #     df = db.querydatafromdatabase(sql, value, col)
# #     return df['item_id'].tolist()

# This file contains the functions used in po_profile.py
import dash_bootstrap_components as dbc
from dash import html

from apps import dbconnect as db


def getItemDropdown(mode='add', repair_id=0, car_repair_repair_part_id=None): #OK
    sql = """ SELECT item_id as value,
        item_name as label
    FROM repair_part
    WHERE
        TRUE
    """
    # we put true so we can add additional constraints below
    val = []
    
    if mode == 'add' and not repair_id:
        # if po is not yet in db
        pass
    
    elif mode == 'add' and repair_id:
        # if po already in db
        # exclude the items already in the PO
        
        sql += """ AND item_id NOT IN (
            SELECT item_id 
            FROM car_repair_repair_part 
            WHERE repair_id = %s
                AND NOT car_repair_repair_part_delete_ind
        )"""
        val += [repair_id]
        
    else:
        # if edit mode, add the current item_id in the options
        # so it appears on the dropdown
        sql += """ AND item_id NOT IN (
            SELECT item_id 
            FROM car_repair_repair_part 
            WHERE repair_id = %s
                AND car_repair_repair_part_id <> %s
                AND NOT car_repair_repair_part_delete_ind
        )"""
        val += [repair_id, car_repair_repair_part_id]
    
    df = db.querydatafromdatabase(sql, val, ['value', 'label'])
    
    return df.to_dict('records')


def converttoint(num):
    try:
        num = int(num)
        if num > 0:
            return num
        else:
            return 0
    except:
        return 0
    

def createRepairrecord(date, remarks, car, repair_status):
    sql = """INSERT INTO car_repair(repair_date, repair_remarks, car_id, repair_status_id)
    VALUES (%s, %s, %s, %s) 
    RETURNING repair_id"""
    values = [date, remarks, car, repair_status]
    repair_id = db.modifydatabasereturnid(sql, values)
    return repair_id



# def updatePOrecord(date, remarks, supplier, po_id):
#     sql = """UPDATE repair_parts_po_transaction
#     SET po_date = %s, 
#     po_remarks = %s, 
#     supplier_id = %s
#     WHERE po_id = %s"""
#     values = [date, remarks, supplier, po_id]
#     db.modifydatabase(sql, values)


    
def manageRepairItem(repair_id, newline):
    
    # note that the table has restrictions 
    # on having unique(po_id, item_id).
    # If we insert a duplicate row, this sql command 
    # updates the existing record instead.
    sql = """INSERT INTO car_repair_repair_part(repair_id, item_id, repair_part_used_quantity, repair_part_price)
    VALUES (%(repairid)s, %(itemid)s, %(qty)s, %(unit_price)s) 
    ON CONFLICT (repair_id, item_id) DO 
    UPDATE 
        SET 
            car_repair_repair_part_delete_ind = false,
            repair_part_used_quantity = %(qty)s,
            repair_part_price = %(unit_price)s"""
    values = {
        'repairid': repair_id,
        'itemid': newline['itemid'],
        'qty': newline['itemqty'],
        'unit_price': newline['unitprice']
    }
    db.modifydatabase(sql, values)


def removeRepairItem(car_repair_repair_part_id):
    sql = """UPDATE car_repair_repair_part
    SET car_repair_repair_part_delete_ind = true
    WHERE car_repair_repair_part_id = %s"""
    
    val = [car_repair_repair_part_id]
    db.modifydatabase(sql, val)
    

def queryRepairItems(repair_id):
    sql = """SELECT
    item_name,
    repair_part_used_quantity,
    repair_part_price,
    (repair_part_used_quantity * repair_part_price) AS total_amount,
    car_repair_repair_part_id
FROM
    car_repair_repair_part pi
INNER JOIN
    repair_part i ON i.item_id = pi.item_id
WHERE 
    NOT car_repair_repair_part_delete_ind AND
    repair_id = %s
"""

    val = [repair_id]
    cols = ['Item', 'Qty', 'Unit Price', 'Total Amount', 'id']
    
    return db.querydatafromdatabase(sql, val, cols)


def formatRepairTable(df):
    # align numbers to the right
    df['Item'] = df['Item'].apply(lambda num: html.Div(f"{num:}", style={'text-align': 'right'}))
    df['Qty'] = df['Qty'].apply(lambda num: html.Div(f"{num:}", style={'text-align': 'right'}))
    df['Unit Price'] = df['Unit Price'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
    df['Total Amount'] = df['Total Amount'].apply(lambda num: html.Div(f"₱{num:,.2f}", style={'text-align': 'right'}))
    
    # add the Edit buttons
    buttons = []
    for id in df['id']:
        buttons += [
            html.Div(
                dbc.Button('Edit', id={'index':id, 'type': 'repairprof_editlinebtn'},
                            size='sm', color='warning'),
                style={'text-align': 'center'}
            )
        ]
    
    df['Action'] = buttons
    
    # add an item# column
    df.insert(
        loc=0, 
        column='Item #', 
        value=[html.Div(i+1, style={'text-align': 'right'}) for i in range(len(df.index))]
    )
    
    # remove the id column
    df.drop('id', axis=1, inplace=True)
    
    return dbc.Table.from_dataframe(df, striped=True, bordered=True,
            hover=True, size='sm', style={'text-align': 'center'})
    
    


def getRepairPartLineData(lineid):
    sql = """SELECT
        item_id, 
        repair_part_used_quantity,
        repair_part_price
    FROM car_repair_repair_part
    WHERE 
        car_repair_repair_part_id = %s
    """
    val = [lineid]
    cols = ['item', 'qty', 'amount']
    
    df = db.querydatafromdatabase(sql, val, cols)
    
    return [df[i][0] for i in cols]



def checkRepairLineItems(repair_id):
    sql = """SELECT COUNT(*)
    FROM car_repair_repair_part
    WHERE NOT car_repair_repair_part_delete_ind
        AND repair_id = %s"""
    val = [repair_id]
    col = ['count']
    
    df = db.querydatafromdatabase(sql, val, col)
    
    return df['count'][0]


def deleteRepairTransaction(repair_id):
    sql = """UPDATE car_repair
    SET car_repair_delete_ind = true
    WHERE repair_id = %s"""
    
    val = [repair_id]
    db.modifydatabase(sql, val)



def deletePO_repairpart(po_id):
    sql = """UPDATE repair_parts_po_repair_part
    SET po_item_delete_ind = true
    WHERE po_id = %s"""

    val = [po_id]
    db.modifydatabase(sql, val)


def deleteRepair_repairpart(repair_id):
    sql = """UPDATE car_repair_repair_part
    SET car_repair_repair_part_delete_ind = true
    WHERE repair_id = %s"""

    val = [repair_id]
    db.modifydatabase(sql, val)

def checkExistingRepairRecordForCar(car_id):
    # Assuming you have a connection to your database, you can execute a query to check for existing records
    sql = "SELECT COUNT(*) FROM car_repair WHERE car_id = %s"
    values = [car_id]
    column = ['count']
    result = db.querydatafromdatabase(sql, values, column)
    result_value = result['count'].iloc[0]
    return result_value

    
def deletenullrepairid_repairpart(repair_id):
    sql = """UPDATE car_repair_repair_part
             SET car_repair_repair_part_delete_ind = true
             WHERE repair_id = 0"""

    val = []
    db.modifydatabase(sql, val)


# # functions for repair_parts_repair_parts_supplier table
# def insert_repair_parts_repair_parts_supplier(newline):
#     # Prepare SQL query
#     sql = """
#     INSERT INTO repair_parts_repair_parts_supplier(item_id, supplier_id, repair_parts_repair_parts_supplier_delete_ind)
#     VALUES (%(itemid)s, %(supplier_id)s, false) 
#     ON CONFLICT (item_id, supplier_id) DO UPDATE
#     SET
#         repair_parts_repair_parts_supplier_delete_ind = false
#     """
    
#     # Prepare values for the SQL query
#     values = {
#         'itemid': newline['itemid'],
#         'supplier_id': newline['supplierid']
#     }
    
#     # Execute SQL query using db.modifydatabase
#     db.modifydatabase(sql, values)


# def check_supplier_repair_part_entries(item_id, supplier_id):
#     sql = """SELECT COUNT(*)
#     FROM repair_parts_po_transaction
#     INNER JOIN repair_part_supplier ON repair_parts_po_transaction.supplier_id=repair_part_supplier.supplier_id
#     INNER JOIN repair_parts_po_repair_part ON repair_parts_po_repair_part.po_id = repair_parts_po_transaction.po_id
#     WHERE NOT po_item_delete_ind 
#     AND item_id = %s
#     AND repair_part_supplier.supplier_id = %s"""
#     val = [item_id, supplier_id]
#     col = ['count']
#     df = db.querydatafromdatabase(sql, val, col)
#     print(item_id)
#     print(supplier_id)
#     print("check suppplier entry function")
#     return df['count'][0]


# def delete_repair_parts_repair_parts_supplier(item_id, supplier_id):
#     # Prepare SQL query
#     sql = """
#     UPDATE repair_parts_repair_parts_supplier
#     SET repair_parts_repair_parts_supplier_delete_ind = true
#     WHERE item_id =%s AND supplier_id = %s"""
    
#     # Prepare values for the SQL query
#     values = [item_id, supplier_id]
#     db.modifydatabase(sql, values)
#     print(item_id)
#     print(supplier_id)
#     print("hello")



# def retrieve_item_id(po_id):
#     sql = """SELECT repair_parts_po_repair_part.item_id FROM repair_parts_po_repair_part
#     INNER JOIN repair_part ON repair_part.item_id=repair_parts_po_repair_part.item_id
#     WHERE po_id = %s"""

#     value = [po_id]
#     col = ['item_id']
#     df = db.querydatafromdatabase(sql, value, col)
#     return df['item_id'].tolist()