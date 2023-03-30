from dfa import DFA
from dfacomplement import DFA_Complement
from dfaintersection import DFA_Intersection
from dfaminimize import DFA_Strip

if __name__ == "__main__":
  
  # T1.1 a: Set of all nonempty binary strings with alternating symbols.
  M1a = DFA(
    states={"q0","q1","q2","q3"}, 
    alphabet={"0","1"}, 
    transition={
    "q0": {"0": "q1", "1": "q2"},
    "q1": {"0": "q3", "1": "q2"},
    "q2": {"0": "q1", "1": "q3"},
    "q3": {"0": "q3", "1": "q3"}}, 
    start_state="q0", 
    accept_states={"q1","q2"}
  )
  
  print(M1a)
  for input_states in ["01010101","1100010101","0101001","01","10"]:
    print(M1a.accepts(input_states))
  
  # M1a.render_diagram(filename="M1a")
  
  # T1.1 b: Set of all binary strings starting and ending with 101.
  M1b = DFA(
    states={"q0","q1","q2","q3","q4","q5","q6","q7"},
    alphabet={"0","1"},
    transition={
    "q0": {"0": "q6", "1": "q1"},
    "q1": {"0": "q2", "1": "q6"},
    "q2": {"0": "q6", "1": "q3"},
    "q3": {"0": "q4", "1": "q7"},
    "q4": {"0": "q5", "1": "q3"},
    "q5": {"0": "q5", "1": "q7"},
    "q6": {"0": "q6", "1": "q6"},
    "q7": {"0": "q4", "1": "q7"}},
    start_state="q0",
    accept_states={"q3"}
  )
  
  # print(M1b)
    
  # M1b.render_diagram(filename="M1b")
  
  #T1.2 a: Set of all binary strings that contain neither the substrings 01 nor 10.
  M2a = DFA(
    states={"q0","q1","q2","q3","q4"},
    alphabet={"0","1"},
    transition={
      "q0": {"0": "q1", "1": "q2"},
      "q1": {"0": "q1", "1": "q3"},
      "q2": {"0": "q4", "1": "q2"},
      "q3": {"0": "q4", "1": "q2"},
      "q4": {"0": "q1", "1": "q3"},
    },
    start_state="q0",
    accept_states={"q3","q4"}
  )
  
  # M2a_comp = DFA_Complement(M2a)
  # print(M2a_comp)
  # for input_string in ["10000001","101011001","10111","01","11","10"]:
  #   print(M2a_comp.accepts(input_string))
  
  #T1.2 b: Set of all binary strings that do not contain exactly two 0’s.
  M2b = DFA(
    states={"q0","q1","q2","q3"},
    alphabet={"0","1"},
    transition={
      "q0": {"0": "q1", "1": "q0"},
      "q1": {"0": "q2", "1": "q1"},
      "q2": {"0": "q3", "1": "q2"},
      "q3": {"0": "q3", "1": "q3"},
    },
    start_state="q0",
    accept_states={"q2"}
  )
  
  # M2b_comp = DFA_Complement(M2b)
  # print(M2b_comp)
  # for input_string in ["10000001","1111001","1010111","00","001","1000"]:
  #   print(M2b_comp.accepts(input_string))
    
  # print(M_complement)
  # for input_string in ["100", "111", "110"]:
  #   print(M_complement.__repr__() + " accepts " + input_string + "? " + M_complement.accepts(input_string))
    
    
  # M.render_diagram(filename="M")
  # M_complement.render_diagram(filename="M_complement")
  M_complement = DFA_Complement(M2a)
  M_intersection = DFA_Intersection(M2a, M_complement)
  print(M_intersection)
  M_intersection.render_diagram(filename="M_intersection")
  
  # M_strip = DFA_Strip(M)
  # print(M_strip)