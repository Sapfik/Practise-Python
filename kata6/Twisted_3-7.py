

def sort_twisted37(arr):
    tr=str.maketrans('37','73')   #Взаимозаменяет один объект на другой и ответом выдет словарь из цифр
    return sorted(arr,key=lambda n:int(str(n).translate(tr)))  #translate - как раз таки переводит в нормальный вид словарь из maketrans
    
    

print(sort_twisted37([12,13,14]))