#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import unittest
import re
from noipy import dnsupdater

class Test(unittest.TestCase):

    def test_get_ip(self):
        ip = dnsupdater.get_ip()
        valid_ip_regex = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
        self.assertTrue(re.match(valid_ip_regex, ip), 'get_ip() failed.')


if __name__ == "__main__":
    unittest.main()
