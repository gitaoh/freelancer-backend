from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from app.abstract import MinimalModel
from app.choices import AdminCategory
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.utils.timezone import now
from order.choices import EducationLevelChoices
from order.models import Writer
from django.core.validators import MaxValueValidator
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    send_mail(
        # title:
        "Joseph Gitau {title}".format(title="Kromon"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class User(AbstractUser, MinimalModel):
    """ Model for Users """
    phone_number = models.CharField(_("phone number"), max_length=15, null=True, unique=True,
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

    updates = models.BooleanField(_("updates"), default=True, help_text=_("Send updates to user about our services"))
    user_type = models.CharField(_('type'), default=AdminCategory.USER, choices=AdminCategory.choices, max_length=6,
                                 help_text=_('Define the type of the user :User always'))
    terms = models.BooleanField(_("terms"), default=True, help_text=_("Agreement on our platform terms and conditions"))
    # TODO: Loop over the data to find the different discipline/ topics the user like to order their paper with.
    # discipline = models.ManyToManyField(verbose_name="disciplines", to=app.Discipline, blank=True)
    # topic = models.ManyToManyField(verbose_name="topics", to=app.PaperType, blank=True)
    email = models.EmailField(_("email"), max_length=254, null=False, unique=True,
                              validators=[MaxLengthValidator(limit_value=254, message="Email is too long")])

    def __str__(self):
        return self.username

    def deactivate(self):
        """ Deactivate/Mark Deleted """
        self.is_active = False
        self.deletedAt = now()
        self.is_staff = False
        self.is_superuser = False
        self.save()
        return

    @property
    def active(self):
        """ Check is a user has a state of is_active """
        return self.is_active

    def make_admin(self):
        """ Convert a User/Mater To Admin """
        self.user_type = AdminCategory.ADMIN
        self.is_staff = True
        self.is_superuser = True
        self.save()
        return

    def make_master(self):
        """ Convert a User/Admin To master Admin """
        self.user_type = AdminCategory.MASTER
        self.is_staff = True
        self.is_superuser = True
        self.save()
        return

    def make_user(self):
        """ Convert a Master/Admin To a user """
        self.user_type = AdminCategory.USER
        self.is_staff = False
        self.is_superuser = False
        self.save()
        return

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")
        db_table = "User"


class Avatar(MinimalModel):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, null=False, to_field='username',
                             limit_choices_to={'is_active': True})
    # Todo: The default avatar should be handled on the frontend if the user does not upload their own.
    avatar = models.ImageField(upload_to="Avatar/", )
    is_avatar = models.BooleanField(help_text="If an avatar is deleted", default=True)

    def __str__(self):
        return self.user.username

    def hidden(self):
        """ Set avatar to hidden state """
        self.is_avatar = False
        self.deletedAt = now()
        self.save()

    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _("Avatars")
        db_table = "Avatar"
        ordering = ('-createdAt',)


class Defaults(MinimalModel):
    """ Defaults that a User can place """
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, null=True, default=None,
                             limit_choices_to={'is_active': True, 'is_staff': False}, to_field='username')
    writer = models.ForeignKey(to_field='username', to=Writer, on_delete=models.SET_DEFAULT, default=None,
                               limit_choices_to={'is_active': True}, null=True)
    academic = models.CharField(choices=EducationLevelChoices.choices, default=EducationLevelChoices.__empty__,
                                null=False, max_length=17, help_text=_('Client default academic level'))
    native = models.BooleanField(help_text=_('Client Only wants native English writers to work on their order'),
                                 default=False, null=False)
    topic = models.CharField(max_length=200, null=True,
                             help_text=_("Topic a would like to always requests their paper to be done"))
    paper = models.CharField(max_length=200, null=True,
                             help_text=_("type of paper a would like to always requests their paper to be done"))
    format = models.CharField(max_length=200, null=True,
                              help_text=_("Paper format a would like to always requests their paper to be done"))

    def __str__(self):
        return f'{self.user} -> {self.writer}'

    class Meta:
        verbose_name = "Default"
        verbose_name_plural = "Defaults"
        db_table = 'Default'


class Rating(MinimalModel):
    """ Custom rating from the user when they delete their account """
    # Not more tha 10 in count
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=10)])
    client = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', on_delete=models.PROTECT,
                               null=False)

    def __str__(self):
        return f"{self.rate}, {self.client}"

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        db_table = 'Rating'
