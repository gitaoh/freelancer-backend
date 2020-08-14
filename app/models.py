from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from app.abstract import MinimalModel
from app.choices import NotificationChoices, PreferencesChoices, SpacingChoices, FormatChoices, StatusChoices, \
    EducationLevelChoices
from django.conf import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Discipline(MinimalModel):
    """
    Register a new discipline
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _("Disciplines")
        db_table = "Discipline"


class PaperType(MinimalModel):
    """
    Register a paper type
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('PaperType')
        verbose_name_plural = _("PaperTypes")
        db_table = "PaperType"


class OrderFiles(MinimalModel):
    fileDescription = models.CharField(max_length=200, blank=True, null=True)
    paper_files = models.FileField(help_text="Please add files if you have any.", upload_to='files')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.fileDescription

    def deleted(self):
        self.is_deleted = True
        self.save()

    def restore(self):
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
                             null=True, default=0)
    paper_type = models.CharField(_("paper_type"), max_length=200, null=False, blank=False)
    discipline = models.CharField(_("discipline"), max_length=200, null=False, blank=False, )
    academic = models.CharField(_("academic"), choices=EducationLevelChoices.choices,
                                default=EducationLevelChoices.HIGHSCHOOL, max_length=200, null=False, blank=False, )
    title = models.CharField(_("title"), max_length=200, null=False, blank=False)
    instructions = models.TextField()
    additional_materials = models.ManyToManyField(OrderFiles, blank=True)

    format = models.CharField(choices=FormatChoices.choices, default=FormatChoices.MLA, blank=False,
                              max_length=30)
    spacing = models.CharField(choices=SpacingChoices.choices, default=SpacingChoices.SINGLE, blank=False,
                               max_length=10)
    preference = models.CharField(choices=PreferencesChoices.choices, default=PreferencesChoices.BEST, blank=False,
                                  max_length=20)
    # Todo Needs WORK
    deadline = models.DateTimeField(default=timezone.now)
    pages = models.PositiveIntegerField()
    sources = models.PositiveIntegerField()
    charts = models.PositiveIntegerField()
    powerpoint = models.PositiveIntegerField()
    native = models.BooleanField(default=False)
    smart = models.BooleanField(default=False)
    progressive = models.BooleanField(default=False)

    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=False, max_length=10)

    payments_url = models.URLField(_('payment_url'), blank=True, null=True, unique=True)

    cost = models.PositiveIntegerField(blank=True)

    # :notifications about this order
    is_smart_paper = models.BooleanField(
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
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


class Rating(MinimalModel):
    """
    Custom rating from the user when they delete their account
    """
    rate = models.PositiveIntegerField()
    client = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username', on_delete=models.SET_DEFAULT,
                               default='deleted')

    def __str__(self):
        return f"{self.rate}{self.client}"

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        db_table = 'Rating'
