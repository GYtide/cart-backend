from django.urls import path, re_path, include
from .views import GetYearList

urlpatterns = [
    path('yearlist/',GetYearList.as_view())
]