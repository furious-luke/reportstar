from django.db import models
from django.utils.translation import ugettext_lazy as _
from questionnaire.models import Subject

class Project(models.Model):
    account = models.CharField(max_length=64, unique=True, verbose_name=_('Account code'))
    leader = models.ForeignKey(Subject, null=True, blank=True, related_name='leading')
    name = models.CharField(max_length=256, null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    members = models.ManyToManyField(Subject, null=True, blank=True, realted_name='member_of')
    cpu_usage = models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name=_('CPU hour usage'))
    disk_quota = models.DecimalField(decimal_places=4, max_digits=10, default=0)
    disk_usage = models.DecimalField(decimal_places=4, max_digits=10, default=0)
