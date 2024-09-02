from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([Countries,States,Cities,Currencies, 
                     Offices,OfficeUsers, 
                     Hubs,HubEmails,HubAdditionalOfficeAddress,HubUsers,HubEmailSettings,
                     Agents,AgentEmails,AgentAdditionalOfficeAddress,
                     Suppliers,SupplierEmails,SupplierAdditionalOfficeAddress,
                     Customers,CustomerEmails,CustomerPostalAddress,CustomerVessels,CustomerUsers,
                     OtherCompanies,OtherCompanyEmails,OtherCompaniesAdditionalOfficeAddress,
                     ShipmentDeparture,ShipmentConsignee,Shipment,ShipmentServiceDetails,Air,Sea,Truck,Coriers,Release,OnBoard])