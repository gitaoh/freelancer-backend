# Generated by Django 3.1.1 on 2020-09-04 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20200903_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=models.ImageField(upload_to='Avatar/'),
        ),
    ]
