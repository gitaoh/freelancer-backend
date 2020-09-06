from django.test import TestCase
import api.base as settings
import os


class BaseSettingsTestCase(TestCase):
    """
    All tests for the base.py settings file
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

    def test_middleware(self):
        self.assertEqual(len(self.config.MIDDLEWARE), 12)

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

    def test_the_root_url_(self):
        """
        ROOT_URLCONF should be api.urls
        """
        self.assertEqual(self.config.ROOT_URLCONF, 'api.urls')

    def test_mere_code_set_(self):
        self.assertEqual(self.config.WSGI_APPLICATION, 'api.wsgi.application')
        self.assertTrue(self.config.USE_TZ)
        self.assertTrue(self.config.USE_L10N)
        self.assertTrue(self.config.CORS_ALLOW_CREDENTIALS)
        self.assertTrue(self.config.USE_I18N)
        self.assertEqual(self.config.LANGUAGE_CODE, 'en-us')
        self.assertEqual(self.config.TIME_ZONE, 'UTC')

    def test_static_urls_(self):
        self.assertEqual(self.config.STATIC_URL, '/static/')
        self.assertEqual(self.config.MEDIA_ROOT, os.path.join(self.config.BASE_DIR, "media"))
        self.assertEqual(self.config.STATIC_ROOT, os.path.join(self.config.BASE_DIR, "staticfiles"))

    def test_rest_framework_config(self):
        """
        Rest framework configurations
        """
        conf = self.config.REST_FRAMEWORK
        self.assertEqual(len(conf['DEFAULT_AUTHENTICATION_CLASSES']), 1)
        self.assertEqual(conf['DEFAULT_AUTHENTICATION_CLASSES'][0], 'knox.auth.TokenAuthentication')
        self.assertEqual(len(conf['DEFAULT_PERMISSION_CLASSES']), 1)
        self.assertEqual(conf['DEFAULT_PERMISSION_CLASSES'][0], 'rest_framework.permissions.AllowAny')
