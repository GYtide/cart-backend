from django.urls import path, re_path, include
from .views import GetYearList ,ImageProjectedView

urlpatterns = [
    path('yearlist/',GetYearList.as_view()),
    path('projectview/',ImageProjectedView.as_view())
]