from django.db import models

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

    class Meta:
        unique_together = ('stock', 'date')


class LivePriceTile(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='live_price')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=32, decimal_places=16)
    volume = models.IntegerField()

    class Meta:
        unique_together = ('stock', 'time')


class User(models.Model):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
        )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='male')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'User'
        verbose_name_plural = 'User'