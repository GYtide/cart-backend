from django.urls import path, re_path, include
from .views import GetYearList ,ImageProjectedView,ImageFileView

urlpatterns = [
    path('yearlist/',GetYearList.as_view()),
    path('projectview/',ImageProjectedView.as_view()),
    path('image/',ImageFileView.as_view())
]