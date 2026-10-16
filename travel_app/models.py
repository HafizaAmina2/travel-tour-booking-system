from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TourPackage(models.Model):
    title = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.CharField(max_length=50)
    description = models.TextField()
    image = models.URLField(blank=True)

    def __str__(self):
        return self.title


class SeatType(models.Model):
    WINDOW = 'Window'
    MIDDLE = 'Middle'
    FRONT  = 'Front'
    BACK   = 'Back'

    SEAT_CHOICES = [
        (WINDOW, 'Window Seat'),
        (MIDDLE, 'Middle Seat'),
        (FRONT,  'Front Seat'),
        (BACK,   'Back Seat'),
    ]

    name = models.CharField(max_length=20, choices=SEAT_CHOICES, unique=True)
    capacity_per_date = models.PositiveIntegerField(
        default=5,
        help_text='Max persons that can book this seat type for one travel date.'
    )

    def __str__(self):
        return self.get_name_display()


class Booking(models.Model):
    user    = models.ForeignKey(User,        on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    seat_type = models.ForeignKey(
        SeatType, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='bookings'
    )

    # Comma-separated assigned seat numbers, e.g. "2" or "3, 4, 5"
    seat_numbers = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='Auto-assigned seat numbers for this booking (e.g. "3, 4")'
    )

    persons      = models.IntegerField()
    travel_date  = models.DateField()
    booking_date = models.DateField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    booking_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def seat_numbers_display(self):
        """Returns e.g. 'Window Seat - No. 3, 4' for display in templates."""
        if self.seat_type and self.seat_numbers:
            return f"{self.seat_type.get_name_display()} - No. {self.seat_numbers}"
        return "Not Assigned"
