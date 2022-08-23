from django.http import HttpResponse

def principal(request): # primera vista

    return HttpResponse('Hola mundo')


def MutuaMF(request):

    return HttpResponse('aquí irá el input file')