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
        dont_show_on_pre_alert = self.request.query_params.get('dont_show_on_pre_alert', None)
        mark_as_arrived = self.request.query_params.get('mark_as_arrived', None)
        search = self.request.query_params.get('search', None)
        sortby = self.request.query_params.get('sortby', 'id')
        sortdirection = self.request.query_params.get('sortdirection', 'desc')

        if sortdirection == 'desc':
            sortby = '-' + sortby
        
        if search is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(Q(name__icontains=search) | Q(company_id__icontains=search) | Q(customer_number__icontains=search))
        if dont_show_on_pre_alert is not None:
            queryset = queryset.filter(dont_show_on_pre_alert=dont_show_on_pre_alert)     
        if mark_as_arrived is not None:
            queryset = queryset.filter(mark_as_arrived=mark_as_arrived)  
        queryset = queryset.order_by(sortby)    
        return queryset
    
class ShipmentCreate(generics.CreateAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        shipment = serializer.save()
        crr_ids = json.loads(self.request.data.get('stock_items', []))  # Get tag IDs from request data
        stock_items = CRR.objects.filter(id__in=crr_ids)
        shipment.stock_items.set(stock_items)  # Add tags to the article

class ShipmentDetails(generics.RetrieveAPIView):
    serializer_class = ShipmentReadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Shipment.objects.all()

class ShipmentUpdate(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        shipment = serializer.save()

        # Update stock items
        crr_ids = json.loads(request.data.get('stock_items', '[]'))
        service = request.data.get('service', None)
        print(service)
        if service is not None:
            if service == 'A':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(air__isnull=False).delete()
            elif service == 'S':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(sea__isnull=False).delete()
            elif service == 'T':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(truck__isnull=False).delete()
            elif service == 'C':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(coriers__isnull=False).delete()
            elif service == 'R':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(release__isnull=False).delete()
            elif service == 'O':
                ShipmentServiceDetails.objects.filter(shipment=shipment).exclude(on_board__isnull=False).delete()
        stock_items = CRR.objects.filter(id__in=crr_ids)
        shipment.stock_items.set(stock_items)

        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        shipment = serializer.save()
        crr_ids = json.loads(self.request.data.get('stock_items', []))  # Get tag IDs from request data\
        print(crr_ids)
        stock_items = CRR.objects.filter(id__in=crr_ids)
        shipment.stock_items.set(stock_items)
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
    pagination_class = None
    queryset = ShipmentServiceDetails.objects.all()
    serializer_class = ShipmentServiceDetailsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = ShipmentServiceDetails.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        shipment_filter = self.request.query_params.get('shipment', None)
        if shipment_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(shipment=shipment_filter)
        return queryset

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
