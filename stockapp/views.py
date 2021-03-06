from django.shortcuts import render
from stockapp.models import *
from django.db.models import Count, Sum, Max, Min
from rest_framework import filters, viewsets, generics
from stockapp.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import ModelChoiceFilter, DateFromToRangeFilter, FilterSet
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError, transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.http import JsonResponse

import traceback
# Create your views here.



class StockViewSet(viewsets.ModelViewSet):
    """
    Stocks stored in the db.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class HistoricalFilter(FilterSet):
    stock = ModelChoiceFilter(queryset=Stock.objects.all())
    date = DateFromToRangeFilter()

    class Meta:
        model = HistoricalPriceTile
        fields = ['stock', 'date']

class HistoricalViewSet(viewsets.ModelViewSet):
    """
    Historical price stored in the db.
    """
    serializer_class = HistoricalPriceTileSerializer
    queryset = HistoricalPriceTile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = HistoricalFilter
    filterset_fields = ['stock', 'date']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class IndicatorFilter(FilterSet):
    stock = ModelChoiceFilter(queryset=Stock.objects.all())
    price__date = DateFromToRangeFilter()

    class Meta:
        model = Indicator
        fields = ['name', 'price__stock', 'price__date']

class IndicatorViewSet(viewsets.ModelViewSet):
    """
    Indicator stored in the db.
    """
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = IndicatorFilter
    filterset_fields = ['name', 'price__stock', 'price__date']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class PredictionFilter(FilterSet):
    stock = ModelChoiceFilter(queryset=Stock.objects.all())
    price__date = DateFromToRangeFilter()

    class Meta:
        model = Prediction
        fields = ['name', 'price__stock', 'price__date']

class PredictionViewSet(viewsets.ModelViewSet):
    """
    Prediction stored in the db.
    """
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = PredictionFilter
    filterset_fields = ['name', 'price__stock', 'price__date']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class LiveViewSet(viewsets.ModelViewSet):
    """
    Live price stored in the db.
    """
    serializer_class = LivePriceTileSerializer
    queryset = LivePriceTile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stock']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


def ren2res(template: str, req, dict=None, json_res=False):
    if dict is None:
        dict = {}
    if req.user.is_authenticated:
        dict.update({'user': {
            "username": req.user.username,
        }})
    else:
        dict.update({'user': False})
    if req:
        if json_res and req.is_ajax() and req.method == 'GET':
            return JsonResponse(dict)
        return render(req, template, dict)
    else:
        return render(req, template, dict)

@login_required(login_url='/login/')
def index(req):
    return ren2res("index.html", req, {})

@login_required(login_url='/login/')
def query(req):
    if req.method == "POST" and req.is_ajax():
        serialize_hs = lambda hs: [
                {
                    'name': h.stock.name,
                    'date': h.date,
                    'open': h.open,
                    'high': h.high,
                    'low': h.low,
                    'close': h.close,
                    'volume': h.volume,
                } for h in hs
            ]
        query_type = req.POST.get('query_type')
        print("query_type:{}".format(query_type))
        response = {'status':'err', 'msg':'Server Error'}
        if query_type == 'All':
            stock = req.POST.get('stock')
            date_start = req.POST.get('date_start')
            date_end = req.POST.get('date_end')
            hs = HistoricalPriceTile.objects.all()
            if stock:
                hs = hs.filter(stock__symbol=stock)
            if date_start and date_end:
                hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
            response['status'] = 'ok'
            response['results'] = serialize_hs(hs)
        elif query_type == 'Highest':
            stock = req.POST.get('stock')
            date_start = req.POST.get('date_start')
            date_end = req.POST.get('date_end')
            hs = HistoricalPriceTile.objects.all()
            if stock:
                hs = hs.filter(stock__symbol=stock)
            if date_start and date_end:
                hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
            hs = hs.filter(high=hs.aggregate(Max('high'))['high__max'])
            print(hs)
            response['status'] = 'ok'
            response['results'] = serialize_hs(hs)
        elif query_type == 'Average':
            stock = req.POST.get('stock')
            date_start = req.POST.get('date_start')
            date_end = req.POST.get('date_end')
            hs = HistoricalPriceTile.objects.all()
            if stock:
                hs = hs.filter(stock__symbol=stock)
            if date_start and date_end:
                hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
            response['status'] = 'ok'
            response['results'] = [
                {
                    'name': hs[0].stock.name,
                    'date': '{} -- {}'.format(date_start, date_end),
                    'open': hs.aggregate(Sum('open'))['open__sum'] / hs.count(),
                    'high': hs.aggregate(Sum('high'))['high__sum'] / hs.count(),
                    'low': hs.aggregate(Sum('low'))['low__sum'] / hs.count(),
                    'close': hs.aggregate(Sum('close'))['close__sum'] / hs.count(),
                    'volume': hs.aggregate(Sum('volume'))['volume__sum'] / hs.count(),
                }
            ]
        elif query_type == 'Lowest':
            stock = req.POST.get('stock')
            date_start = req.POST.get('date_start')
            date_end = req.POST.get('date_end')
            hs = HistoricalPriceTile.objects.all()
            if stock:
                hs = hs.filter(stock__symbol=stock)
            if date_start and date_end:
                hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
            hs = hs.filter(low=hs.aggregate(Min('low'))['low__min'])
            print(hs)
            response['status'] = 'ok'
            response['results'] = serialize_hs(hs)
        elif query_type == 'AverageLessThanLowest':
            stock = req.POST.get('stock')
            date_start = req.POST.get('date_start')
            date_end = req.POST.get('date_end')
            hs = HistoricalPriceTile.objects.all()
            if stock:
                hs = hs.filter(stock__symbol=stock)
            if date_start and date_end:
                hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
            low = hs.aggregate(Min('low'))['low__min']
            response['status'] = 'ok'
            response['results'] = []
            for stock in Stock.objects.all():
                hs = HistoricalPriceTile.objects.filter(stock=stock)
                if date_start and date_end:
                    hs = hs.filter(date__gte=date_start).filter(date__lte=date_end)
                average = hs.aggregate(Sum('high'))['high__sum'] / hs.count()
                if average <= low:
                    response['results'].append({
                        'name': hs[0].stock.name,
                        'date': '{} -- {}'.format(date_start, date_end),
                        'open': hs.aggregate(Sum('open'))['open__sum'] / hs.count(),
                        'high': hs.aggregate(Sum('high'))['high__sum'] / hs.count(),
                        'low': hs.aggregate(Sum('low'))['low__sum'] / hs.count(),
                        'close': hs.aggregate(Sum('close'))['close__sum'] / hs.count(),
                        'volume': hs.aggregate(Sum('volume'))['volume__sum'] / hs.count(),
                    })

        return JsonResponse(response)


    return ren2res("query.html", req, {})


def login(req):
    if req.method == 'GET':
        if req.user.is_anonymous:
            if req.GET.get('next'):
                req.session['next'] = req.GET.get('next')
            return ren2res("login.html", req, {})
        else:
            return HttpResponseRedirect("/index")
    elif req.method == 'POST':
        user = auth.authenticate(username=req.POST.get('Username'), password=req.POST.get('Password'))
        if user:
            auth.login(req, user)
            next = req.session.get('next', '/index')
            return HttpResponseRedirect(next)
        else:
            return ren2res("login.html", req, {'err': "The username or password is incorrect."})


def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')


@transaction.atomic
def register(req):
    if req.method == 'GET':
        req_dict = {}
        if req.GET.get('err'):
            req_dict.update({'err': req.GET.get('err')})
        if req.user.is_anonymous:
            if req.GET.get('next'):
                req.session['next'] = req.GET.get('next')
            return ren2res('register.html', req, req_dict)
        else:
            return HttpResponseRedirect('/')
    elif req.method == 'POST':
        name = req.POST.get('Username')
        user_result = User.objects.filter(username=name)
        if not name:
            return ren2res('register.html', req, {'err': "Username format Error"})
        elif user_result.exists():
            return ren2res('register.html', req, {'err': "This username has been registered"})
        elif not req.POST.get('TOS'):
            return ren2res('register.html', req, {'err': "Please read and accept the terms of use"})
        else:
            pw1 = req.POST.get('Password')
            if not pw1:
                return ren2res('register.html', req, {'err': "Password can not be blank"})
            pw2 = req.POST.get('Retype password')
            if pw1 != pw2:
                return ren2res('register.html', req, {'err': "Password do not match"})
            else:
                try:
                    with transaction.atomic():
                        new_user = User()
                        new_user.username = name
                        new_user.set_password(pw1)
                        new_user.save()
                        new_info = UserInfo(user=new_user)
                        new_info.save()
                        new_user = auth.authenticate(username=name, password=pw1)
                        auth.login(req, user=new_user)
                        next = req.session.get('next')
                        if next:
                            return HttpResponseRedirect(next)
                        else:
                            return ren2res('register.html', req, {'success': "You have successfully registered"})
                except IntegrityError:
                    traceback.print_exc()
                    return ren2res('register.html', req, {'err': "Database Integrity Error"})
                except Exception:
                    traceback.print_exc()
                    return ren2res('register.html', req, {'err': "Server Error"})
