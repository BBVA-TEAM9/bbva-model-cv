import pyodbc
import pandas as pd
# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
df = pd.read_csv("datasets/real_time.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:bbva-team9.database.windows.net' 
database = 'BBVA' 
username = 'administrador' 
password = '@BbvaTeam9_123456789' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#cursor.execute("CREATE TABLE [HackatonBBVA].[Aforo]([DepartmentID] [smallint] NOT NULL,[Name] [dbo].[Name] NOT NULL,[GroupName] [dbo].[Name] NOT NULL) GO")
# Insert Dataframe into SQL Server:
for index, row in df.iterrows():
    cursor.execute("INSERT INTO AforoHistorico (Fecha,AforoFinal,OficinaId) values(?,?,?)", row.Datetime, row.Aforo, row.Oficina)
cnxn.commit()
cursor.close()