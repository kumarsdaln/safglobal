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
class CRRList(generics.ListAPIView):
    serializer_class = CRRReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CRR.objects.all()

        # Retrieve query parameters for filtering, for instance, 'name'
        accept = self.request.query_params.get('accept', 0)
        search = self.request.query_params.get('search', None)
        sortby = self.request.query_params.get('sortby', 'id')
        sortdirection = self.request.query_params.get('sortdirection', 'asc')

        if sortdirection == 'desc':
            sortby = '-' + sortby
        
        if search is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(Q(name__icontains=search) | Q(company_id__icontains=search) | Q(customer_number__icontains=search))
        queryset = queryset.filter(accept=accept)    
        queryset = queryset.order_by(sortby)    
        return queryset
    
class CRRCreate(generics.CreateAPIView):
    serializer_class = CRRSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        register_by = self.request.user
        serializer.save(register_by=register_by)

class CRRDetails(generics.RetrieveAPIView):
    serializer_class = CRRReadSerializer
    permission_classes = [IsAuthenticated]
    queryset = CRR.objects.all()

class CRRUpdate(generics.UpdateAPIView):
    queryset = CRR.objects.all()
    serializer_class = CRRSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class CRRDelete(generics.DestroyAPIView):
    queryset = CRR.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
    
#Shipment Service Details
class CRRStockItemList(generics.ListAPIView):
    pagination_class = None
    serializer_class = CRRStockItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = CRRStockItem.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        crr_filter = self.request.query_params.get('crr', None)
        if crr_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(crr=crr_filter)
        return queryset
class CRRStockItemCreate(generics.CreateAPIView):
    serializer_class = CRRStockItemSerializer
    permission_classes = [IsAuthenticated] 

class CRRStockItemUpdate(generics.UpdateAPIView):
    queryset = CRRStockItem.objects.all()
    serializer_class = CRRStockItemSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class CRRStockItemDelete(generics.DestroyAPIView):
    queryset = CRRStockItem.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
    

#Shipment Service Details
class CRRDocumentsList(generics.ListAPIView):
    pagination_class = None
    serializer_class = CRRDocumentsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = CRRDocuments.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        crr_filter = self.request.query_params.get('crr', None)
        if crr_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(crr=crr_filter)
        return queryset

class CRRDocumentsCreate(generics.CreateAPIView):
    serializer_class = CRRDocumentsSerializer
    permission_classes = [IsAuthenticated] 

class CRRDocumentsUpdate(generics.UpdateAPIView):
    queryset = CRRDocuments.objects.all()
    serializer_class = CRRDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class CRRDocumentsDelete(generics.DestroyAPIView):
    queryset = CRRDocuments.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)
