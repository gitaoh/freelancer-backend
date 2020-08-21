# Generated by Django 3.0.7 on 2020-08-20 20:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('phone_number', models.CharField(help_text='Ensure you Phone number only contain numbers', max_length=15, null=True, unique=True, validators=[django.core.validators.MaxLengthValidator(limit_value=15, message='Phone number is too large max length is 15 digits'), django.core.validators.RegexValidator(code='Invalid Phone Number Entered', inverse_match=False, message='Phone number should only contain numbers', regex='^[0-9]*$')], verbose_name='phone number')),
                ('updates', models.BooleanField(default=True, help_text='Send updates to user about our services', verbose_name='updates')),
                ('user_type', models.CharField(choices=[(None, 'Unknown'), ('USER', 'USER'), ('ADMIN', 'ADMIN'), ('MASTER', 'MASTER')], default='USER', help_text='Define the type of the user :User always', max_length=6, verbose_name='type')),
                ('terms', models.BooleanField(default=True, help_text='Agreement on our platform terms and conditions', verbose_name='terms')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.MaxLengthValidator(limit_value=254, message='Email is too long')], verbose_name='email')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('avatar', models.FileField(upload_to='Avatar/')),
                ('is_avatar', models.BooleanField(default=False, help_text='If an avatar is deleted')),
            ],
            options={
                'verbose_name': 'Avatar',
                'verbose_name_plural': 'Avatars',
                'db_table': 'Avatar',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('rate', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=10, message='Rating cannot be more than ten.')])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
                'db_table': 'Rating',
            },
        ),
        migrations.CreateModel(
            name='Defaults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(help_text='uuid is required', unique=True, validators=[django.core.validators.MaxLengthValidator, django.core.validators.MinLengthValidator], verbose_name='uuid')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
                ('deletedAt', models.DateTimeField(null=True, verbose_name='deletedAt')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='updatedAt')),
                ('academic', models.CharField(choices=[(None, 'Unknown'), ('HIGHSCHOOL', 'HIGHSCHOOL'), ('PHD', 'PHD'), ('GRADUATE', 'GRADUATE'), ('UNDERGRADUATE_1_2', 'UNDERGRADUATE_1_2'), ('UNDERGRADUATE_3_4', 'UNDERGRADUATE_3_4')], default=None, help_text='Client default academic level', max_length=17, null=True)),
                ('native', models.BooleanField(help_text='Client Only wants native English writers to work on their order')),
                ('topic', models.CharField(help_text='Topic a would like to always requests their paper to be done', max_length=200, null=True)),
                ('paper', models.CharField(help_text='type of paper a would like to always requests their paper to be done', max_length=200, null=True)),
                ('format', models.CharField(help_text='Paper format a would like to always requests their paper to be done', max_length=200, null=True)),
                ('user', models.ForeignKey(default=None, limit_choices_to={'is_active': True, 'is_staff': False}, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Default',
                'verbose_name_plural': 'Defaults',
                'db_table': 'Default',
            },
        ),
    ]
