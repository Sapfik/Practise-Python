

# def bin_to_dec(digit):   
#     try:     
#         dlina=len(str(digit))            
#         chislo_dec=0           
#         for i in range(0, dlina):               
#             chislo_dec=chislo_dec+int(digit[i])*(2**(dlina-i-1))           
#         return chislo_dec
    
#     except:
#         return -1
    
# def invert(binary_number):
#     decimal_number = bin_to_dec(binary_number)
#     if decimal_number % 3 == 0:
#         return True
#     return False
    
    
# print(invert(' 0'))



import re

def bin_to_dec(digit):   
    try:     
        dlina=len(str(digit))            
        chislo_dec=0           
        for i in range(0, dlina):               
            chislo_dec=chislo_dec+int(digit[i])*(2**(dlina-i-1))           
        return chislo_dec
    
    except:
        return -1

def pattern_func(bin_num):     
    pattern = re.compile(r"[0-1]")
    bin_result = pattern.findall(bin_num)
    bin_result = ''.join(bin_result)
    result = bin_to_dec(bin_result)
    return True if result % 3 == 0 and re.findall(r"\D", bin_num) == [] else False

    
print(pattern_func('101111000110000101001110'))