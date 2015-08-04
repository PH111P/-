import io
from . import appoint, special

_exp_string = ""

def _dtfa(a):
    return datetime(a[0], a[1], a[2], a[3], a[4])
def _int(lst):
    return [int(a) for a in lst]
def _calc_td(a):
    return (datetime(a[0].year+a[4][0], a[0].month, a[0].day, a[0].hour,
        a[0].minute)-a[0])+timedelta(a[4][1], 3600*a[4][2]+60*a[4][3])
def _concat(a):
    result = a[0]
    for i in range(1,len(a)):
        result += ' ' + a[i]
    return result
def _simplify(lni, token_map):
    return _concat([a for a in ln if not a[0] in token_map])
def _extract_specials(ln, token_map):
    return {a[0]: a[1:] for a in ln
            if a[0] in token_map}

def read_appoints(path,
        fail_if_locked=True,
        token_map=special._token_map,
        evolution_map=special._evolution_map,
        print_map=special._print_map):
    if not os.path.exists(path):
        return None
    if fail_if_locked and os.path.exists(path+'.lock'):
        return None

    f = open(path)
    lines = [ln.split() for ln in f.readlines() if ln!='\n' and ln[0]!='#']
    f.close()

    return [appoint(start=_dtfa(_int(lines[4*i])),
        end=_dtfa(_int(lines[4*i+1])),
        inc=_calc_td(_int(lines[4*i+2][0:3])),
        prio=int(lines[4*i+2][4]),
        text=_simplify(lines[4*i+3], token_map),
        spec=special(
            tokens=_extract_specials(lines[4*i+3], token_map),
            token_map=token_map,
            evolution_map=evolution_map,
            print_map=print_map))
        for i in range(0, int(len(lines)/4))]

def write_appoints(appoints, path, fail_if_locked=True):
    if fail_if_locked and os.path.exists(path+'.lock'):
        return False

    f = open(path)
    f.write(_exp_string)

    f.close()
    return True

#Syncing stuff (TODO)
def pull_appoints():
    return None

def push_appoints():
    return False
