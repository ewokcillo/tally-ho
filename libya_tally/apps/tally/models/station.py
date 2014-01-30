from django.db import models
from django_enumfield import enum

from libya_tally.libs.models.base_model import BaseModel
from libya_tally.libs.models.enums.gender import Gender


class Station(BaseModel):
    class Meta:
        app_label = 'tally'

    center = models.ForeignKey('Center')
    sub_constituency = models.ForeignKey('SubConstituency')

    code = models.PositiveSmallIntegerField()  # aka number
    gender = enum.EnumField(Gender)
    registrants = models.PositiveIntegerField()
    station_number = models.PositiveIntegerField()
