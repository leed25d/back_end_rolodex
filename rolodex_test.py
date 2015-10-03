import unittest
from rolodex import Rolodex

class RolodexTest(unittest.TestCase):

    def testCreation(self):
      self.assertIsNotNone(Rolodex())

