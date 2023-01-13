"""zentrader_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]

#urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns += (
    path("api/v1/", include('stock.urls')),
    path("api/v1/", include('operation.urls')),
    path("api/v1/", include('experience.urls')),
    path("api/v1/", include('buy.urls')),
    path("api/v1/", include('sell.urls')),
    path("api/v1/", include('ir_br.urls')),
    path("api/v1/", include('account.urls')),
    path("api/v1/", include('notes.urls')),
    path("api/v1/", include('learning.urls')),
    path("api/v1/", include('report.urls')),
    path("api/v1/", include('zen_fortune.urls')),
    path("api/v1/", include('trade_system.urls')),
    path("oauth/", include('zen_oauth.urls'))
)
