from django.shortcuts import render
from django.http import FileResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import ProjectDataSerializer ,ProjectFileSerializer ,ImageFileSerializer
from astropy.io import fits
import os
import io
import numpy as np
from pathlib import Path
import json
# Create your views here.

# 根据年份获取有数据的日期
class GetYearList(views.APIView):
    
    def get(self,request):
        """
        get方法处理GET请求
        """

        try:
            year = request.GET.get('year')
            Yearlist = models.ProjectData.objects.filter(date__year=year)
            serializer = ProjectDataSerializer(Yearlist, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except :
            return  Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
        

# todo: 使用二进制进行浮点数组的传输，使用utf-8数据太大
# class ImageProjectedView(views.APIView):
    
#     def get(self,request):
        
#         try:
#             date = request.GET.get('date')
#             queryset = models.ProjectData.objects.filter(date__exact=date)
#             serializer = ProjectFileSerializer(queryset,many=True)
#             filename = serializer.data[0]['file_name']
#             path = serializer.data[0]['file_path']
#             path = os.path.join(path,filename)

#             # 读取文件 
#             hdu = fits.open(path)
#             data = hdu[0].data #float32
#             timearr = hdu[1].data['TIME'] #int32
#             buffer = io.BytesIO()

#             np.savez(buffer,data=data,timearr = timearr)
#             buffer.seek(0)

#             return FileResponse(buffer,filename='matrices.npz' ,as_attachment=True)
#         except:
#             return Response([{'a':0,'b':0}],status=status.HTTP_404_NOT_FOUND)

# 暂时使用最简单的json传输
class ImageProjectedView(views.APIView):
    
    def get(self,request):
        
        try:
            date = request.GET.get('date')
            queryset = models.ProjectData.objects.filter(date__exact=date)
            serializer = ProjectFileSerializer(queryset,many=True)
            filename = serializer.data[0]['file_name']
            path = serializer.data[0]['file_path']
            path = os.path.join(path,filename)

            # 读取文件 
            hdu = fits.open(path)
            data = hdu[0].data #float32
            timearr = hdu[1].data['TIME'] #int32
            hdu.close()
            pixelarr = np.arange(0,data.shape[0],1)
            buffer = io.BytesIO()

            np.savez(buffer,data=data,timearr = timearr)
            buffer.seek(0)

            return Response([{'data':data,'timearr':timearr,'pixelarr':pixelarr}],status=status.HTTP_200_OK)
        except:
            return Response([],status=status.HTTP_404_NOT_FOUND)

class ImageFileView(views.APIView):

    def get(self,requset):

        try:
            name = 'ODACH_DSRT02_SRIM_L2_150.9MHz_202303010955.fits'
            # queryset = models.ImageData.objects.filter(file_name__exact=name)
            # serializer = ImageFileSerializer(queryset,many=True)
            # filename = serializer.data[0]['file_name']
            # path = serializer.data[0]['file_path']
            # path = os.path.join(path,filename)

            path = r'/home/gytide/dsrtprod/data/2023/03/image_data/ODACH_DSRT02_SRIM_L2_150.9MHz_202303010955.fits'
            
            # 打开文件并传回hdu文件头信息和第一帧

            hdu = fits.open(path)

            print(hdu)
            header =  hdu[0].header

            data = hdu[1].data['STOKESI'][0]
            return Response([{'width':128 ,'height':128 ,'header':header,'data':data.flatten()}],status=status.HTTP_200_OK)
        
        except:
            return Response([],status=status.HTTP_404_NOT_FOUND)



