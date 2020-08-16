from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from app.abstract import MinimalModel
from app.choices import AdminCategory
import app.models as app
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from order.choices import EducationLevelChoices
from order.models import Writer


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Kromon"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class User(AbstractUser, MinimalModel):
    """
    Model for Users
    """
    phone_number = models.CharField(_("phone number"), max_length=15, null=True, blank=True, unique=True,
                                    help_text="Ensure you Phone number only contain numbers",
                                    validators=[
                                        MaxLengthValidator(limit_value=15,
                                                           message="Phone number is too large max length is 15 digits"),
                                        RegexValidator(
                                            regex='^[0-9]*$',
                                            message="Phone number should only contain numbers",
                                            code="Invalid Phone Number Entered",
                                            inverse_match=False)
                                    ])

    updates = models.BooleanField(
        _("updates"),
        default=True,
        help_text=_(
            "Send updates to user about our services"
        ),
    )
    user_type = models.CharField(
        _('type'),
        default=AdminCategory.USER,
        choices=AdminCategory.choices,
        max_length=6,
        help_text=_(
            'Define the type of the user :User always'
        ),
    )
    terms = models.BooleanField(
        _("terms"),
        default=True,
        help_text=_(
            "Agreement on our platform terms and conditions"
        ),
    )
    # TODO: Loop over the data to find the different discipline/ topics the user like to order their paper with.
    # discipline = models.ManyToManyField(verbose_name="disciplines", to=app.Discipline, blank=True)
    # topic = models.ManyToManyField(verbose_name="topics", to=app.PaperType, blank=True)
    email = models.EmailField(_("email"), max_length=254, null=False, blank=False, unique=True,
                              validators=[MaxLengthValidator(limit_value=254, message="Email is too long")])

    def __str__(self):
        return self.username

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.deletedAt = timezone.now
            self.save()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")
        db_table = "User"


class Avatar(MinimalModel):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=1)
    # Todo: The default avatar should be handled on the frontend if the user does not upload their own.
    avatar = models.FileField(upload_to="Avatar/")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _("Avatars")
        db_table = "Avatar"


class Defaults(MinimalModel):
    """
    Defaults tah a User can place
    """
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=0,
                             limit_choices_to={'is_active': True, 'is_staff': False}, to_field='username')
    writer = models.ForeignKey(to_field='username', to=Writer, on_delete=models.SET_DEFAULT, default=0,
                               limit_choices_to={'is_active': True})
    academic = models.CharField(choices=EducationLevelChoices.choices, default=None, null=True, blank=True,
                                max_length=17, help_text=_('Client default academic level'))
    native = models.BooleanField(help_text=_('Client Only wants native English writers to work on their order'))
    topic = models.CharField(max_length=200, null=True, blank=True,
                             help_text=_("Topic a would like to always requests their paper to be done"))
    paper = models.CharField(max_length=200, null=True, blank=True,
                             help_text=_("type of paper a would like to always requests their paper to be done"))
    format = models.CharField(max_length=200, null=True, blank=True,
                              help_text=_("Paper format a would like to always requests their paper to be done"))

    def __str__(self):
        return f'{self.user} -> {self.writer}'

    class Meta:
        verbose_name = "Default"
        verbose_name_plural = "Defaults"
        db_table = 'Defaults'
