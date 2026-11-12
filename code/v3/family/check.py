"""Exact identities + digitwise sanity checks for an all-k symbolic proof.
The proof is paper/family_positive_dimension.tex. Finite checks are not the proof.
No optional dependencies; words are least-significant-digit first.
"""
from fractions import Fraction as F
from math import log
from pathlib import Path
import json

class Poly:
    def __init__(self, *a):
        self.a=list(map(F,a))
        while self.a and not self.a[-1]: self.a.pop()
    def __add__(self,o):
        if not isinstance(o,Poly):o=Poly(o)
        n=max(len(self.a),len(o.a))
        return Poly(*[(self.a[i] if i<len(self.a) else 0)+(o.a[i] if i<len(o.a) else 0) for i in range(n)])
    __radd__=__add__
    def __neg__(self):return Poly(*[-x for x in self.a])
    def __sub__(self,o):return self+-o if isinstance(o,Poly) else self+Poly(-o)
    def __rsub__(self,o):return -self+o
    def __mul__(self,o):
        if not isinstance(o,Poly):o=Poly(o)
        if not self.a or not o.a:return Poly()
        r=[F(0)]*(len(self.a)+len(o.a)-1)
        for i,a in enumerate(self.a):
            for j,b in enumerate(o.a):r[i+j]+=a*b
        return Poly(*r)
    __rmul__=__mul__
    def __truediv__(self,o):return self*F(1,o)
    def __pow__(self,n):
        r=Poly(1)
        for _ in range(n):r=r*self
        return r
    def __eq__(self,o):return self.a==o.a

t=Poly(0,1); M=621*t-20; c=69*t; reach_len_power=729*t**3
p=(540*t**2+261*t-1)/20
q=(151281*t**2-5841*t+20)/20
assert M*p-23*reach_len_power==q
# Geometric base81 expansion of q, valid for k>=2.
q_digits=1+36*t+(t**2-6561*t)/20+31*t**2+12*81*t**2+81**2*t**2
assert q_digits==q
r=t/81
b=(r-1)/20+1003*r+F(19683,20)*r*(r-1)+3*t**2+81*t**3
b_simple=81*t**3+F(63,20)*t**2+F(7,30)*t-F(1,20)
assert b==b_simple
z=(20169*t**3+4914*t**2+1997*t+60)/60
assert M*b+c-reach_len_power*c==z
# Geometric base81 expression, valid k>=1, with one harmless merge k=1.
z_digits=1+t/3+37*t+(t**2-81*t)/20+13*t**2+13*81*t**2+F(3,20)*(81*t**3-6561*t**2)+4*81*t**3
assert z_digits==z
assert (621*t-20)+23==3+9*c
# Loop A has value3^(m-2)=3*t and length m, hence3^m=27*t.
assert M*(3*t)+c==9*t+27*t*c

def value(w):return sum(int(a)*3**i for i,a in enumerate(w))
def digits(n,length):
    out=[]
    for _ in range(length):out.append(n%3);n//=3
    assert n==0
    return ''.join(map(str,out))
def verify_path(M,word,initial,final):
    carry=initial;out=[]
    for digit in word:
        q,b=divmod(M*int(digit)+carry,3)
        assert b in (0,1)
        assert q>=0
        carry=q;out.append(str(b))
    assert carry==final
    assert M*value(word)+initial==value(''.join(out))+3**len(word)*final
    return ''.join(out)
def root(m,L):
    lo=0.0;hi=1.0
    for _ in range(70):
        mid=(lo+hi)/2
        if 3**(-m*mid)+3**(-L*mid)>1:lo=mid
        else:hi=mid
    return (lo+hi)/2

samples=[]
for k in range(101):
    M=621*81**k-20
    if k==0:
        c=69;P='1110010010';A='010';B='101110010010'
        assert verify_path(M,P,0,c)=='1011001101'
        assert verify_path(M,A,c,c)=='001'
        assert verify_path(M,B,c,c)=='110101101101'
    else:
        m=4*k+3;L=12*k+6;c=69*81**k
        P='1100'*k+'111'+'0'*(4*k)+'1'+'0'*(4*k+2)
        A='0'*(m-2)+'10'
        B='1100'*(k-1)+'11010110'+'0110'*(k-1)+'01'+'0'*(4*k+2)+'10'
        assert len(P)==len(B)==L and len(A)==m
        Q=verify_path(M,P,0,23)
        assert verify_path(M,'10',23,c)=='01'
        if k==1:q81=[1,36,27,12,1]
        else:q81=[1]+[0]*(k-1)+[36,0]+[4]*(k-2)+[31,12,1]
        assert value(Q)==sum(a*81**i for i,a in enumerate(q81))
        assert verify_path(M,A,c,c)=='0'*(m-1)+'1'
        Z=verify_path(M,B,c,c)
        if k==1:z81=[28,37,13,13,4]
        else:z81=[1]+[0]*(k-2)+[27,37]+[4]*(k-1)+[13,13]+[12]*(k-1)+[4]
        assert value(Z)==sum(a*81**i for i,a in enumerate(z81))
        P+='10'
    assert A[0]=='0' and B[0]=='1'
    assert verify_path(M,A+B,c,c)
    assert verify_path(M,B+A,c,c)
    if k<=5:samples.append({'k':k,'M':M,'prefix_length':len(P),'loop_lengths':[len(A),len(B)],'simple_lower_bound':log(2)/log(3)/(len(A)+len(B)),'moran_lower_bound':root(len(A),len(B))})
result={'status':'PASS','symbolic_polynomial_identities':7,'checked_k':list(range(101)),'scope':'Symbolic identities prove all k with digit-pattern argument; finite digitwise checks are supplemental.','samples':samples}
out=Path(__file__).with_name('family_positive_verification.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checked_k'},indent=2))
