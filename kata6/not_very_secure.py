import re

def alphanumeric(password):
    return bool(re.match('^[A-Za-z0-9]*$', password)) if password != "" else False

print(alphanumeric(''))