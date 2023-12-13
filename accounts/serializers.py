from rest_framework import serializers
from . import models


class BitCampUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.BitCampUser
        fields = [
            "id", "username", "email", "phone_number", "password"
        ]