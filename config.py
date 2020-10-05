import pyodbc
conn = pyodbc.connect(
    "DRIVER={SQL Server}; SERVER=10.81.2.28,1433; DATABASE=QASys; UID=sa; PWD=1qaz@WSX"
    )
cursor = conn.cursor()
