# Generated by Django 5.0.1 on 2024-03-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_user_adhar_num_user_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
