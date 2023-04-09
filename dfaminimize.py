from collections import defaultdict
from itertools import product
import copy 
from dfa import DFA

def DFA_Strip(M):
  reachable_states = {M.start_state}
  new_states = {M.start_state}
  
  while len(new_states) != 0:
    temp_states = set()
    
    for r in new_states:
      for a in M.alphabet:
        temp_states = temp_states.union({M.transition[r][a]})
    new_states = temp_states.difference(reachable_states)
    reachable_states = reachable_states.union(new_states)
    
  Q_prime = reachable_states
  F_prime = M.accept_states.intersection(reachable_states)
  delta_prime = M.transition
  
  for q in M.states.difference(Q_prime):
    for a in M.alphabet:
      delta_prime[q].pop(a)
  
  return (DFA(Q_prime, M.alphabet, delta_prime, M.start_state, F_prime))

def DFA_Minimize(M):
  M = DFA_Strip(M)

  G = defaultdict(lambda: 0)
  for state in M.states:
    G[state] = defaultdict(lambda: 0)

  D_Prime = defaultdict(dict)
  for state in M.states:
    D_Prime[state] = defaultdict(str)

  for (q, r) in product(M.accept_states, M.states.difference(M.accept_states)):
    G[q][r] = 1
    G[r][q] = 1

  Temp = copy.deepcopy(G)

  def update():
    for (q, r) in product(M.states, M.states):
      if q == r: 
        continue
      for a in M.alphabet:
        if G[M.transition[q][a]][M.transition[r][a]] == 1:
          G[q][r] = 1
          G[r][q] = 1

  update()

  while Temp != G:
    Temp = copy.deepcopy(G)
    update()
          
  Q_Prime = set()
  F_Prime = set()
  q0_Prime = ""
  qe = ""

  equiv_class = defaultdict(str)

  for a in M.alphabet:
    D_Prime[a] = dict()
  
  for q in M.states:
    qe = ' '.join([r for r in M.states if G[q][r] == 0]) #[q]
    equiv_class[q] = qe
    
    Q_Prime.add(qe)

    if q == M.start_state:
      q0_Prime = qe

    if q in M.accept_states:
      F_Prime.add(qe)

  def retrieve_key(d, value):
    keys = [k for k, v in d.items() if v == value]
    if keys:
      return keys[0]
    return None

  for (qq, a) in product(Q_Prime, M.alphabet):
      q = retrieve_key(equiv_class, qq)
      D_Prime[qq].update({a : equiv_class[M.transition[q][a]]})

  return DFA(Q_Prime, M.alphabet, D_Prime, q0_Prime, F_Prime)