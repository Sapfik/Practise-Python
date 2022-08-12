

def narcisstic (value):
    st = int(len(str(value)))
    val = 0
    for i in str(value):
        val += int(i) ** st
    return True if val == value else False

print(narcisstic(4887))


### SECOND SOLUTION
def narcisstic (value):
    return value == sum(int(x) ** len(str(value)) for x in str(value))