# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..core.validators import MsisdnValidator


class MsisdnValidatorTests(TestCase):
    def test_no_plus(self):
        with self.assertRaises(ValidationError):
            MsisdnValidator()("48 601 123 123")
        with self.assertRaises(ValidationError):
            MsisdnValidator()("48601123123")

    def test_pl(self):
        MsisdnValidator()("+48 601 123 123")
        MsisdnValidator()("+48601123123")
        MsisdnValidator()("+48 22 751 12 12")
        MsisdnValidator()("+48 801 123 123")
        MsisdnValidator()("+48 22 234 7497")

    def test_usa(self):
        MsisdnValidator()("+1 310 997 62 24")
