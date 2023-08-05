"""
TODO
"""


import numpy as np
import matpopmod.mathtools as mt

# TODO: make sure both version work: NumPy's API was changed!
# Maybe put the line that follow in a separate module rgn, so 
# we can just "import rgn" whenever we need RNG in one of our modules
# We also need to provide an easy a way to reseed the random generator!
older_than_1_17 = [int(s) for s in np.__version__.split(".")] < [1, 17, 0]
if older_than_1_17:
  rng = np.random
else:
  rng = np.random.default_rng()


def irreducible_MPM(dim, number_edges = None, allow_mixed_transitions = True):
  r"""
  TODO
  """

  #---- Parse argument number_edges -----
  if number_edges is None:
    tot_edges = None
  elif isinstance(number_edges, int):
    tot_edges = number_edges
    if allow_mixed_transitions:
      p_vect = [1/3, 1/3, 1/3]
    else:
      p_vect = [1/2, 1/2, 0]
    s_edges, f_edges, m_edges = rng.multinomial(number_edges, p_vect)
  else:
    try:
      if len(number_edges) == 2:
        s_edges, f_edges = number_edges
        if allow_mixed_transitions:
          # to be coherent with other cases, we should use an hypergeometric
          # distribution for the number of mixed transitions. But for
          # simplicity we use a binomial one.
          m_edges = rng.binomial(
            min(s_edges, f_edges), max(s_edges, f_edges) / (dim*dim))
          aux = rng.binomial(m_edges, 1/2)
          s_edges -= aux
          f_edges -= (m_edges - aux)
        else:
          m_edges = 0
      elif len(number_edges) == 3:
        if allow_mixed_transitions:
          s_edges, f_edges, m_edges = number_edges
        else:
          raise ValueError("Mixed transitions are not allowed "
            "but a number of mixed transitions was supplied.")
      else:
        raise ValueError("Incorrect type for argument number of edges.")
      tot_edges = s_edges + f_edges + m_edges
    except:
      raise ValueError("Incorrect type for argument number of edges.")

  #---- Check that the number of edges is realizable -----
  if not tot_edges is None:
    if tot_edges < dim: 
      raise ValueError("Incorrect number of edges: " + 
        f"an irreducible {dim}x{dim} model has at least {dim} edges.")

  def free_edges():
    S = np.zeros((dim, dim))
    F = np.zeros((dim, dim))
    all_edges = [(i, j) for i in range(dim) for j in range(dim)]
    for _ in range(dim):
      i, j = all_edges.pop(rng.randrange(len(all_edges)))
      u = rng.random()
      if allow_mixed_transitions and u > 1/3 and u < 2/3:
        S[i, j] = 1
        F[i, j] = 1
      elif u < 0.5:
        S[i, j] = 1
      else:
        F[i, j] = 1
    while not mt.is_irreducible(S + F):
      i, j = all_edges.pop(rng.randrange(len(all_edges)))
      if rng.random() < 0.5:
        S[i, j] = 1
      else:
        F[i, j] = 1
    return (S, F)

  def fixed_edges(s_edges, f_edges, m_edges):
    tot_edges = s_edges + f_edges + m_edges
    S = np.array([[0]]) # to get in the loop directly
    F = np.array([[0]]) #
    while not mt.is_irreducible(S + F):
      S = np.zeros((dim, dim))
      F = np.zeros((dim, dim))
      current_number_edges = 0
      all_edges = [(i, j) for i in range(dim) for j in range(dim)]
      while current_number_edges < tot_edges:
        i, j = all_edges.pop(rng.randrange(len(all_edges)))
        if current_number_edges < m_edges:
          S[i, j] = 1
          F[i, j] = 1
        elif current_number_edges < m_edges + s_edges:
          S[i, j] = 1
        else:
          F[i, j] = 1
        current_number_edges += 1
    return (S, F)

  if tot_edges:
    S, F = fixed_edges(s_edges, f_edges, m_edges)
  else:
    S, F = free_edges()

  return (S, F)

