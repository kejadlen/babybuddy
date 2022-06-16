# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

from hypothesis import given, settings
import hypothesis.strategies as st
from hypothesis.extra.django import TestCase

from core import models
from reports.graphs import sleep_pattern


class SleepPatternTestCase(TestCase):
    @given(
            st.timezones(),
            st.datetimes(timezones=st.timezones()),
            st.lists(
                st.tuples(
                    st.integers(min_value=1, max_value=1000),
                    st.integers(min_value=1, max_value=200),
                ),
                min_size=1,
            )
    )
    @settings(deadline=None)
    def test_fuzz_sleep_pattern(self, user_tz, start_dt, sleeps_raw):
        c = models.Child(birth_date=datetime.now())
        c.save()

        original_tz = timezone.get_current_timezone()
        timezone.activate(user_tz)

        last_sleep_end = start_dt
        for delta, duration in sleeps_raw:
            start = last_sleep_end + timedelta(minutes=delta)
            end = start + timedelta(minutes=duration)
            last_sleep_end = end
            models.Sleep.objects.create(
                child=c,
                start=start,
                end=end,
            )

        sleep_pattern(models.Sleep.objects.order_by("start"))

        timezone.activate(original_tz)
