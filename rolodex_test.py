import unittest
from rolodex import Rolodex

class RolodexTest(unittest.TestCase):

    def testCreation(self):
      self.assertIsNotNone(Rolodex())

    def testOneGoodLIne(self):
        in_list= ['Noah, Moench, 123123121, 232 695 2394, yellow']
        expected_out= '''{
    "entries": [
        {
            "color": "yellow",
            "firstname": "Noah",
            "lastname": "Moench",
            "phonenumber": "232-695-2394",
            "zipcode": "123123121"
        }
    ],
    "errors": []
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)

    def testBadPhoneNumber(self):
        in_list= ['Noah, Moench, 123123121, 2324 695 2394, yellow']
        expected_out= '''{
    "entries": [],
    "errors": [
        0
    ]
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)

    def testTooManyFields(self):
        in_list= ['Noah, Moench, 123123121, 2324 695 2394, yellow, 35']
        expected_out= '''{
    "entries": [],
    "errors": [
        0
    ]
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)

    def testTooFewFields(self):
        in_list= ['Noah, Moench, 123123121']
        expected_out= '''{
    "entries": [],
    "errors": [
        0
    ]
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)

    def testOneGoodLineAndOneBadLine(self):
        in_list= [
            "Noah, Moench, 123123121, 232 695 2394, yellow, 35",
            "Ria Tillotson, aqua marine, 97671, 196 910 5548",
            ]
        expected_out= '''{
    "entries": [
        {
            "color": "aqua marine",
            "firstname": "Ria",
            "lastname": "Tillotson",
            "phonenumber": "196-910-5548",
            "zipcode": "97671"
        }
    ],
    "errors": [
        0
    ]
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)
    def testOrdering(self):
        in_list= [
            "Noah, Moench, 123123121, 232 695 2394, yellow",
            "Ria Tillotson, aqua marine, 97671, 196 910 5548",
            "Annalee, Loftis, 97296, 905 329 2054, blue",
            "James Johnston, gray, 38410, 628 102 3672",
            "Liptak, Quinton, (653)-889-7235, yellow, 70703",
            "0.547777482345",
            ]
        expected_out= '''{
    "entries": [
        {
            "color": "gray",
            "firstname": "James",
            "lastname": "Johnston",
            "phonenumber": "628-102-3672",
            "zipcode": "38410"
        },
        {
            "color": "yellow",
            "firstname": "Quinton",
            "lastname": "Liptak",
            "phonenumber": "653-889-7235",
            "zipcode": "70703"
        },
        {
            "color": "blue",
            "firstname": "Annalee",
            "lastname": "Loftis",
            "phonenumber": "905-329-2054",
            "zipcode": "97296"
        },
        {
            "color": "yellow",
            "firstname": "Noah",
            "lastname": "Moench",
            "phonenumber": "232-695-2394",
            "zipcode": "123123121"
        },
        {
            "color": "aqua marine",
            "firstname": "Ria",
            "lastname": "Tillotson",
            "phonenumber": "196-910-5548",
            "zipcode": "97671"
        }
    ],
    "errors": [
        5
    ]
}'''
        r= Rolodex(in_list)
        out= r.run()
        self.assertEqual(out, expected_out)
