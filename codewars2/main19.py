

def snail(input_list):
    output_list = []
    
    try:
        while True:
            
            #Изначально мы сто процентов делаем то, что добавляем первый список в конечный список и удаляем его из input_list
            for element in input_list[0]:
                output_list.append(element)
            input_list.pop(0)
            
            #Затем нам нужно удалить из input_list все элементы(кроме последнего в последнем списке) и добавить в output_list
            
            for list in input_list:
                if list != input_list[-1]:
                    output_list.append(list.pop())

            
            # Переворачиваем самый нижний и последний список обратно (для того, чтобы последовательность змейки была верной)
            input_list[-1].reverse()
            for element in input_list[-1]:
                output_list.append(element)
            input_list.remove(input_list[-1])
            
            #Переворачиваем список обратно 
            input_list.reverse()
            for list in input_list:
                output_list.append(list[0])
                list.remove(list[0])
            
            input_list.reverse()
            
    
    except:
        return output_list
    

print(snail([[1,2,3],
         [8,9,4],
         [7,6,5]]))




###SECOND SOLUTION
def snail(array):
    out = []
    while len(array):
        out += array.pop(0)
        array = list(zip(*array))[::-1] # Rotate
    return out
