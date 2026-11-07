#!/usr/bin/env python3
"""Exact checks for the LE-406 endpoint / moving-window stage.
Python 3.10+, standard library, assertions enabled.
The asymptotic endpoint and logarithmic discrepancy arguments are written proofs,
not conclusions inferred by these finite tests.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, gcd, log
from pathlib import Path
import hashlib
import importlib.util
import json
import time

assert __debug__, 'Run without -O.'
ROOT = Path(__file__).resolve().parent


def digits(n, length, base=3):
    ans=[]
    for _ in range(length):
        n,d=divmod(n,base); ans.append(d)
    return ans


def digits01(length):
    ans=[0]; p=1
    for _ in range(length):
        ans += [x+p for x in ans]; p*=3
    return ans


def rational_digits(a,b,length):
    assert b>0 and b%3
    ans=[]; inv=pow(b,-1,3)
    for _ in range(length):
        d=(a*inv)%3
        ans.append(d)
        assert (a-b*d)%3==0
        a=(a-b*d)//3
    return ans


def rational_member(a,b):
    assert b>0 and b%3
    seen=set(); inv=pow(b,-1,3)
    while a not in seen:
        seen.add(a); d=(a*inv)%3
        if d==2:return False
        a=(a-b*d)//3
    return True


def previous_dependencies():
    p=ROOT/'dependencies'/'block_coset_checks.py'
    spec=importlib.util.spec_from_file_location('previous_checks',p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    out={}
    # The actual dependencies are rerun, not just read from old PASS labels.
    for name in ('energy','block_lifting','affine_fibonacci'):
        out[name]=getattr(mod,'check_'+name)()
    return out


# Tiny polynomial arithmetic in a formal variable s, with rational coefficients.
def pa(a,b):
    c=[Fraction(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def pm(a,b):
    c=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def ps(a,b):return pa(a,[-x for x in b])


def endpoint_algebra():
    one=[Fraction(1)]; s=[0,Fraction(1)]
    # a=(3s-1)/4, A=(6-2s)/(3s-1), rho=(3-s)/2.
    aden=[-1,3]; Anum=[6,-2]
    assert pm(aden,Anum)==pm([6,-2],aden)
    assert Anum==[4*Fraction(3,2),4*Fraction(-1,2)]
    # A-1=(7-5s)/(3s-1), alpha=(3s-1)/(7-5s).
    assert ps(Anum,aden)==[7,-5]
    # beta=s+(2s-1)*alpha=(1+s)^2/(7-5s).
    beta_num=pa(pm(s,[7,-5]),pm([-1,2],[-1,3]))
    assert beta_num==[1,2,1]
    # D exponent in the boundary Farey estimate.
    # -s/2 +(1-3s)/4*(L-h) -> h coefficient (s-1)/4.
    assert pa([0,Fraction(-1,2)],[-Fraction(1,4),Fraction(3,4)])==[-Fraction(1,4),Fraction(1,4)]
    # Needed strict sign facts, all exact.
    assert 2**5>3**3       # s>3/5, hence eta0<s and A<6
    assert 2**7<3**5       # s<5/7, hence A>4
    assert 2**4<3**3       # eta0=3-4s>0
    assert 2<3            # rho>1
    # Integer control of h=ceil(log_3 D^2).
    sampling_scales=0
    for D in range(2,501):
        h=0
        while 3**h<D*D:h+=1
        assert D*D<=3**h<3*D*D
        for l in range(h+1):
            assert 3**l<3*D*D
            sampling_scales+=1
    # Formal endpoint bookkeeping, with any rational surrogate for s in the
    # relevant interval. This verifies rounding inequalities, not a theorem
    # about irrational constants by numerical testing.
    rounding=0
    for sv in (Fraction(61,100),Fraction(63,100),Fraction(2,3)):
        A=(6-2*sv)/(3*sv-1); alpha=1/(A-1)
        for H in (2,20,300):
            d=128; logc=-(H+d+4)/(A-1)
            for logx in range(1000,1050):
                k=(alpha*logx+logc).__floor__()
                L=(Fraction(logx)+k-1).__floor__()-d
                assert L-A*k>=H+2
                rounding+=1
    return {'formal_polynomial_identities':5,'exact_sign_checks':4,
            'sampling_scale_checks':sampling_scales,'rational_rounding_cases':rounding,
            'scope':'Algebra/rounding only; the endpoint mean bound is proved analytically.'}



def main():
    out={'dependencies':previous_dependencies(),'endpoint_algebra':endpoint_algebra(),'status':'PASS'}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
