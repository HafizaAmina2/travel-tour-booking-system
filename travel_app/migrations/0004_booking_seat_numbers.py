from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0003_seed_tour_packages'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seat_numbers',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Auto-assigned seat numbers for this booking (e.g. "3, 4")',
                max_length=100,
            ),
        ),
    ]
