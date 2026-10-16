from django.contrib import admin
from django.urls import path
from travel_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',                              views.login,             name='start'),
    path('home/',                         views.home,              name='home'),
    path('register/',                     views.register,          name='register'),
    path('login/',                        views.login,             name='login'),
    path('booking/',                      views.booking,           name='booking'),
    path('receipt/<int:booking_id>/',     views.receipt,           name='receipt'),
    path('booking-history/',              views.booking_history,   name='booking_history'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('seat-availability/',            views.seat_availability, name='seat_availability'),
    path('logout/',                       views.logout,            name='logout'),
]
