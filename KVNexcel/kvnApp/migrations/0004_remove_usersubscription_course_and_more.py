# Generated by Django 4.2.3 on 2023-09-16 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kvnApp', '0003_alter_subscriptionmodule_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscription',
            name='course',
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='module',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='kvnApp.subscriptionmodule'),
        ),
    ]
