#!/usr/bin/env python3
"""Exact verifier for the all-k reverse invariant.
The proof is in parametric_reverse_invariant.txt. This program checks the
finite carry table and polynomial register identities, not only sample k.
It also checks the separate k=0 finite certificate and instantiations.
Standard library only; no floating point, graph spectrum, or external solver.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
BASE=Path(__file__).parent
I=set(range(-11,11))
Z={-10,-9,-4,-3,-1}; O={-8,-7,-5,-4,10}
P={-2,-1,1,2,7,8,10}; PP=P|{4,5}
Q={-7,-6,-4,-3,2,3,5,6}; R={-10,-9,5,6,8,9}
S={1,2,4,5,10}; U={-8,-7,-5,-4}; UP=U|{-6,-3}
W={2,3,5,6}; WP=W|{4,7}; Hc={5,6,8,9}
Ic={-10,-9}; Jc={-11,-6,-5,-3,-2}; Kc={-10,-9,-7,-6,8,9}; Nc=U

# Affine polynomials in formal independent variables X=16^k,Y=T_j.
def poly(x=0,y=0,c=0):return (F(x),F(y),F(c))
def add(p,q):return tuple(a+b for a,b in zip(p,q))
def scale(a,p):return tuple(a*b for b in p)
X=poly(x=1); Y=poly(y=1); one=poly(c=1); zero=poly()
Tk=poly(x=F(1,5),c=F(-1,5)); H=poly(x=F(16,5),c=F(-1,5))
V=poly(x=F(24,5),c=F(-4,5)); Tnext=add(scale(16,Y),poly(c=3))
# Each entry: source register, high bit, carries, destinations for x=0,1.
# A destination is (register polynomial, exact carry image, containing mask).
rows=[]
def row(name,A,a,ds,d0=None,d1=None):rows.append((name,A,a,ds,(d0,d1)))
row('Z0',zero,0,Z,(zero,{-10,-9,-4,-3},Z),(one,O,O))
row('O0',one,0,O,None,(poly(c=3),P,P))
row('P_j',Y,0,P,(scale(2,Y),Q,Q),None)
row('P_last',H,0,PP,(scale(2,H),Q,Q),None)
row('Q_interior',scale(2,Y),0,Q,(scale(4,Y),R,R),(add(scale(4,Y),one),S,S))
row('Q_last',scale(2,H),1,Q,(V,Jc,Jc),(add(V,one),Kc,Kc))
row('R_j',scale(4,Y),0,R,None,(add(scale(8,Y),one),U,U))
row('S_j',add(scale(4,Y),one),0,S,(add(scale(8,Y),poly(c=2)),W,W),None)
row('U_interior',add(scale(8,Y),one),0,U,None,(Tnext,P,P))
row('U_last',add(scale(8,Tk),one),0,UP,(add(H,poly(c=-1)),Ic,Ic),(H,PP,PP))
row('W_j',add(scale(8,Y),poly(c=2)),0,W,(add(Tnext,one),Hc,Hc),None)
row('W_last',add(scale(8,Tk),poly(c=2)),0,WP,(add(H,one),Hc,Hc),None)
row('H_j',add(Tnext,one),0,Hc,None,None)
row('I0row',add(H,poly(c=-1)),0,Ic,None,(add(scale(2,H),poly(c=-1)),Nc,Nc))
row('I1row',add(V,poly(c=-1)),1,Ic,None,None)
row('Jrow',V,1,Jc,None,(add(scale(8,Tk),one),{-7,-6,-4,-3},UP))
row('Krow',add(V,one),1,Kc,(add(scale(8,Tk),poly(c=2)),{3,4,6,7},WP),None)
row('Nrow',add(scale(2,H),poly(c=-1)),1,Nc,None,(add(V,poly(c=-1)),Ic,Ic))

def check_symbolic():
    count=0
    for name,A,a,ds,dest in rows:
        assert ds<=I
        for x in (0,1):
            img={3*d-20*a-b+23*x for d in ds for b in (0,1)}&I
            target=dest[x]
            if target is None:assert not img,(name,x,img)
            else:
                reg,expected,mask=target
                assert img==expected,(name,x,img,expected)
                assert img<=mask,(name,x,img,mask)
                got=add(add(scale(2,A),scale(-8*a,X)),poly(c=x))
                assert got==reg,(name,x,got,reg)
            count+=2*len(ds)
    return count

def T(j):return (16**j-1)//5

def certificate(k):
    assert k>=1
    groups=[(0,Z),(1,O)]
    for j in range(1,k+2):
        groups += [(T(j),PP if j==k+1 else P),(2*T(j),Q)]
    for j in range(1,k+1):
        groups += [(4*T(j),R),(4*T(j)+1,S),(8*T(j)+1,UP if j==k else U),
                   (8*T(j)+2,WP if j==k else W),(T(j+1)+1,Hc)]
    v=(3*T(k+1)-1)//2
    groups += [(T(k+1)-1,Ic),(v-1,Ic),(v,Jc),(v+1,Kc),(2*T(k+1)-1,Nc)]
    assert len(set(A for A,ds in groups))==len(groups)
    out={(A,d) for A,ds in groups for d in ds}
    assert len(out)==38*k+50
    return out

BASE0={
0:{-10,-9,-4,-3,-1,3,4,6,7,8,9},
1:{-8,-7,-6,-5,-4,-3,10},
2:{-10,-9,3,4,6,7},
3:{-10,-9,-2,-1,1,2,4,5,7,8,10},
4:{-11,-6,-5,-3,-2,8,9},
5:{-10,-9,-8,-7,-6,-5,-4,8,9},
6:{-7,-6,-4,-3,2,3,5,6},
7:{-10,-9,-8,-7,-5,-4}}

def check_concrete(m,states):
    assert (0,-1) in states and (0,0) not in states
    n=0
    for A,d in states:
        assert 0<=A<2**m and d in I
        a=A>>(m-1)
        for x in (0,1):
            AA=2*A-a*2**m+x
            for b in (0,1):
                dd=3*d-20*a-b+23*x
                if dd in I:assert (AA,dd) in states,(m,A,d,a,x,b,AA,dd)
                n+=1
    return n

def main():
    symbolic_checks=check_symbolic()
    base={(A,d) for A,ds in BASE0.items() for d in ds}
    assert len(base)==65
    base_checks=check_concrete(3,base)
    # Redundant integer instantiations catch transcription/indexing mistakes;
    # the all-k argument is the symbolic table plus the analytic bounds in text.
    sample=[]
    for k in [1,2,3,4,5,10,25,100]:
        ss=certificate(k);checks=check_concrete(4*k+3,ss)
        sample.append({'k':k,'states':len(ss),'predecessor_choices':checks})
    result={'status':'PASS','symbolic_rows':len(rows),'symbolic_carry_choices':symbolic_checks,
            'formal_variables':['X=16^k','Y=T_j'], 'base_k0_states':65,'base_choices':base_checks,
            'redundant_instantiations':sample,
            'scope':'finite symbolic carry images and polynomial register identities; high-bit inequalities and witness bridge proved in text',
            'proof_sha256':hashlib.sha256((BASE/'parametric_reverse_invariant.txt').read_bytes()).hexdigest()}
    (BASE/'parametric_certificate_result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
