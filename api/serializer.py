from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    Converted_Currency = serializers.CharField()
    