from django.contrib.auth.validators import UnicodeUsernameValidator
from app.abstract import MinimalModel
from django.db import models
from .choices import NotificationChoices, PreferencesChoices, SpacingChoices, FormatChoices, StatusChoices, \
    EducationLevelChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.timezone import now


class Writer(MinimalModel):
    """
    Virtual Writer's
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=150, unique=True, validators=[username_validator],
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _("A user with that username already exists.")})
    first_name = models.CharField(_('first name'), max_length=30, blank=True, help_text=_("Writer first name."))
    last_name = models.CharField(_('last name'), max_length=150, blank=True, help_text=_("Writer last name."))
    email = models.EmailField(_('email address'), blank=False, unique=True, help_text=_("Writer email."))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Writer is active/deactivated'))
    level = models.CharField(choices=PreferencesChoices.choices, default=PreferencesChoices.STANDARD, max_length=8,
                             help_text=_("Experience level of the writer"))

    def __str__(self):
        return self.username

    def deactivate(self):
        """
        Deactivate writers account
        """
        self.is_active = False
        self.save()

    def activate(self):
        """
        Activate writer's Account
        """
        self.is_active = True
        self.save()

    class Meta:
        verbose_name = 'Writer'
        verbose_name_plural = 'Writers'
        db_table = 'Writer'


class Files(MinimalModel):
    """
    File uploaded to an order
    """
    # order = models.ForeignKey(to=Order, to_field='card', on_delete=models.SET_DEFAULT, default='deleted',
    #                           limit_choices_to={'is_paper': True}, help_text=_('Link to the order'))
    description = models.CharField(max_length=200, blank=True, null=True,
                                   help_text='Client description of what this files contains')
    file = models.FileField(help_text="Please add files if you have any.", upload_to='files')
    is_deleted = models.BooleanField(default=False, help_text=_('if file is deleted or not'))

    def __str__(self):
        return self.description

    def deleted(self):
        """
        Orders are set to is_deleted=True to signify that they are deleted
        :return:
        """
        self.is_deleted = True
        self.save()

    def restore(self):
        """
        Orders are set to is_deleted=False to signify that they are not deleted
        :return:
        """
        self.is_deleted = False
        self.save()

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        db_table = "File"


class Order(MinimalModel):
    """
    Model for orders
    """
    # card = models.CharField(max_length=10, unique=True, blank=False, null=False, default='not card',
    #                         help_text=_('Order unique number'))
    writer = models.ForeignKey(verbose_name="writer", to=Writer, on_delete=models.SET_DEFAULT,
                               limit_choices_to={'is_active': True, }, to_field='username', default=None, null=True,
                               help_text=_('Who is assigned to work on this order'))
    user = models.ForeignKey(verbose_name="user", to=settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT,
                             limit_choices_to={'is_active': True, 'is_staff': False}, to_field='username', default=None,
                             null=True, help_text=_('Client Placing the order'))
    paper_type = models.CharField(_("paper_type"), max_length=200, null=False,
                                  help_text=_('This order paper type'))
    discipline = models.CharField(_("discipline"), max_length=200, null=False,
                                  help_text=_('This orders discipline'))
    academic = models.CharField(_("academic"), choices=EducationLevelChoices.choices,
                                default=EducationLevelChoices.HIGHSCHOOL, max_length=17, null=False, blank=False,
                                help_text=_('Clients academic level'))
    format = models.CharField(choices=FormatChoices.choices, default=FormatChoices.MLA, null=False,
                              max_length=16, help_text=_('Format chosen by client for this order, eg. MLA, APA6...'))
    spacing = models.CharField(choices=SpacingChoices.choices, default=SpacingChoices.SINGLE, null=False, max_length=6,
                               help_text=_('Whether order is single or double spaced'))
    preference = models.CharField(choices=PreferencesChoices.choices, default=PreferencesChoices.STANDARD,
                                  max_length=20,
                                  help_text=_('The writer preference a the client chose for this order.'))
    powerpoint = models.PositiveIntegerField(default=0,
                                             help_text=_('Number of powerpoints requested in the current order'))
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE, max_length=10,
                              help_text=_('Where an order belongs to ether active, deleted, or ..'))

    payments_url = models.URLField(_('payment_url'), null=True, unique=True,
                                   help_text=_('A payment url to verify user paid the order'))
    title = models.CharField(_("title"), max_length=200, null=False, help_text=_('This orders title'))
    instructions = models.TextField(help_text=_('This paper instructions'))
    additional_materials = models.ManyToManyField(Files, limit_choices_to={'is_deleted': False})
    deadline = models.DateTimeField(default=timezone.now, help_text=_('The deadline of this order'))
    pages = models.PositiveIntegerField(default=0, help_text=_('Number of pages requested in the current order'))
    sources = models.PositiveIntegerField(default=0, help_text=_('Number of sources requested in the current order'))
    charts = models.PositiveIntegerField(default=0, help_text=_('Number of charts requested in the current order'))
    native = models.BooleanField(default=False, help_text=_('To a assign a native writer for the current order'))
    progressive = models.BooleanField(default=False, help_text=_('If order is a progressive delivery'))
    cost = models.PositiveIntegerField(default=0, help_text=_('The cost of a paper'))
    smart = models.BooleanField(_('is_smart'), default=False, help_text=_('Whether an order is  a smart paper.'))
    paid = models.BooleanField(_('paid'), default=False, help_text=_('Whether an order is paid or not.'))
    confirmed = models.BooleanField(_('confirmed'), default=False, help_text=_('Whether an order is confirmed.'))
    dispute = models.BooleanField(_('dispute'), default=False, help_text=_('Whether an order is or was a dispute.'))
    revision = models.BooleanField(_('revision'), default=False, help_text=_('Whether an order is or was a revision.'))
    is_paper = models.BooleanField(_('is_paper'), default=True, help_text=_('Whether a paper id deleted/canceled.'))

    def __str__(self):
        return f"{self.discipline}, {self.paper_type}"

    def trash(self):
        self.is_paper = False
        self.deletedAt = now()
        self.save()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")
        db_table = "Order"
        order_with_respect_to = 'user'
        # ordering = 'createdAt'


class Notification(MinimalModel):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', on_delete=models.SET_NULL,
                             default=None, null=True, limit_choices_to={'is_active': True, 'user_type': 'USER'},
                             help_text=_('User to be sent this notification'))
    content = models.TextField(help_text=_('Notification message'), max_length=10000)
    created = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field="username", on_delete=models.SET_NULL,
                                default=None, null=True, related_name='created', related_query_name='creator',
                                help_text=_('Which admin created'),
                                limit_choices_to={'is_active': True, 'user_type': ['MASTER', 'ADMIN']})
    notify = models.CharField(choices=NotificationChoices.choices, default=NotificationChoices.NOTIFICATION,
                              max_length=12, help_text=_('Type of notification to send the user'))
    """
    If Update a Drop down 
    If Notification a Message 
    """
    read = models.BooleanField(default=False, help_text=_('If notifications is read or unread'))

    def __str__(self):
        return f"{self.user}, {self.read}"

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        db_table = "Notification"
