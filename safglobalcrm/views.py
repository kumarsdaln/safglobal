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
from django.urls import get_resolver, URLPattern, URLResolver

# Create your views here.
def index(request):
    urls = []

    def collect_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if isinstance(pattern, URLResolver):
                collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                urls.append(prefix + str(pattern.pattern))

    resolver = get_resolver()
    collect_urls(resolver.url_patterns)
    # return urls
    # url_patterns = []
    # resolver = get_resolver()
    # for url_pattern in resolver.url_patterns:
    #     print(url_pattern.pattern)
    #     url_patterns.append(url_pattern.pattern)
    return render(request, "safglobalcrm/index.html", {"url_patterns": urls})

# Create your views here.
class CountriesList(generics.ListAPIView):
    pagination_class = None
    queryset = Countries.objects.all()
    serializer_class = CountriesSerializer
    permission_classes = [IsAuthenticated]
class StatesList(generics.ListAPIView):
    pagination_class = None
    serializer_class = StatesSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = States.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        country_filter = self.request.query_params.get('country', None)
        if country_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(country=country_filter)
        return queryset
class CitiesList(generics.ListAPIView):
    pagination_class = None
    serializer_class = CitiesSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Cities.objects.all()
        # Retrieve query parameters for filtering, for instance, 'name'
        state_filter = self.request.query_params.get('state', None)
        if state_filter is not None:
            # Apply filtering based on the 'name' parameter
            queryset = queryset.filter(state=state_filter)
        return queryset
class CurrenciesList(generics.ListAPIView):
    pagination_class = None
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [IsAuthenticated]

