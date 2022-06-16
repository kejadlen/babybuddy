# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase
from django.utils import timezone

from core import models
from reports.graphs import sleep_pattern


class SleepPatternTestCase(TestCase):
    def setUp(self):
        self.original_tz = timezone.get_current_timezone()
        self.tz = ZoneInfo("America/Los_Angeles")
        timezone.activate(self.tz)

    def tearDown(self):
        timezone.activate(self.original_tz)

    def test_sleep_pattern(self):

        c = models.Child(birth_date=datetime.now())
        c.save()

        s = models.Sleep.objects.create(
            child=c,
            start=datetime(2021, 8, 14, 19, 37, tzinfo=self.tz),
            end=datetime(2021, 8, 14, 19, 53, tzinfo=self.tz),
        )
        s = models.Sleep.objects.create(
            child=c,
            start=datetime(2022, 6, 16, 19, 37, tzinfo=self.tz),
            end=datetime(2022, 6, 16, 19, 53, tzinfo=self.tz),
        )

        sleep_pattern(models.Sleep.objects.order_by("start"))
