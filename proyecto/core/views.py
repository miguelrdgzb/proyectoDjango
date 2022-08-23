from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, Http404
from . import models
import pandas as pd
from core.src import main, Crossed, ExtractMF, ExtractMutua, fundae2
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pathlib import Path
import os

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def mutua(request):

    if request.method == "POST":
     
        
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        

     
        # Guardando la info en la base de datos
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()
        print(request.FILES['uploadedFile'].name)
        documents = models.Document.objects.all()
        #path = '../../UploadedFiles/{}'.format(uploadedFile.name)
        path = settings.BASE_DIR / 'UploadedFiles\\{}'.format(uploadedFile.name)
        main.main(path)
        return main.download(request, settings.DOWNLOAD_ROOT_DEV + '//InformeAbsentismo.xls')


    documents = models.Document.objects.all()
    
    

    return render(request, "core/mutua.html", context = {
        "files": documents
    })
    

def fundae(request):
    
    
    if request.method == "POST":
        cif = request.POST["cifEmpresa"]
        ccc = request.POST["CCC"]
        periodo = request.POST["periodoFormacion"]
        importesPeriodo = request.POST["importesPeriodos"]
        costes = request.POST["costes"]
        idAccion = request.POST["idAccion"]
        idGrupo = request.POST["idGrupo"]
        file = request.FILES["uploadedFile"]



        document = models.FundaeDoc(
            title = file.name,
            idAccion = idAccion,
            idGrupo = idGrupo,
            cif = cif,
            ccc = ccc,
            periodo = periodo,
            importesPeriodo = importesPeriodo,
            costes = costes,
            uploadedFile = file
        )
        document.save()

        documents = models.FundaeDoc.objects.all()

        fundae2.GeneradorXMLFundae(settings.UPLOAD_ROOT_DEV + '//' + file.name, cif, ccc, periodo, importesPeriodo, costes, idAccion, idGrupo)
        return fundae2.download(request, settings.DOWNLOAD_ROOT_DEV + "//fichero-envio.xml")
        

        return render(request, 'core/fundae.html', context= {
            "files": documents
        }) 
        '''cif = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]
        
        
        # Guardando la info en la base de datos
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()
        documents = models.Document.objects.all()
        #path = '../../UploadedFiles/{}'.format(uploadedFile.name)
        path = settings.BASE_DIR / 'UploadedFiles\\{}'.format(uploadedFile.name)
        main.main(path)
        return main.download(request, settings.DOWNLOAD_ROOT_DEV + '//InformeAbsentismo.xls')'''
    
    return render(request, 'core/fundae.html')




        
    
