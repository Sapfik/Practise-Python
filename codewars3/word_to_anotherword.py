

from numpy import broadcast_arrays


def transfer(file_path):
    with open(file_path, encoding='utf-8') as file:
        array = [line.strip() for line in file.readlines()]
    for char in array:
        # if '' == char:
        #     array.remove(char)
        
        if any(w in char for w in ['A:', 'Michelle:', 'Trevor:']):
            letter = char.split(':')[0]
            char = char.replace(letter, 'Dragonborned|TAT').replace('-', ' ').replace(':', '')
            print
            with open('a_words.txt', 'a',encoding='utf-8') as file:
                file.write(f"{char}\n")

                
        elif any(w in char for w in ['B:', 'Michael:', 'Charles:']):
            letter = char.split(':')[0]
            char = char.replace(letter, 'REAPER Ronin Slash').replace('-', ' ').replace(':', '')
            with open('b_words.txt', 'a',encoding='utf-8') as file:
                file.write(f"{char}\n")

            
    # print(b_array)
    
    

transfer(r'D:\Practise Python\Codewars\codewars\dialog.txt')