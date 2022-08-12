import requests

def cookies_from_file(filename):
  with open(filename) as file:
    cookies_data = file.read().replace('\n','').split(';')
  cookies_dic = {}
  for x in cookies_data:
    key = x.split('=')[0]
    value = x.split('=')[1]
    cookies_dic[key]=value
  return cookies_dic

cookies = cookies_from_file('cookies.txt')
response = requests.get(url='http://httpbin.org/cookies',cookies=cookies)