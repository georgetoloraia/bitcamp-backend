from rest_framework import serializers
from . import models


class BitCampUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.BitCampUser
        fields = [
            "id", "first_name", "last_name", "phone_number", "email", "username", "password"
        ]

class PaymentSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()

    class Meta:
        model = models.Payment
        fields = [
            'id', 'enrollment', 'amount', 'status', 
            'payze_transactionId', 'payze_paymentId', 'cardMask', 'token', 
            'paymentUrl', 'title'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)  # Adjust source if needed

    class Meta:
        model = models.Enrollment
        fields = [
            "id", "enrollment_date", "enrollment_cancel_date", "user", "service_id", 
            "program_id", "mentor_id", "status", "payments"
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        if user:
            validated_data["user"] = user
        return super().create(validated_data)
    
    
