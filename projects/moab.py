def coerce(val):
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    if val not in ['-----', '------']:
        return val
    return None

def parse_moab_file(filename):
    col_names = []
    entries = []
    with open(filename) as mf:
        for line in mf:
            words = line.split()

            # Any line without 17 words is not important.
            if len(words) != 17:
                continue

            # If the second word is "Jobs" this line is the list
            # of column names.
            if words[1] == 'Jobs':
                for w in words:
                    if w == '%':
                        col_names.append(col_names[-1] + '%')
                    else:
                        col_names.append(w)

            # This is a proper entry.
            else:
                entries.append(map(coerce, words))
    return dict([(e[0], dict([(col_names[i + 1], v) for i, v in enumerate(e[1:])])) for e in entries])

def parse_proc_usage(filename):
    entries = parse_moab_file(filename)
    return dict([(a, v['PHDed']) for a, v in entries.iteritems() if a[0] == 'p' and a[4:] in ['_swin', '_astro']])

if __name__ == '__main__':
    import sys
    entries = parse_proc_usage(sys.argv[1])
    print entries
