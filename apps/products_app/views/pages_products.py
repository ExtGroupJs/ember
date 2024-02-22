from django.shortcuts import render


# Create your views here.


def classification(request):
    return render(request, "productos/classification.html")


def destination(request):
    return render(request, "productos/destination.html")


def entity(request):
    return render(request, "productos/entity.html")


def munit(request):
    return render(request, "productos/munit.html")


def plans(request):
    return render(request, "productos/plans.html")


def individualpackaging(request):
    return render(request, "productos/individualpackaging.html")


def groupingpackaging(request):
    return render(request, "productos/groupingpackaging.html")


def product(request):
    return render(request, "productos/product.html")


def production(request):
    return render(request, "productos/production.html")
