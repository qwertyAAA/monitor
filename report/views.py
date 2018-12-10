from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import time
from datetime import *


# Create your views here.
def index(request):
    return render(request, 'report/report_index.html')


def search(request):
    # time.strptime()
    report_name = request.POST.get("report_name", None)
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    start_time = datetime.strptime(start_time, "%Y-%m-%d")
    end_time = datetime.strptime(end_time, "%Y-%m-%d")
    print(report_name, start_time, end_time)
    return HttpResponse("查询成功")


def sucai(request):
    return render(request, 'report/sucai_index.html')


def mould(request):
    return render(request, 'report/mould_index.html')


def collection(request):
    return render(request, 'report/collection_index.html')
