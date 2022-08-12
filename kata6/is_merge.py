

def is_merge(s, part1, part2):
    part1 = part1.replace(' ','')
    part2 = part2.replace(' ', '')
    return True if sorted(list(s)) == sorted([*part1, *part2]) else False

def is_merge(s, p1, p2, cache=None):
    if cache is None:
        cache = {}
    key = s, frozenset((p1, p2))
    if key not in cache:
        cache[key] = \
            p1 and p1[0] == s[0] and is_merge(s[1:], p1[1:], p2, cache) or \
            p2 and p2[0] == s[0] and is_merge(s[1:], p1, p2[1:], cache) or \
            False if s else not p1 and not p2
    return cache[key]


print(is_merge('codewars', '  c   d   w         ', '    o   e   a r s   '))