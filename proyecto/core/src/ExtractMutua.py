from posixpath import dirname
import pandas as pd
import numpy as np
import os 
import pyodbc
 



def ExtraerMutua(new):
    try:
        mutua = pd.read_excel(new)
        return mutua
    except Exception as ex:
        return print('El fichero debe ser único en el directorio y debe tener formato xlsx o xls .', ex)    
    




