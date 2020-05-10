from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(blank=True, max_length=128)

    def __str__(self):
        return self.symbol


class HistoricalPriceTile(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='historical_price')
    date = models.DateField()
    open = models.DecimalField(max_digits=32, decimal_places=16)
    high = models.DecimalField(max_digits=32, decimal_places=16)
    low = models.DecimalField(max_digits=32, decimal_places=16)
    close = models.DecimalField(max_digits=32, decimal_places=16)
    adj_close = models.DecimalField(max_digits=32, decimal_places=16)
    volume = models.IntegerField()

    def __str__(self):
        return "{}--{}".format(self.stock, self.date)

    class Meta:
        unique_together = ('stock', 'date')


class LivePriceTile(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='live_price')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=32, decimal_places=16)
    volume = models.IntegerField()

    def __str__(self):
        return "{}--{}".format(self.stock, self.time)

    class Meta:
        unique_together = ('stock', 'time')


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="info")
    stocks = models.ManyToManyField(Stock, related_name='sub_users', blank=True)

    def __str__(self):
        return str(self.user)

class Indicator(models.Model):
    name = models.CharField(max_length=16)
    price = models.ForeignKey(HistoricalPriceTile, related_name='indicators', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)

