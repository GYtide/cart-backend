from rest_framework import serializers

from .models import ProjectData

# 对投影文件的序列化，为了得到有数据的日期
class ProjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = ['file_name','date']
