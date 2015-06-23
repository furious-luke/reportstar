import re

class ParseError(Exception):

    def __init__(self, line):
        self.line = line

    def __str__(self):
        return 'Failed to parse quota at line: %s'%self.line

def to_tb(val_str):
    if val_str == 'unlimited':
        return None
    val = float(val_str[:-2])
    if val_str[-2:] == 'kB':
        return val/1000000000
    elif val_str[-2:] == 'MB':
        return val/1000000
    else:
        return val/1000

def parse_quota(filename):
    num_re = r'((?:\d+(?:\.\d+)?(?:kB|MB|GB))|(?:unlimited))'
    prog = re.compile(r'\A(.+?)\s+.*?' + num_re + '\s+.*?' + num_re + '.*')
    res = {}
    with open(filename) as file:
        for line in file:
            match = prog.match(line)
            if not match:
                raise ParseError(line)
            res[match.group(1)] = {'usage': to_tb(match.group(2)), 'quota': to_tb(match.group(3))}
    return res

if __name__ == '__main__':
    import sys
    res = parse_quota(sys.argv[1])
    print res
