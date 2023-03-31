from dfa import DFA
from dfacomplement import DFA_Complement
from dfaintersection import DFA_Intersection
from dfaminimize import DFA_Strip, DFA_Minimize

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
  
  M1a.render_diagram(filename="M1a")
  
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
  
  print(M1b)
    
  M1b.render_diagram(filename="M1b")
  
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
  
  M2a.render_diagram(filename="M2a")
  
  M2a_comp = DFA_Complement(M2a)
  print(M2a_comp)
  
  M2a_comp.render_diagram(filename="M2a_comp")
  
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
  
  M2b.render_diagram(filename="M2b")
  
  M2b_comp = DFA_Complement(M2b)
  print(M2b_comp)
    
  M2b_comp.render_diagram(filename="M2b_comp")
  
    
  # debugging
  A1 = DFA(
    states={"q", "q0", "q1"},
    start_state="q",
    accept_states={"q0"},
    transition={
      "q" : {"0": "q0", "1": "q1"},
      "q0" : {"0": "q0", "1": "q0"},
      "q1" : {"0": "q1", "1": "q1"},
    },
    alphabet={"0", "1"}
  )
  A2 = DFA(
    states={"r", "r0"},
    start_state="r",
    accept_states={"r0"},
    transition={
      "r" : {"0": "r0", "1" : "r", "x": "r"},
      "r0" : {"0": "r0", "1" : "r", "x": "r"},
    },
    alphabet={"0", "1", "x"}
  )
  
  # M_intersection = DFA_Intersection(A1, A2)
  # print(M_intersection)  