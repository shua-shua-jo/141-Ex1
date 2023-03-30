from itertools import product
from dfa import DFA

def DFA_Intersection(M1, M2):
  states = set(product(M1.states, M2.states))
  alphabet = M1.alphabet.intersection(M2.alphabet)
  print("States: ", states)
  print("Alphabet: ", alphabet)
  transition = dict()
  for (q1, q2) in states:
    value = dict()
    for a in alphabet:
      value.update({a : str((M1.transition.get(q1)[a], M2.transition.get(q2)[a]))})
    transition.update({str((q1,q2)) : value})
  start_state = (M1.start_state, M2.start_state)
  accept_states = product(M1.accept_states, M2.accept_states)
  return (DFA(states, alphabet, transition, start_state, accept_states))