from django.shortcuts import render
from stockapp.models import *
from rest_framework import viewsets, generics
from stockapp.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.db import IntegrityError, transaction

from django.http import JsonResponse

import traceback
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
    Live price stored in the db.
    """
    serializer_class = LivePriceTileSerializer
    queryset = LivePriceTile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stock']


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


def index(req):
    return ren2res("index.html", req, {})


def login(req):
    if req.method == 'GET':
        if req.user.is_anonymous:
            if req.GET.get('next'):
                req.session['next'] = req.GET.get('next')
            return ren2res("login.html", req, {})
        else:
            return HttpResponseRedirect("/index")
    elif req.method == 'POST':
        user = auth.authenticate(username=req.POST.get('Email'), password=req.POST.get('Password'))
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
        email = req.POST.get('Email')
        emailresult = User.objects.filter(username=email)
        if not email:
            return ren2res('register.html', req, {'err': "Email format Error"})
        elif emailresult.exists():
            return ren2res('register.html', req, {'err': "This address has been registered"})
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
                        newuser = User()
                        newuser.username = email
                        newuser.set_password(pw1)
                        newuser.save()
                        newinfo = UserInfo(user=newuser)
                        newinfo.save()
                        newuser = auth.authenticate(username=email, password=pw1)
                        auth.login(req, user=newuser)
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
