


### SECOND SOLUTION
MOVES = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

def street_fighter_selection(fighters, initial_position, moves):
    y, x = initial_position
    hovered_fighters = []
    for move in moves:
        dy, dx = MOVES[move]
        y += dy
        if not 0 <= y < len(fighters):
            y -= dy
        x = (x + dx) % len(fighters[y])
        hovered_fighters.append(fighters[y][x])
    return hovered_fighters



def street_fighter_selection(fighters, initial_position, moves):
    array = []
    for i in moves:
        if i == 'right':
            if initial_position[1] == 5:
                initial_position = (initial_position[0], 0)
            else:
                initial_position = (initial_position[0], initial_position[1] + 1)
        elif i == 'left':
            if initial_position[1] == 0:
                initial_position = (initial_position[0], 5)   
            else:
                initial_position = (initial_position[0], initial_position[1] - 1)
        elif i == 'up':
            if initial_position[0] == 0:
                initial_position = (0, initial_position[1])    
            else:       
                initial_position = (initial_position[0] - 1, initial_position[1])
        elif i == 'down':
            if initial_position[0] == 1:
                initial_position = (1, initial_position[1])    
            else:
                initial_position = (initial_position[0] + 1, initial_position[1])
        
        array.append(fighters[initial_position[0]][initial_position[1]])
    return array


print(street_fighter_selection(	[["Ryu", "E.Honda", "Blanka", "Guile", "Balrog", "Vega"],
	["Ken", "Chun Li", "Zangief", "Dhalsim", "Sagat", "M.Bison"]], (0,0), ["up","left","down","right"]*2))