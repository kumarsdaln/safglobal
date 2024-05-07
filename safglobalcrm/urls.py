from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .crmviews.OfficesView import *
from .crmviews.HubsView import *
from .crmviews.AgentsView import *
from .crmviews.SuppliersView import *
from .crmviews.CustomersView import *
from .crmviews.OtherCompaniesView import *
from .crmviews.ShipmentView import *
from .crmviews.CRRView import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', views.index, name='crm.index'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', obtain_auth_token, name='crm.login'),
    path('countries/', views.CountriesList.as_view(), name='crm.counties.list'),
    path('states/', views.StatesList.as_view(), name='crm.state.list'),
    path('cities/', views.CitiesList.as_view(), name='crm.cities.list'),
    path('currencies/', views.CurrenciesList.as_view(), name='crm.currencies.list'),
    path('offices/', include([
        path('', OfficesList.as_view(), name='crm.offices.list'),
        path('create/', OfficesCreate.as_view(), name='crm.offices.create'),
        path('<int:pk>/edit/', OfficesUpdate.as_view(), name='crm.offices.edit'),
        path('<int:pk>/delete/', OfficesDelete.as_view(), name='crm.offices.delete'),
        path('users/', include([
            path('', OfficesUsersList.as_view(), name='crm.offices.users.list'),
            path('create/', OfficesUsersCreate.as_view(), name='crm.offices.users.create'),
            path('<int:pk>/edit/', OfficesUsersUpdate.as_view(), name='crm.offices.users.delete'),
            path('<int:pk>/delete/', OfficesUsersDelete.as_view(), name='crm.offices.users.edit'),
            path('<int:pk>/change-status/', OfficesUsersUpdate.as_view(), name='crm.offices.users.change-status'),
        ])),
    ])),
    path('hubs/', include([
        path('', HubsList.as_view(), name='crm.hubs.list'),
        path('create/', HubsCreate.as_view(), name='crm.hubs.create'),
        path('<int:pk>/edit/', HubsUpdate.as_view(), name='crm.hubs.edit'),
        path('<int:pk>/delete/', HubsDelete.as_view(), name='crm.hubs.delete'),
        path('users/', include([
            path('', HubsUsersList.as_view(), name='crm.hubs.users.list'),
            path('create/', HubsUsersCreate.as_view(), name='crm.hubs.users.create'),
            path('<int:pk>/edit/', HubsUsersUpdate.as_view(), name='crm.hubs.users.edit'),
            path('<int:pk>/delete/', HubsUsersDelete.as_view(), name='crm.hubs.users.delete'),
            path('<int:pk>/change-status/', HubsUsersUpdate.as_view(), name='crm.hubs.users.change-status'),
        ])),
        path('<int:hub>/email-settings/', include([
            path('', HubEmailSettingsRetrieve.as_view(), name='crm.hubs.emailsettings'),
            path('create/', HubEmailSettingsCreate.as_view(), name='crm.hubs.emailsettings.create'),
            path('edit/', HubEmailSettingsUpdate.as_view(), name='crm.hubs.emailsettings.edit'),
        ])),
    ])),
    path('agents/', include([
        path('', AgentsList.as_view(), name='crm.agents.list'),
        path('create/', AgentsCreate.as_view(), name='crm.agents.create'),
        path('<int:pk>/edit/', AgentsUpdate.as_view(), name='crm.agents.edit'),
        path('<int:pk>/delete/', AgentsDelete.as_view(), name='crm.agents.delete'),
    ])),
    path('suppliers/', include([
        path('', SuppliersList.as_view(), name='crm.suppliers.list'),
        path('create/', SuppliersCreate.as_view(), name='crm.suppliers.create'),
        path('<int:pk>/edit/', SuppliersUpdate.as_view(), name='crm.suppliers.edit'),
        path('<int:pk>/delete/', SuppliersDelete.as_view(), name='crm.suppliers.delete'),
    ])),
    path('customers/', include([
        path('', CustomersList.as_view(), name='crm.customers.list'),
        path('create/', CustomersCreate.as_view(), name='crm.customers.create'),
        path('<int:pk>/edit/', CustomersUpdate.as_view(), name='crm.customers.edit'),
        path('<int:pk>/delete/', CustomersDelete.as_view(), name='crm.customers.delete'),
        path('users/', include([
            path('', CustomersUsersList.as_view(), name='crm.customers.users.list'),
            path('create/', CustomersUsersCreate.as_view(), name='crm.customers.users.create'),
            path('<int:pk>/edit/', CustomersUsersUpdate.as_view(), name='crm.customers.users.edit'),
            path('<int:pk>/delete/', CustomersUsersDelete.as_view(), name='crm.customers.users.delete'),
            path('<int:pk>/change-status/', CustomersUsersUpdate.as_view(), name='crm.customers.users.change-status'),
        ])),
        path('vessels/', include([
            path('', CustomersVesselsList.as_view(), name='crm.customers.vessels.list'),
            path('create/', CustomersVesselsCreate.as_view(), name='crm.customers.vessels.create'),
            path('<int:pk>/edit/', CustomersVesselsUpdate.as_view(), name='crm.customers.vessels.edit'),
            path('<int:pk>/delete/', CustomersVesselsDelete.as_view(), name='crm.customers.vessels.delete'),
        ])),
    ])),
    path('other-companies/', include([
        path('', OtherCompaniesList.as_view(), name='crm.othercompanies.list'),
        path('create/', OtherCompaniesCreate.as_view(), name='crm.othercompanies.create'),
        path('<int:pk>/edit/', OtherCompaniesUpdate.as_view(), name='crm.othercompanies.edit'),
        path('<int:pk>/delete/', OtherCompaniesDelete.as_view(), name='crm.othercompanies.delete'),
    ])),
    path('shipment/', include([
        path('', ShipmentList.as_view(), name='crm.shipment.list'),
        path('create/', ShipmentCreate.as_view(), name='crm.shipment.create'),
        path('<int:pk>/edit/', ShipmentUpdate.as_view(), name='crm.shipment.edit'),
        path('<int:pk>/delete/', ShipmentDelete.as_view(), name='crm.shipment.delete'),
        path('service-details/', include([
            path('', ShipmentServiceDetailsList.as_view(), name='crm.shipment.service-details.list'),
            path('create/', ShipmentServiceDetailsCreate.as_view(), name='crm.shipment.service-details.create'),
            path('<int:pk>/edit/', ShipmentServiceDetailsUpdate.as_view(), name='crm.shipment.service-details.edit'),
            path('<int:pk>/delete/', ShipmentServiceDetailsDelete.as_view(), name='crm.shipment.service-details.delete'),
        ])),
    ])),
    path('crr/', include([
        path('', CRRList.as_view(), name='crm.crr.list'),
        path('create/', CRRCreate.as_view(), name='crm.crr.create'),
        path('<int:pk>/edit/', CRRUpdate.as_view(), name='crm.crr.edit'),
        path('<int:pk>/delete/', CRRDelete.as_view(), name='crm.crr.delete'),
        path('stock-items/', include([
            path('', CRRStockItemList.as_view(), name='crm.crr.stock-item.list'),
            path('create/', CRRStockItemCreate.as_view(), name='crm.crr.stock-item.create'),
            path('<int:pk>/edit/', CRRStockItemUpdate.as_view(), name='crm.crr.stock-item.edit'),
            path('<int:pk>/delete/', CRRStockItemDelete.as_view(), name='crm.crr.stock-item.delete'),
        ])),
        path('documents/', include([
            path('', CRRDocumentsList.as_view(), name='crm.crr.documents.list'),
            path('create/', CRRDocumentsCreate.as_view(), name='crm.crr.documents.create'),
            path('<int:pk>/edit/', CRRDocumentsUpdate.as_view(), name='crm.crr.documents.edit'),
            path('<int:pk>/delete/', CRRDocumentsDelete.as_view(), name='crm.crr.documents.delete'),
        ])),
    ])),
]