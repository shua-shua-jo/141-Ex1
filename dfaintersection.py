from itertools import product
from dfa import DFA


def DFA_Intersection(M1, M2):
  states = set(product(M1.states, M2.states))
  new_states = set(" ".join(state) for state in states)
  alphabet = M1.alphabet.intersection(M2.alphabet)
  transition = dict()
  for (q1, q2) in states:
    value = dict()
    for a in alphabet:
      value.update({a : " ".join((M1.transition[q1][a], M2.transition[q2][a]))})
    transition.update({" ".join((q1,q2)) : value})
  start_state = " ".join((M1.start_state, M2.start_state))
  accept_states = product(M1.accept_states, M2.accept_states)
  new_accept_states = set(" ".join(state) for state in accept_states)
  return (DFA(new_states, alphabet, transition, start_state, new_accept_states))