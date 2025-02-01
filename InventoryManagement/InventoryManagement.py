from asyncio.windows_events import NULL
from gettext import Catalog
from pathlib import Path
import json
import os

inventory_current_file_name = "inventory_current.json"
inventory_history_file_name = "inventory_history.json"
orderable_item_file_name = "orderable_items.json"
transaction_log_file_name = "transaction_log.json"
order_history_file_name = "order_history.json"   

def initialize():
    
    inventory_file_path = Path(inventory_current_file_name)
    if inventory_file_path.exists():
        print("Inventory Located.")
    else:
        print("Inventory Not Located... Generating Inventory.")
        temp_inventory_current = {
            1001:{'quantity':'10',
                  'count':'250'
                  },
            1002:{'quantity':'10',
                  'count':'10'
                  },
            1003:{'quantity':'3',
                  'count':'1440'}
            }
        with open(inventory_current_file_name, "w") as f:
            json.dump(temp_inventory_current, f, indent=4)
    
    # inventory_history_file_path = Path(inventory_history_file_name)
    # if inventory_history_file_path.exists():
    #     print("Inventory History Located.")
    # else:
    #     print("Inventory History Not Located... Generating Inventory History.")
    #     temp_inventory_history = {
    #         }
    #     with open(inventory_history_file_name, "w") as f:
    #         json.dump(temp_inventory_history, f, indent=4)
    
    orderable_items_file_path = Path(orderable_item_file_name)
    if orderable_items_file_path.exists():
        print("Orderable Items Catalogue Located.")
    else:
        print("Orderable Items Catalogue Not Located... Generating Orderable Items Catalogue.") 
        create_catalogue()

    transaction_log_file_path = Path(transaction_log_file_name)
    if transaction_log_file_path.exists():
        print("Transaction Log Located.")
    else:
        print("Transaction Log Not Located... Generating New Transaction Log.")
        temp_transaction_log = {
            0: {'orderID':'111',
                'itemID':'1001',
                'quantity':'10',
                'count':'250',
                'date':'2025-01-27'},
            1: {'orderID':'111',
                'itemID':'1002',
                'quantity':'10',
                'count':'10',
                'date':'2025-01-27'},
            3: {'orderID':'222',
                'itemID':'1003',
                'quantity':'2',
                'count':'960',
                'date':'2025-01-28'},
            4: {'userID':'123123',
                'itemID':'1003',
                'quantity':'1',
                'count':'480',
                'date':'2025-01-29'}
            }
        with open(transaction_log_file_name, "w") as f:
            json.dump(temp_transaction_log, f, indent=4)

    order_history_file_path = Path(order_history_file_name)
    if order_history_file_path.exists():
        print("Order History Located.")
    else:
        print("Order History Not Located... Generating New Order History Log.")
        temp_transaction_log = {
            0: {
                'order_number':'1098475-123',
                'status_dates':{
                    'placed':'2025-01-01',
                    'fulfilled':'2025-01-02',
                    'shipped':'2025-01-03',
                    'received':'2025-01-04'
                    },
                'supplier':'Sample Supplier',
                'item_list':{
                    '0':{
                        'itemID':'100',
                        'quantity':'1'
                        },
                    '1':{
                        'itemID':'101',
                        'quantity':'2'
                        }
                    },
                'special_instructions':'Sample Order'
                }
                        
    #status dates: placed, fulfilled, shipped, received
    #supplier
    #item list: itemID, quantity
    #special instructions
    
            }
        with open(order_history_file_name, "w") as f:
            json.dump(temp_transaction_log, f, indent=4)

    return

def create_catalogue():
    item_list = {1001: {"part_num":"721001",
                        "name":"Cell Culture Flask",
                        "brand":"NEST",
                        "category": "Consumable",
                        "subcategory": "Flasks",
                        "price":"$147.00",
                        "size":"1",
                        "units":"L",
                        "count":"25",
                        "supplier":"SoCalBioMed",
                        "website":"www.socalbiomed.com"
                        },
                 1002: {"part_num":"A1705",
                        "name":"Agarose LE",
                        "brand":"Benchmark",
                        "category": "Chemicals|Reagents",
                        "subcategory": "Agarose",
                        "price":"$369.00",
                        "size":"500",
                        "units":"g",
                        "count":"1",
                        "supplier":"SoCalBioMed",
                        "website":"www.socalbiomed.com"
                        },
                 1003: {"part_num":"K-2604",
                        "name":"Taq PCR PreMix, 0.2mL thin-wall 8-strip tubes",
                        "brand":"AccuPower",
                        "category": "Chemicals|Reagents",
                        "subcategory": "DNA/RNA Amplification",
                        "price":"$322.00",
                        "size":"50",
                        "units":"uL",
                        "count":"480",
                        "supplier":"SoCalBioMed",
                        "website":"www.socalbiomed.com"
                        },
                 }
    with open(orderable_item_file_name, "w") as f:
        json.dump(item_list, f, indent=4)
    return

def format_json_table(data):
    #works for inventory and transaction log
    #probably because they're unnested dictionaries
    import pandas as pd
    
    table = pd.DataFrame()

    for i in data.keys():
        temp = pd.DataFrame(columns=['ID'])
        temp['ID'] = [i]

        for j in data[i].keys():
            temp[j] = [data[i][j]]

        table = pd.concat([table,temp])
        
    table = table.sort_values(by='ID')
    table = table.reset_index(drop=True)
    
    return table

def get_orderable_items():
    
    f = open(orderable_item_file_name, 'r')
    txt = f.read()
    f.close()

    table = format_json_table(json.loads(txt))

    table = table.loc[:,["ID", 
                 "name",
                 "part_num",
                 "brand",
                 "category",
                 "subcategory",
                 "price",
                 "size",
                 "units",
                 "count",
                 "supplier",
                 "website"]]

    from IPython.display import display
    display(table)

    return

def get_inventory_current():
    f = open(inventory_current_file_name, 'r')
    txt = f.read()
    f.close()

    table = format_json_table(json.loads(txt))

    table = table.loc[:,['ID',
                 "name",
                 "brand",
                 "category",
                 "subcategory",
                 "size",
                 "units",
                 "count",
                 "quantity"
                 ]]
    #need to differentiate between counts and quantity - 1 quantity can have 1 or more counts
    #eg, 1 qty of a 50-count box of sample tubes - person should specify that box is removed and, based on the catalogue item, the program will deduct accordingly
    from IPython.display import display
    display(table)

    return

def get_transaction_log():
    f = open(transaction_log_file_name, 'r')
    txt = f.read()
    f.close()
    
    table = format_json_table(json.loads(txt))

    table = table.loc[:,["itemID",
                         "userID",
                         "orderID",
                         "count",
                         "quantity",
                         "date"
                         ]]
    #need to differentiate between counts and quantity - 1 quantity can have 1 or more counts
    #eg, 1 qty of a 50-count box of sample tubes - person should specify that box is removed and, based on the catalogue item, the program will deduct accordingly
    from IPython.display import display
    display(table)
    
    return

def add_item_to_order(catalogue_data, order_df):
    os.system('cls')
        
    import pandas as pd

    item_id = input("enter item ID: ")

    if item_id not in catalogue_data.keys():
        print("item ID not found in catalogue")
    else:
        temp = pd.DataFrame(columns = ['ID'])
        temp['ID'] = [item_id]

        for j in catalogue_data[item_id].keys():
            temp[j] = [catalogue_data[item_id][j]]
            
        temp = temp.loc[:,["ID", 
                 "name",
                 "part_num",
                 "brand",
                 "category",
                 "subcategory",
                 "price",
                 "size",
                 "units",
                 "count",
             "supplier",
             "website"]]
        from IPython.display import display
        display(temp)
            
        if input("confirm ordering item ID {} (y/n):".format(item_id)) != 'y':
            print("item removed from order.")
            
        else:
            item_qty = input("enter item quantity: ")
            if input("confirm ordering qty {} of item ID {} (y/n): ".format(item_qty, item_id)) != 'y':
                print("item removed from order.")
            else:
                order_df.loc[len(order_df)] = [item_id, item_qty]
    return order_df

def change_ordered_itemid(catalogue_data, order_df):

    return order_df
    
def change_ordered_item_qty(catalogue_data, order_df):

    return order_df
    
def remove_ordered_item(order_df):
    print(order_df)
    item_delete = input("select itemid to remove: ")

    order_df = order_df[order_df.itemID != item_delete]

    return order_df

def create_new_order(order_df):
    #creates a new entry in the "order_history.json"   file
    #start new order with new order number
    #locate item(s) by item ID from catalogue
    #extract relevant data from catalogue
    #add order number and date for transaction log
    #-------> add option to add ordered item directly to catalogue
    #-------> ie. "ItemID not found. Add new Item to Catalogue?" --> later when received?
    #-------> would use ItemID to start and then call add_orderable_item_to_catalogue to get rest of imformation

    f = open(order_history_file_name, 'r')
    txt = f.read()
    f.close()
    data = json.loads(txt)

    #order number
    #status dates: placed, fulfilled, shipped, received
    #supplier
    #item list: itemID, quantity
    #special instructions

    max_ID = int(max(data.keys()))+1

    order_placed = input("order place date: ")
    order_fulfilled = "NA"
    order_shipped = "NA"
    order_received = "NA"
    supplier = input("order supplier: ")
    order_number = input("supplier order number: ")
    order_special = input("order instructions: ")

    state_date_list = ["placed", "fulfilled", "shipped","received"]
    state_date_entries = [order_placed, order_fulfilled, order_shipped, order_received]
    
    item_json = order_df.to_json(orient="index")
    parsed = json.loads(item_json)

    
    state_list = ["ID",
                 "order_number",
                 "status_dates",
                 "supplier",
                 "item_list",
                 "special_instructions"]

    state_entries = []
    state_entries.append(max_ID)
    state_entries.append(order_number)
    state_entries.append({state_date_list[i]: state_date_entries[i] for i in range(len(state_date_entries))})
    state_entries.append(supplier)
    state_entries.append(parsed)
    state_entries.append(order_special)

    # state_entries[0] = max_ID
    # state_entries[1] = order_number
    # state_entries[2] = {state_date_list[i]: state_date_entries[i] for i in range(len(state_date_entries))}
    # state_entries[3] = supplier
    # state_entries[4] = order_df.to_json(orient="index")
    # state_entries[5] = order_special

    data[state_entries[0]] = {state_list[i]: state_entries[i] for i in range(1,len(state_list))}

    
        
    #print(state_entries)

    #print(data)

    js = json.dumps(data)
    f = open(order_history_file_name, 'w')
    f.write(js)
    f.close()
 

    return

def order_item_from_catalogue():
    import json
    import pandas as pd
    
    f = open(orderable_item_file_name, 'r')
    txt = f.read()
    f.close()
    catalogue_data = json.loads(txt)

    order_status = "empty"
    order_df = pd.DataFrame(columns = ['itemID','quantity'])

    while order_status != "confirmed" and order_status != "cancelled":
        print("Order Menu: ")
        if order_status == "empty":
            order_action = int(input(" 1: add item to order\n"+
                                     " 0: cancel order\n")
                               )
            if order_action == 1:
                order_df = add_item_to_order(catalogue_data, order_df)
                if len(order_df) == 0:
                    order_status = "empty"
                else:
                    order_status = "unconfirmed"
            elif order_action == 0:
                order_status = "cancelled"
        else:
            order_action = int(input(" 1: add item to order\n"+
                                    #" 2: change itemID\n"+
                                    #" 3: change item quantity\n"+
                                    " 4: remove item from order\n"+
                                    " 5: show current order\n"+
                                    " 9: confirm order\n"+
                                    " 0: cancel order\n")
                               )
            if order_action == 1:
                order_df = add_item_to_order(catalogue_data, order_df)
                order_status = "unconfirmed"
            elif order_action == 2:
                order_df = change_ordered_item_qty(catalogue_data, order_df)
                order_status = "unconfirmed"
            elif order_action == 3:
                order_df = change_ordered_item_qty(catalogue_data, order_df)
                order_status = "unconfirmed"
            elif order_action == 4:
                order_df = remove_ordered_item(catalogue_data, order_df)
                if len(order_df) == 0:
                    order_status = "empty"
                else:
                    order_status = "unconfirmed"
            elif order_action == 5:
                order_status ="unconfirmed" 
                print(order_df)

            elif order_action == 9:
                print(order_df)
                if input("confirm order (y/n): ")=='y':
                    order_status ="confirmed"
                else:
                    order_status = "unconfirmed"
                
            elif order_action == 0:
                order_status = "cancelled"
 
    if order_status == "confirmed":
        create_new_order(order_df)


    return

def update_order_status():
    #when order received date is updated, call add_ordered_item_to_inventory
    update_continue = True
    send_to_inventory = False

    while update_continue:
        f = open(order_history_file_name, 'r')
        txt = f.read()
        f.close()
        data = json.loads(txt)
        
        order_update = input("enter order id to update or 'n' to cancel: ")

        if order_update =='n':
            update_continue = False
        elif order_update not in data.keys():
            print
            update_continue = True
        else:
            print(data.get(order_update))
            print("update order status date: ")
            k = int(input(
                " 1: order placed date\n"+
                " 2: order fulfilled date\n"+
                " 3: order shipped date\n"+
                " 4: order received date\n"+
                " 0: cancel or end\n"
                    )
                )

            os.system('cls')
        
            if k==0:
                update_continue = False
        
            if update_continue:
                if k==1:
                    print("enter new order placed date: ")
                elif k==2:
                    print("enter new order fulfilled date: ")
                elif k==3:
                    print("enter new order shipped date: ")
                elif k==4:
                    print("enter new order received date: ")
                else:
                    print("retry entry")
            
                new_date = input()
            
                if k==1:
                    data[order_update]["status_dates"]["placed"] = new_date
                elif k==2:
                    data[order_update]["status_dates"]["fulfilled"] = new_date
                elif k==3:
                    data[order_update]["status_dates"]["shipped"] = new_date
                elif k==4:
                    data[order_update]["status_dates"]["received"] = new_date
                    if input("send order to inventory (y/n): ") == "y":
                        send_to_inventory = True

                else:
                    print("retry entry")

                print("updated status dates for order {}:".format(order_update))
                print(data[order_update]["status_dates"])
                
                js = json.dumps(data)
                f = open(order_history_file_name, 'w')
                f.write(js)
                f.close()

        if send_to_inventory:
            print("sending order to inventory...")
            add_item_to_inventory("received",i = order_update)
            send_to_inventory = False

    return

def prep_ordered_item_for_inventory(orderID, itemID, quantity, date=NULL):
    from datetime import date
    state_list = ["orderID",
                  "itemID",
                  "quantity",
                  "count",
                  "date"]

    if date == NULL:
        date = str(date.today())

    state_entries = [orderID,
                     itemID,
                     quantity,
                     '0',
                     date]

    item_output = {state_list[i]: state_entries[i] for i in range(0,len(state_list))}

    return item_output

def prep_manual_item_for_inventory():
    #query itemID, userID, quantity, count
    state_list = ["userID",
                  "itemID",
                  "quantity",
                  "count",
                  "date"]
    
    state_entries = ["not entered"]*len(state_list)

    incomplete_check = True
    
    input_step = 0
    input_state = state_list[input_step]
    print("step {}: {}".format(input_step, input_state))
    while incomplete_check and input_state != "abort":
        input_state = state_list[input_step]
 
        os.system('cls')
        print("step {}: {}".format(input_step, input_state))
        
        state_entries[input_step] = input("enter {}: ".format(input_state))
        if input("confirm {}: {} (y/n):".format(input_state, state_entries[input_step])) == 'y':
            input_step += 1
            
        elif input("retry {} (y/n)?: ".format(input_state)) !='y':
            input_state = "abort"
                
        if "not entered" not in state_entries:
            edit_check = True
            while edit_check:
                os.system('cls')
                print("review properties:")
                for i in range(len(state_list)):
                    print("{} : {} : {}".format(i, state_list[i],state_entries[i]))
                if input("confirm properties (y/n): ")=='y':
                    incomplete_check = False
                    edit_check = False
                else:
                    input_step = input("select property for editing or 'a' to abort: ")
                    if input_step == 'a':
                        input_state = "abort"
                        edit_check = False
                    elif input_step.isnumeric() and int(input_step) > 0 and int(input_step) < len(state_list):
                        edit_check = False
                        input_step = int(input_step)
                        state_entries[input_step] = "not entered"
                    else:
                        print("incorrent selection, please retry")
    
    if input_state == "abort":
        print("inventory addition process ended\n"+
              "press any key to return to main menu")
        input()
        os.system('cls')
    else:
        item_output = {state_list[i]: state_entries[i] for i in range(0,len(state_list))}

    return item_output


def add_item_to_inventory(option, i=0):
    import pandas as pd
    import json

    if option == "manual":
        #queries the details for a single item 
        item_list = prep_manual_item_for_inventory()
        #returns a dictionary of:
        #{"userID": val
        # "itemID": val
        # "quantity": val
        # "count": val}
        commit_item_to_inventory(itemID=item_list['itemID'], 
                                 quantity=item_list['quantity'], 
                                 count=item_list['count'], 
                                 userID = item_list['userID'],
                                 transact_date=item_list['date'])

        #options:
        #update_inventory_transaction_log(itemID=item_list['itemID'], quantity = item_list['quantity'], count=item_list['count'], userID = item_list['userID'])
        #update_orderable_catalogue(itemID=item_list['itemID'], quantity = item_list['quantity'], count=item_list['count'], userID = item_list['userID'])

    elif option == "ordered" or option == "received":
        f = open(order_history_file_name, 'r')
        txt = f.read()
        f.close()
        data = json.loads(txt)

        continue_process = True
        while continue_process:
                #check against order history log
            if i not in data.keys():
                i = input("enter order id for entry: ")
                if i not in data.keys():
                    if input("order id not found. retry? (y/n): ") != 'y':
                        continue_process = False
                    else:
                        continue_process = True
        
            
            else:
                os.system('cls')
                print("order id: {} \n".format(i)+
                      "supplier: {} \n".format(data[i]["supplier"])+
                      "order number: {} \n".format(data[i]["order_number"])+
                      "instructions: {}\n".format(data[i]["special_instructions"])
                    )
                for k in data[i]['status_dates'].keys():
                    print(k+": "+data[i]['status_dates'][k])
                for j in sorted(data[i]['item_list'].keys()):
                    print(j+": "+str(data[i]['item_list'][j]))#, sort_keys = True))
                print("\n")

                if input('enter all ordered items (y/n): ') == 'y':
                    for n in data[i]['item_list'].keys():
                        if option == "received":
                            item_list = prep_ordered_item_for_inventory(i, 
                                                                        data[i]['item_list'][n]['itemID'],
                                                                        data[i]['item_list'][n]['quantity'],
                                                                        data[i]['status_dates']['received'])
                        
                        #print(item_list)
                        commit_item_to_inventory(itemID=item_list['itemID'], quantity=item_list['quantity'], count=item_list['count'], orderID = item_list['orderID'])

                else:
                    while continue_process:
                        n = input('item to enter to inventory: ')
                        if n not in data[i]['item_list'].keys():
                            if input("item not found. retry? (y/n): ") != 'y':
                                continue_process = False
                            else:
                                continue_process = True
                        else:
                            item_list = prep_ordered_item_for_inventory(i, 
                                                                        data[i]['item_list'][n]['itemID'],
                                                                        data[i]['item_list'][n]['quantity'],
                                                                        )
                            #print(item_list)
                            commit_item_to_inventory(itemID=item_list['itemID'], quantity=item_list['quantity'], count=item_list['count'], orderID = item_list['orderID'])

                        if input('enter another item (y/n): ') != 'y':
                            continue_process = False
                        else: continue_process = True
                
        #item_list = prep_ordered_item_for_inventory(orderID, itemID)
        #print(item_list)
        
        #can check against the transaction log if items were already added
        
        #commit_item_to_inventory(itemID=item_list['itemID'], quantity = item_list['quantity'], count=item_list['count'], orderID = item_list['orderID'])



    else:
        print('error')

    return

def commit_item_to_inventory(itemID, quantity=0, count=0, userID=0, orderID=0, transact_date=NULL):
    from datetime import date

    #input is data for a single item, can be multiple quantity or count, and add or sub
    print("preparing data...")
    print("itemID: {}".format(itemID))
    print("quantity: {}".format(quantity))
    print("count: {}".format(count))
    print("userID: {}".format(userID))
    print("orderID: {}".format(orderID))

    #load catalogue to get itemID count
    import json
    f = open(orderable_item_file_name, 'r')
    txt = f.read()
    f.close()
    catalogue = json.loads(txt)
    #catalogue key is itemID

    #load transaction history - this is a check on orderID
    f = open(transaction_log_file_name, 'r')
    txt = f.read()
    f.close()
    transactions = json.loads(txt)
    #transaction format: {ID: 
                # {'orderID':'111','userID':uid
                # 'itemID':'1001',
                # 'quantity':'10',
                # 'count':'250',
                # 'date':'2025-01-27'}
    transact_id = int(max(transactions.keys()))+1
    if transact_date is NULL:
        transact_date = str(date.today)

    #load inventory current
    f = open(inventory_current_file_name, 'r')
    txt = f.read()
    f.close()
    inventory = json.loads(txt)
    #inventory format: {itemID: {quantity: qty, count: ct}}
    
    #steps:
    #confirm count
    #check ordered against transaction history 

    process_inventory = True
    confirm_inventory = False
    while process_inventory:
        #find/query item count
        if count==0 and quantity == 0:
            quantity = input('enter item quantity: ')
            count = input('enter item count: ')
        elif count == 0 and quantity != 0:
            if itemID in catalogue.keys():
                count = int(quantity) * int(catalogue[itemID]['count'])
                print('updating count.')
            else:
                while count == 0:
                    print("transaction item count cannot be 0.")
                    item_count = input('enter total item count: ') 
                    count = item_count
        elif count != 0 and quantity == 0:
            if itemID in catalogue.keys():
                quantity = count // int(catalogue[itemID]['count'])
            else:
                quantity = input('enter item quantity: ')
        else:
            count = count
            quantity = quantity
        
        if userID == 0 and orderID == 0:
            transact_list = ['itemID', 'quantity', 'count', 'date']
            transact_vals = [itemID, quantity, count, transact_date]
        elif userID == 0:
            transact_list = ['itemID', 'quantity', 'count', 'orderID', 'date']
            transact_vals = [itemID, quantity, count, orderID, transact_date]
        else:
            transact_list = ['itemID', 'quantity', 'count', 'userID', 'date']
            transact_vals = [itemID, quantity, count, userID, transact_date]
    
        #check transaction history for orderID and itemID for duplicate entry
        if orderID != 0:
            for t in transactions.keys():
                if transactions[t].get('orderID') is not None: 
                    if orderID == transactions[t]['orderID']:
                        if itemID == transactions[t][orderID]['itemID']:
                            print('ordered item already entered.')
                            process_inventory = False
        
        #confirm transaction:
        for i in range(len(transact_list)):
            print("{} : {} : {}".format(i, transact_list[i],transact_vals[i]))
        
        if input("confirm inventory addition (y/n): ")=='y':
            confirm_inventory = True
            process_inventory = False
        else:
            confirm_inventory = False
            process_inventory = False

        if confirm_inventory:
            #inventory math - just add quantity and count and then relevel quantity at the end
            #look for itemID in inventory
            if itemID not in inventory.keys():
                inventory[itemID] = {'quantity':quantity, 'count':count}
            else:
                inventory[itemID]['count'] = int(inventory[itemID]['count']) + int(count)
                inventory[itemID]['quantity'] = int(inventory[itemID]['quantity']) + int(quantity)
                
                if itemID in catalogue.keys():
                    inventory[itemID]['quantity'] = int(inventory[itemID]['count']) // int(catalogue[itemID]['count'])
                    #good enough for now
            transactions[transact_id] = {transact_list[i]: transact_vals[i] for i in range(0,len(transact_list))}
            
            #dump to inventory and transaction log!
            js = json.dumps(inventory)
            f = open(inventory_current_file_name, 'w')
            f.write(js)
            f.close()

            js = json.dumps(transactions)
            f = open(transaction_log_file_name, 'w')
            f.write(js)
            f.close()
 

    
    return

def remove_item_from_inventory():
    import json
    #person can remove an item from inventory
    item_list = prep_manual_item_for_inventory()

    #check current stock
    f = open(inventory_current_file_name, 'r')
    txt = f.read()
    f.close()
    inventory = json.loads(txt)
    
    f = open(orderable_item_file_name, 'r')
    txt = f.read()
    f.close()
    catalogue = json.loads(txt)
    
    stock_check = False

    if item_list['itemID'] not in inventory.keys():
        stock_check = False
        print('error: itemID not in inventory.')
    
    elif int(item_list['count']) > int(inventory[item_list['itemID']]['count']):
        stock_check = False
        print('error: insufficient stock.')
    
    elif item_list['count'] == 0:
        if item_list['itemID'] in catalogue.keys():
            if int(item_list['quantity'])*int(catalogue[item_list['itemID']]['count']) > int(inventory[item_list['itemID']]['count']):
                stock_check = False
                print('error: insufficient stock.')
            else:
                stock_check = True
        else:
            print('error: unknown itemID.')
            stock_check = False
        
        print('error: unknown count.')
        stock_check = False
    else: 
        stock_check = True


    if stock_check:
        commit_item_to_inventory(itemID=item_list['itemID'], 
                             quantity=int(item_list['quantity']) * -1, 
                             count=int(item_list['count']) * -1, 
                             userID = item_list['userID'],
                             transact_date=item_list['date'])

    return

def add_orderable_item_to_catalogue():
    import json
    f = open(orderable_item_file_name, 'r')
    txt = f.read()
    f.close()
    data = json.loads(txt)
    
    state_list = ["ID",
                 "name",
                 "part_num",
                 "brand",
                 "category",
                 "subcategory",
                 "price",
                 "size",
                 "units",
                 "count",
                 "supplier",
                 "website"]

    state_entries = ["not entered"]*len(state_list)

    incomplete_check = True

    # unique_only = ["ID"]

    # drop_down_options = ["brand",
    #              "category",
    #              "subcategory",
    #              "supplier",
    #              "website"]

    input_step = 0
    input_state = state_list[input_step]
    print("step {}: {}".format(input_step, input_state))

    while input_state == state_list[input_step] and state_entries[input_step]=="not entered":
        max_ID = int(max(data.keys()))+1
    
        if input("confirm suggested new item {} {} (y/n): ".format(input_state,max_ID)) =='y':
            state_entries[input_step] = max_ID
            input_step += 1
        else: 
            state_entries[input_step] = input("enter new item {}:".format(input_state))
        
            if state_entries[input_step] not in data.keys():
                print("{} {} accepted.".format(input_state, state_entries[input_step]))
                input("press any key to continue to next step.")
                input_step += 1
            
            elif input("{} {} already in catalogue, retry entry (y/n)?: ".format(input_state, state_entries[input_step])) =='y':
                state_entries[input_step] = "not entered"
            else:
                input_state = "abort"
    
    while incomplete_check and input_state != "abort":
        input_state = state_list[input_step]
 
        os.system('cls')
        print("step {}: {}".format(input_step, input_state))
        
        state_entries[input_step] = input("enter new item {}: ".format(input_state))
        if input("confirm new item {}: {} (y/n):".format(input_state, state_entries[input_step])) == 'y':
            input_step += 1
            
        elif input("retry product {} (y/n)?: ".format(input_state)) !='y':
            input_state = "abort"
                
        if "not entered" not in state_entries:
            edit_check = True
            while edit_check:
                os.system('cls')
                print("review new item properties:")
                for i in range(len(state_list)):
                    print("{} : {} : {}".format(i, state_list[i],state_entries[i]))
                if input("confirm new item properties (y/n): ")=='y':
                    incomplete_check = False
                    edit_check = False
                else:
                    input_step = input("select property for editing or 'a' to abort: ")
                    if input_step == 'a':
                        input_state = "abort"
                        edit_check = False
                    elif input_step.isnumeric() and int(input_step) > 0 and int(input_step) < len(state_list):
                        edit_check = False
                        input_step = int(input_step)
                        state_entries[input_step] = "not entered"
                    else:
                        print("incorrent selection, please retry")
    
    if input_state == "abort":
        print("new catalogue entry process ended")
        
    else:
        data[state_entries[0]] = {state_list[i]: state_entries[i] for i in range(1,len(state_list))}
        
        js = json.dumps(data)
        f = open(orderable_item_file_name, 'w')
        f.write(js)
        f.close()
 
    return

def remove_orderable_item_from_catalogue():
    import json
    f = open(orderable_item_file_name,'r')
    txt = f.read()
    data = json.loads(txt)
    f.close()
    
    temp = input("enter ID of item for deletion: ")
    
    if temp in data.keys():
        print(data[temp])

        if input('confirm deletion of catalogue item (y/n)') == 'y':
            data.pop(temp)
            print("item id {} deleted successfully".format(temp))

            js = json.dumps(data)
            f = open(orderable_item_file_name, 'w')
            f.write(js)
            f.close()

    else: 
        print("invalid product id.")
        input("press any key to return to main menu.")

    return

def get_order_history_log():
    #when an item(s) are ordered or removed(?) it goes here
    import pandas as pd
    import json
    
    f = open(order_history_file_name, 'r')
    txt = f.read()
    f.close()
    data = json.loads(txt)
    
    show_orders = True
    i=int(max(data.keys())) #default most recent

    while show_orders:
        
        order_select = int(input("select order by: \n"+
                "1: order ID \n"+
                "2: first order\n"+
                "3: most recent order\n"+
                "4: see prior order\n"+
                "5: see next order\n"+
                "0: return to main menu\n"+
                ": "))
        
        if order_select == 1:
            i = input("enter order ID: ")
            
        elif order_select == 2:
            i = 0

        elif order_select == 3:
            int_k = []
            for k in data.keys():
                int_k.append(int(k))
                
            i=str(max(int_k))

        elif order_select == 4:
            i = str(max(int(i)-1, 0))
        elif order_select == 5:
            i = str(min(int(i)+1, int(max(data.keys()))))
        else:
            show_orders = False

        if i in data.keys():
            os.system('cls')
            print("order id: {} \n".format(i)+
                "supplier: {} \n".format(data[i]["supplier"])+
                "order number: {} \n".format(data[i]["order_number"])+
                "instructions: {}\n".format(data[i]["special_instructions"])
                )
            for k in data[i]['status_dates'].keys():
                print(k+": "+data[i]['status_dates'][k])
            for j in data[i]['item_list'].keys():
                print(data[i]['item_list'][j])
                print("\n")
        else:
            print("invalid order selection.\n")
        
    os.system('cls')
            
    
    return

def add_to_inventory_log():
    return


def get_personnel_report():
    #when a person removes an item(s) it goes here
    return

def search_catalogue():
    return

def main_menu():
    print("Menu: ")
    print(
            " 1: see inventory\n"+
            " 2: add item directly to inventory\n"+
            " 3: add ordered item(s) to inventory\n"+
            " 4: remove item from inventory\n"+
            " 5: see inventory history log\n"+
            "\n"+
            "11: see catalogue\n"+
            "12: order item from catalogue\n"+
            "13: add item to catalogue\n"+
            "14: remove item from catalogue\n"
            "15: update order status\n"+
            "16: display order history log\n"+
            "\n"+
            "21: display personnel reports\n"+
            "\n"+
            " 0: quit\n")
    return

def main_selection():
    k = int(input("menu selection: "))
    os.system('cls')
    program_continue = True

    if k==1:
        get_inventory_current()
    elif k==2:
        add_item_to_inventory("manual")
    elif k==3:
        add_item_to_inventory("ordered")
    elif k==4:
        remove_item_from_inventory()
    elif k==5:
        get_transaction_log()
    
    elif k==11:
        get_orderable_items()
    elif k==12:
        order_item_from_catalogue()            
    elif k==13:
        add_orderable_item_to_catalogue()
    elif k==14:
        remove_orderable_item_from_catalogue()
    elif k==15:
        update_order_status()
    elif k==16:
        get_order_history_log()
    
    elif k==21:
        get_personnel_report()
    
    elif k==0:
        program_continue = False
    
    return program_continue

def main():
    initialize()
    
    print("Welcome to Inventory Managment")
    
    program_run = True
    
    while program_run:

        main_menu()
        
        program_run = main_selection()

        if(program_run):
            input('\n \n \npress enter to return to main menu.')
            os.system('cls')


main()