

class Nikola:
    
    __slots__ = ['name', 'age']  #Позволяет ограничить затрачиваемое место на атрибуты, тем самым ограничивая их списком
    
    def __init__(self, name, age):
        self.name = name
        if self.name != 'Николай':
            self.name = f"Я {self.name}, а не Николай"
        
        self.age = age
        if isinstance(age, (float, int)) and 1 < age < 110:
            self.age = age
        else:
            self.age = f"Недопустимый возраст {self.age}"
        
person = Nikola('Роберт', 111)
print(person.name)
print(person.age)