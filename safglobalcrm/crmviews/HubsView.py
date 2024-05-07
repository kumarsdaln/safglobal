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
class HubsList(generics.ListAPIView):
    queryset = Hubs.objects.all()
    serializer_class = HubsReadSerializer
    permission_classes = [IsAuthenticated]
    
class HubsCreate(generics.CreateAPIView):
    serializer_class = HubsSerializer
    permission_classes = [IsAuthenticated]

class HubsUpdate(generics.UpdateAPIView):
    queryset = Hubs.objects.all()
    serializer_class = HubsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class HubsDelete(generics.DestroyAPIView):
    queryset = Hubs.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)  

# Hub Users Views.
class HubsUsersCreate(generics.CreateAPIView):
    serializer_class = HubUsersSerializer
    permission_classes = [IsAuthenticated]
class HubsUsersList(generics.ListAPIView):
    serializer_class = HubUsersSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = HubUsers.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        hub_filter = self.request.query_params.get('hub', None)
        if hub_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(hub=hub_filter)
        return queryset
class HubsUsersUpdate(generics.UpdateAPIView):
    queryset = HubUsers.objects.all()
    serializer_class = HubUsersSerializer
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
class HubsUsersDelete(generics.DestroyAPIView):
    queryset = HubUsers.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
    
class HubEmailSettingsRetrieve(generics.RetrieveAPIView):
    queryset = HubEmailSettings.objects.all()
    serializer_class = HubEmailSettingsSerializer
    lookup_field = 'hub'
    permission_classes = [IsAuthenticated]
class HubEmailSettingsCreate(generics.CreateAPIView):
    serializer_class = HubEmailSettingsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
    # Add extra value to request data
        request_data = request.data.copy()
        request_data['hub'] = self.kwargs['hub']

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class HubEmailSettingsUpdate(generics.UpdateAPIView):
    queryset = HubEmailSettings.objects.all()
    serializer_class = HubEmailSettingsSerializer
    lookup_field = 'hub'   
    permission_classes = [IsAuthenticated] 

