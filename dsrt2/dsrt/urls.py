from django.urls import path, re_path, include
from .views import GetYearList ,ImageProjectedView,ImageFileView,Quicklook,ImageFileList,SpecFileView,SpeFileList,DownLoadFile,Flowalculation

urlpatterns = [
    path('yearlist/',GetYearList.as_view()),
    path('projectview/',ImageProjectedView.as_view()),
    path('imagefile/',ImageFileView.as_view()), #获取成像文件
    path('specfile/',SpecFileView.as_view()), 
    path('quicklook/',Quicklook.as_view()),
    path('imgfilelist/',ImageFileList.as_view()),
    path('spefilelist/',SpeFileList.as_view()),
    path('download/',DownLoadFile.as_view()),
    path('flowalculation/',Flowalculation.as_view())
] 