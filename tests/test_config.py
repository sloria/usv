from unittest import TestCase
from nose.tools import *

from ConfigParser import SafeConfigParser


class ConfigTest(TestCase):
    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./tests/config_example.txt')

    def test_can_get_setting(self):
        assert_equal(self.config.get('training', 'train_path'),
                    '/Users/johndoe/projects/usv/trainsets')
