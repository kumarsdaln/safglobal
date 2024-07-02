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
class ShipmentList(generics.ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentReadSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Shipment.objects.all()

        # Retrieve query parameters for filtering, for instance, 'name'
        search = self.request.query_params.get('search', None)
        sortby = self.request.query_params.get('sortby', 'id')
        sortdirection = self.request.query_params.get('sortdirection', 'asc')

        if sortdirection == 'desc':
            sortby = '-' + sortby
        
        if search is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(Q(name__icontains=search) | Q(company_id__icontains=search) | Q(customer_number__icontains=search))
        queryset = queryset.order_by(sortby)    
        return queryset
    
class ShipmentCreate(generics.CreateAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]


class ShipmentUpdate(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class ShipmentDelete(generics.DestroyAPIView):
    queryset = Shipment.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        ShipmentConsignee.objects.get(pk=instance.consignee.id).delete()
        ShipmentDeparture.objects.get(pk=instance.departure.id).delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
    
#Shipment Service Details
class ShipmentServiceDetailsList(generics.ListAPIView):
    queryset = ShipmentServiceDetails.objects.all()
    serializer_class = ShipmentServiceDetailsSerializer
    permission_classes = [IsAuthenticated]

class ShipmentServiceDetailsCreate(generics.CreateAPIView):
    serializer_class = ShipmentServiceDetailsSerializer
    permission_classes = [IsAuthenticated] 

class ShipmentServiceDetailsUpdate(generics.UpdateAPIView):
    queryset = ShipmentServiceDetails.objects.all()
    serializer_class = ShipmentServiceDetailsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class ShipmentServiceDetailsDelete(generics.DestroyAPIView):
    queryset = ShipmentServiceDetails.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        if instance.air:
            Air.objects.get(pk=instance.air.id).delete()
        if instance.sea:
            Air.objects.get(pk=instance.sea.id).delete()
        if instance.truck:
            Air.objects.get(pk=instance.truck.id).delete()
        if instance.coriers:
            Air.objects.get(pk=instance.coriers.id).delete()
        if instance.release:
            Air.objects.get(pk=instance.release.id).delete()
        if instance.on_board:
            Air.objects.get(pk=instance.on_board.id).delete()    
        # ShipmentConsignee.objects.get(pk=instance.consignee.id).delete()
        # ShipmentDeparture.objects.get(pk=instance.departure.id).delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
