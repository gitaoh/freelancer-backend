# Generated by Django 3.0.7 on 2020-08-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20200817_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(None, 'Unknown'), ('ACTIVE', 'ACTIVE'), ('DRAFT', 'DRAFT'), ('REVISION', 'REVISION'), ('FINISHED', 'FINISHED'), ('CANCELED', 'CANCELED'), ('DISPUTE', 'DISPUTE')], default='ACTIVE', help_text='Where an order belongs to ether active, deleted, or ..', max_length=10),
        ),
    ]
