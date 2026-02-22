
from .models import Product
from .serializers import ProductSerializers
from decimal import Decimal, InvalidOperation
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

# Create your views here.

class ProductListCreateView(GenericAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

    def get(self,request):
        search=self.request.query_params.get('search',None) or request.data.get('search')
        price_parm = self.request.query_params.get('price', None) or request.data.get('price')
        try:
            if price_parm:
                price = Decimal(price_parm)
            else:
                price = Decimal(0)
        except (InvalidOperation, ValueError):
            price = Decimal(0)
        if search:
            product = Product.objects.filter(Q(title__icontains=search) & Q(price__gte=price))
            print(product)
            if not product.exists():
                data={
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message':'Topilmadi',
                }
                return Response(data,status=status.HTTP_404_NOT_FOUND)
            serializer=self.get_serializer(product,many=True)
            data={
                'status':status.HTTP_200_OK,
                'message':'products',
                'data':serializer.data
            }
            return Response(data)
        product=self.get_queryset()
        serializer=self.get_serializer(product,many=True)
        data={
            'status':status.HTTP_200_OK,
            'message':'Mahsulotlar',
            'data':serializer.data
        }
        return Response(data)

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'status':status.HTTP_201_CREATED,
                'message':'product saqlandi',
                'data':serializer.data
            }
            return Response(data)
        data={
            'status':status.HTTP_400_BAD_REQUEST,
            'message':'Error',
            'data':serializer.errors
        }
        return Response(data)



