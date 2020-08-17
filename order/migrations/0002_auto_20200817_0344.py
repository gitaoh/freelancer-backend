# Generated by Django 3.0.7 on 2020-08-17 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content',
            field=models.TextField(help_text='Notification message', max_length=10000),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created',
            field=models.ForeignKey(default=None, help_text='Which admin created', limit_choices_to={'is_active': True, 'user_type': ['MASTER', 'ADMIN']}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created', related_query_name='creator', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=None, help_text='User to be sent this notification', limit_choices_to={'is_active': True, 'user_type': 'USER'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]