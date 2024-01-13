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
            "id", "enrollment_date", "enrollment_cancel_date", "user", "service_id", "program_id", "mentor_id", "status"
        ]
    
    def create(self, validated_data):
        user = self.context.get("user")
        if user:
            validated_data["user"] = user

        return super().create(validated_data)
    
    
class PaymentSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()

    class Meta:
        model = models.Payment
        fields = [
            'id', 'enrollment', 'amount', 'status', 
            'payze_transactionId', 'payze_paymentId', 'cardMask', 'token', 
            'paymentUrl', 'title'
        ]