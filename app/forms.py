from django import forms
from .models import Hotel, City


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['city', 'code', 'name', 'description', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()
