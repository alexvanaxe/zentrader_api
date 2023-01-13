"""location URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

For the django rest used here please see:
    http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/

Examples:
    1. snippet_list = SnippetViewSet.as_view({'get': 'list','post': 'create'})
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trade_system.views import AnalysisViewSet,\
                               TechnicalAnalyzeViewSet,\
                               IndicatorViewSet

router = DefaultRouter()

router.register(r'trade-system/analysis', AnalysisViewSet, basename='analysis')
router.register(r'trade-system/indicator', IndicatorViewSet, basename='indicator')
router.register(r'trade-system/technical_analyze', TechnicalAnalyzeViewSet,
                basename='technical_analyze')

urlpatterns = [
        path('', include(router.urls)),
]
