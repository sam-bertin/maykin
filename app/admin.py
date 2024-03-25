from django.contrib import admin
from .models import City, Hotel


# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'code')
    list_filter = ('city',)
    search_fields = ('name', 'city__name', 'code')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
