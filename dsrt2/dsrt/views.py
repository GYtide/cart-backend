from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import ProjectDataSerializer, SpecViewFileSerialzer, ProjectFileSerializer, ImageFileSerializer, SpecDataSerializer, SpecDataListSerializer
from astropy.io import fits
from django.core.exceptions import ObjectDoesNotExist
import os
import io
from google.protobuf.internal import encoder, decoder
from google.protobuf.message import Message
import numpy as np
from pathlib import Path
import json
import base64
from django.db.models import Q
from datetime import datetime
import zipfile
from .renderers import BinaryRenderer
from . import utils
from .utils import redis_connection_pool, FlowCal
import redis
from io import BytesIO

from proto import frame_pb2


# Create your views here.

# 根据年份获取有数据的日期


class GetYearList(views.APIView):

    def get(self, request):
        """
        get方法处理GET请求
        """

        try:
            year = request.GET.get('year')
            Yearlist = models.ProjectData.objects.filter(date__year=year)
            serializer = ProjectDataSerializer(Yearlist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

# 暂时使用最简单的json传输


class ImageProjectedView(views.APIView):

    def get(self, request):

        try:
            date = request.GET.get('date')
            queryset = models.ProjectData.objects.filter(date__exact=date)
            serializer = ProjectFileSerializer(queryset, many=True)
            filename = serializer.data[0]['file_name']
            path = serializer.data[0]['file_path']
            path = os.path.join(path, filename)

            # 读取文件
            hdu = fits.open(path)
            data = hdu[0].data  # float32
            timearr = hdu[1].data['TIME']  # int32
            hdu.close()
            pixelarr = np.arange(0, data.shape[0], 1)
            buffer = io.BytesIO()

            np.savez(buffer, data=data, timearr=timearr)
            buffer.seek(0)

            return Response([{'data': data, 'timearr': timearr, 'pixelarr': pixelarr}], status=status.HTTP_200_OK)
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

# /data/imagefile   ?type= openfile || appdata &fname= filename & index =


class ImageFileView(views.APIView):
    renderer_classes = (BinaryRenderer, )

    def get(self, request):

        try:
            name = 'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'
            path = r'/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'
            # 判断request中的 type 属性,如果打开文件并传回hdu文件头信息和第一帧
            reqtype = request.GET.get('type')
            redis_con = redis.Redis(connection_pool=redis_connection_pool)
            if reqtype == 'openfile':
                header = redis_con.hget(name, 'header')
                hdudata = redis_con.hget(name, 1)
                # 判断有没有redis缓存，如果有则从缓存中取出,否则加入缓存
                if not header:
                    # 如果没有缓存则加入缓存
                    hdu = fits.open(path)
                    num = 1
                    pipe = redis_con.pipeline()

                    header = [{}, {}]
                    for card in hdu[0].header.cards:
                        header[0][str(card[0])] = str(card[1])

                    for card in hdu[1].header.cards:
                        header[1][str(card[0])] = str(card[1])

                    header_str = json.dumps(header)

                    redis_con.hset(
                        'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 'header', header_str)
                    for data in hdu[1].data:
                        data_str = str([item.tolist() if isinstance(
                            item, np.ndarray) else item for item in data])
                        redis_con.hset(
                            'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', num, data_str)
                        num = num + 1
                    redis_con.expire(
                        'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 180)
                    pipe.execute()
                    hdu.close()
                    header = redis_con.hget(name, 'header')
                    hdudata = redis_con.hget(name, 1)

                # 返回文件头信息
                header = json.loads(header)
                hdudata = json.loads(hdudata)
                frame = frame_pb2.ImgFrame()
                message = frame_pb2.OpenImgFileAck()

                frame.time = hdudata[0]
                frame.freq = hdudata[1]
                frame.sunx.extend(hdudata[4])
                frame.suny.extend(hdudata[5])
                for row in hdudata[2]:
                    frame.stokesi.extend(row)
                for row in hdudata[3]:
                    frame.stokesv.extend(row)

                message.frame.CopyFrom(frame)
                for card in header[0]:
                    message.header0[card] = header[0][card]

                for card in header[1]:
                    message.header1[card] = header[1][card]
                message.index = 0
                # message.header1 = hdu[1].header
                # 传回文件头和 STOKESI 的第一帧

                respdata = message.SerializeToString()
                response = Response(respdata, status=status.HTTP_200_OK)
                response["Content-Type"] = "application/octet-stream"
                return response
            elif reqtype == 'appdata':
                # 判断有没有redis缓存，如果有则从缓存中取出,否则加入缓存
                index = int(request.GET.get('index'))
                hdudata = redis_con.hget(name, index)
                if not hdudata:
                    # 如果没有缓存则加入缓存
                    hdu = fits.open(path)
                    num = 1
                    pipe = redis_con.pipeline()

                    header = [{}, {}]
                    for card in hdu[0].header.cards:
                        header[0][str(card[0])] = str(card[1])

                    for card in hdu[1].header.cards:
                        header[1][str(card[0])] = str(card[1])

                    header_str = json.dumps(header)

                    redis_con.hset(
                        'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 'header', header_str)
                    for data in hdu[1].data:
                        data_str = str([item.tolist() if isinstance(
                            item, np.ndarray) else item for item in data])
                        redis_con.hset(
                            'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', num, data_str)
                        num = num + 1
                    redis_con.expire(
                        'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 180)
                    pipe.execute()
                    hdu.close()
                    header = redis_con.hget(name, 'header')
                    hdudata = redis_con.hget(name, 1)

                hdudata = json.loads(hdudata)

                message = frame_pb2.ImgAppAck()
                frame = frame_pb2.ImgFrame()

                frame.time = hdudata[0]
                frame.freq = hdudata[1]
                frame.sunx.extend(hdudata[4])
                frame.suny.extend(hdudata[5])
                for row in hdudata[2]:
                    frame.stokesi.extend(row)
                for row in hdudata[3]:
                    frame.stokesv.extend(row)

                message.index = index
                message.frame.CopyFrom(frame)
                respdata = message.SerializeToString()
                return Response(respdata, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print('err:', e)
            return Response(status=status.HTTP_404_NOT_FOUND)

# /data/imgfilelist ?type= image || spec & start= & end=
# 获取时间段内的成像数据文件的列表


class ImageFileList(views.APIView):

    def get(self, request):

        try:

            return Response([{'name': 'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits',
                              'path': '/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits',
                              'freq': 233.0,
                              'time_beg': '2022-04-17 03:26:00',
                              'time_end': '2022-04-17 03:39:59'}], status=status.HTTP_200_OK)
        except:
            return Response([{'asdasd'}], status=status.HTTP_200_OK)

# /data/specfile


class SpecFileView(views.APIView):
    renderer_classes = (BinaryRenderer, )

    def post(self, request):
        try:
            path = r'/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417061006_V01.01.fits'

            hdu = fits.open(path)
            frame = frame_pb2.Frame()

            frame.height = hdu[0].data[0].shape[0]
            frame.width = hdu[0].data[0].shape[1]

            frame.id = 1
            frame.fname = 'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'

            # frame.data = hdu[0].data[0]
            for row in hdu[0].data[0]:
                frame.data.extend(row)

            data = frame.SerializeToString()

            response = Response(data, status=status.HTTP_200_OK)
            response["Content-Type"] = "application/octet-stream"

            # 禁用默认渲染器
            return response
        except Exception as e:
            print(e)
            return Response('404', status=status.HTTP_404_NOT_FOUND)

    def get(self, request):

        try:
            path = r'/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417061006_V01.01.fits'

            hdu = fits.open(path)
            data = hdu[0].data[0]

            img = data
            frame = frame_pb2.Frame()

            frame.height = img.shape[0]
            frame.width = img.shape[1]

            frame.id = 1
            frame.fname = 'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'
            for row in img:
                frame.data.extend(row)

            data = frame.SerializeToString()

            response = Response(data, status=status.HTTP_200_OK)
            response["Content-Type"] = "application/octet-stream"

            # 禁用默认渲染器
            return response
        except:
            return Response('404', status=status.HTTP_404_NOT_FOUND)
# /data/spefilelist


class SpeFileList(views.APIView):

    def get(self, request):
        try:
            start = request.GET.get('start')
            end = request.GET.get('end')

            # 查询开始时间、结束时间有一项在时间范围内即可。并按时间排序
            queryset = models.SpecData.objects.filter(
                Q(time_begin__lte=start, time_end__gte=start) |
                Q(time_begin__lte=end, time_end__gte=end) |
                Q(time_begin__gte=start, time_end__lte=end)).order_by('time_begin')
            serializer = SpecDataListSerializer(queryset, many=True)
            return Response({'list': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'asdasd'}, status=status.HTTP_404_NOT_FOUND)


class Quicklook(views.APIView):
    def get(self, request):

        try:
            # 获取频谱概图
            # date = request.GET.get('date')  # 传入日期，查询相应文件
            start_time = request.GET.get('start')
            end_time = request.GET.get('end')
            date = datetime.strptime(
                start_time, '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d')

            spequeryset = models.SpecView.objects.filter(date__exact=date)
            speserializer = SpecViewFileSerialzer(spequeryset, many=True)
            spepath = speserializer.data[0]['file_path']

            proqueryset = models.ProjectData.objects.filter(date__exact=date)
            proserializer = ProjectFileSerializer(proqueryset, many=True)
            propathlist = [d['file_path'] for d in proserializer.data]
            # 读取文件并生成概图
            figspec, figimg = utils.genQuicklook(
                spepath, propathlist[0], propathlist[1::], start_times=start_time, end_times=end_time)

            imglist = []
            # 文件缓冲区，保存为base64
            specbuffer = io.BytesIO()
            figspec.savefig(specbuffer, format='png')
            specbuffer.seek(0)
            spe_str = base64.b64encode(specbuffer.read()).decode()
            imglist.append(spe_str)

            # 读取投影图数组，都保存为 base64

            for fig in figimg:
                probuffer = io.BytesIO()
                fig.savefig(probuffer, format='png')
                probuffer.seek(0)
                pro_str = base64.b64encode(probuffer.read()).decode()
                imglist.append(pro_str)

            return Response(imglist, status=status.HTTP_200_OK)

        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)


# /data/download 根据文件列表下载文件

class DownLoadFile(views.APIView):

    def post(self, request):
        try:
            file_list = request.data['filelist']
            query = Q(file_name__in=file_list)
            # 查出频谱数据文件的路径
            queryset = models.SpecData.objects.filter(query)
            serializer = SpecDataSerializer(queryset, many=True)

            # 将 serializer.data 转换为 JSON 格式的字符串
            spe_list = list(serializer.data)
            filepaths = [d['file_path'] for d in spe_list]

            # 查出成像数据文件的路径
            queryset = models.ImageData.objects.filter(query)
            serializer = ImageFileSerializer(queryset, many=True)
            print(queryset)

            # 将 serializer.data 转换为 JSON 格式的字符串
            img_list = list(serializer.data)
            filepaths += [d['file_path'] for d in img_list]

            print(filepaths)

            # 将要下载的文件打包成 ZIP 文件
            now = datetime.now()
            zip_filename = '%s.zip' % now.strftime('%Y-%m-%d %H:%M:%S.%f')
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for filepath in filepaths:
                        zip_file.write(filepath, os.path.basename(filepath))

            # 创建新的 BytesIO 对象，并将 ZIP 文件内容写入其中
                zip_data = zip_buffer.getvalue()
            response_data = io.BytesIO(zip_data)
            # 将 ZIP 文件作为响应发送给客户端浏览器进行下载
            response = FileResponse(
                response_data, as_attachment=True, filename=zip_filename)
            return response
        except ObjectDoesNotExist:
            return Response({'error': '无法找到一个或多个文件'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# /data/flowalculation
class Flowalculation(views.APIView):
    renderer_classes = (BinaryRenderer, )

    def post(self, request):
        try:
            file_list = request.data['filelist']
            area = request.data['area']
            message = FlowCal(file_list, area)
            respdata = message.SerializeToString()
            return Response(respdata, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': '无法找到一个或多个文件'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
