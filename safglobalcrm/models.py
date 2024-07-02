from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class Countries(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='uploads/icons/countries')
    slug = models.SlugField()

    def __str__(self) -> str:
        return f"{self.name}"

class States(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"

class Cities(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    state = models.ForeignKey(States, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"

class Currencies(models.Model):
    name = models.CharField(max_length=100)
    sign = models.CharField(max_length=5)   

    def __str__(self) -> str:
        return f"{self.name}"

class Offices(models.Model):
    name = models.CharField(max_length=150)
    company_id = models.CharField(max_length=20)
    short_name = models.CharField(max_length=10)
    customer_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    eori_number = models.CharField(max_length=20) 
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.name}"

class OfficeUsers(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    activated = models.BooleanField(default=1)
    office = models.ForeignKey(Offices, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"

class Hubs(models.Model):
    name = models.CharField(max_length=100)
    company_id = models.CharField(max_length=20)
    customer_number = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    code_description = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    remarks = models.TextField()
    is_gst = models.BooleanField()
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    eori_number = models.CharField(max_length=20, null=True)
    un_lo_code = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

class HubEmails(models.Model):
    email = models.EmailField()
    hub = models.ForeignKey(Hubs, related_name='emails', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.hub.name} - Emails"

class HubAdditionalOfficeAddress(models.Model):
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    hub = models.ForeignKey(Hubs, related_name='additionalAddresses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.hub.name} - Additional Address"

class HubUsers(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    activated = models.BooleanField(default=1)
    hub = models.ForeignKey(Hubs, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.hub.name} - Users"

class HubEmailSettings(models.Model):
    airfreight_import_email = models.EmailField()
    airfreight_export_email = models.EmailField()
    courier_export_email = models.EmailField()
    courier_import_email = models.EmailField()
    onboard_delivery_import_email = models.EmailField()
    onboard_delivery_export_email = models.EmailField()
    release_import_email = models.EmailField()
    release_export_email = models.EmailField()
    seafreight_import_email = models.EmailField()
    seafreight_export_email = models.EmailField()
    truck_import_email = models.EmailField()
    truck_export_email = models.EmailField()
    hub = models.OneToOneField(Hubs, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.hub.name} - Email Settings"

class Agents(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    code_description = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    remarks = models.TextField()
    special_consideration = models.TextField()
    show_pre_alert = models.BooleanField()
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    port_code = models.CharField(max_length=10)
    vat_number = models.CharField(max_length=20)
    eori_number = models.CharField(max_length=20)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    un_lo_code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.name}"

class AgentEmails(models.Model):
    email = models.EmailField()
    agent = models.ForeignKey(Agents, related_name='emails', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.agent.name} - Emails"

class AgentAdditionalOfficeAddress(models.Model):
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    agent = models.ForeignKey(Agents, related_name='additionalAddresses', on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.agent.name} - Additional Address"   

class Suppliers(models.Model):
    name = models.CharField(max_length=100)
    company_id = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    remarks = models.TextField()
    special_consideration = models.TextField()
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    port_code = models.CharField(max_length=10)
    vat_number = models.CharField(max_length=20)
    eori_number = models.CharField(max_length=20)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    un_lo_code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.name}"

class SupplierEmails(models.Model):
    email = models.EmailField()
    supplier = models.ForeignKey(Suppliers, related_name='emails', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.supplier.name} - Emails"

class SupplierAdditionalOfficeAddress(models.Model):
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    supplier = models.ForeignKey(Suppliers, related_name='additionalAddresses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.supplier.name} - Additional Address"

class Customers(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    notify_email = models.EmailField()
    remarks = models.TextField()
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    port_code = models.CharField(max_length=10)
    main_account_manager = models.ForeignKey(OfficeUsers, on_delete=models.CASCADE, related_name='main_account_manager')
    all_account_manager = models.ForeignKey(OfficeUsers, on_delete=models.CASCADE, related_name='all_account_manager')
    responsible_office = models.ForeignKey(Offices, on_delete=models.CASCADE)
    customer_logo = models.ImageField(upload_to='uploads/logo/customers')
    display_logo_address_on_menifest = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name}"

class CustomerEmails(models.Model):
    email = models.EmailField()
    customer = models.ForeignKey(Customers, related_name='emails', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.customer.name} - Emails"

class CustomerPostalAddress(models.Model):
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    customer = models.ForeignKey(Customers, related_name='additionalAddresses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.customer.name} - Postal Address"

class CustomerVessels(models.Model):
    name = models.CharField(max_length=100)
    vessel_code = models.CharField(max_length=20)
    imo = models.CharField(max_length=100)
    inactive_vessel = models.BooleanField()
    in_transit = models.BooleanField()
    vessal_type = models.CharField(max_length=100)
    fleet_category = models.CharField(max_length=100)
    registered_in_country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    internal_shipment = models.CharField(max_length=100)
    expect_from_hubs =  models.CharField(max_length=100)
    remarks = models.TextField()
    manager_from_customer = models.CharField(max_length=100)
    account_manager = models.CharField(max_length=100)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.customer.name} - Vessels"

class CustomerUsers(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    activated = models.BooleanField(default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.customer.name} - Users"

class OtherCompanies(models.Model):
    name = models.CharField(max_length=100)
    office_name = models.CharField(max_length=100) 
    code = models.CharField(max_length=10)
    code_description = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    remarks = models.TextField()
    special_consideration = models.TextField()
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    port_code = models.CharField(max_length=10)
    vat_number = models.CharField(max_length=20)
    eori_number = models.CharField(max_length=20)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    un_lo_code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.name}"

class OtherCompanyEmails(models.Model):
    email = models.EmailField()
    other_company = models.ForeignKey(OtherCompanies, related_name='emails', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.other_company.name} - Emails"

class OtherCompaniesAdditionalOfficeAddress(models.Model):
    address = models.TextField()
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    other_company = models.ForeignKey(OtherCompanies, related_name='additionalAddresses', on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.other_company.name} - Addtional Address"  
    
class ShipmentDeparture(models.Model):
    departure_from_hub = models.ForeignKey(Hubs, on_delete=models.CASCADE, null=True, blank=True)
    departure_from_office = models.ForeignKey(Offices, on_delete=models.CASCADE, null=True, blank=True)
    departure_from_agent = models.ForeignKey(Agents, on_delete=models.CASCADE, null=True, blank=True)

class ShipmentConsignee(models.Model):
    consignee_from_hub = models.ForeignKey(Hubs, on_delete=models.CASCADE, null=True, blank=True)
    consignee_from_office = models.ForeignKey(Offices, on_delete=models.CASCADE, null=True, blank=True)
    consignee_from_agent = models.ForeignKey(Agents, on_delete=models.CASCADE, null=True, blank=True)

class Shipment(models.Model):
    SHIPMENT_STATUS_CHOICES = {
    "P": "In Progress",
    "T": "In Transit",
    "D": "Delivered",
    }
    SHIPMENT_CHOICES = {
    "H": "Hub",
    "O": "Office",
    "A": "Agent",
    }
    SERVICE_CHOICES = {
        "A":"Air",
        "S":"Sea",
        "T":"Truck",
        "C":"Coriers",
        "R":"Release",
        "O":"On Board"
    }
    departure_in = models.CharField(max_length=2, choices=SHIPMENT_CHOICES)
    departure = models.ForeignKey(ShipmentDeparture, on_delete=models.CASCADE)
    port_code = models.CharField(max_length=100)
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)
    preferred_shipment_date = models.DateField()
    deadline_arrival_date = models.DateField()
    vessel_eta = models.DateField()
    vessel_etd = models.DateField()
    pre_alert_reminder = models.DateField()
    customer_reference = models.CharField(max_length=100)
    consignee_in = models.CharField(max_length=2, choices=SHIPMENT_CHOICES)
    consignee = models.ForeignKey(ShipmentConsignee, on_delete=models.CASCADE)
    consignee_address = models.TextField()
    consignee_country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    consignee_state = models.ForeignKey(States, on_delete=models.CASCADE)
    consignee_city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    consignee_zip_code = models.CharField(max_length=10)
    att = models.CharField(max_length=100)
    consignee_email = models.EmailField()
    account_manager = models.CharField(max_length=100)
    special_consideration = models.TextField()
    dont_show_on_shipping_instruction = models.BooleanField()
    comment_to_departure_hub = models.TextField()
    comment_to_consignee = models.TextField()
    dont_show_on_pre_alert = models.BooleanField()
    project_logistic_shipment = models.BooleanField()
    shipment_status = models.CharField(max_length=10, choices=SHIPMENT_STATUS_CHOICES)
    mark_as_arrived = models.BooleanField(default=0)

class Air(models.Model):
    airway_bill = models.CharField(max_length=100)
    flt_no = models.CharField(max_length=100)
    dep_dt = models.CharField(max_length=100)
    arr_dt = models.CharField(max_length=100)
class Sea(models.Model):
    landing_bill = models.CharField(max_length=100)
    Vessel_voy = models.CharField(max_length=100)
    etd = models.CharField(max_length=100)
    eta = models.CharField(max_length=100)
class Truck(models.Model):
    cmr = models.CharField(max_length=100)
    freight_company = models.CharField(max_length=100)
    dep_dt = models.CharField(max_length=100)
    arr_dt = models.CharField(max_length=100)
class Coriers(models.Model):
    waybill = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100)
    dep_dt = models.CharField(max_length=100)
    arr_dt = models.CharField(max_length=100)
class Release(models.Model):
    freight_company = models.CharField(max_length=100)
    dep_dt = models.CharField(max_length=100)
class OnBoard(models.Model):
    dep_dt = models.CharField(max_length=100)

class ShipmentServiceDetails(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    air = models.ForeignKey(Air, on_delete=models.SET_NULL, null=True)
    sea = models.ForeignKey(Sea, on_delete=models.SET_NULL, null=True)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True)
    coriers = models.ForeignKey(Coriers, on_delete=models.SET_NULL, null=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, null=True)
    on_board = models.ForeignKey(OnBoard, on_delete=models.SET_NULL, null=True)
    
class CRR(models.Model):
    STATUS_CHOICES = {
    "P": "Pending",
    "D": "Delivered",
    "O": "On Call",
    }
    vessel = models.ForeignKey(CustomerVessels, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=20)
    po_remarks = models.TextField()
    content = models.TextField()
    content_description = models.TextField()
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    expected_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True)
    supplier_reference = models.TextField()
    deadline_warehouse = models.DateField()
    internal_shipment = models.TextField()
    delivery_irregulations = models.TextField()
    hub = models.ForeignKey(Hubs, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    transit_id = models.CharField(max_length=20)
    t1_reference = models.CharField(max_length=150)
    ex_a = models.CharField(max_length=150)
    country = models.ForeignKey(Countries, on_delete=models.RESTRICT)
    hs_code = models.CharField(max_length=150)
    currency = models.ForeignKey(Currencies, on_delete=models.RESTRICT)
    customs_value = models.TextField()
    priorty = models.TextField()
    customs_value_usd = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    accept = models.BooleanField(default=False)

class CRRStockItem(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    cbm = models.CharField(max_length=100)
    warhouse_location = models.TextField()
    dgr = models.BooleanField(default=False)
    not_stack = models.BooleanField(default=False)
    medicine = models.BooleanField(default=False)
    x_ray = models.BooleanField(default=False)
    crr = models.ForeignKey(CRR, on_delete=models.CASCADE)

class CRRDocuments(models.Model):
    document = models.FileField(upload_to='uploads/crr/documents') 
    crr = models.ForeignKey(CRR, on_delete=models.CASCADE)
       

