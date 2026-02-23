from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes

from .serializers import UserSerializers,RegisterSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
User = get_user_model()
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

class ProfilUser(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializers

    def get_object(self):
        return self.request.user

class PasswordUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user=request.user
        old_password=self.request.data.get('old_password')
        password=self.request.data.get('password')
        conf_password=self.request.data.get('conf_password')

        if not user.check_password(old_password):
            return Response({"error": "Eski parol noto'g'ri "},status=status.HTTP_400_BAD_REQUEST)
        if password!=conf_password:
            return Response({"error":"Yangi parollar bir-biriga mos emas"},status=status.HTTP_400_BAD_REQUEST)


        token, _=Token.objects.get_or_create(user=user)


        user.set_password(password)
        user.save()
        response={
            'status':status.HTTP_200_OK,
            'message':"Malumotlariz muffaqiyatli yanilandi",
            'data':str(token.key)
        }
        return Response(response)
