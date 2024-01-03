from rest_framework import serializers
from . import models


class BitCampUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.BitCampUser
        fields = [
            "id", "first_name", "last_name", "phone_number", "email", "username", "password"
        ]

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Enrollment
        fields = [
            "id", "enrollment_date", "enrollment_cancel_date", "user_id", "service_id", "program_id", "mentor_id", "status"
        ]
    
    def create(self, validated_data):
        user = self.context.get("user")
        if user:
            validated_data["user_id"] = user

        return super().create(validated_data)