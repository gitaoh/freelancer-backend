import datetime
from django.test import TestCase
import api.local as settings


class SettingsFileTestcase(TestCase):
    """
    Test settings configurations
    """

    @classmethod
    def setUpTestData(cls):
        cls.config = settings

    def test_allowed_host_is_empty(self):
        conf = self.config.ALLOWED_HOSTS
        self.assertEqual(len(conf), 0)

    def test_CORS_ORIGIN_WHITELIST(self):
        conf = self.config.CORS_ORIGIN_WHITELIST
        self.assertEqual(len(list(conf)), 1)
        self.assertEqual(list(conf)[0], 'http://127.0.0.1:3000')

    def test_email_backend(self):
        self.assertEqual(self.config.EMAIL_BACKEND, 'django.core.mail.backends.console.EmailBackend')

    def test_the_local_cors_origin_whitelist_url(self):
        self.assertEqual(len(list(self.config.CORS_ORIGIN_WHITELIST)), 1)
        self.assertEqual(list(self.config.CORS_ORIGIN_WHITELIST)[0], 'http://127.0.0.1:3000')

    def test_email_config_(self):
        self.assertEqual(self.config.DEFAULT_FROM_EMAIL, 'example@gmail.com')
        self.assertEqual(self.config.EMAIL_HOST, 'smtp.mailtrap.io')
        self.assertEqual(self.config.EMAIL_PORT, '465')
        self.assertEqual(self.config.EMAIL_HOST_USER, '04395d2e790d4d')
        self.assertEqual(self.config.EMAIL_HOST_PASSWORD, '6ac9ea9db1be70')
        self.assertFalse(self.config.EMAIL_USE_SSL)
        self.assertTrue(self.config.EMAIL_USE_TLS)

    def test_rest_knox_config_(self):
        conf = self.config.REST_KNOX
        self.assertEqual(conf['TOKEN_TTL'], datetime.timedelta(days=3))
        self.assertEqual(conf['EXPIRY_DATETIME_FORMAT'], 'iso-8601')
        self.assertEqual(conf['AUTH_TOKEN_CHARACTER_LENGTH'], 128)
        self.assertEqual(conf['TOKEN_LIMIT_PER_USER'], 10)
        self.assertTrue(conf['AUTO_REFRESH'])
