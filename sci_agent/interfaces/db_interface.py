import os, io
import pandas as pd
import json
import sqlite3

def check_form_entry(fields):
    msgs = []   
    #for now assume all fields are required  
    for k, v in fields.items():
       
        if not v: msgs.append(f"{k} is required.")    
    return msgs            

def file_check(files):
    msgs = []   
    
    #Check format doing csv for now.
    if files:
        #Get the rules out
        with open("sci_agent\data\\validation.json", 'r') as f:
            rules = json.load(f) 
      
        
        for file in files:            
            if os.path.splitext(file.name)[1].lower() != '.csv':
                msgs.append("{file.name} is not a csv file.")
                continue
         
            df = pd.read_csv(file)     
            file.seek(0,0)
              
            
            for r in rules:
                if r['rule_type'] == 'required':
                    if r['column'].lower() not in [x.lower() for x in df.columns]:
                        msgs.append(r['description'])
                        break
                if r['rule_type'] == 'includes':
                    for c in r['parameters']['values']:
                        if c.lower() not in [x.lower() for x in df[r['column']].unique()]:
                            msgs.append(r['description'])
                            break
                #Add other rules later 
            del df
            
    return msgs

def upload_sample_group(insert):

    con = sqlite3.connect("sci_agent\data\databases\Sample.db")
    cursor = con.cursor()    

    # Data to be inserted
    data = tuple(insert.values())
    
    # Define the INSERT statement with placeholders
    sql_insert = f"INSERT INTO SampleGroups ({', '.join(insert.keys())}) VALUES ({', '.join(['?']*len(data))})"
   
    
    # Execute the INSERT statement
    cursor.execute(sql_insert, data)
    cursor.execute("select last_insert_rowid()")
    rid = cursor.fetchone()[0]
    
    con.commit()
    con.close()
    
    return rid
    

def upload_results(files, rw_id):
    con = sqlite3.connect("sci_agent\data\databases\Sample.db")
            
    for file in files:         
        df = pd.read_csv(file)  
        df['sample_id'] =  rw_id
        df.to_sql('Results', con, if_exists='append', index=False)
    con.close()
   



            

        
