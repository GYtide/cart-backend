from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import ProjectDataSerializer

# Create your views here.

class GetYearList(views.APIView):
    
    def get(self,request):
        """
        get方法处理GET请求
        """

        try:
            Yearlist = models.ProjectData.objects.all()
            year = request.GET.get('year')
            Yearlist = models.ProjectData.objects.filter(date__year=year)
            serializer = ProjectDataSerializer(Yearlist, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except :
            return  Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
        