import datetime
import os
from django.test import TestCase
import api.settings as settings


class SettingsFileTestcase(TestCase):
    """
    Test settings configurations
    """

    @classmethod
    def setUpTestData(cls):
        cls.config = settings

    def test_auth_user_model(self):
        """
        Custom user model is the AUTH_USER_MODEL
        """
        self.assertEqual(self.config.AUTH_USER_MODEL, 'authapp.User')

    def test_secret_is_not_null(self):
        conf = self.config.SECRET_KEY
        self.assertIsNotNone(conf)
        self.assertTrue(len(conf) > 24)

    def test_allowed_host_is_empty(self):
        conf = self.config.ALLOWED_HOSTS
        print(conf)
        self.assertEqual(len(conf), 1)
        self.assertIn(member='*', container=conf)

    def test_middleware(self):
        self.assertEqual(len(self.config.MIDDLEWARE), 12)

    def test_CORS_ORIGIN_WHITELIST(self):
        conf = self.config.CORS_ORIGIN_WHITELIST
        self.assertEqual(len(list(conf)), 1)
        self.assertEqual(list(conf)[0], 'http://127.0.0.1:3000')

    def test_email_backend(self):
        self.assertEqual(settings.EMAIL_BACKEND, 'django.core.mail.backends.console.EmailBackend')

    def test_all_app_registered_(self):
        """
        All installed apps are register to django
        """
        apps = [
            'authapp.apps.AuthappConfig',
            'app.apps.AppConfig',
            'order.apps.OrderConfig'
        ]
        for i in apps:
            self.assertIn(i, container=self.config.INSTALLED_APPS)

    def test_dependency_app_registered(self):
        """
        All application dependent apps are register to django
        """
        apps = [
            'knox',
            'corsheaders',
            'rest_framework',
            'django_rest_passwordreset',
        ]
        for i in apps:
            self.assertIn(i, container=self.config.INSTALLED_APPS)

    def test_the_root_url_(self):
        """
        ROOT_URLCONF should be api.urls
        """
        self.assertEqual(self.config.ROOT_URLCONF, 'api.urls')

    def test_admins_not_none_(self):
        """
        Two admin are set with each having two field for email and name
        """
        admins = list(self.config.ADMINS)
        self.assertEqual(len(admins), 2)

        for i in admins:
            self.assertEqual(type(i), tuple)
            self.assertEqual(len(i), 2)

    def test_the_local_whitelist_url(self):
        self.assertEqual(len(list(self.config.WHITELIST_URL)), 1)
        self.assertEqual(list(self.config.WHITELIST_URL)[0], 'http://127.0.0.1:3000')

    def test_mere_code_set_(self):
        self.assertTrue(self.config.USE_TZ)
        self.assertTrue(self.config.USE_L10N)
        self.assertTrue(self.config.USE_I18N)
        self.assertEqual(self.config.LANGUAGE_CODE, 'en-us')
        self.assertEqual(self.config.TIME_ZONE, 'UTC')

    def test_static_urls_(self):
        self.assertEqual(self.config.STATIC_URL, '/static/')
        self.assertEqual(self.config.MEDIA_ROOT, os.path.join(self.config.BASE_DIR, "media"))
        self.assertEqual(self.config.STATIC_ROOT, os.path.join(self.config.BASE_DIR, "staticfiles"))

    def test_rest_knox_config_(self):
        conf = self.config.REST_KNOX
        self.assertEqual(conf['TOKEN_TTL'], datetime.timedelta(days=3))
        self.assertEqual(conf['EXPIRY_DATETIME_FORMAT'], 'iso-8601')
        self.assertEqual(conf['AUTH_TOKEN_CHARACTER_LENGTH'], 128)
        self.assertEqual(conf['TOKEN_LIMIT_PER_USER'], 10)
        self.assertTrue(conf['AUTO_REFRESH'])

    def test_rest_framework_config(self):
        """
        Rest framework configurations
        """
        conf = self.config.REST_FRAMEWORK
        self.assertEqual(len(conf['DEFAULT_AUTHENTICATION_CLASSES']), 1)
        self.assertEqual(conf['DEFAULT_AUTHENTICATION_CLASSES'][0], 'knox.auth.TokenAuthentication')
        self.assertEqual(len(conf['DEFAULT_PERMISSION_CLASSES']), 1)
        self.assertEqual(conf['DEFAULT_PERMISSION_CLASSES'][0], 'rest_framework.permissions.AllowAny')
