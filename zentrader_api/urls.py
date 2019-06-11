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
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

#urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns += (
    url(r"^api/v1/", include('stock.urls')),
    url(r"^api/v1/", include('operation.urls')),
    url(r"^api/v1/", include('experience.urls')),
    url(r"^api/v1/", include('buy.urls')),
    url(r"^api/v1/", include('ir_br.urls')),
    url(r"^api/v1/", include('account.urls')),
    url(r"^api/v1/", include('notes.urls')),
    url(r"^api/v1/", include('learning.urls')),
    url(r"^api/v1/", include('zen_fortune.urls')),
    url(r"^oauth/", include('zen_oauth.urls'))
)
