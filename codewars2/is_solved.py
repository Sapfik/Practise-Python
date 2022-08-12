

def is_solved(board):
    
    if all(k[0] == 1 for k in board) or all(k[1] == 1 for k in board) or all(k[2] == 1 for k in board) or all(i[k] == 1 for k, i in enumerate(board)) or all(i[k] == 1 for k, i in enumerate(board[::-1])) or any(len(set(i)) == 1 and i[0] == 1 for i in board):
        return 1
    
    elif all(k[0] == 2 for k in board) or all(k[1] == 2 for k in board) or all(k[2] == 2 for k in board) or all(i[k] == 2 for k, i in enumerate(board)) or all(i[k] == 2 for k, i in enumerate(board[::-1])) or any(len(set(i)) == 1 and i[0] == 2 for i in board):
        return 2
    
    elif any(0 in k for k in board):
        return -1

    return 0

print(is_solved([[1, 0, 1],
         [1, 1, 2],
         [1, 1, 0]]))