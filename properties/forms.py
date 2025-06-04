from django import forms
from .models import Building, Country, County, City

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = [
            "name", "address", "country", "county", "city",
            "rental_status", "monthly_rent", "description", "photo"
        ]
        widgets = {
            "country": forms.Select(attrs={"class": "form-select"}),
            "county": forms.Select(attrs={"class": "form-select"}),
            "city": forms.Select(attrs={"class": "form-select bootstrap-select", "data-live-search": "true"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].queryset = County.objects.all().order_by('name')
        self.fields['city'].queryset = City.objects.all().order_by('name')