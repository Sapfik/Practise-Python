from collections import Counter

def is_valid_walk(walk):
    if len(walk) == 10:
        return True if walk.count('n') == walk.count('s') and walk.count('e') == walk.count('w') else False
    return False


def main():
    print(is_valid_walk(['n','s','n','s','n','s','n','s','n', 's', 'e']))
    
if __name__ == '__main__':
    main()