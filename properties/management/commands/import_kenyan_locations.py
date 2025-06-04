from django.core.management.base import BaseCommand
from properties.models import Country, County, City

class Command(BaseCommand):
    help = 'Import Kenyan counties and cities/towns'

    def handle(self, *args, **kwargs):
        kenya, _ = Country.objects.get_or_create(name="Kenya")
        counties_and_cities = [
            ("Nairobi", ["Nairobi"]),
            ("Mombasa", ["Mombasa"]),
            ("Kisumu", ["Kisumu"]),
            ("Uasin Gishu", ["Eldoret"]),
            ("Nakuru", ["Nakuru", "Naivasha"]),
            # ...add all counties and their towns/cities...
        ]
        for county_name, cities in counties_and_cities:
            county, _ = County.objects.get_or_create(name=county_name, country=kenya)
            for city_name in cities:
                City.objects.get_or_create(name=city_name, county=county)
        self.stdout.write(self.style.SUCCESS('Kenyan counties and cities/towns imported!'))