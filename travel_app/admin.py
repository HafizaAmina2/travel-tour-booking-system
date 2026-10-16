from django.contrib import admin
from .models import User, TourPackage, Booking, SeatType


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'destination', 'price', 'duration')
    search_fields = ('title', 'destination')
    list_filter   = ('destination',)


@admin.register(SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity_per_date')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display   = (
        'id', 'user', 'package',
        'seat_type', 'seat_numbers',   # seat numbers now visible
        'persons', 'travel_date', 'booking_date', 'booking_status',
    )
    list_editable  = ('booking_status',)
    list_filter    = ('booking_status', 'seat_type', 'travel_date')
    search_fields  = ('user__name', 'user__email', 'package__title')
    readonly_fields = ('booking_date', 'seat_numbers')
    ordering       = ('-id',)
    list_per_page  = 25

    fieldsets = (
        ('Booking Info', {
            'fields': ('user', 'package', 'seat_type', 'seat_numbers', 'persons', 'travel_date', 'booking_date')
        }),
        ('Status', {
            'fields': ('booking_status',)
        }),
    )
