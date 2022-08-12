import requests
class TriangleChecker:

    def __init__(self, sides):
        self.sides = sides
        
    def is_triangle(self):
        if all(isinstance(side, (int, float)) for side in self.sides):
            if all(side > 0 for side in self.sides):
                sorted_sides = sorted(self.sides)
                if sorted_sides[0] + sorted_sides[1] > sorted_sides[2]:
                    return 'Ура, можно построить треугольник!'
                return 'Жаль, но из этого треугольника ничего не выйдет!'
            return 'С отрицательными числами ничего не выйдет!'
        return 'Нужно вводить только числа'

triangle = TriangleChecker([1, 5, 4])
print(triangle.is_triangle())
