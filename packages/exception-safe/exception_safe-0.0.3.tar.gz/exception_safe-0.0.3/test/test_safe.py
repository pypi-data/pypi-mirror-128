from unittest import TestCase
from safe import safe

def boom():
    raise Exception()

def non_boom():
    return 1


class TestSafe(TestCase):
    
    def test_boom(self):
        self.assertIsNone(safe(lambda: boom()))
    
    def test_non_boom(self):
        self.assertEqual(1, safe(lambda: non_boom()))