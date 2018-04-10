'''validate.py'''
import re
special_character_regex = r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'

class Validate():
    '''class representing validate request data from request.get_json()'''
    def validate_register(self, data):
        '''validate user register data '''
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not username:
            return {"message": "Enter username"}
        if not name:
            return {"message": "Enter name"}
        if bool(re.search(special_character_regex, name)) is True:
            return {"message":"Name cannot contain special characters and numbers"}
        if not email:
            return {"message": "Enter email"}
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return {"message": "Enter a valid email address"}
        if not password:
            return {"message": "Enter password"}
        if len(password) < 6:
            return {"message": "password is too short"}
        if bool(re.search(r'[A-Z][a-z]|[a-z][A-Z]', password)) is False:
            return {"message": "password must contain a mix of upper and lowercase letters"}
        if bool(re.search(special_character_regex, password)) is False:
            return {"message": "password must contain atleast one numeric or special character"}
        if not confirm_password:
            return {"message": "Confirm password missing"}

        my_list = [username, name, password]
        for i in my_list:
            i = i.strip()
            if i is None or not i:
                return {"message": "Enter valid data"}
        if confirm_password != password:
            return {"message": "Passwords don't match"}
        
        return {"username":username, "name":name, "password":password, "email":email}
        