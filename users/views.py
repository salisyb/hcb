from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import EmailVerificationSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from users.email.email_verification import verification
import random
import string


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Verification


def generate_otp():
    characters = string.digits
    result_str = ''.join(random.choice(characters) for i in range(6))
    return result_str


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('first_name') == None and serializer.validated_data.get('last_name') == None:
            return Response({'status': 'Please provide your first name and last name'}, status=400)
        user = serializer.save()
        otp = generate_otp()
        try:
            u = verification(name=user.first_name,
                             recipient=user.email, code=otp)
            u.send()
            Verification.objects.create(owner=user, otp=otp)
        except:
            pass
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }, 201)


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        if not user.security.is_verified:
            Response({'token': AuthToken.objects.create(user)[1]}, status=204)
        res_data = UserSerializer(
            user, context=self.get_serializer_context()).data
        return Response({
            "user": res_data,
            "token": AuthToken.objects.create(user)[1]
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EmailVerificationAPI(request):
    user = request.user
    serializer = EmailVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        verify = Verification.objects.get(owner=user)
    except Verification.DoesNotExist:
        return Response(status=200)

    if verify.otp != serializer.data['otp']:
        return Response({'status': 'failed', 'reason': 'not a valid code'})

    user.security.is_verified = True
    verify.delete()
    user.save()
    ser = UserSerializer(user)
    return Response({'user': ser.data, 'token': AuthToken.objects.create(user)[1]}, status=201)
