# Generated by Django 4.2.3 on 2023-09-16 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kvnApp', '0004_remove_usersubscription_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='transaction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='kvnApp.transaction'),
        ),
    ]
