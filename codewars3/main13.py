

def solution(args):
    array = []
    last_array = []
    new_array = []
    count = 0
    for k, char in enumerate(args):
        try:
            if args[count] - args[count+1] == -1:
                # args.pop(count)
                new_array.append(args[count])
                array.append(args[count])
                count += 1
            else:
                
                if len(new_array) >= 3:
                    new_array.append(args[count])

                    for k, i in enumerate(args):
                        for el in new_array:
                            if el == i:
                                args[k] = f"{new_array[0]}-{new_array[-1]}"
                            
                    new_array.clear()        
                            
                    # return f"{new_array[0]}-{new_array[-1]}"
                    # array.insert(count, '-3-1')
                elif len(new_array) == 2:
                    new_array.append(args[count])

                    for k, i in enumerate(args):
                        for el in new_array:
                            if el == i:
                                args[k] = f"{new_array[0]}-{new_array[-1]}"
                            
                    new_array.clear()   
                new_array.clear()                 
                array.append(count)
                count += 1 
                continue
        except:
            if len(new_array) >= 2:
                new_array.append(args[count])
 
                for k, i in enumerate(args):
                    for el in new_array:
                        if el == i:
                            args[k] = f"{new_array[0]}-{new_array[-1]}"
                            
                new_array.clear()        
                # return f"{new_array[0]}-{new_array[-1]}"   

            break
    for char in args:
        if char in last_array:
            continue
        else:
            last_array.append(str(char))
            
    return ','.join(last_array)
print(solution([-3,-2,-1,2,10,15,16,18,19,20]))




def solution(args):
    out = []
    beg = end = args[0]
    
    for n in args[1:] + [""]:        
        if n != end + 1:
            if end == beg:
                out.append( str(beg) )
            elif end == beg + 1:
                out.extend( [str(beg), str(end)] )
            else:
                out.append( str(beg) + "-" + str(end) )
            beg = n
        end = n
    
    return ",".join(out)

print(solution([-3,-2,-1,2,10,15,16,18,19,20]))