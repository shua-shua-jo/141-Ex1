from dfa import DFA

def DFA_Complement(M):
  return (DFA(M.states, M.alphabet, M.transition, M.start_state, M.states.difference(M.accept_states)))