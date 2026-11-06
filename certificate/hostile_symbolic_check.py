"""Independent exact checker: symbolic register identities and finite carry images.
No discovery code, reverse-state output, or submitted verifier is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import json

# An expression is a rational affine function of independent t=T_j and X=16^k.
def expr(t=0,X=0,c=0): return (F(t),F(X),F(c))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,n): return tuple(n*x for x in a)
def plus(a,n): return add(a,expr(c=n))
Tk=expr(X=F(1,5),c=F(-1,5))
Tl=plus(scale(Tk,16),3)
V=expr(X=F(24,5),c=F(-4,5))
t=expr(t=1)
Z={-10,-9,-4,-3,-1}; O={-8,-7,-5,-4,10}
P={-2,-1,1,2,7,8,10}; PP=P|{4,5}
Q={-7,-6,-4,-3,2,3,5,6}; R={-10,-9,5,6,8,9}
S={1,2,4,5,10}; U={-8,-7,-5,-4}; UP=U|{-6,-3}
W={2,3,5,6}; WP=W|{4,7}; H={5,6,8,9}
I={-10,-9}; J={-11,-6,-5,-3,-2}; K={-10,-9,-7,-6,8,9}
N=U

# A destination is None or (symbolic register, exact image carry set).
rows=[
 ('Z',expr(),Z,0,[(expr(),{-10,-9,-4,-3}),(expr(c=1),O)]),
 ('O',expr(c=1),O,0,[None,(expr(c=3),P)]),
 ('P',t,P,0,[(scale(t,2),Q),None]),
 ('P_terminal',Tl,PP,0,[(scale(Tl,2),Q),None]),
 ('Q',scale(t,2),Q,0,[(scale(t,4),R),(plus(scale(t,4),1),S)]),
 ('Q_terminal',scale(Tl,2),Q,1,[(V,J),(plus(V,1),K)]),
 ('R',scale(t,4),R,0,[None,(plus(scale(t,8),1),U)]),
 ('S',plus(scale(t,4),1),S,0,[(plus(scale(t,8),2),W),None]),
 ('U',plus(scale(t,8),1),U,0,[None,(plus(scale(t,16),3),P)]),
 ('U_terminal',plus(scale(Tk,8),1),UP,0,[(plus(Tl,-1),I),(Tl,PP)]),
 ('W',plus(scale(t,8),2),W,0,[(plus(scale(t,16),4),H),None]),
 ('W_terminal',plus(scale(Tk,8),2),WP,0,[(plus(Tl,1),H),None]),
 ('H',plus(scale(t,16),4),H,0,[None,None]),
 ('I0',plus(Tl,-1),I,0,[None,(plus(scale(Tl,2),-1),N)]),
 ('I1',plus(V,-1),I,1,[None,None]),
 ('J',V,J,1,[None,(plus(scale(Tk,8),1),{-7,-6,-4,-3})]),
 ('K',plus(V,1),K,1,[(plus(scale(Tk,8),2),{3,4,6,7}),None]),
 ('N',plus(scale(Tl,2),-1),N,1,[None,(plus(V,-1),I)]),
]
carry_assignments=0
for name,A,ds,a,dests in rows:
    for x,dest in enumerate(dests):
        vals=set()
        for d in ds:
            for b in (0,1):
                dd=3*d-20*a-b+23*x
                carry_assignments+=1
                if -11<=dd<=10:vals.add(dd)
        if dest is None:
            assert not vals,(name,x,vals)
        else:
            register,expected=dest
            assert vals==expected,(name,x,vals,expected)
            predecessor=add(plus(scale(A,2),x),expr(X=-8*a))
            assert predecessor==register,(name,x,predecessor,register)

base={
0:{-10,-9,-4,-3,-1,3,4,6,7,8,9},
1:{-8,-7,-6,-5,-4,-3,10},
2:{-10,-9,3,4,6,7},
3:{-10,-9,-2,-1,1,2,4,5,7,8,10},
4:{-11,-6,-5,-3,-2,8,9},
5:{-10,-9,-8,-7,-6,-5,-4,8,9},
6:{-7,-6,-4,-3,2,3,5,6},
7:{-10,-9,-8,-7,-5,-4}}
base_states={(A,d) for A,ds in base.items() for d in ds}
assert len(base_states)==65 and (0,-1) in base_states and (0,0) not in base_states
base_predecessors=0
for A,d in base_states:
    a=A//4
    for x in (0,1):
        for b in (0,1):
            AA=2*A-8*a+x
            dd=3*d-20*a-b+23*x
            if -11<=dd<=10:
                assert (AA,dd) in base_states,(A,d,x,b,AA,dd)
                base_predecessors+=1

# A separate instantiated checker tests boundary ranges and count, including
# k=1 where both interior ranges are empty, and very large k with big integers.
def certificate(k):
    tt=lambda j:(16**j-1)//5
    last=tt(k+1); v=(3*last-1)//2
    result={0:set(Z),1:set(O),last:set(PP),last-1:set(I),v-1:set(I),
            v:set(J),v+1:set(K),2*last-1:set(N)}
    def put(A,ds):
        assert A not in result,('register collision',k,A)
        result[A]=set(ds)
    for j in range(1,k+1):
        tj=tt(j)
        put(tj,P);put(2*tj,Q);put(4*tj,R);put(4*tj+1,S)
        put(8*tj+1,UP if j==k else U)
        put(8*tj+2,WP if j==k else W)
        put(tt(j+1)+1,H)
    put(2*last,Q)
    return result
instantiations=[]
for k in (1,2,3,4,5,10,25,100):
    m=4*k+3; mod=2**m
    cert=certificate(k)
    states={(A,d) for A,ds in cert.items() for d in ds}
    assert len(states)==38*k+50
    assert (0,-1) in states and (0,0) not in states
    transitions=0
    for A,d in states:
        assert 0<=A<mod
        a=A//(mod//2)
        for x in (0,1):
            for b in (0,1):
                AA=2*A-mod*a+x
                dd=3*d-20*a-b+23*x
                if -11<=dd<=10:
                    assert (AA,dd) in states,(k,A,d,x,b,AA,dd)
                    transitions+=1
    instantiations.append({'k':k,'m':m,'registers':len(cert),'states':len(states),'valid_predecessors':transitions})
result={'status':'PASS','symbolic_rows':len(rows),'symbolic_carry_assignments':carry_assignments,
        'base_states':len(base_states),'base_valid_predecessors':base_predecessors,
        'instantiations':instantiations,
        'scope':'Symbolic rational-coefficient register identities and all finite carry images certify the parameterized predecessor table; high-bit inequalities and the exclusion argument are independently proved in hostile_review.txt.'}
p=Path(__file__).with_suffix('.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
