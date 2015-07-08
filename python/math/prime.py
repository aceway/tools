#!/usr/bin/env python
import os
import sys

def load_prime_file(pf):
    plist = []
    if os.path.isfile(pf):
        with open(pf, 'r') as rf:
            for line in rf:
                plist += [long(n.strip()) for n in line.strip().split("\t")]
    else:
        print "it's not a file:", pf
    return plist

def is_prime(n):
    if n >= 2:
        for idx in range(2,n):
            if not ( n % idx ):
                return False
    else:
        return False
    return True

def check_guess1(plist):
    idx = 0
    true_list =[]
    false_list =[]
    for p in plist:
        if idx < 2:
            idx += 1
            continue
        guess_ok = False
        for lp in plist:
            if lp >= p: break
            np = 2 * p - lp
            if np in plist or is_prime(np):
                guess_ok = True
                break
        if guess_ok:
            #print p, " is true for guess1"
            true_list.append(p)
        else:
            print p, " is false for guess1"
            false_list.append(p)
        idx += 1
    return false_list, true_list

def check_guess2(plist):
    true_list =[]
    false_list =[]
    max_pos = len(plist) - 2
    for pos in xrange(max_pos):
        p,q= plist[pos], plist[pos+1]
        if (p==2 and q==3) or (p==3 and q==2): continue
        guess_ok = False
        for k in xrange( long(q/2) ):
            nq = q - 2 * k
            np = p + 2 * ( k + 1)
            if np in plist and nq in plist:
                guess_ok = True
                break
            elif np in plist and is_prime(nq):
                guess_ok = True
                break
            elif is_prime(np) and nq in plist:
                guess_ok = True
                break
            elif is_prime(np) and is_prime(nq):
                guess_ok = True
                break

        if guess_ok:
            true_list.append( (plist[pos], plist[pos+1]), )
        else:
            false_list.append((plist[pos], plist[pos+1]), )
            #print plist[pos] , " is false for guess2"
    return false_list, true_list

if __name__ == '__main__':
    if len(sys.argv) == 2:
        pf = sys.argv[1]
        plist = load_prime_file(pf)
        f, t = check_guess1(plist)
        print "guess1 false:", f
        print ""
        f, t = check_guess2(plist)
        print "guess2 false:", f
    else:
        print "usage:\n\t", sys.argv[0], "prime_file"
