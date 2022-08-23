from platform import mac_ver
from django.db import models

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to='UploadedFiles/')
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

class FundaeDoc(models.Model):
    title = models.CharField(max_length=200)
    idAccion = models.CharField(max_length=50, null=True)
    idGrupo = models.CharField(max_length=50, null = True)
    cif = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to='UploadedFiles/')
    ccc = models.CharField(max_length=200)
    periodo = models.CharField(max_length=200)
    costes = models.CharField(max_length=200)
    importesPeriodo = models.CharField(max_length=200)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    




