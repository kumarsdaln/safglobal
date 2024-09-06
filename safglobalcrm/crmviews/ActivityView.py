from rest_framework import generics
from rest_framework.filters import OrderingFilter
from safglobalcrm.models import Activity, CRRStockItem, CRRDocuments
from safglobalcrm.serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated

class ActivityList(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Activity.objects.all()

        # Retrieve query parameters
        model = self.request.query_params.get('model', None)
        object_id = self.request.query_params.get('object_id', None)  # Keep object_id as string for safety
        
        # Make sure object_id is not None and is valid
        if model == "CRR" and object_id:
            try:
                object_id = int(object_id)

                # Get activities for the CRR object
                crr_activities = queryset.filter(model_name="CRR", object_id=object_id)

                # Fetch related stock items and documents
                related_stock_items = CRRStockItem.objects.filter(crr__id=object_id) if object_id else None
                related_documents = CRRDocuments.objects.filter(crr__id=object_id) if object_id else None

                # If there are related stock items, get their activities
                if related_stock_items and related_stock_items.exists():
                    stock_item_activities = queryset.filter(
                        model_name="CRRStockItem", 
                        object_id__in=related_stock_items.values_list('id', flat=True)
                    )
                else:
                    stock_item_activities = Activity.objects.none()

                # If there are related documents, get their activities
                if related_documents and related_documents.exists():
                    document_activities = queryset.filter(
                        model_name="CRRDocuments",
                        object_id__in=related_documents.values_list('id', flat=True)
                    )
                else:
                    document_activities = Activity.objects.none()

                # Combine all activities (CRR, CRRStockItem, CRRDocuments)
                queryset = crr_activities | stock_item_activities | document_activities
                queryset = queryset.order_by('-timestamp')
            except ValueError:
                pass  # Handle invalid object_id if needed
        return queryset
