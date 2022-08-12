
from hashlib import new


opposite = {'NORTH' : 'SOUTH', 'EAST' : 'WEST', 'SOUTH' : 'NORTH', 'WEST' : 'EAST'}

def dirReduc(arr):
    new_plan = []
    for d in arr:
        if new_plan and new_plan[-1] == opposite[d]:
            new_plan.pop()
        else:
            new_plan.append(d)
    return new_plan

print(dirReduc(["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]))