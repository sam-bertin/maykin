from django.http import JsonResponse
from django.views.generic import TemplateView, DeleteView, CreateView
from .models import City, Hotel
from .import_data import import_city_and_hotel_data
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Hotel, Manager
from .forms import HotelForm


# Create your views here.
def hotel_list(request):
    # TODO : Replace import with cron job
    import_city_and_hotel_data()
    cities = City.objects.all()
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'cities': cities, 'hotels': hotels})


def hotels_by_city(request):
    city_id = request.GET.get('city')
    if city_id:
        hotels = Hotel.objects.filter(city_id=city_id)
    else:
        hotels = Hotel.objects.all()
    data = [{'id': hotel.id, 'name': hotel.name, 'city': {'id': hotel.city_id, 'name': hotel.city.name},
             'code': hotel.code} for hotel in hotels]
    return JsonResponse(data, safe=False)


class ManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'manager_view.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser and not hasattr(request.user, 'manager'):
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = None
        try:
            manager = self.request.user.manager
            hotels = Hotel.objects.filter(city=manager.city)
        except Manager.DoesNotExist:
            return redirect('/')
        context['hotels'] = hotels
        context['manager'] = manager
        return context




class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('manager_view')

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.manager = self.request.user.manager
        hotel.save()
        return redirect('manager_view')


class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('manager_view')

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.manager = self.request.user.manager
        hotel.save()
        return redirect('manager_view')

    def test_func(self):
        hotel = self.get_object()
        if self.request.user.is_superuser:
            return True
        return hotel.manager == self.request.user.manager


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('manager_view')

    def test_func(self):
        hotel = self.get_object()
        if self.request.user.is_superuser:
            return True
        return hotel.manager == self.request.user.manager
