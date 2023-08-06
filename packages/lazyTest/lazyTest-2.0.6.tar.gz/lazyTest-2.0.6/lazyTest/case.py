# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : case.py
# Describe :
# ---------------------------------------
import pytest


class TestCase:

    @pytest.fixture(scope="function")
    def setUp(self, getdriver): ...
