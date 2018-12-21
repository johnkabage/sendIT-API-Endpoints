import re
class Validators:
    def valid_username(self, username):
        """ valid username """
        return re.match("^[a-zA-Z0-9]{4,20}$", username)

    def valid_password(self, password):
        """ valid password """
        regex = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{6,15}$"
        return re.match(regex, password)

    def valid_email(self, email):
        """ valid email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_inputs(self, string_inputs):
        """ valid input strings """
        return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)
