'''tests/validate.py'''
import unittest
from application.views.validate import Validate

class ValidateTestCase(unittest.TestCase):
    '''class representing Validate test case'''
    def setUp(self):
        self.validate = Validate()

    def test_validate_email(self):
        '''test to validate email'''
        #successful validate email
        result = self.validate.validate_email("n@h.com")
        self.assertEqual("n@h.com", result)
        #invalid email format
        result2 = self.validate.validate_email("qw")
        self.assertEqual("Enter a valid email address", result2["message"])

    def test_validate_password(self):
        '''test to validate password'''
        #successful validate password
        result = self.validate.validate_password("Test123", "Test123")
        self.assertEqual("Test123", result)
        #short password
        result2 = self.validate.validate_password("Test", "Test")
        self.assertEqual("password is too short", result2["message"])
        #short case only
        result3 = self.validate.validate_password("test123", "test123")
        self.assertEqual(
            "password must contain a mix of upper and lowercase letters", result3["message"])
        #upper case only
        result4 = self.validate.validate_password("TEST123", "TEST123")
        self.assertEqual(
            "password must contain a mix of upper and lowercase letters", result4["message"])
        #alphabetic characters only
        result5 = self.validate.validate_password("Testtest", "Testtest")
        self.assertEqual(
            "password must contain atleast one numeric or special character", result5["message"])
        #confirm_password different from password
        result6 = self.validate.validate_password("Test123", "Test")
        self.assertEqual("Passwords don't match", result6["message"])

    def test_validate_name(self):
        '''test to validate name'''
        #successful validate name
        result = self.validate.validate_name("Njeri Ngigi")
        self.assertEqual("Njeri Ngigi", result)
        #special character in name
        result2 = self.validate.validate_name("Njeri Ngigi!")
        self.assertEqual(
            "Name cannot contain special characters and numbers", result2["message"])
        #number in name
        result3 = self.validate.validate_name("Njeri34 Ngigi12")
        self.assertEqual(
            "Name cannot contain special characters and numbers", result3["message"])

    def test_validate_registration_data(self):
        '''test to validate registration data'''
        #successful register validate
        result = self.validate.validate_register(
            "njery", "Njeri Ngigi", "n@h.com", "Test123", "Test123")
        self.assertEqual("n@h.com", result["email"])
        #invalid white spaces in data
        result2 = self.validate.validate_register(
            "    ", "Njeri Ngigi", "n@h.com", "Test123", "Test123")
        self.assertEqual("Enter valid data", result2["message"])
        #invalid email address
        result3 = self.validate.validate_register(
            "njery", "Njeri Ngigi", "n@h", "Test123", "Test123")
        self.assertEqual("Enter a valid email address", result3["message"])

if __name__ == "__main__":
    unittest.main()
