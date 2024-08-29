from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, "index.html")


def usuarios(request):
    return render(request, "user/usuarios.html")


def first_login(request):
    return render(request, "login/login.html")


def area(request):
    return render(request, "nomencladores/area.html")


def responsability(request):
    return render(request, "nomencladores/responsability.html")
