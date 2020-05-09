"""StockProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from stockapp import views

router = routers.DefaultRouter()
router.register(r'stocks', views.StockViewSet)
router.register(r'historical', views.HistoricalViewSet)
router.register(r'live', views.LiveViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="StockProject API",
      default_version='v1',
      description="The API of StockProject for developers",
      terms_of_service="",
      contact=openapi.Contact(email="yupeng.zhang@rutgers.edu"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   # permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
