

def cakes(recipe, available):
    return min([available[i]//recipe[i] if i in available else 0 for i in recipe])

###SECOND SOLUTION
def cakes(recipe, available):
    array = []
    for i in recipe:
        if i in available:
            if available[i] // recipe[i] >= 1:
                array.append(available[i] // recipe[i])
            else: 
                return 0
        else:
            return 0
    return min(array)

print(cakes({"flour": 500, "sugar": 200, "eggs": 1}, {"flour": 1200, "sugar": 1200, "eggs": 5, "milk": 200}))