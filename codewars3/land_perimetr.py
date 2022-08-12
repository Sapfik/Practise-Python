
# def land_perimetr(arr):
#     last_array  = []
#     help_list = []
#     array = []
#     count = 0
#     for i  in arr:
#         array.append(tuple(i))
    
#     while count < len(array):
#         for i in array:
#             help_list += i[count]
#         last_array.append(tuple(help_list))
#         help_list = []
#         count += 1
#     return last_array
        
        
def land_perimeter(arr):

    m,n = len(arr) , len(arr[0])
    land, nei = 0,0
    for i in range(m):
        for j in range(n):
            if arr[i][j]=='X':
                land+=1
                if i < m-1 and arr[i+1][j]=='X':
                    nei+=1
                if j < n-1 and arr[i][j+1]=='X':
                    nei+=1
    result = "Total land perimeter:" + str(land-nei)

    return(result)
    
    

print(land_perimeter(['XOOXO',  'XOOXO',  'OOOXO',  'XXOXO',  'OXOOO']))