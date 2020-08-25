# Generated by Django 3.1 on 2020-08-25 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200824_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deleted_by',
            field=models.ForeignKey(default=None, help_text='Who deleted this order', limit_choices_to={'is_active': True, 'is_staff': True, 'is_superuser': True, 'user_type': 'MASTER'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_by', to='order.writer', to_field='username', verbose_name='writer'),
        ),
    ]
