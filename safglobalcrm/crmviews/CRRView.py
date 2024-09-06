from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from safglobalcrm.models import *
from safglobalcrm.serializers import *
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.forms.models import model_to_dict
import json
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
        instance = serializer.save(register_by=register_by)
        if instance.hub:
            stock_number = f"{instance.hub.code}-{instance.pk}"
        elif instance.agent:  
            stock_number = f"{instance.agent.code}-{instance.pk}"
        changes = {"stock_number":stock_number}
        Activity.objects.create(
            user=register_by,
            action='ADD',
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            changes=changes
        )

class CRRDetails(generics.RetrieveAPIView):
    serializer_class = CRRReadSerializer
    permission_classes = [IsAuthenticated]
    queryset = CRR.objects.all()

class CRRUpdate(generics.UpdateAPIView):
    queryset = CRR.objects.all()
    serializer_class = CRRSerializer
    permission_classes = [IsAuthenticated]
    def get_instance_data(self, instance):
        """
        Retrieve the original data for comparison.
        """
        data = {}
        for field in instance._meta.fields:
            field_name = field.name
            value = getattr(instance, field_name)
            # Handle special cases for ForeignKey and JSONField
            if isinstance(field, models.ForeignKey):
                value = value.pk if value else None
            elif isinstance(field, models.JSONField):
                value = json.dumps(value, default=str) if value else None
            data[field_name] = value
        return data
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes=changes
        )
        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes=changes
        )

        return Response(serializer.data)
    
    def get_changes(self, old_data, new_data):
        """
        Compare old and new data dictionaries to detect changes.
        """
        changes = {}
        for field_name in old_data:
            old_value = old_data.get(field_name)
            new_value = new_data.get(field_name)
            if old_value != new_value:
                changes[field_name] = {
                    "old_value": old_value,
                    "new_value": new_value
                }
        return changes
    
class CRRDelete(generics.DestroyAPIView):
    queryset = CRR.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.hub:
            stock_number = instance.hub.code
        elif instance.agnet:  
            stock_number = instance.agent.code
        changes = {"stock_number":stock_number}
        # Log the delete activity before deletion
        Activity.objects.create(
            user=request.user,
            action='DELETE',
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            changes=changes
        )
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
    def perform_create(self, serializer):
        new_instance = serializer.save()
        changes = json.dumps(model_to_dict(new_instance))
        Activity.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name=new_instance.__class__.__name__,
            object_id=new_instance.pk,
            changes=changes
        )

class CRRStockItemUpdate(generics.UpdateAPIView):
    queryset = CRRStockItem.objects.all()
    serializer_class = CRRStockItemSerializer
    permission_classes = [IsAuthenticated]

    def get_instance_data(self, instance):
        """
        Retrieve the original data for comparison.
        """
        data = {}
        for field in instance._meta.fields:
            field_name = field.name
            value = getattr(instance, field_name)
            # Handle special cases for ForeignKey and JSONField
            if isinstance(field, models.ForeignKey):
                value = value.pk if value else None
            elif isinstance(field, models.JSONField):
                value = json.dumps(value, default=str) if value else None
            data[field_name] = value
        return data

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        # Log the update activity
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes = changes
        )
        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes=changes
        )
    def get_changes(self, old_data, new_data):
        """
        Compare old and new data dictionaries to detect changes.
        """
        changes = {}
        for field_name in old_data:
            old_value = old_data.get(field_name)
            new_value = new_data.get(field_name)
            if old_value != new_value:
                changes[field_name] = {
                    "old_value": old_value,
                    "new_value": new_value
                }
        return changes
    
class CRRStockItemDelete(generics.DestroyAPIView):
    queryset = CRRStockItem.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        changes = json.dumps(model_to_dict(instance))
        # Log the delete activity before deletion
        Activity.objects.create(
            user=request.user,
            action='DELETE',
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            changes = changes
        )
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
    def perform_create(self, serializer):
        # Save the new instance
        new_instance = serializer.save()
        
        # Convert the new instance to a dictionary
        instance_dict = model_to_dict(new_instance)
        
        # Manually convert file fields to their URLs
        for field in new_instance._meta.get_fields():
            if field.get_internal_type() == 'FileField':
                field_name = field.name
                if getattr(new_instance, field_name):
                    instance_dict[field_name] = getattr(new_instance, field_name).url
        
        # Convert dictionary to JSON
        changes = json.dumps(instance_dict, cls=DjangoJSONEncoder)
        
        # Log the create activity
        Activity.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name=new_instance.__class__.__name__,
            object_id=new_instance.pk,
            changes=changes
        )

class CRRDocumentsUpdate(generics.UpdateAPIView):
    queryset = CRRDocuments.objects.all()
    serializer_class = CRRDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def get_instance_data(self, instance):
        """
        Retrieve the original data for comparison.
        """
        data = {}
        for field in instance._meta.fields:
            field_name = field.name
            value = getattr(instance, field_name)
            # Handle special cases for ForeignKey and JSONField
            if isinstance(field, models.ForeignKey):
                value = value.pk if value else None
            elif isinstance(field, models.JSONField):
                value = json.dumps(value, default=str) if value else None
            elif isinstance(field, models.FileField):
                value = value.url if value else None
            data[field_name] = value
        return data
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
         # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        # Log the update activity
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes=changes
        )
        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Capture old data
        old_instance_data = self.get_instance_data(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
         # Capture new data
        new_instance_data = self.get_instance_data(updated_instance)
        # Log the update activity
        changes = self.get_changes(old_instance_data, new_instance_data)
        # Log the update activity
        Activity.objects.create(
            user=request.user,
            action='EDIT',
            model_name=updated_instance.__class__.__name__,
            object_id=updated_instance.pk,
            changes=changes
        )
        return Response(serializer.data)
    def get_changes(self, old_data, new_data):
        """
        Compare old and new data dictionaries to detect changes.
        """
        changes = {}
        for field_name in old_data:
            old_value = old_data.get(field_name)
            new_value = new_data.get(field_name)
            if old_value != new_value:
                changes[field_name] = {
                    "old_value": old_value,
                    "new_value": new_value
                }
        return changes
class CRRDocumentsDelete(generics.DestroyAPIView):
    queryset = CRRDocuments.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Convert the instance to a dictionary
        instance_dict = model_to_dict(instance)
        
        # Manually convert file fields to their URLs
        for field in instance._meta.get_fields():
            if field.get_internal_type() == 'FileField':
                field_name = field.name
                if getattr(instance, field_name):
                    instance_dict[field_name] = getattr(instance, field_name).url
        
        # Convert dictionary to JSON
        changes = json.dumps(instance_dict, cls=DjangoJSONEncoder)
        
        # Log the delete activity
        Activity.objects.create(
            user=request.user,
            action='DELETE',
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            changes=changes
        )
        
        # Delete the instance
        instance.delete()
        
        return Response({"message": "Data has been deleted."}, status=status.HTTP_204_NO_CONTENT)