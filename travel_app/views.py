from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from datetime import date

from .models import TourPackage, User, Booking, SeatType


# ---------------------------------------------------------------------------
# Seat layout — fixed 20-seat bus configuration
# ---------------------------------------------------------------------------

# Maps seat number (1-20) to its seat type name
SEAT_TYPE_MAP = {
    1: 'Front',  2: 'Front',  3: 'Front',  4: 'Front',
    5: 'Window', 8: 'Window', 9: 'Window', 12: 'Window',
    13: 'Window', 16: 'Window',
    6: 'Middle', 7: 'Middle', 10: 'Middle', 11: 'Middle',
    14: 'Middle', 15: 'Middle',
    17: 'Back',  18: 'Back',  19: 'Back',  20: 'Back',
}

ALL_SEATS = list(range(1, 21))   # 1 .. 20


def get_taken_seats(package, travel_date):
    """
    Returns a set of integer seat numbers already booked for this
    package + travel_date (cancelled bookings release their seats).
    """
    taken = set()
    bookings = Booking.objects.filter(
        package=package,
        travel_date=travel_date,
    ).exclude(booking_status='Cancelled')

    for b in bookings:
        if b.seat_numbers:
            for n in b.seat_numbers.split(','):
                n = n.strip()
                if n.isdigit():
                    taken.add(int(n))
    return taken


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def home(request):
    search = request.GET.get('search')
    if search:
        packages = TourPackage.objects.filter(title__icontains=search)
    else:
        packages = TourPackage.objects.all()
    return render(request, 'home.html', {'packages': packages})


def register(request):
    if request.method == 'POST':
        name             = request.POST['name']
        email            = request.POST['email']
        password         = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
            else:
                User.objects.create(name=name, email=email, password=password)
                messages.success(request, 'Registration Successful!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_email'] = user.email
            messages.success(request, 'Login Successful!')
            return redirect('home')
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            messages.error(request, 'Invalid Email or Password!')

    return render(request, 'login.html')


def seat_availability(request):
    """
    AJAX endpoint — returns taken seat numbers for a package + date.
    GET /seat-availability/?date=YYYY-MM-DD&package=PackageName
    Response: {"taken": [1, 5, 6]}
    """
    travel_date  = request.GET.get('date', '').strip()
    package_name = request.GET.get('package', '').strip()

    if not travel_date or not package_name:
        return JsonResponse({'taken': []})

    try:
        package = TourPackage.objects.get(title=package_name)
    except TourPackage.DoesNotExist:
        return JsonResponse({'taken': []})

    taken = get_taken_seats(package, travel_date)
    return JsonResponse({'taken': sorted(taken)})


def booking(request):
    if request.method == 'POST':
        email            = request.POST.get('email', '').strip()
        package_name     = request.POST.get('package', '').strip()
        travel_date      = request.POST.get('travel_date', '').strip()
        seat_numbers_raw = request.POST.get('seat_numbers', '').strip()

        def back(msg):
            messages.error(request, msg)
            return render(request, 'booking.html', {
                'packages': TourPackage.objects.all(),
            })

        # Validate user + package
        try:
            user    = User.objects.get(email=email)
            package = TourPackage.objects.get(title=package_name)
        except (User.DoesNotExist, TourPackage.DoesNotExist):
            return back('User or Package Not Found!')

        if not travel_date:
            return back('Please select a travel date.')

        # Parse seat numbers submitted by the seat-map JS
        if not seat_numbers_raw:
            return back('Please select at least one seat on the seat map.')

        try:
            selected = sorted({
                int(n.strip())
                for n in seat_numbers_raw.split(',')
                if n.strip()
            })
        except ValueError:
            return back('Invalid seat selection. Please try again.')

        if not selected:
            return back('Please select at least one seat on the seat map.')

        if any(n < 1 or n > 20 for n in selected):
            return back('Invalid seat numbers. Please use the seat map.')

        # Check against seats already booked for this package + date
        taken = get_taken_seats(package, travel_date)
        conflicts = [n for n in selected if n in taken]
        if conflicts:
            return back(
                f'Seat(s) {", ".join(str(n) for n in conflicts)} '
                f'were just booked by someone else. '
                f'Please refresh and choose different seats.'
            )

        # Derive seat_type from the first selected seat
        seat_type_name = SEAT_TYPE_MAP.get(selected[0], 'Middle')
        try:
            seat_type = SeatType.objects.get(name=seat_type_name)
        except SeatType.DoesNotExist:
            seat_type = None

        new_booking = Booking.objects.create(
            user         = user,
            package      = package,
            seat_type    = seat_type,
            seat_numbers = ', '.join(str(n) for n in selected),
            persons      = len(selected),
            travel_date  = travel_date,
        )

        messages.success(
            request,
            'Booking submitted! Your seats are reserved and pending admin approval.'
        )
        return redirect('receipt', booking_id=new_booking.id)

    return render(request, 'booking.html', {
        'packages': TourPackage.objects.all(),
    })


def receipt(request, booking_id):
    booking_obj = get_object_or_404(Booking, id=booking_id)
    return render(request, 'receipt.html', {'booking': booking_obj})


def booking_history(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, 'Please login to view your booking history.')
        return redirect('login')

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        messages.error(request, 'Please login to view your booking history.')
        return redirect('login')

    bookings = Booking.objects.filter(user=user)
    return render(request, 'booking_history.html', {'bookings': bookings})


def cancel_booking(request, booking_id):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, 'Please login to manage your bookings.')
        return redirect('login')

    booking_obj = get_object_or_404(Booking, id=booking_id)

    if booking_obj.user.email != user_email:
        messages.error(request, 'You are not allowed to cancel this booking.')
        return redirect('booking_history')

    if request.method == 'POST':
        if booking_obj.booking_status == 'Cancelled':
            messages.info(request, 'This booking is already cancelled.')
        elif (booking_obj.travel_date - date.today()).days < 2:
            messages.error(
                request,
                'Booking can only be cancelled if the travel date is at least 2 days away.'
            )
        else:
            booking_obj.booking_status = 'Cancelled'
            booking_obj.save()
            messages.success(request, 'Booking cancelled successfully.')

    return redirect('booking_history')


def logout(request):
    request.session.flush()
    return redirect('login')
