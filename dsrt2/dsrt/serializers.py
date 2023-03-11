from rest_framework import serializers

from .models import ProjectData ,ImageData

# 对投影文件的序列化，为了得到有数据的日期
class ProjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = ['file_name','date']

# 对投影文件的序列化，为了得到文件信息
class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = ['file_name','file_path','date']

# 对成像文件的序列化，为了得到文件信息
class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = ['file_name','file_path','date']
