
import random

class Warrior:
    def __init__(self, first_warrior, second_warrior):
        self.first_warrior = first_warrior
        self.second_warrior = second_warrior


    def hit_each_other(self):
        count = random.randint(1,2)
        if count == 1:
            self.first_warrior -= 20
            print(f"Первый воин получил удар на 20 хп")
        else:
            self.second_warrior -= 20
            print(f"Второй воин получил удар на 20 хп")
        return [self.first_warrior, self.second_warrior]
        

a = Warrior(100, 100)
array = a.hit_each_other()
for i in range(1, 100):
    if array[0] > 0 and array[1] > 0:
        array = a.hit_each_other()
    else:
        break

b = "Победил первый воин" if array[1] == 0 else "Победил второй воин"
print(b)