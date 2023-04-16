from collections import defaultdict
from itertools import product
import copy 
from dfa import DFA

def DFA_Strip(M):
  """
  Algorithm functions like a Breadth First Search (BFS)

  DFA_Strip(M) : function

  Parameter: 
    M (DFA) : Deterministic Finite Automata to strip.

  Returns:
    the DFA whose unreachable states are removed 
  """

  """
  reachable_states : set
    Contains the set of reachable states. Initially contains the start state of the DFA
  new_states : set
    Contains the set of new states. That is, the set of previously unseen states reachable from one of the states in ReachableStates in one symbol in the alphabet.
		"""
  reachable_states = {M.start_state}
  new_states = {M.start_state}
  
  while len(new_states) != 0:
    """
    temp_states : set
      Contains all states reachable from the set NewStates using every symbol in the alphabet
    """
    temp_states = set()
    
    for r in new_states:
      for a in M.alphabet:
        temp_states = temp_states.union({M.transition[r][a]})
    
    """
    Update new_states and reachable_states
    """
    new_states = temp_states.difference(reachable_states)
    reachable_states = reachable_states.union(new_states)
    
  """
  Q_prime : set
    Contains the DFA's set of reachable states
  F_prime : set
    Contains the DFA's set of reachable accept states
  delta_prime : dict
    Transition function of the stripped DFA
  """
  Q_prime = reachable_states
  F_prime = M.accept_states.intersection(reachable_states)
  delta_prime = M.transition
  
  """
  Removes the outgoing edges / transitions from each unreachable state q 
  """
  for q in M.states.difference(Q_prime):
    for a in M.alphabet:
      delta_prime[q].pop(a)
      
  """
  Returns the stripped DFA
  """
  return (DFA(Q_prime, M.alphabet, delta_prime, M.start_state, F_prime))

def DFA_Minimize(M):
  """
  Minimizes a given Deterministic Finite Automata(DFA)

  Parameter:
    M (DFA): Deterministic Finite Automata to minimize.

  Returns:
    The minimized DFA.
    
  Attributes:
    states : set
      Collection of states
    alphabet : set
      Collection of symbols
    transition : dict
      Transition function of the form transition[state][symbol] = state
    start_state : str
      Initial state and an element of states
    accept_states : set
      Accepting or final states which is a subset of states
  """
  
  """
  Removes all unreachable states from the given DFA
  """
  M = DFA_Strip(M)

  """
  G : defaultdict
    Contains information regarding pairwise distinguishability between
    the cartesian product of self.states with itself. A pair of states
    (q, r) are distinguishable if G[q][r] == 1

  D_Prime : defaultdict
    Transition function for the minimized DFA
  """
  G = defaultdict(lambda: 0)
  for state in M.states:
    G[state] = defaultdict(lambda: 0)

  D_Prime = defaultdict(dict)
  for state in M.states:
    D_Prime[state] = defaultdict(str)

  """
  We initially mark all pairs of states (q, r) = (r, q) as distinguishiable (set to 1) such that q is an element of the set of accept states and r is the set of non-accepting states.
  """
  for (q, r) in product(M.accept_states, M.states.difference(M.accept_states)):
    G[q][r] = 1
    G[r][q] = 1

  """
  Temp : defaultdict
    Copy of the defaultdict G to be used for the updating part of the algorithm
  """
  Temp = copy.deepcopy(G)

  """
  update() : function
    checks all pairs of states from the cartesian product of self.states with itself such that given two states (q, r) and q != r, mark G[q][r] = 1 (distinguishable) if the pair (self.transition[q][a], self.transition[r][a]) is distinguishable. That is, if the pair of transition states given some symbol "a" in the alphabet is distinguishable 
  """
  def update():
    for (q, r) in product(M.states, M.states):
      if q == r: 
        continue
      for a in M.alphabet:
        if G[M.transition[q][a]][M.transition[r][a]] == 1:
          G[q][r] = 1
          G[r][q] = 1

  """
  Initial update
  """
  update()

  """
  Repeatedly apply the update() function as long as a change in G occurs in the previous iteration
  """
  while Temp != G:
    Temp = copy.deepcopy(G)
    update()
          
  """
  Q_Prime : set
    contains the set of all states for the minimized DFA
  
  F_Prime : set
    contains the set of all accept states for the minimized DFA
  
  q0_Prime : str
    Initial state of the minimized DFA and an element of Q_Prime
  
  equiv_class : defaultdict
    Stores the equivalence class of each state q in self.states. That is, [q] is the set of states that are indistinguishable from q
  """
  Q_Prime = set()
  F_Prime = set()
  q0_Prime = ""
  
  """
  qe : str
    equivalence class of q casted as a string since it needs to be used as a key for dictionaries. A state q is always indistinguishable from itself. 
  """
  qe = ""

  equiv_class = defaultdict(str)

  for a in M.alphabet:
    D_Prime[a] = dict()
  
  for q in M.states:
    qe = " ".join([r for r in M.states if G[q][r] == 0]) #[q]
    
    """
    Maps each state to its equivalence class
    """
    equiv_class[q] = qe
    
    """
    Adds qe to the set of states of the minimized DFA
    """
    Q_Prime.add(qe)

    """
    If the equivalence class of q contains the start state then set it to be the initial state of the minimized DFA 
    """
    if q == M.start_state:
      q0_Prime = qe

    """
    If the equivalence class of q contains an accept state then add it to the set of accept states of the minimized DFA 
    """
    if q in M.accept_states:
      F_Prime.add(qe)

  """
  retrieve_key(d, value) : function

  Parameters:
    d : defaultdict
    value : str

  Given the set of k-v pairs in d such that value == v, returns the first instance of the key of v if it exists
  """
  def retrieve_key(d, value):
    keys = [k for k, v in d.items() if v == value]
    if keys:
      return keys[0]
    return None

  """
  Iterate over the cartesian product of the set of states of the minimized DFA and the alphabet
  """
  for (qq, a) in product(Q_Prime, M.alphabet):
      """
			Retrieve the key of the equivalence class of qq 
			"""
      q = retrieve_key(equiv_class, qq)
      
      """
			Builds the transition function for the minimized DFA. Maps 
			D_Prime[qq][a] to the equivalence class of self.transition[q][a] for each state in Q_Prime 
			"""
      D_Prime[qq].update({a : equiv_class[M.transition[q][a]]})

  """
  Returns the minimized dfa
  """
  return DFA(Q_Prime, M.alphabet, D_Prime, q0_Prime, F_Prime)