from rest_framework import serializers

from .models import ProjectData, ImageData, SpecView, SpecData

# 对投影文件的序列化，为了得到有数据的日期


class ProjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = ['file_name', 'date']

# 对频谱概图文件的序列化, 得到文件路径


class SpecViewFileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = SpecView
        fields = ['file_name', 'file_path', 'date']

# 对投影文件的序列化，为了得到文件路径


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = ['file_name', 'file_path', 'date']

# 对成像文件的序列化，为了得到文件信息


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = ['file_name', 'file_path', 'time_begin', 'time_end']

# 对频谱数据文件序列化,得到文件信息


class SpecDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecData
        fields = ['file_name', 'file_path', 'time_begin', 'time_end']


class SpecDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecData
        fields = ['file_name', 'time_begin', 'time_end']
