"""
CMSC 141 C Exercise 1
Name: Elijah Joshua DL. Abello
      Sean Thomas C. Vizconde
Date: 17 April 2023
"""

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
  
  M1a.render_diagram(filename="M1a", path="Item 1.1 graphs/a", title="T1.1 Set of all nonempty binary strings with alternating symbols.")
  
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
  
  M1b.render_diagram(filename="M1b", path="Item 1.1 graphs/b", title="T1.1 b: Set of all binary strings starting and ending with 101.")
  

  #T1.2 a: Set of all binary strings that contain neither the substrings 01 nor 10.
  M2a = DFA(
    states = {"q0", "q1", "q2", "q3"},
    alphabet = {"0", "1"},
    transition = {
      "q0": { "0": "q1", "1": "q2" },
      "q1": { "0": "q1", "1": "q3" },
      "q2": { "0": "q3", "1": "q2" },
      "q3": { "0": "q3", "1": "q3" }
    },
    start_state = "q0",
    accept_states = {"q3"}
  )
  
  print(M2a)
    
  M2a.render_diagram(filename="M2a", path="Item 1.2 graphs/a", title="T1.2 a: Set of all binary strings that contain either the substrings 01 or 10.")
  
  M2a_comp = DFA_Complement(M2a)
  print(M2a_comp)
  
  M2a_comp.render_diagram(filename="M2a_comp", path="Item 1.2 graphs/a", title="T1.2 a: Set of all binary strings that contain neither the substrings 01 nor 10.")
  
  
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
  
  M2b.render_diagram(filename="M2b", path="Item 1.2 graphs/b", title="T1.2 b: Set of all binary strings that contain exactly two 0's.")
  
  M2b_comp = DFA_Complement(M2b)
  print(M2b_comp)
    
  M2b_comp.render_diagram(filename="M2b_comp", path="Item 1.2 graphs/b", title="T1.2 b: Set of all binary strings that do not contain exactly two 0's.")
  
  #T1.3 a: The set of all binary strings that start with 0 and have at most one 1.
  
  L1a = DFA(
    states={"q0","q1","q2"},
    alphabet={"0","1"},
    transition={
      "q0": {"0": "q1", "1": "q2"},
      "q1": {"0": "q1", "1": "q1"},
      "q2": {"0": "q2", "1": "q2"}  
    },
    start_state="q0",
    accept_states={"q1"}    
  )
  
  L1a.render_diagram(filename="L1a", path="Item 1.3 graphs/a", title="The set of all binary strings that start with 0.")
  
  L2a = DFA(
    states={"r0","r1","r2","r3"},
    alphabet={"0","1"},
    transition={
      "r0": {"0": "r1", "1": "r2"},
      "r1": {"0": "r1", "1": "r2"},
      "r2": {"0": "r2", "1": "r3"},
      "r3": {"0": "r3", "1": "r3"},
    },
    start_state="r0",
    accept_states={"r2"}    
  )
  
  L2a.render_diagram(filename="L2a", path="Item 1.3 graphs/a", title="The set of all binary strings that have at most one 1.")
  
  La_inter = DFA_Intersection(L1a, L2a)
  print(La_inter)
  La_inter.render_diagram(filename="La_inter", path="Item 1.3 graphs/a", title="T1.3 a: The set of all binary strings that start with 0 and have at most one 1.")
  
  # La_inter_stripped = DFA_Strip(La_inter)
  # La_inter_stripped.render_diagram(filename="La_inter_stripped", path="Item 1.3 graphs/a", title="Stripped version of T1.3a")
  
  La_inter_minimized = DFA_Minimize(La_inter)
  La_inter_minimized.render_diagram(filename="La_inter_minimize", path="Item 1.3 graphs/a", title="Minimized version of T1.3a")
  
  print(La_inter_minimized)
  #T1.3 b: The set of all binary strings that having even length and an odd number of 1’s.

  L1b = DFA(
    states={"q0","q1","q2"},
    alphabet={"0","1"},
    transition={
      "q0": {"0": "q1", "1": "q1"},
      "q1": {"0": "q2", "1": "q2"},
      "q2": {"0": "q1", "1": "q1"}  
    },
    start_state="q0",
    accept_states={"qo","q2"}    
  )
  
  L1b.render_diagram(filename="L1b", path="Item 1.3 graphs/b", title="The set of all binary strings that having even length.")
  
  L2b = DFA(
    states={"r0","r1","r2"},
    alphabet={"0","1"},
    transition={
      "r0": {"0": "r0", "1": "r1"},
      "r1": {"0": "r2", "1": "r2"},
      "r2": {"0": "r2", "1": "r1"},
    },
    start_state="r0",
    accept_states={"r1"}    
  )
  
  L2b.render_diagram(filename="L2b", path="Item 1.3 graphs/b", title="The set of all binary strings that having an odd number of 1's.")
  
  Lb_inter = DFA_Intersection(L1b, L2b)
  print(Lb_inter)
  Lb_inter.render_diagram(filename="Lb_inter", path="Item 1.3 graphs/b", title="T1.3 b: The set of all binary strings that having even length and an odd number of 1’s.")
  
  # Lb_inter_stripped = DFA_Strip(Lb_inter)
  # Lb_inter_stripped.render_diagram(filename="Lb_inter_stripped", path="Item 1.3 graphs/b", title="Stripped version of T1.3b")
  
  Lb_inter_minimized = DFA_Minimize(Lb_inter)
  Lb_inter_minimized.render_diagram(filename="Lb_inter_minimized", path="Item 1.3 graphs/b", title="Minimized version of T1.3b")
  
  print(Lb_inter_minimized)
  