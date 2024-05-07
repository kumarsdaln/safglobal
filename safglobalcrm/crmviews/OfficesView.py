from django.shortcuts import render
from django.http import HttpResponse
from safglobalcrm.models import *
from safglobalcrm.serializers import *
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Office Views.
class OfficesCreate(generics.CreateAPIView):
    serializer_class = OfficeSerializer
    permission_classes = [IsAuthenticated]
class OfficesList(generics.ListAPIView):
    queryset = Offices.objects.all()
    serializer_class = OfficeReadSerializer
    permission_classes = [IsAuthenticated]
class OfficesUpdate(generics.UpdateAPIView):
    queryset = Offices.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class OfficesDelete(generics.DestroyAPIView):
    queryset = Offices.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)

# Office Users Views.
class OfficesUsersCreate(generics.CreateAPIView):
    serializer_class = OfficeUsersSerializer
    permission_classes = [IsAuthenticated]
class OfficesUsersList(generics.ListAPIView):
    serializer_class = OfficeUsersSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = OfficeUsers.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        office_filter = self.request.query_params.get('office', None)
        if office_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(office=office_filter)
        return queryset
class OfficesUsersUpdate(generics.UpdateAPIView):
    queryset = OfficeUsers.objects.all()
    serializer_class = OfficeUsersSerializer
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
class OfficesUsersDelete(generics.DestroyAPIView):
    queryset = OfficeUsers.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
