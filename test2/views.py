from .models import Users
from .serializers import UserSerializers,RegisterSerializers
from rest_framework.response import Response
from rest_framework import status,viewsets,mixins,permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        response={
            'status':status.HTTP_201_CREATED,
            'message':user.username
        }
        return Response(response)

class LoginView(APIView):
    def post(self,request):
        username=self.request.data.get('username')
        password=self.request.data.get('password')

        user=authenticate(username=username,password=password)

        if not user:
            raise ValidationError({'message':'username yoki parol xato'})

        token, _=Token.objects.get_or_create(user=user)

        response={
            'status':status.HTTP_200_OK,
            'message':'Siz login qildiz',
            'data':str(token.key)
        }

        return Response(response)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        response={
            'status':status.HTTP_200_OK,
            'message':'logout qilindi '
        }
        return Response(response)







