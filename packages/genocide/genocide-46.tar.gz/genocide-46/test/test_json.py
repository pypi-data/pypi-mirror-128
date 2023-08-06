# This file is placed in the Public Domain.

import unittest

from gcd.obj import Object, dumps

class Test_JSON(unittest.TestCase):
    def test_jsondump(self):
        o = Object()
        o.test = "bla"
        self.assertEqual(dumps(o), '{"test": "bla"}')
