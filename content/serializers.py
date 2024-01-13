from rest_framework import serializers
from . import models

        
# Add ProgramSerializer
class ProgramSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Program
        fields = [
            "id", "title"
        ]
# Add ServiceSerializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Service
        fields = [
            "id", "title", "price"
        ]