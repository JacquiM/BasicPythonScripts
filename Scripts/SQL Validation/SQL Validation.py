
# coding: utf-8

# # SQL Validation
# 
# Conditions for validation:
# - Each table has a primary key
# - TO DO: Create\modified date columns have a default value of getdate()
# - TO DO: Each primary key that is a unique identifier should have the default value of newid()
# - TO DO: Each primary key that is an int needs to have identity specification turned on

# In[73]:


import pandas as pd

import pyodbc
from sqlalchemy import create_engine, event
import urllib

import pymsteams


# In[74]:


def connect_to_sql(server, user, password, database, auth):
    
    driver = '{SQL Server}'
    
    if user == None:

        params = urllib.parse.quote_plus(r'DRIVER={};SERVER={};DATABASE={};'.format(driver, server, database))
        conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
        engine = create_engine(conn_str)
        
        return engine
    
    else:
        
        params = urllib.parse.quote_plus(r'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(driver, server, database, user, password))
        conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
        engine = create_engine(conn_str)
        
        return engine     


# In[75]:


def send_teams_message(text):
    
    webhook = '<add webhook>'
    
    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(webhook)

    # Add text to the message.
    myTeamsMessage.text(text)

    # send the message.
    myTeamsMessage.send()


# In[76]:


def ValidatePrimaryKeys(engine):
    
    query = "select schema_name(tab.schema_id) as [schema_name], tab.[name] as table_name from sys.tables tab left outer join sys.indexes pk on tab.object_id = pk.object_id and pk.is_primary_key = 1 where pk.object_id is null order by schema_name(tab.schema_id), tab.[name]"

    df = pd.read_sql(query, engine)
    
    keysValid = True
    
    text = ""
    
    if len(df) > 0:

        text = 'Primary Key Validation Failed.\n\n'

        for index, element in df.iterrows():

            text += '{} does not have a primary key\n\n'.format(element['table_name'])
            
            keysValid = False

        # send_teams_message(text)
        
    return keysValid, text


# In[77]:


def ValidateTables(engine, tables):

    query = "select tab.[name] as table_name from sys.tables tab"

    df = pd.read_sql(query, engine)

    tables_split = []
    
    tables = tables.replace(' ','')

    if ';' in tables:

        tables_split = tables.split(';')

    elif ',' in tables:

        tables_split = tables.split(',')
    
    elif len(tables) != 0:
        
        tables_split = [tables]

    text = ""

    tablesValid = True

    for table in tables_split:

        if table not in df['table_name'].tolist() and (table != '' and table != None):

            text += 'Table not found in database: {}\n\n'.format(table)
            tablesValid = False

    if tablesValid:

        text = 'Table Validation Passed\n\n'

    else:

        text = 'Table Validation Failed\n\n' + text

    #send_teams_message(text)
    
    return tablesValid, text


# In[114]:


def ValidateFromSchema(schemas, engine):
    
    text = ""
    tableText = ""
    
    schemas_split = []
    
    schemas = schemas.replace(' ','')

    if ';' in schemas:

        schemas_split = schemas.split(';')

    elif ',' in schemas:

        schemas_split = schemas.split(',')
    
    elif len(schemas) != 0:
        
        schemas_split = [schemas]
        
    isValid = True

    for schema in schemas_split:
        
        if (isValid):
        
            query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}'".format(schema)

            df = pd.read_sql(query, engine)
            
            if (len(df) > 0):

                query = "select t.name as table_name from sys.tables t where schema_name(t.schema_id) = '{}'".format(schema)
                
                df = pd.read_sql(query, engine)
                
                tables = ",".join(list(df["table_name"]))
                
                validateTables = ValidateTables(engine, tables)
                
                isValid = validateTables[0]
                tableText += "{}\n\n".format(validateTables[1])
                
            else:
                
                isValid = False
                
                text += "Schema Validation Failed\n\n"
                text += "Schema not found in database: {}\n\n".format(schema)
                    
    if (isValid):
        
        text = "Schema Validation Passed\n\n"
        
        text = "{}\n\n{}".format(text, tableText)
        
    return isValid, text
        


# In[127]:


def ValidateSQL(project, server, database, schemas, tables, auth, username, password):
    
    engine = connect_to_sql(server, username, password, database, auth)
    
    summaryText = None
    
    if (schemas != None):
        
        validateSchemas = ValidateFromSchema(schemas, engine)
        
        isValid = validateSchemas[0]
        text = validateSchemas[1]
    
    else:
        
        validateTables = ValidateTables(engine, tables)
    
        isValid = validateTables[0]
        text = validateTables[1]

    if isValid:
        
        summaryText = 'Primary Key Validation Passed\n\n'
        
        validatePrimaryKeys = ValidatePrimaryKeys(engine)
        
        isKeysValid = validatePrimaryKeys[0]
        
        pkText = validatePrimaryKeys[1]
        
        if isKeysValid:
            
            text += summaryText
            
        else:
            
            text += pkText
        
    else:
        
        summaryText = text
        
    text = "<strong><u>{}<u><strong>:\n\n{}".format(project, text)
                
    send_teams_message(text)
    
    return isValid


# In[128]:


server = '<server>'
user = '<user>'
password = '<password>'
database = '<database>'
auth = 'SQL' # or Windows
schemas = '<schemas comma separatted>'
tables = '<tables comma separated>'
project = '<project>'

ValidateSQL(project, server, database, schemas, tables, auth, user, password)

