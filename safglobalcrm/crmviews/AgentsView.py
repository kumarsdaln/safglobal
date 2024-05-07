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
class AgentsList(generics.ListAPIView):
    queryset = Agents.objects.all()
    serializer_class = AgentsReadSerializer
    permission_classes = [IsAuthenticated]
    
class AgentsCreate(generics.CreateAPIView):
    serializer_class = AgentsSerializer
    permission_classes = [IsAuthenticated]

class AgentsUpdate(generics.UpdateAPIView):
    queryset = Agents.objects.all()
    serializer_class = AgentsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class AgentsDelete(generics.DestroyAPIView):
    queryset = Agents.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Data has been deleted."},status=status.HTTP_204_NO_CONTENT)