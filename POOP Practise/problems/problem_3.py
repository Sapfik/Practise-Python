

class KgToPounds:
    
    def __init__(self, kg):
        self.__kg = kg
        
    def to_pounds(self):
        return self.__kg * 2.205
    
    @property
    def kg(self):
        return self.__kg
    
    @kg.setter
    def kg(self, new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg
        else:
            raise ValueError('Киллограмы задаются только числами!')   #Ловит ошибку и возвращает то, что мы укажем
        
kg = KgToPounds(4)
print(kg.to_pounds())
print(kg.kg)
kg.kg = 313
print(kg.to_pounds())