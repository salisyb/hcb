# Generated by Django 4.0.3 on 2022-03-17 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userplan_owner_remove_userplan_subscription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription_type',
            field=models.CharField(default='None', max_length=100),
        ),
    ]