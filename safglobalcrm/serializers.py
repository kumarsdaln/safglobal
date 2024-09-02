from rest_framework import serializers
from .models import *
from django.urls import reverse
import json
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"

class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = "__all__"

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"

class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = "__all__"

#Offices
class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offices
        fields = "__all__"
class OfficeReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = Offices
        fields = "__all__"
class OfficeUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeUsers
        fields = "__all__"        

#Hubs  
class HubEmailsSerializeer(serializers.ModelSerializer):
    class Meta:
        model = HubEmails
        fields = "__all__"
class HubAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    class Meta:
        model = HubAdditionalOfficeAddress
        fields = "__all__" 
class HubReadAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = HubAdditionalOfficeAddress
        fields = "__all__"        
class HubsSerializer(serializers.ModelSerializer):
    emails = HubEmailsSerializeer(many=True, required=False)
    additionalAddresses = HubAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Hubs
        fields = '__all__' 
    def validate(self, data):
        request = self.context['request']
        if request.data.get('emails'):
            emails = request.data.get('emails')
            data['emails'] = json.loads(emails)
                
        if request.data.get('additionalAddresses'):
            additionalAddresses = request.data.get('additionalAddresses')
            print(additionalAddresses)
            data['additionalAddresses'] = json.loads(additionalAddresses)
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data          

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            hub = Hubs.objects.create(**validated_data)

            for email_data in emails_data:
                HubEmails.objects.create(hub=hub, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    HubAdditionalOfficeAddress.objects.create(hub=hub, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")

        return hub   
    
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            if instance.emails.all():
               instance.emails.all().delete()
            if instance.additionalAddresses.all():
               instance.additionalAddresses.all().delete()
            for email_data in emails_data:
                HubEmails.objects.create(hub=instance, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    HubAdditionalOfficeAddress.objects.create(hub=instance, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()   
        return instance   
      
class HubsReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    emails = HubEmailsSerializeer(many=True, required=False)
    additionalAddresses = HubReadAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Hubs
        fields = '__all__' 
class HubUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubUsers
        fields = '__all__' 
    
class HubEmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubEmailSettings    
        fields = '__all__'

#Agents
class AgentEmailsSerializeer(serializers.ModelSerializer):
    class Meta:
        model = AgentEmails
        fields = "__all__"
class AgentAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    class Meta:
        model = AgentAdditionalOfficeAddress
        fields = "__all__"        
class AgentReadAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = AgentAdditionalOfficeAddress
        fields = "__all__"          
class AgentsSerializer(serializers.ModelSerializer):
    emails = AgentEmailsSerializeer(many=True, required=False)
    additionalAddresses = AgentAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Agents
        fields = '__all__' 

    def validate(self, data):
        request = self.context['request']
        if request.data.get('emails'):
            emails = request.data.get('emails')
            data['emails'] = json.loads(emails)
                
        if request.data.get('additionalAddresses'):
            additionalAddresses = request.data.get('additionalAddresses')
            data['additionalAddresses'] = json.loads(additionalAddresses)
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data          

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            agent = Agents.objects.create(**validated_data)

            for email_data in emails_data:
                AgentEmails.objects.create(agent=agent, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    AgentAdditionalOfficeAddress.objects.create(agent=agent, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")

        return agent   
    
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            if instance.emails.all():
               instance.emails.all().delete()
            if instance.additionalAddresses.all():
               instance.additionalAddresses.all().delete()
            for email_data in emails_data:
                AgentEmails.objects.create(agent=instance, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    AgentAdditionalOfficeAddress.objects.create(agent=instance, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()   
        return instance   
    
class AgentsReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    emails = AgentEmailsSerializeer(many=True, required=False)
    additionalAddresses = AgentReadAdditionalOfficeAddressSerializeer(many=True, required=False)
    currency = CurrenciesSerializer(read_only = True)
    class Meta:
        model = Agents
        fields = '__all__' 

#Suppliers
class SupplierEmailsSerializeer(serializers.ModelSerializer):
    class Meta:
        model = SupplierEmails
        fields = "__all__"
class SupplierAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    class Meta:
        model = SupplierAdditionalOfficeAddress
        fields = "__all__"   
class SupplierReadAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = SupplierAdditionalOfficeAddress
        fields = "__all__"                   
class SuppliersSerializer(serializers.ModelSerializer):
    emails = SupplierEmailsSerializeer(many=True, required=False)
    additionalAddresses = SupplierAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Suppliers
        fields = '__all__' 

    def validate(self, data):
        request = self.context['request']
        if request.data.get('emails'):
            emails = request.data.get('emails')
            data['emails'] = json.loads(emails)
                
        if request.data.get('additionalAddresses'):
            additionalAddresses = request.data.get('additionalAddresses')
            data['additionalAddresses'] = json.loads(additionalAddresses)
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data          

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            supplier = Suppliers.objects.create(**validated_data)

            for email_data in emails_data:
                SupplierEmails.objects.create(supplier=supplier, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    SupplierAdditionalOfficeAddress.objects.create(supplier=supplier, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")

        return supplier   
    
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            if instance.emails.all():
               instance.emails.all().delete()
            if instance.additionalAddresses.all():
               instance.additionalAddresses.all().delete()
            for email_data in emails_data:
                SupplierEmails.objects.create(supplier=instance, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    SupplierAdditionalOfficeAddress.objects.create(supplier=instance, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()   
        return instance   

class SuppliersReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    currency = CurrenciesSerializer(read_only=True)
    emails = SupplierEmailsSerializeer(many=True, required=False)
    additionalAddresses = SupplierReadAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Suppliers
        fields = '__all__' 

#Customers
class CustomerEmailsSerializeer(serializers.ModelSerializer):
    class Meta:
        model = CustomerEmails
        fields = "__all__"
class CustomerAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPostalAddress
        fields = "__all__"        

class CustomerReadAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = CustomerPostalAddress
        fields = "__all__"  
class CustomersSerializer(serializers.ModelSerializer):
    emails = CustomerEmailsSerializeer(many=True, required=False)
    additionalAddresses = CustomerAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Customers
        fields = '__all__' 

    def validate(self, data):
        request = self.context['request']
        if request.data.get('emails'):
            emails = request.data.get('emails')
            data['emails'] = json.loads(emails)
                
        if request.data.get('additionalAddresses'):
            additionalAddresses = request.data.get('additionalAddresses')
            data['additionalAddresses'] = json.loads(additionalAddresses)
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data          

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            customer = Customers.objects.create(**validated_data)

            for email_data in emails_data:
                CustomerEmails.objects.create(customer=customer, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    CustomerPostalAddress.objects.create(customer=customer, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")

        return customer
    
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            if instance.emails.all():
               instance.emails.all().delete()
            if instance.additionalAddresses.all():
               instance.additionalAddresses.all().delete()
            for email_data in emails_data:
                CustomerEmails.objects.create(customer=instance, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    CustomerPostalAddress.objects.create(customer=instance, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()   
        return instance   

class CustomersReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    responsible_office = OfficeReadSerializer(read_only=True)
    main_account_manager = OfficeUsersSerializer(read_only=True)
    all_account_manager = OfficeUsersSerializer(read_only=True)
    emails = CustomerEmailsSerializeer(many=True, required=False)
    additionalAddresses = CustomerReadAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = Customers
        fields = '__all__' 

class CustomerUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUsers
        fields = '__all__'            
        
class CustomerVesselsReadSerializer(serializers.ModelSerializer):
    account_manager = CustomerUsersSerializer(many=True, required=False)
    registered_in_country = CountriesSerializer(read_only=True)
    manager_from_customer = CustomerUsersSerializer(read_only=True)
    
    class Meta:
        model = CustomerVessels
        fields = '__all__'
class CustomerVesselsSerializer(serializers.ModelSerializer):
    account_manager = CustomerUsersSerializer(many=True, required=False)

    class Meta:
        model = CustomerVessels
        fields = '__all__'

#Other Companies 
class OtherCompanyEmailsSerializeer(serializers.ModelSerializer):
    class Meta:
        model = OtherCompanyEmails
        fields = "__all__"
class OtherCompaniesAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    class Meta:
        model = OtherCompaniesAdditionalOfficeAddress
        fields = "__all__"     
class OtherCompaniesReadAdditionalOfficeAddressSerializeer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    class Meta:
        model = OtherCompaniesAdditionalOfficeAddress
        fields = "__all__"    
class OtherCompaniesSerializer(serializers.ModelSerializer):
    emails = OtherCompanyEmailsSerializeer(many=True, required=False)
    additionalAddresses = OtherCompaniesAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = OtherCompanies
        fields = '__all__' 

    def validate(self, data):
        request = self.context['request']
        if request.data.get('emails'):
            emails = request.data.get('emails')
            data['emails'] = json.loads(emails)
                
        if request.data.get('additionalAddresses'):
            additionalAddresses = request.data.get('additionalAddresses')
            data['additionalAddresses'] = json.loads(additionalAddresses)
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data          

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            other_company = OtherCompanies.objects.create(**validated_data)

            for email_data in emails_data:
                OtherCompanyEmails.objects.create(other_company=other_company, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    OtherCompaniesAdditionalOfficeAddress.objects.create(other_company=other_company, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")

        return other_company
    
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        additional_addresses_data = validated_data.pop('additionalAddresses', [])
        
        with transaction.atomic():
            if instance.emails.all():
               instance.emails.all().delete()
            if instance.additionalAddresses.all():
               instance.additionalAddresses.all().delete()
            for email_data in emails_data:
                OtherCompanyEmails.objects.create(other_company=instance, **email_data)

            for additional_address_data in additional_addresses_data:
                try:
                    country_instance = get_object_or_404(Countries, id=additional_address_data['country'])
                    state_instance = get_object_or_404(States, id=additional_address_data['state'])
                    city_instance = get_object_or_404(Cities, id=additional_address_data['city'])

                    additional_address_data['country'] = country_instance
                    additional_address_data['state'] = state_instance
                    additional_address_data['city'] = city_instance

                    OtherCompaniesAdditionalOfficeAddress.objects.create(other_company=instance, **additional_address_data)
                except Countries.DoesNotExist:
                    raise serializers.ValidationError("Invalid country id")
                except States.DoesNotExist:
                    raise serializers.ValidationError("Invalid state id")
                except Cities.DoesNotExist:
                    raise serializers.ValidationError("Invalid city id")
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()   
        return instance
    
class OtherCompaniesReadSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    currency = CurrenciesSerializer(read_only=True)
    emails = OtherCompanyEmailsSerializeer(many=True, required=False)
    additionalAddresses = OtherCompaniesReadAdditionalOfficeAddressSerializeer(many=True, required=False)
    class Meta:
        model = OtherCompanies
        fields = '__all__' 
#CRR
class CRRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRR
        fields = '__all__'
class CRRReadSerializer(serializers.ModelSerializer): 
    agent = AgentsSerializer(required=False)
    hub = HubsSerializer(required=False)
    vessel = CustomerVesselsReadSerializer(required=False)
    supplier = SuppliersSerializer(required=False)
    country = CountriesSerializer(required=False)
    currency = CurrenciesSerializer(required=False)
    register_by = UserSerializer(read_only=True)
    display_status = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = CRR
        fields = '__all__'
class CRRStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRRStockItem
        fields = '__all__'
class CRRDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRRDocuments
        fields = '__all__'        

#Shipment    
class ShipmentDepartureSerializer(serializers.ModelSerializer):
    departure_from_hub = HubsSerializer()
    departure_from_office = OfficeSerializer()
    departure_from_agent = AgentsSerializer()
    class Meta:
        model = ShipmentDeparture
        fields = '__all__'
class ShipmentConsigneeSerializer(serializers.ModelSerializer):
    consignee_from_hub = HubsSerializer()
    consignee_from_office = OfficeSerializer()
    consignee_from_agent = AgentsSerializer()
    class Meta:
        model = ShipmentConsignee
        fields = '__all__'
class ShipmentSerializer(serializers.ModelSerializer):
    departure = ShipmentDepartureSerializer(required=False)
    consignee = ShipmentConsigneeSerializer(required=False)
    stock_items = CRRSerializer(many=True, required=False)
    class Meta:
        model = Shipment
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        if request.data.get('departure'):
            departure = request.data.get('departure')
            data['departure'] = departure
                
        if request.data.get('consignee'):
            consignee = request.data.get('consignee')
            data['consignee'] = consignee
        
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data  
        
    def create(self, validated_data):
        departure = validated_data.pop('departure',None)
        consignee = validated_data.pop('consignee',None)
        departure_in = validated_data['departure_in']
        consignee_in = validated_data['consignee_in']
        with transaction.atomic():
            if departure_in == 'H':
                hub = get_object_or_404(Hubs, id=departure)
                departure = ShipmentDeparture.objects.create(departure_from_hub=hub)
            elif departure_in == 'O':
                office = get_object_or_404(Offices, id=departure)
                departure = ShipmentDeparture.objects.create(departure_from_office=office)
            elif departure_in == 'A':
                agent = get_object_or_404(Agents, id=departure)
                departure = ShipmentDeparture.objects.create(departure_from_agent=agent)

            if consignee_in == 'H':
                hub = get_object_or_404(Hubs, id=consignee)
                consignee = ShipmentConsignee.objects.create(consignee_from_hub=hub)
            elif consignee_in == 'O':
                office = get_object_or_404(Offices, id=consignee)
                consignee = ShipmentConsignee.objects.create(consignee_from_office=office)
            elif consignee_in == 'A':
                agent = get_object_or_404(Agents, id=consignee)
                consignee = ShipmentConsignee.objects.create(consignee_from_agent=agent)

            shipment = Shipment.objects.create(departure=departure, consignee=consignee, **validated_data)   
        return shipment
    
    def update(self, instance, validated_data):
        departure = validated_data.pop('departure',None)
        consignee = validated_data.pop('consignee',None)
        departure_in = validated_data.get('departure_in', None)
        consignee_in = validated_data.get('consignee_in', None)
        
        with transaction.atomic():
            if departure_in == 'H':
                hub = get_object_or_404(Hubs, id=departure)
                departure = ShipmentDeparture.objects.get(pk=instance.departure.id)
                departure.departure_from_hub=hub
                departure.departure_from_office=None
                departure.departure_from_agent=None
            elif departure_in == 'O':
                office = get_object_or_404(Offices, id=departure)
                departure = ShipmentDeparture.objects.get(pk=instance.departure.id)
                departure.departure_from_office=office
                departure.departure_from_hub=None
                departure.departure_from_agent=None
            elif departure_in == 'A':
                agent = get_object_or_404(Agents, id=departure)
                departure = ShipmentDeparture.objects.get(pk=instance.departure.id)
                departure.departure_from_agent=agent
                departure.departure_from_office=None
                departure.departure_from_hub=None
            if departure_in:    
                departure.save()  
            if consignee_in == 'H':
                hub = get_object_or_404(Hubs, id=consignee)
                consignee = ShipmentConsignee.objects.get(pk=instance.consignee.id)
                consignee.consignee_from_hub=hub
                consignee.consignee_from_office=None
                consignee.consignee_from_agent=None
            elif consignee_in == 'O':
                office = get_object_or_404(Offices, id=consignee)
                consignee = ShipmentConsignee.objects.get(pk=instance.consignee.id)
                consignee.consignee_from_office=office
                consignee.consignee_from_hub=None
                consignee.consignee_from_agent=None
            elif consignee_in == 'A':
                agent = get_object_or_404(Agents, id=consignee)
                consignee = ShipmentConsignee.objects.get(pk=instance.consignee.id)
                consignee.consignee_from_agent=agent
                consignee.consignee_from_office=None
                consignee.consignee_from_hub=None
            if consignee_in:    
                consignee.save()    
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if departure_in:    
                instance.departure=departure
            if consignee_in:
                instance.consignee=consignee
            instance.save()   
        return instance

class ShipmentReadSerializer(serializers.ModelSerializer):
    consignee_country = CountriesSerializer(read_only=True)
    consignee_state = StatesSerializer(read_only=True)
    consignee_city = CitiesSerializer(read_only=True)
    departure = ShipmentDepartureSerializer(required=False)
    consignee = ShipmentConsigneeSerializer(required=False)
    display_shipment_status = serializers.CharField(source='get_shipment_status_display', read_only=True)
    display_service = serializers.CharField(source='get_service_display', read_only=True)
    class Meta:
        model = Shipment
        fields = '__all__'

class AirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Air
        fields = '__all__'
class SeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sea
        fields = '__all__'
class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'
class CoriersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coriers
        fields = '__all__'
class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'
class OnBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnBoard
        fields = '__all__'                
class ShipmentServiceDetailsSerializer(serializers.ModelSerializer):
    air = AirSerializer(required=False)
    sea = SeaSerializer(required=False)
    truck = TruckSerializer(required=False)
    coriers = CoriersSerializer(required=False)
    release = ReleaseSerializer(required=False)
    on_board = OnBoardSerializer(required=False)

    class Meta:
        model = ShipmentServiceDetails
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        if request.data.get('air'):
            air = request.data.get('air')
            data['air'] = json.loads(air)     
        if request.data.get('sea'):
            sea = request.data.get('sea')
            data['sea'] = json.loads(sea)
        if request.data.get('truck'):
            truck = request.data.get('truck')
            data['truck'] = json.loads(truck)
        if request.data.get('coriers'):
            coriers = request.data.get('coriers')
            data['coriers'] = json.loads(coriers)     
        if request.data.get('release'):
            release = request.data.get('release')
            data['release'] = json.loads(release)
        if request.data.get('on_board'):
            on_board = request.data.get('on_board')
            data['on_board'] = json.loads(on_board)
        
        # Perform any custom validation here if needed
        # You can access the original validated data using 'super().validate(data)'
        validated_data = super().validate(data)
        return validated_data
        
    def create(self, validated_data):
        air = validated_data.pop('air',None)
        sea = validated_data.pop('sea',None)
        truck = validated_data.pop('truck',None)
        coriers = validated_data.pop('coriers',None)
        release = validated_data.pop('release',None)
        on_board = validated_data.pop('on_board',None)
        shipment = validated_data['shipment']
        result_service_details=[]
        with transaction.atomic():
            shipment_service = shipment.service
            
            if shipment_service == 'A':
                sd = Air.objects.create(**air)
                service_details = ShipmentServiceDetails.objects.create(air=sd, shipment=shipment)  
            elif shipment_service == 'S':
                sd = Sea.objects.create(**sea)
                service_details = ShipmentServiceDetails.objects.create(sea=sd, **validated_data) 
            elif shipment_service == 'T':
                sd = Truck.objects.create(**truck)
                service_details = ShipmentServiceDetails.objects.create(truck=sd, **validated_data)
            elif shipment_service == 'C':
                sd = Coriers.objects.create(**coriers)
                service_details = ShipmentServiceDetails.objects.create(coriers=sd, **validated_data)
            elif shipment_service == 'R':
                sd = Release.objects.create(**release)
                service_details = ShipmentServiceDetails.objects.create(release=sd, **validated_data) 
            elif shipment_service == 'O':
                sd = OnBoard.objects.create(**on_board)
                service_details = ShipmentServiceDetails.objects.create(on_board=sd, **validated_data)  
        return service_details
    
    def update(self, instance, validated_data):
        air = validated_data.pop('air',None)
        sea = validated_data.pop('sea',None)
        truck = validated_data.pop('truck',None)
        coriers = validated_data.pop('coriers',None)
        release = validated_data.pop('release',None)
        on_board = validated_data.pop('on_board',None)
        shipment = instance.shipment
        with transaction.atomic():
            shipment_service = shipment.service
            if shipment_service == 'A':
                sd = get_object_or_404(Air, pk=instance.air.id)
                for attr, value in air.items():
                    setattr(sd, attr, value)
                instance.air = sd
            elif shipment_service == 'S':
                sd = get_object_or_404(Sea, pk=instance.sea.id)
                for attr, value in sea.items():
                    setattr(sd, attr, value)
                instance.sea = sd
            elif shipment_service == 'T':
                sd = get_object_or_404(Truck, pk=instance.truck.id)
                for attr, value in truck.items():
                    setattr(sd, attr, value)
                instance.truck = sd
            elif shipment_service == 'C':
                sd = get_object_or_404(Coriers, pk=instance.coriers.id)
                for attr, value in coriers.items():
                    setattr(sd, attr, value)
                instance.coriers = sd
            elif shipment_service == 'R':
                sd = get_object_or_404(Release, pk=instance.release.id)
                for attr, value in release.items():
                    setattr(sd, attr, value)
                instance.release = sd
            elif shipment_service == 'O':
                sd = get_object_or_404(OnBoard, pk=instance.on_board.id)
                for attr, value in on_board.items():
                    setattr(sd, attr, value)
                instance.on_board = sd
            sd.save()    
            instance.save()   
        return instance
    

