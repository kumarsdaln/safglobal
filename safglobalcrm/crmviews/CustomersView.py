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

# Create your views here.
class CustomersList(generics.ListAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersReadSerializer
    permission_classes = [IsAuthenticated]
    
class CustomersCreate(generics.CreateAPIView):
    serializer_class = CustomersSerializer
    permission_classes = [IsAuthenticated]

class CustomersUpdate(generics.UpdateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class CustomersDelete(generics.DestroyAPIView):
    queryset = Customers.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)

# Customer Users Views.
class CustomersUsersCreate(generics.CreateAPIView):
    serializer_class = CustomerUsersSerializer
    permission_classes = [IsAuthenticated]
class CustomersUsersList(generics.ListAPIView):
    serializer_class = CustomerUsersSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = CustomerUsers.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        customer_filter = self.request.query_params.get('customer', None)
        if customer_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(customer=customer_filter)
        return queryset
class CustomersUsersUpdate(generics.UpdateAPIView):
    queryset = CustomerUsers.objects.all()
    serializer_class = CustomerUsersSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.data.get('activated'):
            instance.activated = request.data.get('activated')
        if request.data.get('name'):
            instance.name = request.data.get('name') 
        if request.data.get('email'):
            instance.email = request.data.get('email')
        if request.data.get('phone'):
            instance.phone = request.data.get('phone')           
        instance.save()
        return Response(serializer.data)
class CustomersUsersDelete(generics.DestroyAPIView):
    queryset = CustomerUsers.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)

# Customer Vessels Views.
class CustomersVesselsCreate(generics.CreateAPIView):
    serializer_class = CustomerVesselsSerializer
    permission_classes = [IsAuthenticated]
class CustomersVesselsList(generics.ListAPIView):
    serializer_class = CustomerVesselsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = CustomerVessels.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        customer_filter = self.request.query_params.get('customer', None)
        if customer_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(customer=customer_filter)
        return queryset
class CustomersVesselsUpdate(generics.UpdateAPIView):
    queryset = CustomerVessels.objects.all()
    serializer_class = CustomerVesselsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class CustomersVesselsDelete(generics.DestroyAPIView):
    queryset = CustomerVessels.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
