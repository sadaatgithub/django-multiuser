from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import StudentRegistrationSerializer,TeacherRegistrationSerializer,\
                         UserProfileSerializer, UserChangePasswordSerializer,UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    def post(self,request,format=None):
        role = request.data.get('role')
        if role == 'ST':
            serializer = StudentRegistrationSerializer(data=request.data)
        elif role == 'TE':
            serializer = TeacherRegistrationSerializer(data=request.data)
        else:
            return Response({'error':'Invalid Role'})
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg':'Success','token':token}, status=status.HTTP_200_OK)
    

class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
class UserLoginView(APIView):

    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    # Change Password View for Users
    def post(self,request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed successfully'}, status=status.HTTP_200_OK)


    

