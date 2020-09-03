# Generated by Django 3.1.1 on 2020-09-03 16:42

from django.conf import settings
import django.contrib.auth.validators
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
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('description', models.CharField(help_text='Client description of what this files contains', max_length=200, null=True)),
                ('file', models.FileField(help_text='Please add files if you have any.', upload_to='files')),
                ('is_deleted', models.BooleanField(default=False, help_text='if file is deleted or not')),
                ('label', models.CharField(choices=[(None, 'Unknown'), ('FINAL', 'FINAL'), ('DRAFT', 'DRAFT'), ('FILE', 'FILE')], default='FILE', max_length=5)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'db_table': 'File',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('username', models.CharField(error_messages={'unique': 'A user with this username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(help_text='Writer first name.', max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(help_text='Writer last name.', max_length=150, verbose_name='last name')),
                ('email', models.EmailField(help_text='Writer email.', max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Writer is active/deactivated', verbose_name='active')),
                ('level', models.CharField(choices=[(None, 'Unknown'), ('STANDARD', 'STANDARD'), ('TOP5', 'TOP5'), ('EXPERT', 'EXPERT')], default='STANDARD', help_text='Experience level of the writer', max_length=8)),
            ],
            options={
                'verbose_name': 'Writer',
                'verbose_name_plural': 'Writers',
                'db_table': 'Writer',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('card', models.CharField(help_text='Order_id_card', max_length=10)),
                ('paper_type', models.CharField(help_text='This order paper type', max_length=200, verbose_name='paper_type')),
                ('discipline', models.CharField(help_text='This orders discipline', max_length=200, verbose_name='discipline')),
                ('academic', models.CharField(choices=[(None, 'Unknown'), ('HIGHSCHOOL', 'HIGHSCHOOL'), ('PHD', 'PHD'), ('GRADUATE', 'GRADUATE'), ('UNDERGRADUATE_1_2', 'UNDERGRADUATE_1_2'), ('UNDERGRADUATE_3_4', 'UNDERGRADUATE_3_4')], default='HIGHSCHOOL', help_text='Clients academic level', max_length=17, verbose_name='academic')),
                ('format', models.CharField(choices=[(None, 'Unknown'), ('MLA', 'MLA'), ('CHICAGO/TURABIAN', 'CHICAGO/TURABIAN'), ('APA7', 'APA7'), ('APA6', 'APA6')], default='MLA', help_text='Format chosen by client for this order, eg. MLA, APA6...', max_length=16)),
                ('spacing', models.CharField(choices=[(None, 'Unknown'), ('SINGLE', 'SINGLE'), ('DOUBLE', 'DOUBLE')], default='SINGLE', help_text='Whether order is single or double spaced', max_length=6)),
                ('preference', models.CharField(choices=[(None, 'Unknown'), ('STANDARD', 'STANDARD'), ('TOP5', 'TOP5'), ('EXPERT', 'EXPERT')], default='STANDARD', help_text='The writer preference a the client chose for this order.', max_length=20)),
                ('powerpoint', models.PositiveIntegerField(default=0, help_text='Number of powerpoints requested in the current order')),
                ('status', models.CharField(choices=[(None, 'Unknown'), ('ACTIVE', 'ACTIVE'), ('DRAFT', 'DRAFT'), ('REVISION', 'REVISION'), ('FINISHED', 'FINISHED'), ('CANCELED', 'CANCELED'), ('DISPUTE', 'DISPUTE')], default='ACTIVE', help_text='Where an order belongs to ether active, deleted, or ..', max_length=10)),
                ('payments_url', models.URLField(help_text='A payment url to verify user paid the order', null=True, unique=True, verbose_name='payment_url')),
                ('title', models.CharField(help_text='This orders title', max_length=200, verbose_name='title')),
                ('instructions', models.TextField(help_text='This paper instructions')),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now, help_text='The deadline of this order')),
                ('pages', models.PositiveIntegerField(default=0, help_text='Number of pages requested in the current order')),
                ('sources', models.PositiveIntegerField(default=0, help_text='Number of sources requested in the current order')),
                ('charts', models.PositiveIntegerField(default=0, help_text='Number of charts requested in the current order')),
                ('native', models.BooleanField(default=False, help_text='To a assign a native writer for the current order')),
                ('progressive', models.BooleanField(default=False, help_text='If order is a progressive delivery')),
                ('cost', models.PositiveIntegerField(default=0, help_text='The cost of a paper')),
                ('smart', models.BooleanField(default=False, help_text='Whether an order is  a smart paper.', verbose_name='is_smart')),
                ('paid', models.BooleanField(default=False, help_text='Whether an order is paid or not.', verbose_name='paid')),
                ('rate', models.PositiveIntegerField(default=0, help_text='Rating of how a paper was done by this writer', null=True)),
                ('confirmed', models.BooleanField(default=False, help_text='Whether an order is confirmed that is can be done.', verbose_name='confirmed')),
                ('dispute', models.BooleanField(default=False, help_text='Whether an order is or was a dispute.', verbose_name='dispute')),
                ('revision', models.BooleanField(default=False, help_text='Whether an order is or was a revision.', verbose_name='revision')),
                ('is_paper', models.BooleanField(default=True, help_text='Whether a paper id deleted/canceled.', verbose_name='is_paper')),
                ('is_approved', models.BooleanField(default=False, help_text='Whether a paper is approved or not approved.', verbose_name='is_approved')),
                ('additional_materials', models.ManyToManyField(limit_choices_to={'is_deleted': False}, to='order.Files')),
                ('deleted_by', models.ForeignKey(default=None, help_text='Who deleted this order', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deletedBy', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('user', models.ForeignKey(help_text='Client Placing the order', limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='user')),
                ('writer', models.ForeignKey(default=None, help_text='Who is assigned to work on this order', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.writer', to_field='username', verbose_name='writer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'Order',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('content', models.TextField(help_text='Notification message', max_length=10000)),
                ('notify', models.CharField(choices=[(None, 'Unknown'), ('ToSUPPORT', 'ToSUPPORT'), ('ToWRITER', 'ToWRITER'), ('SUPPORT', 'SUPPORT'), ('WRITER', 'WRITER')], default='ToSUPPORT', help_text='Who should see this notification.', max_length=12)),
                ('read', models.BooleanField(default=False, help_text='If notifications is read or unread')),
                ('is_notify', models.BooleanField(default=True, help_text='if a notification is deleted or active')),
                ('admin', models.ForeignKey(help_text='Which admin created', limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='created', related_query_name='creator', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('order', models.ForeignKey(limit_choices_to={'is_paper': True}, on_delete=django.db.models.deletion.PROTECT, to='order.order', to_field='uuid')),
                ('user', models.ForeignKey(help_text='User to be sent this notification', limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'Notification',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('reason', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.ForeignKey(limit_choices_to={'is_approved': False, 'is_paper': True}, on_delete=django.db.models.deletion.PROTECT, to='order.order', to_field='uuid')),
                ('user', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Cancel',
                'verbose_name_plural': 'Cancels',
                'db_table': 'Cancel',
            },
        ),
    ]
