from asyncio.windows_events import NULL
import os
import pandas as pd
import numpy as np
from datetime import date
import datetime
import pyodbc
from django.conf import settings



def CruzarDatos(mutua, mf):
    cross = pd.merge(mutua, mf, how='left', on=['NIF', 'Fecha baja']).sort_values(by=['NIF'])
    return cross


def CalcularDiferencias(df):
    df['DIFERENCIADIASMTMF'] = (df['Días de baja'] - df['Dias']).fillna('NULL')
    return df


def LimpiarTabla(df):
    df = df[['NIF', 'Trabajador','FechaAlta', 'NASS', 'CCC', 'Razón Social', 'Tipo', 'Fecha baja', 'Días de baja', 'Dias', 'DIFERENCIADIASMTMF']]
    df = df.rename(columns={
    'NIF':'NIF',
    'NASS': 'NASS',
    'Razón Social': 'RazonSocial',
   'Trabajador':'Trabajador',
    'Tipo' : 'TipoContingencia',
    'Fecha baja' : 'MTFechaInicio',
    'Días de baja':'MTDIAS' ,
    'FechaAlta':'MFFechaAlta',
    'Dias' :'MFDIAS', 
    }
    )
    return df
    

def CrearAntiguedad(df): 
    _listado = list()
    for i,j in zip(df['MFFechaAlta'].isnull(), df['MFFechaAlta']):
        if i:
            j = -10
            _listado.append(j)
        else:
            Resta = np.datetime64('today') - j
            _listado.append(Resta.days)
    return _listado

def CrearAntiguedadEfectiva(df):
     _ListadoDiasEfectivos = list()
     for i, j in zip(df['Antiguedad'], df['MTDIAS']):
          if i < 0:
              _ListadoDiasEfectivos.append('No existe este registro en MF')
          else:
               _ListadoDiasEfectivos.append(i-j)
     return _ListadoDiasEfectivos

def LimpiezaColumnas(df):
     df = df.rename(columns={
    'NIF':'NIF',
    'NASS': 'NASS',
   'Trabajador':'Trabajador',
    'Tipo' : 'TipoContingencia',
    'Fecha baja' : 'MTFechaInicio',
    'Días de baja':'MTDIAS' ,
    'FechaAlta':'MFFechaAlta',
    'Dias' :'MFDIAS', 
     }
     )
     df = df[['NIF','Trabajador','MFFechaAlta', 'NASS', 'CCC', 'RazonSocial', 'TipoContingencia', 'MTFechaInicio', 'MTDIAS', 'MFDIAS', 'DIFERENCIADIASMTMF','Antiguedad','Real']]
     df['MTFechaInicio'] = df['MTFechaInicio'].fillna('0')
     return df.fillna('')


def ExportarExcel(df):
     t1 = pd.Timestamp.now()
     return df.to_excel(settings.DOWNLOAD_ROOT_DEV + '//InformeAbsentismo.xls')

def ExportarCsv(df):
     t1 = pd.Timestamp.now()
     return df.to_csv('InformeAbsentismo {}.csv'.format(t1.date().strftime('%Y-%m-%d')))


def CrearFin(df):
    _listado1 = list()
    _listado2 = list()
    for i,j in zip(df['MTFechaInicio'], df['MTDIAS']):
        if i == '0':
            _listado1.append('NoEncontrado')
        else:
            _listado1.append(pd.to_datetime(i) + datetime.timedelta(days=j))

    for i in _listado1:
        if i == max(_listado1):
            _listado2.append('NULL')
        else:
            _listado2.append(i)
    df['FechaFin'] = _listado2
    return df


def imputarDatosEnTabla(df):
    try:
        server = 'instance-test.public.9fa5b3d48c11.database.windows.net,3342' 
        database = 'MooveCarsBI' 
        username = 'Administrador' 
        password = 'CEJ9hzw4Vs8@vP]z@8A{' 
        cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password + ';Encrypt=YES'  + ';Trusted_Connection=NO')
        cursor = cnxn.cursor()
        funcionInsertRows(cursor, df)
        cnxn.close()
        return df
    except Exception as ex:
        cursor.close()
        print(ex)
        return df

    


def funcionInsertRows(cursor, df):

    try:
        #cursor.execute('''TRUNCATE TABLE anl.BajasMutuaMF''')
        for index, row in df.iterrows():    
            if row.FechaFin != 'NULL': 
                row.FechaFin = "'"+ str(row.FechaFin) + "'"

            if row.MFFechaAlta != 'NULL': 
                row.MFFechaAlta = "'"+ str(row.MFFechaAlta) + "'" 

            if row.MTFechaInicio != 'NULL': 
                row.MTFechaInicio = "'"+ str(row.MTFechaInicio) + "'"         

            cursor.execute('''INSERT INTO anl.BajasMutuaMF (NIF,Trabajador,MFFechaAlta,NASS,CCC,RazonSocial,TipoContingencia,MTFechaInicio,MTDIAS,MFDIAS,DIFERENCIADIASMTMF,Antiguedad,Real,FechaFin)
                  values('{}','{}',{},{},{},'{}','{}',{},{},{},{},{},'{}',{})'''.format(row.NIF,row.Trabajador,row.MFFechaAlta,row.NASS,row.CCC,row.RazonSocial,row.TipoContingencia,row.MTFechaInicio,row.MTDIAS,row.MFDIAS,row.DIFERENCIADIASMTMF,row.Antiguedad,row.Real,row.FechaFin))
            cursor.commit()
        cursor.close()
    except Exception as ex:
        cursor.close()
        print(ex)
    
    





 

