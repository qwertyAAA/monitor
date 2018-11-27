from django.shortcuts import render, redirect, HttpResponse
from organization import models


# Create your views here.
def message(request):
    obj = models.Department.objects.all()
    return render(request, 'organization/message.html', {
        'obj': obj
    })
