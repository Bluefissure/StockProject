from django.contrib import admin

# Register your models here.

from .models import *

class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name']
    search_fields = ['symbol', 'name']

class HistoricalPriceTileAdmin(admin.ModelAdmin):
    list_display = ['stock', 'date', 'open', 'high', 'low', 'close', 'volume']
    search_fields = ['stock', 'date']
    list_filter = ['stock']

class LivePriceTileAdmin(admin.ModelAdmin):
    list_display = ['stock', 'time', 'price', 'volume']
    search_fields = ['stock']
    list_filter = ['stock']

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['price', 'name', 'value']
    search_fields = ['price', 'name']
    list_filter = ['price__stock', 'name']

class PredictionAdmin(admin.ModelAdmin):
    list_display = ['price', 'name', 'value', 'next']
    search_fields = ['price', 'name']
    list_filter = ['price__stock', 'name']


admin.site.register(Stock, StockAdmin)
admin.site.register(HistoricalPriceTile, HistoricalPriceTileAdmin)
admin.site.register(LivePriceTile, LivePriceTileAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Prediction, PredictionAdmin)