# Generated by Django 4.2.3 on 2023-09-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvnApp', '0002_subscriptionmodule_remove_transaction_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionmodule',
            name='price',
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
    ]