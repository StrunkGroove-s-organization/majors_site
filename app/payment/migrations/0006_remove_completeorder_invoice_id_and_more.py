# Generated by Django 4.2.1 on 2023-08-20 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_completeorder_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completeorder',
            name='invoice_id',
        ),
        migrations.RemoveField(
            model_name='completeorder',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='invoice_id',
        ),
    ]