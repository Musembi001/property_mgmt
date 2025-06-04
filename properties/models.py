from django.db import models
from accounts.models import User
from smart_selects.db_fields import ChainedForeignKey

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class County(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='counties')

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class City(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('name', 'county')

    def __str__(self):
        return f"{self.name}, {self.county.name}"

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    rental_status = models.CharField(max_length=20, choices=[('available', 'Available'), ('occupied', 'Occupied')], default='available')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'landlord'})
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_buildings', limit_choices_to={'role': 'agent'})
    caretaker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='caretaker_buildings', limit_choices_to={'role': 'caretaker'})
    photo = models.ImageField(upload_to='property_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=20)
    floor = models.IntegerField()

    def __str__(self):
        return f"{self.building.name} - {self.unit_number}"

class Property(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return self.name
