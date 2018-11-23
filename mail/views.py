from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def template(request):
    return render(request, 'template.html')
