#!/bin/python

import sys, os
from datetime import datetime,timedelta,time
from appoints import io,appoint,special

weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
today = 'Today'
tomorrow = 'Tomorrow'

def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def clearTerminal():
    print( "\x1b[2J\x1b[;f", end="" )

def printGrid( days, start, end ):
    ts = getTerminalSize()
    sepline = '+' + '-'*(ts[0]-days*int(ts[0]/(days + 1))-3) + '+\x1b[7m''+\x1b[27m' + ('-'*(int(ts[0]/(days+1))-1) + '\x1b[7m''+\x1b[27m')*days
    ssepline = '+' + '-'*(ts[0]-days*int(ts[0]/(days + 1))-3) + '+\x1b[7m''+'+ ('-'*(int(ts[0]/(days+1))-1) + '+')*days + '\x1b[27m'
    emptline = '|' + ' '*(ts[0]-days*int(ts[0]/(days + 1))-3) + '|\x1b[7m''|\x1b[27m' + (' '*(int(ts[0]/(days+1))-1) + '\x1b[7m''|\x1b[27m')*days

    print( ssepline )
    print( emptline )
    print( emptline )
    print( ssepline )
    for i in range( 0, int((ts[1]-7)/4) ):
        print( sepline )
        print( emptline )
        print( emptline )
        print( emptline )
    print( sepline )
    print( ssepline )

def printCurrTime( days, start, end ):
    ts = getTerminalSize()
    sepline = '+' + '-'*(ts[0]-days*int(ts[0]/(days + 1))-3) + '+\x1b[7m''+\x1b[27m' + ('-'*(int(ts[0]/(days+1))-1) + '\x1b[7m''+\x1b[27m')*days
    lines = int((ts[1]-7)/4)
    stp = ( end - start ) / lines

    now = datetime.today().time()
    for i in range( 0, 4 * lines + 1 ):
        if start+int(.25*i*stp) == 24:
            break
        act = time(start+int(.25*i*stp),int(15*i*stp)%60)
        eod = act.hour+int((act.minute+int(15*stp))/60) == 24
        if not eod:
            nxt = time( act.hour+int((act.minute+int(.4+15*stp))/60),
                    (act.minute+int(.4 + 15*stp))%60 )
        if act <= now and (eod or now <= nxt):
            print( '\x1b[{y};1H'.format( y=5 + i )
                    + '\x1b[36m' + sepline + '\x1b[39m', end='' )


def printDates( days, start, end ):
    ts = getTerminalSize()
    lines = int((ts[1]-7)/4)
    fscolwd = ts[0]-days*int(ts[0]/(days + 1))-3
    colwd = int(ts[0]/(days+1))-1

    stp = ( end - start ) / lines

    print( '\x1b[2;{x}H''\\ Date\n\x1b[3;{x2}H''Time \\'.format(
        x=int(fscolwd/2 ),
        x2=int(fscolwd/2 - 2)), end='')
    for i in range( 0, lines + 1 ):
        print( '\x1b[{y};{x}H''{h:02}:{m:02}'.format( y=5 + 4 * i,
            x=int(fscolwd/2 - 1.5),
            h=start+int(i*stp),
            m=int(60*i*stp)%60 ), end='' )

        nns = [today[:colwd]]+[tomorrow[:colwd]]+[weekdays[(i + datetime.today().weekday()) % 7 ][:colwd] for i in range( 2, days ) ]
    for i in range( 0, days):
        print( '\x1b[2;{x}H''{st}{d}{ed}'.format(
            x=int(colwd/2)+4-int(len(nns[i])/2)+fscolwd+i*(colwd+1),
            d=nns[ i ],
            st= '\x1b[1m' if i==0 else '',
            ed= '\x1b[0m' if i==0 else ''), end='')
        print( '\x1b[3;{x}H''{str}'.format(
            x=int(.5+colwd/2)+2+fscolwd+i*(colwd+1),
            str='{m:02}-{d:02}'.format(
            m=(datetime.today()+timedelta(i)).month,
            d=(datetime.today()+timedelta(i)).day )[-colwd:]), end='')


    print( '\x1b[{};0H'.format( ts[ 1 ] - 1) )

#appoints = [(startmn,endmn,prio,(text,specials))]
def printAppoints( days, start, end, day, appoints ):
    ts = getTerminalSize()
    lines = int((ts[1]-7)/4)
    fscolwd = ts[0]-days*int(ts[0]/(days + 1))-3
    colwd = int(ts[0]/(days+1))-1

    stp = ( end - start ) / lines

    #apps = [ [ (pos,prio,text,bord) ] ]
    apps = [[] for i in range( 0, 1+4*lines)]
    for j in appoints:
        p = 0
        while True:
            good = True
            for i in range( 0, 1+4*lines ):
                acmin = start * 60 + i * stp * 15
                if acmin > j[0] and acmin < j[1]:
                    for x in apps[ i ]:
                        if x[ 0 ] == p:
                            good = False
                            break
                if not good:
                    break
            if good:
                break
            p = p+1
        for i in range( 0, 1+4*lines ):
            acmin = start * 60 + i * stp * 15
            if acmin >= j[0] and acmin <= j[1]:
                apps[ i ] += [( p, j[2], j[3], acmin==j[0] or acmin==j[1])]
    mx = 0
    for i in apps:
        for j in i:
            mx = max( mx, j[0] )
    nlen = int(colwd / ( mx + 1 ))
    flen = nlen + colwd % ( mx + 1 )
    txts = {}

    def _center( curr, length ):
        naclen = 0 if length < len(curr) else int((length-len(curr))/2)
        nacmd = 0 if length < len(curr) else (length-len(curr)) % 2
        curr = (' '*naclen)+curr+(' '*(nacmd+naclen))
        return curr
    def _split( line, length, autocenter=True ):
        ftx = []
        curr = line[0][:length]
        line[0] = line[0][length:]
        i = 0
        while i != len(line):
            if len( curr + ' ' + line[ i ] ) <= length:
                curr += ' ' + line[ i ]
                i = i + 1
                continue
            ftx += [_center(curr, length) if autocenter else curr]
            curr = line[i][:length]
            line[i] = line[i][length:]
        curr = curr[:len(curr)-1]
        if len( curr ) != 0:
            ftx += [_center(curr, length) if autocenter else curr]
        return ftx
    def _specials( stuff, length, skiplen = 2 ):
        ftx = []
        if length <= skiplen:
            return ftx
        ftx = stuff.print().split('∥')
        ftx = [ _center( a, length + len('\x1b[4;2m''\x1b[24;22m') )
                for a in ftx if a != '' and len(a) <= length + len('\x1b[4;2m''\x1b[24;22m') ]
        return ftx

    for ap in appoints:
        flen2 = max( 1, flen - 2 )
        nlen2 = max( 1, nlen - 1 )
        txts[ ap[3][0] ] = ( _split(ap[3][0].split(), flen2) + _specials(ap[3][1], flen2) + [' '*flen2],
                _split(ap[3][0].split(), nlen2) + _specials(ap[3][1], nlen2) + [' '*nlen2])
    #print(txts)
    #return
    for i in range( 0, 1+4*lines ):
        for j in apps[ i ]:
            posx = flen -1+ (j[0]-1)*nlen if j[0]>0 else 0
            aclen = max(1,(flen-2) if j[0]==0 else (nlen-1))
            txt = txts[j[2][0]][j[0]>0]
            if not j[3]:
                print( '\x1b[{y};{x}H''|\x1b[{clr}m''{str}\x1b[49m|'.format(
                    y=5+i,
                    x=fscolwd+4+day*(colwd+1)+posx,
                    clr=40+j[1],
                    str=txt[(i+len(txt)-1)%len(txt)],
                    end='') )
            else:
                print( '\x1b[{y};{x}H''+{str}+'.format(
                    y=5+i,
                    x=fscolwd+4+day*(colwd+1)+posx,
                    str=aclen*'-'),
                    end='' )
    print( '\x1b[{};0H'.format( ts[ 1 ] - 1) )

def getAppoints( day, appoints ):
    td = datetime.today() + timedelta( day )

    past = [ a for a in appoints if a.is_past(td) and a.inc != [0, 0, 0, 0] ]
    appoints = [ a for a in appoints if a.is_present_on_day(td) ]

    while len(past) != 0:
        past = [ a.evolve() for a in past if a.evolve() != None ]
        appoints += [ a for a in past if a.is_present_on_day(td) ]
        past = [ a for a in past if a.is_past(td) ]

    return [ a.to_tuple(td) for a in appoints if a.to_tuple(td) != None ]

def main( days=7, start=6, end=20, path=os.path.expanduser('~') + '/.appointlist' ):
    appoints = io.read_appoints(path=path,
            fail_if_locked=False,
            print_map={
                special._number:lambda tokens:
                    '' if special._count in tokens
                    else '\x1b[2;2m('+tokens[special._number]\
                            +')\x1b[22;22m∥',
                special._count:lambda tokens:
                    '' if not special._number in tokens
                    else '\x1b[2;2m('+tokens[special._number]+'/'\
                            +tokens[special._count]+')\x1b[22;22m∥',
                special._location:lambda tokens:
                    '\x1b[2;4m'+tokens[special._location]+'\x1b[22;24m∥'
                }
            )
    clearTerminal()
    printGrid( days, start, end )
    printCurrTime( days, start, end )
    printDates( days, start, end )
    for i in range( 0, days ):
        #print(getAppoints(i, appoints))
        printAppoints( days, start, end, i, getAppoints(i, appoints) )

d = 7
s = 6
e = 20
path = os.path.expanduser('~') + '/.appointlist'
if len(sys.argv) >= 2:
    d = int(sys.argv[ 1 ])
if len(sys.argv) >= 3:
    s = int(sys.argv[ 2 ])
if len(sys.argv) >= 4:
    e = int(sys.argv[ 3 ])
if len(sys.argv) >= 5:
    path = int(sys.argv[ 4 ])

main( min(15,max(1,d)), max(s,0), min(e,24), path )
