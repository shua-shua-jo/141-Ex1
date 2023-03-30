from itertools import product
from dfa import DFA

def DFA_Strip(M):
  reachable_states = M.start_state
  new_states = M.start_state
  while len(new_states) != 0:
    temp_states = set()
    for r in new_states:
      for a in M.alphabet:
        temp_states = temp_states.union(dict({r : {a : M.transition.get(new_states)[a]}}))
    new_states = temp_states.difference(reachable_states)
    reachable_states = str(set(reachable_states).union(new_states))
  Q_prime = reachable_states
  F_prime = M.accept_states.intersection(reachable_states)
  transition_comp = M.transition
  for (q, a) in (product(M.states.difference(Q_prime), M.alphabet)):
    transition_comp.pop(q,a)
  return (DFA(Q_prime, M.alphabet, transition_comp, M.start_state, F_prime))

def DFA_Minimize(M):
  return M