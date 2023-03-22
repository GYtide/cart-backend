from django.shortcuts import render
from django.http import FileResponse,HttpResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import ProjectDataSerializer,SpecViewFileSerialzer,ProjectFileSerializer ,ImageFileSerializer,SpecDataSerializer,SpecDataListSerializer
from astropy.io import fits
from django.core.exceptions import ObjectDoesNotExist
import os
import io
import numpy as np
from pathlib import Path
import json
import base64
from django.db.models import Q
import datetime
import zipfile

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

# /data/imagefile   ?type= openfile || appdata &fname= filename & index = 
class ImageFileView(views.APIView):

    def get(self,request):

        try:
            name = 'ODACH_DSRT02_SRIM_L2_150.9MHz_202303010955.fits'
            # queryset = models.ImageData.objects.filter(file_name__exact=name)
            # serializer = ImageFileSerializer(queryset,many=True)
            # filename = serializer.data[0]['file_name']
            # path = serializer.data[0]['file_path']
            # path = os.path.join(path,filename)

            path = r'/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'
            
            # 判断request中的 type 属性,如果打开文件并传回hdu文件头信息和第一帧
            reqtype = request.GET.get('type')
            print('reqtype',reqtype)

            if reqtype == 'openfile':

                # 打开文件并返回文件头信息

                hdu = fits.open(path)
                
                data = hdu[1].data[0]

                frame = {'time':data[0],'freq':data[1],
                         'stokesi':data[2],'stokesv':data[3],'sunx':data[4],'suny':data[5]}

                # 传回文件头和 STOKESI 的第一帧

                header0 = hdu[0].header
                header1 = hdu[1].header

                hdu.close()

                return Response([{'header0':header0,'header1':header1},{'frame':frame,'index':1}],status=status.HTTP_200_OK)
            elif reqtype == 'appdata':
                    index = int(request.GET.get('index'))
                    hdu = fits.open(path)
                    # print('index',hdu[1].data[index])
                    data = hdu[1].data[index]

                    frame = {'time':data[0],'freq':data[1],
                         'stokesi':data[2],'stokesv':data[3],'sunx':data[4],'suny':data[5]}

                    hdu.close()
                    return Response([{'frame':frame,'index':index}],status=status.HTTP_200_OK)
            
            else:
                return Response([{'NOTDATA'}],status=status.HTTP_404_NOT_FOUND)
        
        except:
            return Response([],status=status.HTTP_404_NOT_FOUND)

# /data/specfile ?start= 开始时间  & end= 结束时间
class SpecFileView(views.APIView):
    def get(self,request):
        try:
            # ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits
            
            hdu1 = fits.open('/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits')
            hdu2 = fits.open('/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits')
            hdu3 = fits.open('/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits')
            hdu4 = fits.open('/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits')
            hdu5 = fits.open('/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits')

            fitslist = [hdu1]

            '''将待处理文件的数据导入新的数组'''

            # 导入时间矩阵和频点矩阵
            # 频点矩阵
            freArray = fitslist[0][1].data['frequency'][0]
            freArray = list(map(lambda x: round(x, 2), freArray))
            # 时间矩阵

            otimeArray = fitslist[0][1].data['TIME']

            for i in range(1, len(fitslist)):
                otimeArray = np.hstack((otimeArray, fitslist[i][1].data['TIME']))

            # # 数据矩阵

            odataArray = fitslist[0][0].data

            # for i in range(1, len(fitslist)):
            #     odataArray = np.concatenate((odataArray, fitslist[i][0].data), axis=2)

            return Response({'frearr':freArray,'time':otimeArray,'data':odataArray},status=status.HTTP_200_OK)
        except:

            return Response(['SpecFileViewNotFound'],status=status.HTTP_404_NOT_FOUND)

# /data/imgfilelist ?type= image || spec & start= & end=
# 获取时间段内的成像数据文件的列表
class ImageFileList(views.APIView):

    def get(self,request):

        try:
            
            return Response([{'name':'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits',
                              'path':'/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits',
                              'freq':233.0,
                              'time_beg':'2022-04-17 03:26:00',
                              'time_end':'2022-04-17 03:39:59'}],status=status.HTTP_200_OK)
        except:
            return Response([{'asdasd'}],status=status.HTTP_200_OK)

# /data/spefilelist

class SpeFileList(views.APIView):

    def get(self,request):
        try:
            start = request.GET.get('start')  
            end = request.GET.get('end')

            # 查询开始时间、结束时间有一项在时间范围内即可。并按时间排序
            queryset = models.SpecData.objects.filter(
                Q(time_begin__lte=start, time_end__gte=start) | 
                Q(time_begin__lte=end, time_end__gte=end) | 
                Q(time_begin__gte=start, time_end__lte=end)).order_by('time_begin')
            serializer = SpecDataListSerializer(queryset,many=True)
            return Response({'list':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'asdasd'},status=status.HTTP_404_NOT_FOUND)

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
        


# /data/download 根据文件列表下载文件

class DownLoadFile(views.APIView):

    def post(self,request):
        try:
            file_list = request.data['filelist']
            query = Q(file_name__in=file_list)
            # 查出路径
            queryset = models.SpecData.objects.filter(query)
            serializer = SpecDataSerializer(queryset,many=True)
            
            # 将 serializer.data 转换为 JSON 格式的字符串
            data_list = list(serializer.data)
            filepaths = [d['file_path'] for d in data_list]

            # 将要下载的文件打包成 ZIP 文件
            now = datetime.datetime.now()
            zip_filename = '%s.zip' % now.strftime('%Y-%m-%d %H:%M:%S.%f')
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for filepath in filepaths:
                        zip_file.write(filepath,os.path.basename(filepath))

            # 创建新的 BytesIO 对象，并将 ZIP 文件内容写入其中
                zip_data = zip_buffer.getvalue()
            response_data  = io.BytesIO(zip_data)


            # 将 ZIP 文件作为响应发送给客户端浏览器进行下载
            response = FileResponse(response_data,as_attachment=True,filename=zip_filename)
            # response['Content-Disposition'] = 'attachment; filename="{}"'.format(zip_filename)
            # response['Content-Type'] = 'application/octet-stream'
            return response
        except ObjectDoesNotExist:
            return Response({'error': '无法找到一个或多个文件'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







