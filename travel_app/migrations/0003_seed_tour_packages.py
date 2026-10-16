from django.db import migrations


def seed_tour_packages(apps, schema_editor):
    TourPackage = apps.get_model('travel_app', 'TourPackage')

    sample_packages = [
        {
            'title': 'Hunza Valley Tour',
            'destination': 'Hunza',
            'price': 25000,
            'duration': '5 Days',
            'description': 'Explore the breathtaking valleys, lakes and '
                            'mountains of Hunza with comfortable stays and '
                            'guided sightseeing.',
            'image': 'https://images.unsplash.com/photo-1605640840605-14ac1855827b?w=800',
        },
        {
            'title': 'Skardu Adventure',
            'destination': 'Skardu',
            'price': 30000,
            'duration': '6 Days',
            'description': 'Visit Skardu Fort, Shangrila Resort and the '
                            'stunning Deosai Plains on this adventure-packed '
                            'tour.',
            'image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800',
        },
        {
            'title': 'Swat Valley Getaway',
            'destination': 'Swat',
            'price': 18000,
            'duration': '4 Days',
            'description': 'Discover the "Switzerland of Pakistan" with its '
                            'lush green meadows, rivers and pleasant '
                            'weather.',
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
        },
        {
            'title': 'Naran Kaghan Tour',
            'destination': 'Naran',
            'price': 20000,
            'duration': '4 Days',
            'description': 'Experience Saif-ul-Malook Lake and the scenic '
                            'beauty of the Kaghan Valley on this popular '
                            'family tour.',
            'image': 'https://images.unsplash.com/photo-1500534623283-312aade485b7?w=800',
        },
        {
            'title': 'Murree Hills Escape',
            'destination': 'Murree',
            'price': 12000,
            'duration': '2 Days',
            'description': 'A quick and relaxing weekend getaway to the '
                            'pine-covered hills of Murree, perfect for short '
                            'trips.',
            'image': 'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=800',
        },
    ]

    for pkg in sample_packages:
        TourPackage.objects.get_or_create(
            title=pkg['title'],
            defaults={
                'destination': pkg['destination'],
                'price': pkg['price'],
                'duration': pkg['duration'],
                'description': pkg['description'],
                'image': pkg['image'],
            }
        )


def remove_tour_packages(apps, schema_editor):
    TourPackage = apps.get_model('travel_app', 'TourPackage')
    TourPackage.objects.filter(
        title__in=[
            'Hunza Valley Tour',
            'Skardu Adventure',
            'Swat Valley Getaway',
            'Naran Kaghan Tour',
            'Murree Hills Escape',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0002_seed_seat_types'),
    ]

    operations = [
        migrations.RunPython(seed_tour_packages, remove_tour_packages),
    ]
