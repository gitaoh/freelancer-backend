from django.contrib.auth.validators import UnicodeUsernameValidator
from app.abstract import MinimalModel
from django.db import models
from .choices import (
    NotificationChoices, PreferencesChoices, SpacingChoices, FormatChoices, StatusChoices,
    EducationLevelChoices)
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
                                error_messages={'unique': _("A user with this username already exists.")})
    first_name = models.CharField(_('first name'), max_length=30, help_text=_("Writer first name."))
    last_name = models.CharField(_('last name'), max_length=150, help_text=_("Writer last name."))
    email = models.EmailField(_('email address'), unique=True, help_text=_("Writer email."))
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
        self.deletedAt = now()
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
        ordering = ('-createdAt',)


class Files(MinimalModel):
    """
    File uploaded to an order
    """
    description = models.CharField(max_length=200, null=True,
                                   help_text='Client description of what this files contains')
    file = models.FileField(help_text="Please add files if you have any.", upload_to='files')
    is_deleted = models.BooleanField(default=False, help_text=_('if file is deleted or not'))

    def __str__(self):
        return self.description

    def deleted(self):
        """
        Orders are set to is_deleted=True to signify that they are deleted
        """
        self.is_deleted = True
        self.deletedAt = now()
        self.save()

    def restore(self):
        """
        Orders are set to is_deleted=False to signify that they are not deleted
        """
        self.is_deleted = False
        self.save()

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        db_table = "File"
        ordering = ('-createdAt',)


class Order(MinimalModel):
    """
    Model for orders
    """
    card = models.CharField(null=False, help_text='Order_id_card', max_length=10)
    writer = models.ForeignKey(verbose_name="writer", to=Writer, on_delete=models.PROTECT,
                               limit_choices_to={'is_active': True, }, to_field='username', null=True, default=None,
                               help_text=_('Who is assigned to work on this order'))
    user = models.ForeignKey(verbose_name="user", to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             limit_choices_to={'is_active': True, 'is_staff': False}, to_field='username',
                             null=False, help_text=_('Client Placing the order'))
    paper_type = models.CharField(_("paper_type"), max_length=200, null=False, help_text=_('This order paper type'))
    discipline = models.CharField(_("discipline"), max_length=200, null=False, help_text=_('This orders discipline'))
    academic = models.CharField(_("academic"), choices=EducationLevelChoices.choices, max_length=17, null=False,
                                default=EducationLevelChoices.HIGHSCHOOL, help_text=_('Clients academic level'))
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
    rate = models.PositiveIntegerField(null=True, default=0,
                                       help_text=_('Rating of how a paper was done by this writer'))
    confirmed = models.BooleanField(_('confirmed'), default=False,
                                    help_text=_('Whether an order is confirmed that is can be done.'))
    dispute = models.BooleanField(_('dispute'), default=False, help_text=_('Whether an order is or was a dispute.'))
    revision = models.BooleanField(_('revision'), default=False, help_text=_('Whether an order is or was a revision.'))
    is_paper = models.BooleanField(_('is_paper'), default=True, help_text=_('Whether a paper id deleted/canceled.'))
    is_approved = models.BooleanField(_('is_approved'), default=False,
                                      help_text=_('Whether a paper is approved or not approved.'))
    deleted_by = models.ForeignKey(verbose_name="writer", to=Writer, on_delete=models.PROTECT, default=None,
                                   limit_choices_to={'is_active': True, 'is_superuser': True, 'is_staff': True,
                                                     'user_type': 'MASTER'}, to_field='username', null=True,
                                   help_text=_('Who deleted this order'), related_name='deleted_by')

    def __str__(self):
        return f"{self.discipline}, {self.paper_type}"

    def trash(self):
        """ Delete/trash an order """
        self.is_paper = False
        self.deletedAt = now()
        self.save()

    def cancel(self):
        """ Allow users to cancel an order they had canceled """
        self.is_paper = False
        self.status = StatusChoices.CANCELED
        self.save()

    def un_cancel(self):
        """ Allow users to un_cancel an order they had canceled """
        self.is_paper = True
        self.status = StatusChoices.DRAFT
        self.save()

    def files(self):
        """ Order additional materials """
        return self.additional_materials

    def approve(self):
        self.is_approved = True
        self.save()

    def un_approve(self):
        self.is_approved = False
        self.save()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")
        db_table = "Order"
        ordering = ('-createdAt',)


class Notification(MinimalModel):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', on_delete=models.PROTECT,
                             default=None, null=True,
                             limit_choices_to={'is_active': True, 'user_type': 'USER', 'is_staff': False,
                                               'is_superuser': False},
                             help_text=_('User to be sent this notification'))
    content = models.TextField(help_text=_('Notification message'), max_length=10000)
    created = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field="username", on_delete=models.PROTECT,
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
    is_notify = models.BooleanField(help_text="if a notification is deleted or active", default=True)

    def __str__(self):
        return f"{self.user}, {self.read}"

    def hidden(self):
        self.is_notify = False
        self.deletedAt = now()
        self.save()

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        db_table = "Notification"
        ordering = ('-createdAt',)


class Cancel(MinimalModel):
    """
    Handel all the reasons that a user can input to describe why they want to cancel an order
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', limit_choices_to={"is_active": True},
                             on_delete=models.PROTECT, null=False)
    # Todo on th frontend give the user a select ui and then post the selected reason
    reason = models.CharField(max_length=200, null=False)
    order = models.ForeignKey(to=Order, to_field='uuid', on_delete=models.PROTECT, null=False,
                              limit_choices_to={'is_paper': True, 'is_approved': False})
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reason

    def trash(self):
        self.is_active = False
        self.deletedAt = now()
        self.save()

    class Meta:
        db_table = 'Cancel'
        verbose_name = 'Cancel'
        verbose_name_plural = 'Cancels'
