# Generated by Django 3.1.2 on 2021-09-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210909_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memory',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
