"""
This module regroups miscellaneous general-purpose tools that are used by other
modules but are typically not meant to be used by the end user.
"""

import ast

import numpy as np


##### PSEUDO-RANDOM NUMBER GENERATION #####
if np.lib.NumpyVersion(np.__version__) < "1.17.0":
  rng = np.random
else:
  rng = np.random.default_rng()

def set_rng_seed(n):
  global rng
  if np.lib.NumpyVersion(np.__version__) < "1.17.0":
    # This changes the seed for all of NumPy
    rng.seed(n)
  else:
    # This only changes the seed of the generator used by matpopmod
    rng = np.random.default_rng(n)


##### GLOBAL CONSTANTS FOR FLOAT COMPARISON #####
_REL_TOL = 1e-10
_ABS_TOL = 1e-12 


#### GLOBAL SWITCH FOR WARNINGS #####
_ISSUE_WARNINGS = True


class NotAvailable(Exception):
  """
  Exception raised when a descriptor cannot be computed, either because
  only the projection matrix is known and the computation requires
  the survival matrix **S** and the fertility matrix **F**, or because there is
  a problem of some sort with the model (e.g, singular matrix **S**).

  This exception is not meant to be used is situations where the fact that
  a descriptor cannot be computed does not necessarily indicate a problem with
  the model but simply that the descriptor is not defined (as can happen, e.g,
  when the projection matrix is not primitive). In this case, a warning is
  issued and ``nan`` values are returned.
  """
  pass

class MissingArguments(Exception):
  """Raise to indicate missing arguments."""
  pass

class UnexpectedMathError(Exception):
  """
  Raised to indicate failure of a mathematical assertion that can
  only result from numerical errors or a serious bug in the code.
  """
  pass

class InadequateMatrix(Exception):
  """Raised to indicate non-specific problems with a matrix argument."""
  pass

class NonConvergentMatrix(Exception):
  """Raised to indicate that a matrix is (numerically) not convergent."""
  pass

class IncorrectDims(InadequateMatrix):
  """Raised to indicate a problem in the dimensions of matrices."""
  pass

class MissingEntries(InadequateMatrix):
  """Raised to indicate that a matrix contains ``nan`` entries."""
  pass

class NegativeEntries(InadequateMatrix):
  """Raised to indicate that a matrix contains negative entries."""
  pass

class CannotCompute(InadequateMatrix):
  """Raised to indicate that a quantity cannot be computed numerically."""
  pass


def assert_square(M, name=""):
  """
  Check that the NumPy array `M` is a square matrix;
  raise :exc:`IncorrectDims` otherwise.
  """
  if M.ndim != 2:
    raise IncorrectDims(f"Matrix {name} is not 2-dimensional: {M.ndim}-D.")
  n, m = M.shape
  if n != m:
    raise IncorrectDims(f"Matrix {name} is not square: {n}x{m}.")

def assert_nonnegative(M, name=""):
  """
  Check that the NumPy array `M` has non-negative entries;
  raise :exc:`MissingEntries` or :exc:`NegativeEntries` otherwise.
  """
  if np.isnan(M).any():
    pos = ", ".join([str(ij) for ij in zip(*np.isnan(M).nonzero())])
    raise MissingEntries(f"Array {name} contains NaN entries: {pos}.")
  if (M < 0).any():
    pos = ", ".join([str(ij) for ij in zip(*(M < 0).nonzero())])
    raise NegativeEntries(f"Array {name} contains negative entries: {pos}.")

def assert_same_dimensions(M, N, name_M="", name_N=""):
  """
  Check that the NumPy arrays `M` and `N` have the same dimensions;
  raise :exc:`IncorrectDims` otherwise.
  """
  if M.shape != N.shape:
    names =  ""
    dims =  f"{M.shape} vs {N.shape}"
    if not (name_M == "" or name_N == ""):
      names = f"of {name_M} and {name_N} "
    raise IncorrectDims(f"Matrix dimensions {names}do not match: {dims}.")

def assert_substochastic(M, name=""):
  r"""
  Check that the entries of the NumPy array `M` are non-negative, that each of
  the columns sums to at most 1, and that at least one of them sums to less
  than 1. Raise appropriate exceptions otherwise.
  """
  assert_nonnegative(M, name)
  sum_columns = np.sum(M, axis=0)  
  if (sum_columns > 1).any():
    raise InadequateMatrix(f"Matrix {name} has a column whose sum is > 1.")
  if (sum_columns == 1).all():
    raise InadequateMatrix(
            f"Matrix {name} does not have a column whose sum is < 1.")

def assert_vector(vect, length, name=""):
  r"""
  Check that `vect` is a vector of length `length`. Raise exceptions
  otherwise. The argument `name` is used in error messages.
  """
  try:
    if vect.shape != (length,):
      if len(vect.shape) == 1:
        raise ValueError(
          f"Incorrect length for {name}: expected {length}, got {len(vect)}.")
      else:
        raise ValueError(
          f"Incorrect argument {name}: {vect} is not a vector.")
  except:
    raise ValueError(f"Incorrect argument {name}: "
      f"expected a vector of length {length}, got {vect}.")

def assert_positive_integer(n, name=""):
  r"""
  Check that the argument is a positive integer. Raises appropriate
  exceptions otherwise.
  """
  if not isinstance(n, int) or isinstance(n, np.int_):
    raise ValueError(f"Incorrect argument {name} = {n}: not an integer.")
  if n <= 0:
    raise ValueError(f"Incorrect argument {name} = {n} <= 0.")

def assert_nonnegative_number(n, name=""):
  r"""
  Check that the argument is a non-negative number. Raises appropriate
  exceptions otherwise.
  """
  try:
    negative = (n < 0)
  except TypeError:
    raise ValueError(f"Incorrect argument {name} = {n}: not a number.")
  if negative:
    raise ValueError(f"Incorrect argument {name} = {n} < 0.")

def represents_integer(n):
  r"""
  Whether the argument corresponds to an integer, be it a Python ``int`` /
  ``float`` or a NumPy ``int_`` / ``float_``.
  """
  if isinstance(n, (int, np.int_)):
    return True
  if isinstance(n, float):
    return n.is_integer()
  if isinstance(n, np.float_):
    return np.mod(n, 1) == 0
  return False

def vector_of_nan(n):
  """Returns a 1-D NumPy array of ``np.nan`` with length `n`.""" 
  v = np.empty((n,))
  v[:] = np.nan
  return v

def matrix_of_nan(n):
  """Returns a 2-D NumPy array of ``np.nan`` with dimension (`n`, `n`).""" 
  M = np.empty((n, n))
  M[:] = np.nan
  return M

def parse_array_string(data):
  """
  Converts a string representing a matrix into a list of lists.
  Rows have to be separated by semicolons and columns by spaces and/or
  commas. Example:

  >>> convert_from_string("1 2; 3 4")
  [[1, 2], [3, 4]]

  Copied from NumPy's deprecated matrices :func:`_convert_from_string`.
  """
  for char in '[]':
    data = data.replace(char, '')
  rows = data.split(';')
  newdata = []
  count = 0
  for row in rows:
    trow = row.split(',')
    newrow = []
    for col in trow:
      temp = col.split()
      newrow.extend(map(ast.literal_eval, temp))
    if count == 0:
      Ncols = len(newrow)
    elif len(newrow) != Ncols:
      raise ValueError("Rows not the same size.")
    count += 1
    newdata.append(newrow)
  return newdata

