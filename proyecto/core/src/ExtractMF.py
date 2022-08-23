import pandas as pd
import numpy as np
import pyodbc
import os
import asyncio



def ExtraerDatosMF(sql):
    server = 'tcp:sqlmoovecarsbi.public.187c6f330c66.database.windows.net,3342' 
    database = 'MooveCarsBI' 
    username = 'Administrador' 
    password = 'CEJ9hzw4Vs8@vP]z@8A{' 
    cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password + ';Encrypt=YES'  + ';Trusted_Connection=NO')
    data = pd.read_sql(sql, cnxn)
    cnxn.close()
    return  data



def TratarDatosMF(data):
    data = data[['DNI', 'FechaAlta', 'FechaInicio','Dias', 'Nombre', 'Apellido1']]
    data.rename(columns={
    'DNI':'NIF',
    'FechaInicio': 'Fecha baja',
    'Días': 'Días MF'
    }, inplace=True)
    return data

    

