from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from . import serializers, models
import datetime
import requests
from django.conf import settings


class SignupUser(APIView):
    @extend_schema(responses=serializers.BitCampUserSerializer)
    def post(self, request, **kwargs):
        serializer = serializers.BitCampUserSerializer(
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            user.set_password(request.data["password"])
            user.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    @extend_schema(responses=serializers.BitCampUserSerializer)
    def post(self, request, **kwargs):
        user = get_object_or_404(
            models.BitCampUser,
            username=request.data["username"]
        )
        
        if not user.check_password(request.data["password"]):
            return Response(
                {"detail": "Not found."}, 
                status = status.HTTP_401_UNAUTHORIZED
            )
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "token" : token.key
        })
        
class CurrentUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=serializers.BitCampUserSerializer)
    def get(self, request, **kwargs):
        user_data = dict(
            serializers.BitCampUserSerializer(
                instance=request.user
            ).data
        )
        
        user_data.pop("password")
        
        return Response(user_data)

class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=serializers.BitCampUserSerializer)
    def put(self, request, **kwargs):        
        serializer = serializers.BitCampUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewEnroll(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=serializers.EnrollmentSerializer)
    def post(self, request, **kwargs):
        serializer = serializers.EnrollmentSerializer(
            data=request.data,
            context={"user": request.user},
            partial=True
        )
        serializer.user_id = request.user.id

        if serializer.is_valid():
            enrollment = serializer.save()
            service = enrollment.service_id  # Assuming service_id is a ForeignKey to Service

            # Ensure service is not None
            if service is not None and hasattr(service, 'payze_product_id'):
                payze_response = self.create_payze_subscription(request.user, service.payze_product_id)

                if payze_response.status_code == 200:
                    # Process successful response
                    payze_data = payze_response.json()
                    enrollment.payze_subscription_id = payze_data['id']
                    enrollment.payze_payment_url = payze_data['transactionUrl']
                    enrollment.save()
                    return Response(payze_data, status=status.HTTP_201_CREATED)
                else:
                    # Handle errors from Payze
                    return Response(payze_response.json(), status=payze_response.status_code)

            # Handle the case where service or payze_product_id is not available
            return Response({"error": "Service or Payze product ID not available"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def create_payze_subscription(self, user, payze_product_id):
        payload = {
            "productId": payze_product_id,
            "cardToken": "PAY123ZE...",  # This should be dynamically obtained
            "hookUrl": "https://yourdomain.com/hook",  # Your server for webhooks
            "email": user.email,  # User's email
            "phone": user.phone_number,  # User's phone number
            "callback": "https://yourdomain.com/callback",  # Callback URL after successful payment
            "callbackError": "https://yourdomain.com/callback-error",  # Callback URL after failed payment
            "sendEmails": False  # Set based on your preference
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer " + settings.PAYZE_API_KEY  # Your Payze API Key
        }
        response = requests.post(
            'https://payze.io/v2/api/subscription',
            json=payload,
            headers=headers
        )
        return response

    
class MyEnrolls(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=serializers.EnrollmentSerializer)
    def get(self, request, **kwargs):
        enrollments = models.Enrollment.objects.filter(
            user_id=request.user.id
        )
        serializer = serializers.EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateEnroll(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=serializers.EnrollmentSerializer)
    def put(self, request, id, **kwargs):
        enrollment = get_object_or_404(
            models.Enrollment,
            id=id
        )
        
        serializer = serializers.EnrollmentSerializer(
            enrollment,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckPayzeSubscriptionStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, **kwargs):
        try:
            enrollment = models.Enrollment.objects.get(id=id)
        except models.Enrollment.DoesNotExist:
            return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription_status = self.check_payze_subscription_status(enrollment.payze_subscription_id)
        if subscription_status:
            # Logic to update enrollment based on the status
            if subscription_status == 'Active':
                enrollment.status = 'Active'
                enrollment.enrollment_date = datetime.date.today()
                enrollment.save()
                # Additional logic if needed
                return Response({"status": "Enrollment updated to Active"}, status=status.HTTP_200_OK)
            elif subscription_status == 'Cancelled':
                # Handle cancellation
                pass
            else:
                # Handle other statuses or unknown status
                pass
        else:
            return Response({"error": "Unable to verify subscription status"}, status=status.HTTP_400_BAD_REQUEST)

    def check_payze_subscription_status(self, subscription_id):
        url = f"https://payze.io/v2/api/subscription?$filter=Id eq {subscription_id}"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer " + settings.PAYZE_API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                return data[0]['status']
        return None