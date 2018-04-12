'''tests/validate.py'''
import unittest
from application.views.validate import Validate

class ValidateTestCase(unittest.TestCase):
    '''class representing Validate test case'''
    def setUp(self):
        self.validate = Validate()

    def test_validate_email(self):
        '''test to validate email'''
        result = self.validate.validate_email("n@h.com")
        self.assertEqual("n@h.com", result)
        result2 = self.validate.validate_email("qw")
        self.assertEqual("Enter a valid email address", result2["message"])

    def test_validate_password(self):
        '''test to validate password'''
        result = self.validate.validate_password("Test123", "Test123")
        self.assertEqual("Test123", result)
        result2 = self.validate.validate_password("Test", "Test")
        self.assertEqual("password is too short", result2["message"])
        result3 = self.validate.validate_password("test123", "test123")
        self.assertEqual(
            "password must contain a mix of upper and lowercase letters", result3["message"])
        result4 = self.validate.validate_password("Testtest", "Testtest")
        self.assertEqual(
            "password must contain atleast one numeric or special character", result4["message"])
        result5 = self.validate.validate_password("Test123", "Test")
        self.assertEqual("Passwords don't match", result5["message"])

    def test_validate_name(self):
        '''test to validate name'''
        result = self.validate.validate_name("Njeri Ngigi")
        self.assertEqual("Njeri Ngigi", result)
        result2 = self.validate.validate_name("Njeri Ngigi!")
        self.assertEqual(
            "Name cannot contain special characters and numbers", result2["message"])
        result3 = self.validate.validate_name("Njeri34 Ngigi12")
        self.assertEqual(
            "Name cannot contain special characters and numbers", result3["message"])

    def test_validate_registration_data(self):
        '''test to validate registration data'''
        result = self.validate.validate_register(
            "njery", "Njeri Ngigi", "n@h.com", "Test123", "Test123")
        self.assertEqual("n@h.com", result["email"])
        result2 = self.validate.validate_register(
            "    ", "Njeri Ngigi", "n@h.com", "Test123", "Test123")
        self.assertEqual("Enter valid data", result2["message"])
        result3 = self.validate.validate_register(
            "njery", "Njeri Ngigi", "n@h", "Test123", "Test123")
        self.assertEqual("Enter a valid email address", result3["message"])
