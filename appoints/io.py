_exp_string =   '# List of appoints\n'\
                '#\n'\
                '# Line 1: Start Date\n'\
                '# Line 2: End Date\n'\
                '# Line 3: Next repitition and priority\n'\
                '# Line 4: Subject\n'\
                '#\n'\
                '# Empty Lines and lines starting with a #'\
                    ' will be ignored\n'\
                '# Any line that gets ignored once will be deleted;'\
                    ' excluding this paragraph.\n'\
                '# Any part of the subject starting with a #'\
                    ' will be incremented on every event.\n'

def _dtfa(a):
    from datetime import datetime
    return datetime(a[0], a[1], a[2], a[3], a[4])
def _int(lst):
    return [int(a) for a in lst]
def _concat(a):
    if len(a) == 0:
        return ''
    result = a[0]
    for i in range(1,len(a)):
        result += ' ' + a[i]
    return result
def _simplify(ln, token_map):
    return _concat([a for a in ln if not a[0] in token_map])
def _extract_specials(ln, token_map):
    return {a[0]: a[1:] for a in ln
            if a[0] in token_map}

def read_appoints(path,
        fail_if_locked=True,
        token_map={},
        evolution_map={},
        print_map={},
        auto_add_maps=True):
    import os, io
    from datetime import datetime
    from . import appoint, special

    if not os.path.exists(path):
        return None
    if fail_if_locked and os.path.exists(path+'.lock'):
        return None

    f = open(path, 'r')
    lines = [ln.split() for ln in f.readlines() if ln!='\n' and ln[0]!='#']
    f.close()

    #Add missing default tokens
    if auto_add_maps:
        token_map = special._replace_entries(special._token_map, token_map)

    return [appoint.appoint(
        start=_dtfa(_int(lines[4*i])),
        end=_dtfa(_int(lines[4*i+1])),
        inc=_int(lines[4*i+2][0:4]),
        prio=int(lines[4*i+2][4]),
        text=_simplify(lines[4*i+3], token_map),
        spec=special.special(
            tokens=_extract_specials(lines[4*i+3], token_map),
            token_map=token_map,
            evolution_map=evolution_map,
            print_map=print_map,
            auto_add_maps=auto_add_maps
            )
        ) for i in range(0, int(len(lines)/4))]

def write_appoints(appoints, path, fail_if_locked=True):
    import os, io
    from datetime import datetime
    from . import appoint, special

    if fail_if_locked and os.path.exists(path+'.lock'):
        return False

    f = open(path, 'w')
    f.write(_exp_string)

    for ap in appoints:
        f.write('\n')
        f.write(ap.start.strftime('%Y %m %d %H %M\n'))
        f.write(ap.end.strftime('%Y %m %d %H %M\n'))
        f.write(str(ap.inc[0])+' '+str(ap.inc[1])+' '+\
                str(ap.inc[2])+' '+str(ap.inc[3])+' '+\
                str(ap.prio)+'\n')
        f.write(ap.text+' '+_concat(ap.spec.to_list())+'\n')
    f.close()
    return True

#Encryption/ Decryption stuff
def _bxor(b1, b2):
    res = bytearray(b1)
    for i, b in enumerate(b2):
        res[i] ^= b
    return bytes(res)

#Use twofish as encryption algo
def enc_appoints(appoints, symmetric_key):
    from twofish import Twofish as twofish
    t = twofish(symmetric_key[0:32].encode())
    dec_data = [ap.to_bytes() for ap in appoints]
    enc_data = []
    for dec in dec_data:
        iv = ('\x00'*16).encode()
        for i in range(0, len(dec)):
            iv = _bxor(dec[i], iv)
        cenc = [t.encrypt(iv)]
        for i in range(1, len(dec)):
            cenc = [t.encrypt(_bxor(cenc[0],dec[i]))] + cenc
        cenc += [('\x00'*16).encode()]
        enc_data += cenc
    return enc_data
def dec_appoints(enc_data,
        symmetric_key,
        token_map={},
        evolution_map={},
        print_map={},
        auto_add_maps=True):
    from twofish import Twofish as twofish
    from . import appoint, special
    t = twofish(symmetric_key[0:32].encode())
    appoints = []
    dec_apps = []
    tmp = []
    for ln in enc_data:
        if ln != ('\x00'*16).encode():
            tmp += [ln]
        else:
            app = []
            iv = ('\x00'*16).encode()
            for i in range(0, len(tmp)-1):
                app = [_bxor(tmp[i+1],t.decrypt(tmp[i]))] + app
                iv = _bxor(iv, app[0])
            app = [_bxor(iv, t.decrypt(tmp[len(tmp)-1]))] + app
            dec_apps += [app]
            tmp = []

    #Add missing default tokens
    if auto_add_maps:
        token_map = special._replace_entries(special._token_map, token_map)

    for ap in dec_apps:
        start = appoint._dec_dt(ap[0])
        end = appoint._dec_dt(ap[1])

        tm = appoint._dec_inc(ap[2])
        inc = tm[0]
        prio = tm[1]
        dec_txt = appoint._dec_text(ap[3:len(ap)-1])
        appoints += [appoint.appoint(
            start=start,
            end=end,
            inc=inc,
            prio=prio,
            text=_simplify(dec_txt.split(), token_map),
            spec=special.special(
                tokens=_extract_specials(dec_txt.split(), token_map),
                token_map=token_map,
                evolution_map=evolution_map,
                print_map=print_map,
                auto_add_maps=auto_add_maps
            )
        )]
    return appoints
