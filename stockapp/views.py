from django.shortcuts import render
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