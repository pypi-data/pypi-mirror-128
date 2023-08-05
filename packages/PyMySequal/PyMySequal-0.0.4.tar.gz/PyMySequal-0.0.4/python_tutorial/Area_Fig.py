import pyodbc
import pandas as pd

def records(server,database,query):
    ser=Server
    db=Database
    sql_query=Query
    conn_string=f"Driver={{SQL Server}} ;Server={ser} ;Database={db} ; Trusted_Connection=yes;"
    objConn = pyodbc.connect(conn_string)
    df=pd.read_sql(sql_query, objConn)
    print(df)
