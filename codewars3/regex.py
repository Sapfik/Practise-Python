import re 


# if re.search("^(?=.[A-Z])(?=.[a-z])(?=.*[0-9])\w{6,}$", 'sfsdfHG234'):
#     print(True)
# else:
#     print(False)

print(bool(re.search("^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[^\W_]{6,}$", '4fdg5Fj3')))