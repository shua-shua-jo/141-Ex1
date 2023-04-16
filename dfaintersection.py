"""
CMSC 141 X Exercise 1
Name: Elijah Joshua DL. Abello
      Sean Thomas C. Vizconde
Date: 17 April 2023
"""

from itertools import product
from dfa import DFA


def DFA_Intersection(M1, M2):
  """
  A function that returns the intersection of two DFAs.
  DFA_Intersection(M1, M2) : function

  Parameters:
    M1 : DFA
    M2 : DFA

  Returns:
    The intersection of the M1 and M2.
  """

  """
  states : list[tuple]
    Cartesian product between the states of the two input DFAs

  alphabet : set
    Intersection between the alphabet of the two input DFAs

  delta : dict
    Transition function for the intersection of the two input DFAs 
  """
  states = set(product(M1.states, M2.states))
  new_states = set(" ".join(state) for state in states)
  alphabet = M1.alphabet.intersection(M2.alphabet)
  transition = dict()
  for (q1, q2) in states:
    """
    For each ordered pair in states (Q) and every symbol a in alphabet, map the pair into their pairwise transition which is also an element of Q
    """
    value = dict()
    for a in alphabet:
      value.update({a : " ".join((M1.transition[q1][a], M2.transition[q2][a]))})
    transition.update({" ".join((q1,q2)) : value})
  
  """
  start_state : tuple
    Initial state of the DFA intersection

  The initial state of the intersection of two DFAs is the ordered pair consisting of the initial state of each DFA
  """
  start_state = " ".join((M1.start_state, M2.start_state))
  
  """
  accept_states : list[tuple]
    Cartesian product between the accept states of the two input DFAs
  """
  accept_states = product(M1.accept_states, M2.accept_states)
  
  # converts tuples to string
  new_accept_states = set(" ".join(state) for state in accept_states)
  
  """
  Returns the intersection of the two DFAs
  """
  return (DFA(new_states, alphabet, transition, start_state, new_accept_states))