from app.abstract import MinimalModel
from django.db import models
from app.choices import NotificationChoices, PreferencesChoices, SpacingChoices, FormatChoices, StatusChoices, \
    EducationLevelChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class OrderFiles(MinimalModel):
    """
    File uploaded to an order
    """
    fileDescription = models.CharField(max_length=200, blank=True, null=True)
    paper_files = models.FileField(help_text="Please add files if you have any.", upload_to='files')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.fileDescription

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
        verbose_name = _('OrderFile')
        verbose_name_plural = _('OrderFiles')
        db_table = "OrderFile"


# Order Model
class Order(MinimalModel):
    """
    Model for orders
    """
    user = models.ForeignKey(verbose_name="user", to=settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT,
                             null=True, default=0, help_text=_('Client Placing the order'))
    paper_type = models.CharField(_("paper_type"), max_length=200, null=False, blank=False,
                                  help_text=_('This order paper type'))
    discipline = models.CharField(_("discipline"), max_length=200, null=False, blank=False,
                                  help_text=_('This orders discipline'))
    # Can be made a s default setting on the front end
    academic = models.CharField(_("academic"), choices=EducationLevelChoices.choices,
                                default=EducationLevelChoices.HIGHSCHOOL, max_length=200, null=False, blank=False,
                                help_text=_('Clients academic level'))
    title = models.CharField(_("title"), max_length=200, null=False, blank=False, help_text=_('This orders title'))
    instructions = models.TextField(help_text=_('This paper instructions'))
    additional_materials = models.ManyToManyField(OrderFiles, blank=True)

    format = models.CharField(choices=FormatChoices.choices, default=FormatChoices.MLA, blank=False,
                              max_length=30, help_text=_('Format chosen by client for this order, eg. MLA, APA6...'))
    spacing = models.CharField(choices=SpacingChoices.choices, default=SpacingChoices.SINGLE, blank=False,
                               max_length=10, help_text=_('Whether order is single or double spaced'))
    preference = models.CharField(choices=PreferencesChoices.choices, default=PreferencesChoices.BEST, blank=False,
                                  max_length=20,
                                  help_text=_('The writer preference a the client chose for this order.'))
    # Todo Needs WORK
    deadline = models.DateTimeField(default=timezone.now, help_text=_('The deadline of this order'))
    pages = models.PositiveIntegerField(default=0, help_text=_('Number of pages requested in the current order'))
    sources = models.PositiveIntegerField(default=0, help_text=_('Number of sources requested in the current order'))
    charts = models.PositiveIntegerField(default=0, help_text=_('Number of charts requested in the current order'))
    powerpoint = models.PositiveIntegerField(default=0,
                                             help_text=_('Number of powerpoints requested in the current order'))
    native = models.BooleanField(default=False, help_text=_('To a assign a native writer for the current order'))
    progressive = models.BooleanField(default=False, help_text=_('If order is a progressive delivery'))

    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=False, max_length=10,
                              help_text=_('Where an order belongs to ether active, deleted, or ..'))

    payments_url = models.URLField(_('payment_url'), blank=True, null=True, unique=True,
                                   help_text=_('A payment url to verify user paid the order'))

    cost = models.PositiveIntegerField(default=0, help_text=_('The cost of a paper'))

    smart = models.BooleanField(
        default=False,
        help_text=_('Whether an order is  a smart paper.'),
    )
    paid = models.BooleanField(
        _('paid'),
        default=False,
        help_text=_('Whether an order is paid or not.'),
    )
    cancelled = models.BooleanField(
        _('cancelled'),
        default=False,
        help_text=_('Whether an order is cancelled.'),
    )
    draft = models.BooleanField(
        _('draft'),
        default=False,
        help_text=_('Whether to store an order as draft'),
    )
    orders_confirmed_status = models.BooleanField(
        default=False,
        help_text=_('Whether an order is confirmed.'),
    )
    dispute_status = models.BooleanField(
        default=False,
        help_text=_('Whether an order is or was a dispute.'),
    )
    revision_status = models.BooleanField(
        default=False,
        help_text=_('Whether an order is or was a revision.'),
    )
    is_paper = models.BooleanField(default=True, help_text=_('Whether a paper id deleted/canceled.'))

    def __str__(self):
        return f"{self.discipline}, {self.paper_type}"

    def trash(self):
        if self.is_paper:
            self.is_paper = False
            self.deletedAt = timezone.now
            self.save()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")
        db_table = "Order"


# Additional services
class Notification(MinimalModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=0)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="created_by")
    type_notify = models.CharField(choices=NotificationChoices.choices, default=NotificationChoices.NOTIFICATION,
                                   max_length=12)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, {self.read}"

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        db_table = "Notification"
