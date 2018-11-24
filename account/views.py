from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password


def login(request):
    return render(request, "login.html")


def register(request):
    pass


def logout(request):
    pass


def forget_pwd(request):
    pass


def index(request):
    return render(request, "base.html")