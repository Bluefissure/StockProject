from django.shortcuts import render, redirect
from stockapp.models import *
from rest_framework import viewsets, generics
from stockapp.serializers import *
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class StockViewSet(viewsets.ModelViewSet):
    """
    Stocks stored in the db.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class HistoricalViewSet(viewsets.ModelViewSet):
    """
    Historical price stored in the db.
    """
    serializer_class = HistoricalPriceTileSerializer
    queryset = HistoricalPriceTile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stock']


class LiveViewSet(viewsets.ModelViewSet):
    """
    Historical price stored in the db.
    """
    serializer_class = LivePriceTileSerializer
    queryset = LivePriceTile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stock']


def index(request):
    pass
    return render(request, 'stockapp/index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = "Please fill out all fields"
        if username and password:
            username = username.strip()
            try:
                user = User.objects.get(name=username)

                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "password is incorrect"
            except:
                message = "username is incorrect"
        return render(request, 'stockapp/login.html', {"message": message})
    return render(request, 'stockapp/login.html')


def register(request):
    pass
    return render(request, 'stockapp/register.html')


def logout(request):
    pass
    return redirect('/index/')
