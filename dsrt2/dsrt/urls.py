from django.urls import path, re_path, include
from .views import GetYearList ,ImageProjectedView,ImageFileView,OverView,ImageFileList

urlpatterns = [
    path('yearlist/',GetYearList.as_view()),
    path('projectview/',ImageProjectedView.as_view()),
    path('imagefile/',ImageFileView.as_view()), #获取成像文件
    path('quicklook/',OverView.as_view()),
    path('filelist/',ImageFileList.as_view())
]