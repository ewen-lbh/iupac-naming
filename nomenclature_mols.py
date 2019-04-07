def transform_list(iterable, func):
    return [func(i) for i in iterable]


LEN_SUFFIXES = {
    1: 'meth',
    2: 'eth',
    3: 'prop',
    4: 'but',
    5: 'pent',
    6: 'hex',
    7: 'hept',
    8: 'oct',
}

COUNT_SUFFIXES = {
    2: 'di',
    3: 'tri',
    4: 'tetra',
}

helptxt = \
    """
    N: Nombre de...
    P: Position de...
    L: Longueur de...
    E: Existance de...
    """


def numberof(what):
    numworks_safe_print("N: %s ?" % what)
    return int(input('>'))


def num_choose(msg, choices):
    choicemap = {i + 1: v for i, v in enumerate(choices)}
    numworks_safe_print(msg)
    print("Choix possibles:")
    for i, v in choicemap.items():
        numworks_safe_print("{}: {}".format(i, v))

    chosen = int(input('>'))
    while chosen not in choicemap.keys():
        chosen = int(input('>'))

    return choicemap[chosen]

def posof(what="ce groupe"):
    numworks_safe_print("P: %s ?" % what)
    return int(input('>'))


def lenof(what):
    numworks_safe_print("L: %s ?" % what)
    return int(input('>'))


def presenceof(what):
    numworks_safe_print("E: %s ?" % what)
    return input('>').lower().strip().startswith('y')


def numworks_safe_print(string):
    for line in string.split('\n'):
        print(line)


DEBUG = False
# len: pos
subs = {}

if not DEBUG:

    aldehydegroup  = "-CH=O"
    carboxylegroup = "-C|OH=O"
    hydroxylegroup = "-OH"
    carbonylegroup = "C=O"

    numworks_safe_print(helptxt)

    pchain_len = lenof("chaine principale")

    def choose_special_sub():
        choices = ('aucun', hydroxylegroup, carbonylegroup, aldehydegroup, carboxylegroup)
        chosen  = num_choose("Quel groupe est présent ?",list(choices))
        return chosen == choices[0], chosen == choices[1], chosen == choices[2], chosen == choices[3], chosen == choices[4]

    is_not_particular, is_alcool, is_carbonyle, is_aldehyde, is_acid_carboxylique = choose_special_sub()

    if is_alcool or is_carbonyle:
        # ask for hydroxyle if not is_carbonyle else ask for carbonyle
        special_sub_pos = posof(["Groupe hydroxyle","Groupe carbonyle"][int(is_carbonyle)])
    else:
        special_sub_pos = 0

    n_subs = numberof("substituants")

else:
    pchain_len = 6
    hydroxyle_pos = 3
    n_subs = 3
    subs_len = [1] * 3
    subs_pos = [2] + [4] * 2

for _ in range(n_subs):
    if not DEBUG:
        slen = lenof("substituant")
        spos = posof("substituant")
    else:
        slen = subs_len[_]
        spos = subs_pos[_]
    if subs.get(slen):
        subs[slen].append(spos)
    else:
        subs[slen] = [spos]

# sort subs dict by length
sorted_subs = sorted(subs.items(), key=lambda kv: kv[0])

subs_str = []
for slen, spos in sorted_subs:
    if len(spos) > 1:
        posstr = ','.join(transform_list(spos, str)) + '-' + COUNT_SUFFIXES[len(spos)]
    else:
        posstr = str(spos[0]) + '-'

    substr = posstr + LEN_SUFFIXES[slen] + 'yl'

    subs_str.append(substr)

subs_str = '-'.join(subs_str)

if is_alcool:
    special_sub_str = "-%s-ol" % special_sub_pos
elif is_carbonyle:
    special_sub_str = "-%s-one" % special_sub_pos
elif is_aldehyde:
    special_sub_str = 'al'
elif is_acid_carboxylique:
    special_sub_str = 'oique'
else:
    special_sub_str = str()

acid = 'acide ' if special_sub_str == 'oique' else ''

final_str = acid + subs_str + LEN_SUFFIXES[pchain_len] + 'an' + special_sub_str

if final_str == 'propan-2-ol': final_str = 'isopropyl'

numworks_safe_print('-' * 20 + '\n' + final_str)