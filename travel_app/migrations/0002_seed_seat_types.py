from django.db import migrations


def seed_seat_types(apps, schema_editor):
    SeatType = apps.get_model('travel_app', 'SeatType')

    default_seat_types = ['Window', 'Middle', 'Front', 'Back']

    for seat_name in default_seat_types:
        SeatType.objects.get_or_create(
            name=seat_name,
            defaults={'capacity_per_date': 5}
        )


def remove_seat_types(apps, schema_editor):
    SeatType = apps.get_model('travel_app', 'SeatType')
    SeatType.objects.filter(
        name__in=['Window', 'Middle', 'Front', 'Back']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_seat_types, remove_seat_types),
    ]
