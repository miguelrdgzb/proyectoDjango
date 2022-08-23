from logging import warning
import os
import pandas as pd
import numpy as np
import time
import warnings
from django.conf import settings
from django.http import HttpResponse, Http404
warnings.filterwarnings('ignore')


# Las preguntas implicarian las columnas de las que beberán las variables cifEmpresa y ctaCotizacion, costes, idaccion e idgrupo.
'''excel = pd.read_excel('excelplantilla.xlsx')
print('=======================================================')
print('         Conversor ficheros xml para FUNDAE            ')
print('=======================================================')
cif = input('¿Cuál es el CIF de la empresa a la que pertenecen los trabajadores?\n')
cuenta = input('¿Cual es el numero de CCC correspondiente?\n')
periodos = input('Periodos en los que se encuentra la formacion (Número de mes)(Si es mas de uno, separar los numeros con una coma (,)EJ: 10,11: \n')
periodos = periodos.split(',')
importes = input('Importes imputados a cada periodo (Si es mas de un periodo, separar los importes con una coma en el mismo orden que los periodos) EJ: 1200,1000: \n')
importes = importes.split(',')

if len(importes) != len(periodos):
    print('Debe haber el mismo numero de importes que de periodos, vuelva a ejecutar el programa\n')
    quit()
else: pass
costes = input('Imputa los costes directos, indirectos y salariales, en este orden. EJ("1200,1400,2000"): \n')
costes = costes.split(',')
if len(costes) != 3:
    print('Debe imputar los tres importes de los costes en orden y separados por comas EJ: 1200,1500,1300\n')
    quit()
else: pass
 
idaccion = input('¿Cuál es el IdAccion? : \n')
idgrupo = input('Por último, ¿cuál es el idGrupo?: \n')

print('El fichero a procesar tendrá como valores CIF: {}, y CCC : {}\n'.format(cif, cuenta))
print('Presiona Ctrl+C para salir y ejecute de nuevo el script, de lo contrario el fichero xml se procesará en 5 segundos\n')

time.sleep(6)

'''

def GeneradorXMLFundae(pathExcel, cif, cuenta, periodos, importes, costes, idaccion, idgrupo):
    excel = pd.read_excel(pathExcel)
    importes = importes.split(',')
    periodos = periodos.split(',')
    #En caso de que no existe el segundo apellido, la tabla interpreta un NaN que lo sustituimos por un espacio en blanco
    excel['apellido2'] = excel['apellido2'].fillna('')
    excel['TELEFONO'] = excel['TELEFONO'].fillna('902151654')
    excel['MAIL'] = excel['MAIL'].fillna('')
    excel.FECHA = pd.to_datetime(excel.FECHA).dt.strftime('%d-%m-%Y') # Formateo de la fecha


    N_TIPO_DOCUMENTO = [] # Si el valor comienza por una letra es un NIE que adquiere el valor 60, en caso de ser DNI el valor es 10.
    for i in excel.DNI:
        if i != "" and i[0].isalpha():
            N_TIPO_DOCUMENTO.append('60')
        else:
            N_TIPO_DOCUMENTO.append('10')



    nif = excel.DNI.values
    primerApellido = excel.apellido.values
    segundoApellido = excel.apellido2.values
    nombre = excel.NOMBRE.values
    niss = excel.NISS.values
    fechaNacimiento = excel.FECHA
    cifEmpresa = []
    email = excel.MAIL.values
    telefono = excel.TELEFONO.values
    for i in range(len(excel)):
        cifEmpresa.append(cif)

    ctaCotizacion = []
    for i in range(len(excel)):
        ctaCotizacion.append(cuenta)

    sexo = []
    for i in excel.SEXO:
        if i.startswith('H'):
            sexo.append('M')
        else:
            sexo.append('F')

    # Como cada fichero incluira un CIF y CCC, se creara una lista con un numero para cada grupo.

    textos = ''
    for i in range(len(excel)):
        # La plantilla tiene unas partes fijas que son las declaradas en las cabeceras y la parte dinamica que es txt.
        cabecera1 = '''
        <grupos>
        <grupo>
        <idAccion>{}</idAccion>
        <idGrupo>{}</idGrupo>
        <participantes>'''.format(idaccion, idgrupo)


        texto_coste = '''
        </participantes>
        <costes>
        <coste>
        <directos>{}</directos>
        <indirectos>{}</indirectos>
        <salariales>{}</salariales>
        <periodos>'''.format(costes[0],costes[1],costes[2])



        if len(periodos) == 1:
            texto = '''
            <periodo>
            <mes>{}</mes>
            <importe>{}</importe>
            </periodo>'''.format(periodos[0],periodos[0])
            xml_periodos = str()
            xml_periodos = texto

        else:
            for el in range(len(periodos)):
                texto = '''
                <periodo>
                <mes>{}</mes>
                <importe>{}</importe>
                </periodo>'''.format(periodos[el],periodos[el]) 


                xml_periodos = str()
                xml_periodos += texto



        cabecera2 = '''
        </periodos>
        </coste>
        </costes>
        </grupo>
        </grupos>
        '''


        txt = '''
        <participante>
        <nif>{}</nif>
        <N_TIPO_DOCUMENTO>{}</N_TIPO_DOCUMENTO>
        <nombre>{}</nombre>
        <primerApellido>{}</primerApellido>
        <segundoApellido>{}</segundoApellido>
        <niss>{}</niss>
        <cifEmpresa>{}</cifEmpresa>
        <ctaCotizacion>{}</ctaCotizacion>
        <fechaNacimiento>{}</fechaNacimiento>
        <sexo>{}</sexo>
        <email>{}</email>
        <telefono>{}</telefono>
        <discapacidad>false</discapacidad>
        <afectadosTerrorismo>false</afectadosTerrorismo>
        <afectadosViolenciaGenero>false</afectadosViolenciaGenero>   
        <categoriaprofesional>3</categoriaprofesional>
        <grupocotizacion>8</grupocotizacion>  
        <nivelestudios>4</nivelestudios>     
        <DiplomaAcreditativo>S</DiplomaAcreditativo> 
        </participante>
        '''.format(nif[i],N_TIPO_DOCUMENTO[i],nombre[i],primerApellido[i],segundoApellido[i],niss[i].replace('/',''),cifEmpresa[i],ctaCotizacion[i],fechaNacimiento[i].replace('-','/'), sexo[i], email[i], telefono[i])

    
        textos += txt
        # La variable textos incluye un txt por iteracion de forma concatenada

    final = cabecera1 + textos + texto_coste + xml_periodos + cabecera2 # Añadimos las cabeceras a textos.

    f = open(settings.DOWNLOAD_ROOT_DEV + "fichero-envio.xml","w+", encoding="utf-8")
    f.write(final)
    f.close()


     
    
#Exporta la información en formato xml.
def download(request, path):
    file_path = settings.DOWNLOAD_ROOT_DEV + "//fichero-envio.xml"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/xhtml+xml")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404