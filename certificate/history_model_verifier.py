#!/usr/bin/env python3
"""Independent delayed-carry and k=0 certificate checks; no all-k closure check."""
from pathlib import Path
from collections import deque
import re,ast,json,hashlib
P=Path(__file__).resolve().parent
source=P/'parametric_reverse_invariant.txt'
text=source.read_text();I=range(-11,11)

def transitions(m,A,d):
    old=A%2
    for new in (0,1):
        for out in (0,1):
            numerator=d+20*new+out-23*old
            if numerator%3:continue
            target=(A//2+new*2**(m-1),numerator//3)
            assert -11<=target[1]<=10
            yield target,new,out

local=0
for d in I:
 for a in (0,1):
  for b in (0,1):
   for x in (0,1):
    value=d+20*a+b-23*x
    if value%3==0:
     assert -11<=value//3<=10
     local+=1
incoming={}
for m in (1,2,3,7):
 inc=[]
 for A in range(2**m):
  for d in I:
   for target,a,b in transitions(m,A,d):
    if target==(0,0):inc.append((A,d,a,b))
 assert sorted(inc)==[(0,-1,0,1),(0,0,0,0)]
 incoming[m]=inc
 first=list(transitions(m,0,0))
 assert ((2**(m-1),7),1,1) in first
 assert all(target==(0,0) and b==0 for target,a,b in first if a==0)

section=text.split('5. The base case')[1].split('6. Membership')[0]
provided=set()
for label,values in re.findall(r'A=(\d+): (\{[^\n]+\})',section):
 for d in ast.literal_eval(values):provided.add((int(label),d))
assert len(provided)==65
allstates=[(A,d) for A in range(8) for d in I]
rev={state:[] for state in allstates}
for state in allstates:
 for dest,a,b in transitions(3,*state):rev[dest].append(state)
seed=(0,-1);seen={seed};queue=deque([seed])
while queue:
 for pred in rev[queue.popleft()]:
  if pred not in seen:seen.add(pred);queue.append(pred)
assert seen==provided
assert (0,0) not in provided
for state in provided:assert set(rev[state])<=provided
assert all(621*3**(4*k)-20==23*3**(4*k+3)-20 for k in range(12))
result={'status':'PASS','proof_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'valid_local_carry_choices':local,'tested_delays_incoming_zero':incoming,
 'k0_backward_certificate_states':len(provided),'k0_certificate_equals_full_backward_reachable':True,
 'scope':'exact model range, zero-return predecessor, first input, and k=0 certificate; symbolic all-k closure reviewed separately by core'}
(P/'history_model_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
