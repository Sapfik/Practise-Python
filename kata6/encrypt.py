

def encrypt(encrypted_text, n):
    array = list(encrypted_text)
    for i in range(1, n+1):
        array = array[1:len(array):2] + array[0:len(array):2]
    return ''.join(array)

print(encrypt("This is a test!", 2))