from django.shortcuts import render
from django.http import FileResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import ProjectDataSerializer,SpecViewFileSerialzer,ProjectFileSerializer ,ImageFileSerializer
from astropy.io import fits
import os
import io
import numpy as np
from pathlib import Path
import json
import base64
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


class OverView(views.APIView):
    def get(self,request):

        try:
            # 获取频谱概图
            date = request.GET.get('date')  # 传入日期，查询相应文件
            start_time = request.GET.get('start')
            end_time = request.GET.get('end')
            spequeryset = models.SpecView.objects.filter(date__exact=date)
            proqueryset = models.ProjectData.objects.filter(date__exact=date)

            # 如果都是空返回无数据
            # if spequeryset.count()==0 and proqueryset.count()==0:
            #     return Response(['NOT FOUND DATA'],status=status.HTTP_404_NOT_FOUND)

            serializer = SpecViewFileSerialzer(spequeryset)

            with open(r'/home/gytide/dsrtdev/dsrt2/dsrt/output.png','rb') as f:
                 img_byte = f.read()  # 二进制编码
                 img_b64 = base64.b64encode(img_byte)  # img_b64是字节类型变量，b64.encode()对字节类型变量进行b64编码，bytes->bytes
                 img_res = img_b64.decode('utf-8')  # 相当于去掉字符串前面的b'....'
       
            return Response([{'res':img_res}],status=status.HTTP_200_OK)
        
        except:
            return Response([],status=status.HTTP_404_NOT_FOUND)