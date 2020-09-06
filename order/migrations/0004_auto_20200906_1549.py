# Generated by Django 3.1.1 on 2020-09-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_writer_bio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-createdAt',), 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[(None, 'Unknown'), ('REVIEW', 'REVIEW'), ('ACTIVE', 'ACTIVE')], default='REVIEW', help_text='IF a message can be read by user eg. wen can create a message and put it on review then after a review set the state to active the the client will be able to view the message', max_length=6),
        ),
        migrations.AlterModelTable(
            name='message',
            table='Message',
        ),
    ]
