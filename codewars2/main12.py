

def domain_name(name):
    return name.replace('www.', '').split('//')[1].split('.')[0] if '//' in name else name.replace('www.', '').split('.')[0]
    

print(domain_name('www.xakep.ru'))


### SECOND SOLUTION

import re
def domain_name(url):
    return re.search('(https?://)?(www\d?\.)?(?P<name>[\w-]+)\.', url).group('name')