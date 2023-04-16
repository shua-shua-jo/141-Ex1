"""
CS 141 Python Module for Deterministic Finite Automata (DFA)
"""

from typing import Union

import pandas as pd
from pandas import DataFrame
from colormath.color_objects import sRGBColor
from graphviz import Digraph
from IPython.display import display

from visual_automata.colors import (
    create_palette,
    hex_to_rgb_color,
    list_cycler,
)

class DFA():
  """
  Class for Deterministic Finite
  
  Attributes
  ----------
    states : set
      collection of states
    alphabet : set
      collection of symbols
    transition : dict
      transition function of the form transition[state][symbols] -> state
    start_state : str
      the initial state
    accept_states : set
      the accepting or final state
  """
  
  def __init__(self, states=set(), alphabet=set(), transition=dict(), start_state=None, accept_states=set()) -> None:
    """
    Class initialization
    """
    self.states = set(states)
    self.alphabet = set(alphabet)
    self.transition = transition
    self.start_state = start_state
    self.accept_states = set(accept_states)
  
  def __repr__(self) -> str:
    """
    Class representation

    Returns:
        str: _description_
    """
    return "Deterministic Finite Automaton (DFA) at " + f"{hex(id(self))}"
  
  def __str__(self) -> str:
    """
    String representation

    Returns:
        str: _description_
    """
    
    str_self = (self.__repr__() + "\n" 
                + "States: " + f"{self.states}" + "\n"  
                + "Symbols: " + f"{self.alphabet}" + "\n" 
                + "Transitions: " + self.str_transition() + "\n" 
                + "Start State: " + f"{self.start_state}" + "\n" 
                + "Accept States: " + f"{self.accept_states}")
    return str_self
  
  def __get_next_current_state(
        self, current_state: str, input_symbol: str
    ) -> str:
        """
        Follow the transition for the given input symbol on the current state.

        Args:
            current_state (str): Current state.
            input_symbol (str): Input symbol.

        Returns:
            str: The next current state after entering input symbol.
        """
        if input_symbol in self.transition[current_state]:
            return self.transition[current_state][input_symbol]
  
  def str_transition(self):
    """
    String representation of the transition function.
    """
    string = "state, symbol -> state"
    for state in self.transition:
      state_transitions = self.transition[state]
      for symbol in state_transitions:
        string += "\n\t" + str(state) + " , " + symbol + " -> " + str(state_transitions[symbol])
    return string
  
  @staticmethod
  def __transition_steps(
      initial_state, final_states, input_str: str, transitions_taken: list, status: bool
  ) -> DataFrame:
      """
      Generates a table of taken transitions based on the input string and it's result.

      Args:
          initial_state (str): The DFA's initial state.
          final_states (set): The DFA's final states.
          input_str (str): The input string to run on the DFA.
          transitions_taken (list): Transitions taken from the input string.
          status (bool): The result of the input string.

      Returns:
          DataFrame: Table of taken transitions based on the input string and it's result.
      """
      current_states = transitions_taken.copy()
      for i, state in enumerate(current_states):
          if (
              state == initial_state and state in
              final_states
          ):
              current_states[i] = "->*" + state
          elif state == initial_state:
              current_states[i] = "->" + state
          elif state in final_states:
              current_states[i] = "*" + state

      new_states = current_states.copy()
      del current_states[-1]
      del new_states[0]
      inputs = [str(x) for x in input_str]

      transition_steps: dict = {
          "Current state:": current_states,
          "Input symbol:": inputs,
          "New state:": new_states,
      }

      transition_steps = pd.DataFrame.from_dict(
          transition_steps
      )
      transition_steps.index += 1
      transition_steps = pd.DataFrame.from_dict(
          transition_steps
      ).rename_axis("Step:", axis=1)
      if status:
          transition_steps.columns = pd.MultiIndex.from_product(
              [["[Accepted]"], transition_steps.columns]
          )
          return transition_steps
      else:
          transition_steps.columns = pd.MultiIndex.from_product(
              [["[Rejected]"], transition_steps.columns]
          )
          return transition_steps
  
  def accepts(self, input_string="", return_result=False) -> Union[bool, list, list]:
    """
    Check if DFA accepts the input string

    Parameters
    ----------
      input_string : str (optional) 
        the string to be read, default is the empty string
    """
    if not isinstance(input_string, str):
      raise TypeError(f"input_str should be a string. {input_string} is {type(input_string)}, not a string.")

    current_state = self.start_state
    transitions_taken = [current_state]
    symbol_sequence: list = []
    status: bool = True

    for symbol in input_string:
      symbol_sequence.append(symbol)
      current_state = self.__get_next_current_state(
          current_state, symbol
      )
      transitions_taken.append(current_state)

    if transitions_taken[-1] not in self.accept_states:
      status = False
    else:
      status = True

    taken_transitions_pairs = [
        (a, b, c)
        for a, b, c in zip(
            transitions_taken, transitions_taken[1:], symbol_sequence
        )
    ]
    taken_steps = self.__transition_steps(
        initial_state=self.start_state,
        final_states=self.accept_states,
        input_str=input_string,
        transitions_taken=transitions_taken,
        status=status,
    )
    if return_result:
      return status, taken_transitions_pairs, taken_steps
    else:
      return taken_steps
   
  @staticmethod  
  def __transitions_pairs(transitions: dict) -> list:
        """
        Generates a list of all possible transitions pairs for all input symbols.

        Args:
            transition_dict (dict): DFA transitions.

        Returns:
            list: All possible transitions for all the given input symbols.
        """
        transition_possibilities: list = []
        for state, transitions in transitions.items():
            for symbol, transition in transitions.items():
                transition_possibilities.append((state, transition, symbol))
        return transition_possibilities
      
  def render_diagram(
      self,
      input_str: str = None,
      filename: str = None,
      format_type: str = "png",
      path: str = None,
      title: str = None,
      *,
      view=False,
      cleanup: bool = True,
      horizontal: bool = True,
      reverse_orientation: bool = False,
      fig_size: tuple = (256, 256),
      font_size: float = 14.0,
      arrow_size: float = 0.85,
      state_seperation: float = 1.0,
  ) -> Digraph:
      """
      Generates the graph associated with the given DFA.

      Args:
          dfa (DFA): Deterministic Finite Automata to graph.
          input_str (str, optional): String list of input symbols. Defaults to None.
          filename (str, optional): Name of output file. Defaults to None.
          format_type (str, optional): File format [svg/png/...]. Defaults to "png".
          path (str, optional): Folder path for output file. Defaults to None.
          view (bool, optional): Storing and displaying the graph as a pdf. Defaults to False.
          cleanup (bool, optional): Garbage collection. Defaults to True.
          horizontal (bool, optional): Direction of node layout. Defaults to True.
          reverse_orientation (bool, optional): Reverse direction of node layout. Defaults to False.
          fig_size (tuple, optional): Figure size. Defaults to (8, 8).
          font_size (float, optional): Font size. Defaults to 14.0.
          arrow_size (float, optional): Arrow head size. Defaults to 0.85.
          state_seperation (float, optional): Node distance. Defaults to 0.5.

      Returns:
          Digraph: The graph in dot format.
      """
      # Converting to graphviz preferred input type,
      # keeping the conventional input styles; i.e fig_size(8,8)
      fig_size = ", ".join(map(str, fig_size))
      font_size = str(font_size)
      arrow_size = str(arrow_size)
      state_seperation = str(state_seperation)

      # Defining the graph.
      graph = Digraph(strict=False)
      graph.attr(
          size=fig_size,
          dpi="250",
          ranksep=state_seperation,
      )
      if title is not None:
          graph.attr(
            label=title,
            labelloc="top",
            labeljust="center",
            )
      if horizontal:
          graph.attr(rankdir="LR")
      if reverse_orientation:
          if horizontal:
              graph.attr(rankdir="RL")
          else:
              graph.attr(rankdir="BT")

      # Defining arrow to indicate the initial state.
      graph.node("Initial", label="", shape="point", fontsize=font_size)

      # Defining all states.
      for state in sorted(self.states):
          if (
              state in self.start_state and state in
              self.accept_states
          ):
              graph.node(state, shape="doublecircle", fontsize=font_size, style='filled', fillcolor="#4ea1ce", color="red")
          elif state in self.start_state:
              graph.node(state, shape="circle", fontsize=font_size, style='filled', fillcolor="#4ea1ce")
          elif state in self.accept_states:
              graph.node(state, shape="doublecircle", fontsize=font_size, style='filled', fillcolor="#ea9e3a", color="red")
          else:
              graph.node(state, shape="circle", fontsize=font_size)

      # Point initial arrow to the initial state.
      graph.edge("Initial", self.start_state, arrowsize=arrow_size)

      # Define all tansitions in the finite state machine.
      all_transitions_pairs = self.__transitions_pairs(self.transition)

      if input_str is None:
          for pair in all_transitions_pairs:
              graph.edge(
                  pair[0],
                  pair[1],
                  label=" {} ".format(pair[2]),
                  arrowsize=arrow_size,
                  fontsize=font_size,
              )
          status = None

      else:
          status, taken_transitions_pairs, taken_steps = self.accepts(
              input_string=input_str, return_result=True
          )
          remaining_transitions_pairs = [
              x
              for x in all_transitions_pairs
              if x not in taken_transitions_pairs
          ]

          # Define color palette for transitions
          if status:
              start_color = hex_to_rgb_color("#FFFF00")
              end_color = hex_to_rgb_color("#00FF00")
          else:
              start_color = hex_to_rgb_color("#FFFF00")
              end_color = hex_to_rgb_color("#FF0000")
          number_of_colors = len(input_str)
          palette = create_palette(
              start_color, end_color, number_of_colors, sRGBColor
          )
          color_gen = list_cycler(palette)

          # Define all tansitions in the finite state machine with traversal.
          counter = 0
          for pair in taken_transitions_pairs:
              counter += 1
              edge_color = next(color_gen)
              graph.edge(
                  pair[0],
                  pair[1],
                  label=" [{}]\n{} ".format(counter, pair[2]),
                  arrowsize=arrow_size,
                  fontsize=font_size,
                  color=edge_color,
                  penwidth="2.5",
              )

          for pair in remaining_transitions_pairs:
              graph.edge(
                  pair[0],
                  pair[1],
                  label=" {} ".format(pair[2]),
                  arrowsize=arrow_size,
                  fontsize=font_size,
              )

      # Write diagram to file. PNG, SVG, etc.
      if filename:
          graph.render(
              filename=filename,
              format=format_type,
              directory=path,
              cleanup=cleanup,
          )

      if view:
          graph.render(view=True)
      if input_str:
          display(taken_steps)
          return graph
      else:
          return graph