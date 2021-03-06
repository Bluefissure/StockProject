from stockapp.models import *
from rest_framework import serializers


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ('url', 'symbol', 'name')

class HistoricalPriceTileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HistoricalPriceTile
        fields =('__all__')

class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Indicator
        fields =('__all__')

class LivePriceTileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LivePriceTile
        fields =('__all__')

class PredictionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prediction
        fields = ('__all__')