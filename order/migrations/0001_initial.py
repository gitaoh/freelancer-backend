# Generated by Django 3.0.7 on 2020-08-15 13:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, help_text='uuid is required', null=True, unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(blank=True, null=True, verbose_name='deletedAt')),
                ('updateAt', models.DateTimeField(auto_now=True, verbose_name='updateAt')),
                ('fileDescription', models.CharField(blank=True, max_length=200, null=True)),
                ('paper_files', models.FileField(help_text='Please add files if you have any.', upload_to='files')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'OrderFile',
                'verbose_name_plural': 'OrderFiles',
                'db_table': 'OrderFile',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, help_text='uuid is required', null=True, unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(blank=True, null=True, verbose_name='deletedAt')),
                ('updateAt', models.DateTimeField(auto_now=True, verbose_name='updateAt')),
                ('paper_type', models.CharField(help_text='This order paper type', max_length=200, verbose_name='paper_type')),
                ('discipline', models.CharField(help_text='This orders discipline', max_length=200, verbose_name='discipline')),
                ('academic', models.CharField(choices=[('HIGHSCHOOL', 'HIGHSCHOOL'), ('PHD', 'PHD'), ('GRADUATE', 'GRADUATE'), ('UNDERGRADUATE_1_2', 'UNDERGRADUATE_1_2'), ('UNDERGRADUATE_3_4', 'UNDERGRADUATE_3_4')], default='HIGHSCHOOL', help_text='Clients academic level', max_length=200, verbose_name='academic')),
                ('title', models.CharField(help_text='This orders title', max_length=200, verbose_name='title')),
                ('instructions', models.TextField(help_text='This paper instructions')),
                ('format', models.CharField(choices=[('MLA', 'MLA'), ('CHICAGO/TURABIAN', 'CHICAGO/TURABIAN'), ('APA7', 'APA7'), ('APA6', 'APA6')], default='MLA', help_text='Format chosen by client for this order, eg. MLA, APA6...', max_length=30)),
                ('spacing', models.CharField(choices=[('SINGLE', 'SINGLE'), ('DOUBLE', 'DOUBLE')], default='SINGLE', help_text='Whether order is single or double spaced', max_length=10)),
                ('preference', models.CharField(choices=[('BEST AVAILABLE', 'BEST AVAILABLE'), ('ADVANCED', 'ADVANCED'), ('TOP10', 'TOP10'), ('TOP25', 'TOP25')], default='BEST AVAILABLE', help_text='The writer preference a the client chose for this order.', max_length=20)),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now, help_text='The deadline of this order')),
                ('pages', models.PositiveIntegerField(default=0, help_text='Number of pages requested in the current order')),
                ('sources', models.PositiveIntegerField(default=0, help_text='Number of sources requested in the current order')),
                ('charts', models.PositiveIntegerField(default=0, help_text='Number of charts requested in the current order')),
                ('powerpoint', models.PositiveIntegerField(default=0, help_text='Number of powerpoints requested in the current order')),
                ('native', models.BooleanField(default=False, help_text='To a assign a native writer for the current order')),
                ('progressive', models.BooleanField(default=False, help_text='If order is a progressive delivery')),
                ('status', models.CharField(choices=[('DRAFT', 'DRAFT'), ('REVISION', 'REVISION'), ('ACTIVE', 'ACTIVE'), ('FINISHED', 'FINISHED'), ('CANCELED', 'CANCELED'), ('DISPUTE', 'DISPUTE')], default='ACTIVE', help_text='Where an order belongs to ether active, deleted, or ..', max_length=10)),
                ('payments_url', models.URLField(blank=True, help_text='A payment url to verify user paid the order', null=True, unique=True, verbose_name='payment_url')),
                ('cost', models.PositiveIntegerField(default=0, help_text='The cost of a paper')),
                ('smart', models.BooleanField(default=False, help_text='Whether an order is  a smart paper.')),
                ('paid', models.BooleanField(default=False, help_text='Whether an order is paid or not.', verbose_name='paid')),
                ('cancelled', models.BooleanField(default=False, help_text='Whether an order is cancelled.', verbose_name='cancelled')),
                ('draft', models.BooleanField(default=False, help_text='Whether to store an order as draft', verbose_name='draft')),
                ('orders_confirmed_status', models.BooleanField(default=False, help_text='Whether an order is confirmed.')),
                ('dispute_status', models.BooleanField(default=False, help_text='Whether an order is or was a dispute.')),
                ('revision_status', models.BooleanField(default=False, help_text='Whether an order is or was a revision.')),
                ('is_paper', models.BooleanField(default=True, help_text='Whether a paper id deleted/canceled.')),
                ('additional_materials', models.ManyToManyField(blank=True, to='order.OrderFiles')),
                ('user', models.ForeignKey(default=0, help_text='Client Placing the order', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, help_text='uuid is required', null=True, unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(blank=True, null=True, verbose_name='deletedAt')),
                ('updateAt', models.DateTimeField(auto_now=True, verbose_name='updateAt')),
                ('content', models.TextField()),
                ('type_notify', models.CharField(choices=[('UPDATE', 'UPDATE'), ('NOTIFICATION', 'NOTIFICATION')], default='NOTIFICATION', max_length=12)),
                ('read', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'Notification',
            },
        ),
    ]