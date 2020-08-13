# Generated by Django 3.0.7 on 2020-08-12 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200813_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='academic',
            field=models.CharField(choices=[('HIGHSCHOOL', 'HIGHSCHOOL'), ('PHD', 'PHD'), ('GRADUATE', 'GRADUATE'), ('UNDERGRADUATE_1_2', 'UNDERGRADUATE_1_2'), ('UNDERGRADUATE_3_4', 'UNDERGRADUATE_3_4')], default='HIGHSCHOOL', max_length=200, verbose_name='academic'),
        ),
    ]
