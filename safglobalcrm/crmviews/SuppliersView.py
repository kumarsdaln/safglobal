from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from safglobalcrm.models import *
from safglobalcrm.serializers import *
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Create your views here.
class SuppliersList(generics.ListAPIView):
    serializer_class = SuppliersReadSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Suppliers.objects.all()

        # Retrieve query parameters for filtering, for instance, 'name'
        search = self.request.query_params.get('search', None)
        sortby = self.request.query_params.get('sortby', 'id')
        sortdirection = self.request.query_params.get('sortdirection', 'asc')

        if sortdirection == 'desc':
            sortby = '-' + sortby
        
        if search is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(Q(name__icontains=search) | Q(company_id__icontains=search) | Q(phone_number__icontains=search))
        queryset = queryset.order_by(sortby)
        return queryset
    
class SuppliersCreate(generics.CreateAPIView):
    serializer_class = SuppliersSerializer
    permission_classes = [IsAuthenticated]

class SuppliersDetails(generics.RetrieveAPIView):
    serializer_class = SuppliersReadSerializer
    queryset = Suppliers.objects.all()
    permission_classes = [IsAuthenticated]    

class SuppliersUpdate(generics.UpdateAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class SuppliersDelete(generics.DestroyAPIView):
    queryset = Suppliers.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)