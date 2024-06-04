from django.contrib import admin
from .models import City, Hotel, Manager, Room


# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'code')
    list_filter = ('city',)
    search_fields = ('name', 'city__name', 'code')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            manager = request.user.manager
            return qs.filter(city=manager.city)
        except Manager.DoesNotExist:
            return qs.none()


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    search_fields = ('user__username', 'city__name')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'price')
    list_filter = ('hotel',)
    search_fields = ('title', 'hotel__name')


admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Room, RoomAdmin)
