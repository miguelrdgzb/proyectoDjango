# Importar librerias y recursos de otros archivos


import os
import pandas as pd
import numpy as np
import pyodbc
from datetime import date
import time
from django.conf import settings
from django.http import HttpResponse, Http404
from pathlib import Path


######################################################################################


from . import ExtractMF
from . import ExtractMutua
from . import Crossed




def main(new):
    sql = '''
    SELECT  b.DNI,b.Nombre,b.Apellido1,b.Apellido2, B.FechaAlta, a.ConductorId,FechaInicio,FechaFin, Dias, MotivoBajaIT
    FROM(
    SELECT * 
    FROM 
    uber_xtr.conductorbajas)a
    LEFT JOIN
    (SELECT *
    FROM
    uber_xtr.conductor)b
    ON a.ConductorId = b.Id
    WHERE (FechaFin > '2021-01-01' or FechaFin is null) and FechaInicio > '2020-06-15' and ParqueId=6 and MotivoBajaIT <> 6
    '''

    # Extrae datos del archivo excel cargado en el mismo directorio
    data_mutua = ExtractMutua.ExtraerMutua(new)
    # Extrae datos de la base de datos con una query en txt en el directorio source, devuelve un dataframe.
    data_mf = ExtractMF.ExtraerDatosMF(sql)   
    data_mf_tratados = ExtractMF.TratarDatosMF(data_mf)

    # Cruzamos las tablas por dni y por FechaInicio de la baja. || Calculamos diferencias de dias
    tabla = Crossed.CruzarDatos(data_mutua, data_mf_tratados)
    tabla = Crossed.CalcularDiferencias(tabla)    

    # Formateamos nombres de columnas

    result = Crossed.LimpiarTabla(tabla)

    # Calculamos los dias de antiguedad en la empresa y la antiguedad relativa restando los dias de baja.
    result['Antiguedad'] = Crossed.CrearAntiguedad(result)
    result['Real'] = Crossed.CrearAntiguedadEfectiva(result)

    # Limpiamos de nuevo las columnas y exportamos a excel

    Final = Crossed.LimpiezaColumnas(result.fillna('NULL'))

    # Nueva columna V1.1, Tambien a su vez imputamos los registros en la base de datos
    FinalConColumna = Crossed.imputarDatosEnTabla(Crossed.CrearFin(Final))
    print(FinalConColumna)
    # Devolvemos un csv y un excel para su posible manipulación.
    
    return Crossed.ExportarExcel(FinalConColumna)




def download(request, path):
    file_path = settings.DOWNLOAD_ROOT_DEV + '//InformeAbsentismo.xls'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404