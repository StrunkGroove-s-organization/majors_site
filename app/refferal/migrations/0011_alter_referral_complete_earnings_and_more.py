# Generated by Django 4.2.5 on 2024-03-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refferal', '0010_remove_referral_complete_payments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='complete_earnings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='referral',
            name='earnings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]