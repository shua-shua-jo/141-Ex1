from dfa import DFA

def DFA_Complement(M):
  """
  A function that returns the complement of a given DFA.

  Parameter:
    M (DFA) : Deterministic Finite Automata to complement.

  Returns: 
    The complement of the DFA. That is, given a DFA.
    M = (Q, Sigma, Delta, q0, F), it returns M' = (Q, Sigma, Delta, q0, Q - F)
  """
  return (DFA(M.states, M.alphabet, M.transition, M.start_state, M.states.difference(M.accept_states)))