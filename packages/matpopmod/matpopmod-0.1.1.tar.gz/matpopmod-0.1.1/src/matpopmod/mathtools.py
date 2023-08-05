"""
This module is a collection of mathematical functions.
"""

import math
import warnings

import numpy as np
import matpopmod.utils as ut


def spectral_radius(M):
  """
  Returns the spectral radius of the matrix **M**, i.e. the maximum of the
  modulus of its eigenvalues. 
  """
  return np.abs(np.linalg.eigvals(M)).max()


def geometric_multiplicity(M, lmbd):
  r"""
  Returns the geometric multiplicity of *λ* as an eigenvalue of **M**, that is,

  .. math::

    \mathrm{dim}(\mathrm{ker}(\mathbf{M} - \lambda \mathbf{I}))
    \;=\; n - \mathrm{rank}(\mathbf{M} - \lambda \mathbf{I}), 

  where *n* is the number of rows/columns of **M**. The implementation uses
  NumPy's :func:`linalg.matrix_rank`, which uses singular value decomposition.
  This technique is the standard but is relatively error-prone.
  """
  ut.assert_square(M)
  n, _ = M.shape
  return n - np.linalg.matrix_rank(M - lmbd * np.eye(n))


def are_linearly_independent(vectors):
  r"""
  Whether the vectors :math:`\mathbf{v}_0, \ldots, \mathbf{v}_{m}`
  of the iterable `vectors` are linearly independent,meaning that

  .. math::

    \big(\mu_0 \mathbf{v}_0 + \cdots + \mu_m \mathbf{v}_m \;=\; 0\big)
    \implies \big(\mu_0 = \cdots = \mu_m = 0\big)

  This implementation uses NumPy's :func:`linalg.matrix_rank`, which uses
  singular value decomposition.
  """
  m = len(vectors)
  if m == 0:
    return True
  else:
    if any(not isinstance(v, np.ndarray) or v.ndim != 1 for v in vectors):
      raise ValueError("One of elements supplied is not a vector")
    else:
      n = np.shape(vectors[0])[0]
      if any(v.shape[0] != n for v in vectors):
        raise ut.IncorrectDims("Vectors do not have the same length.")
      else:
        if m > n:
          return False
        else:
          a = np.array(vectors)
          rank = np.linalg.matrix_rank(a)
          return (rank >= m)


def eigen_elements(M, eps = 1e-12, left = False):
  r"""
  .. rst-class:: nospaceafter

  Returns the eigenvalues and right eigenvectors of the matrix **M**,
  as a couple (`eigvals`, `eigvects`), where:

  - `eigvals` is the tuple of eigenvalues, in decreasing order of their
    modulus and increasing order of their argument in :math:`[0, 2\pi[`.
    Note that we make sure that, for non-negative matrices, the Perron
    root (that is, the spectral radius) is returned first. As a result, due
    to roundoff error it is possible that, numerically,
    
    .. code-block::
    
      abs(eigvals[0]) < abs(eigvals[1])

    Each eigenvalue is repeated according to its algebraic multiplicity,
    and real eigenvalues are returned as floats rather than as complex numbers.

  - `eigvects` is the tuple of right-eigenvectors, where
    `eigvects[i]` is the right-eigenvector associated to `eigvals[i]`.
    Each eigenvector :math:`(x_0, \ldots, x_{n-1})` is normalized so that

    i. :math:`\mathrm{Re}(x_0) \geq 0` (and :math:`\mathrm{Re}(x_1) \geq 0`
       if :math:`\mathrm{Re}(x_0) = 0`, etc)
    ii. :math:`\sum_i |x_i| = 1` 

  If the parameter `left` is set to ``True``, then the left eigenvectors
  are computed as well and a tuple (`eigvals`, `right_eigvects`,
  `left_eigvects`) is returned. The same normalization is used for the
  left eigenvectors as for the right ones.
  
  The parameter `eps` is a threshold for rounding to zero: any real or
  imaginary part smaller than `eps` will be set to 0. This is useful, e.g,
  because eigen-elements that are supposed to be real-valued can have small
  imaginary parts due to numerical errors. The default value `eps=1e-12` should
  be a bit higher than the typical precision of the calculation of the
  eigen-elements, but well below its guaranteed precision in the worst case.

  This function uses NumPy's :func:`linalg.eig`, of which it is essentially
  a wrapper.

  Be aware of the following facts:

  1. The geometric multiplicity of an eigenvalue (dimension of
     the associated eigenspace) is less than or equal to its algebraic
     multiplicity (multiplicity as a root of the characteristic polynomial).
     Thus, some elements of `eigvects` can be linear combinations
     of each others.  Do not interpret the fact that this function returns *k*
     distinct eigenvectors associated to an eigenvalue *λ* as indicating that 
     :math:`\mathrm{dim}(\mathrm{ker}(\mathbf{M} - \lambda \mathbf{I})) = k`.

  2. The eigenvectors are not uniquely defined: any linear combination of
     eigenvectors associated to a given eigenvalue is also an eigenvector
     for this eigenvalue.

  3. Numerical computation of eigen-elements is always approximate, and
     relatively prone to error. One can evaluate the precision of an
     eigen-pair :math:`(\lambda, \mathbf{w})` simply 
     by inspecting :math:`\mathbf{Mw} - \lambda \mathbf{w}`:

     >>> M = numpy.random.random((3, 3))
     >>> M
     array([[0.88823173, 0.83257899, 0.55164511],
            [0.91645353, 0.61479613, 0.18260078],
            [0.43758445, 0.84650269, 0.41032252]])
     >>> lmbd, w = mathtools.eigenvalues_and_vectors(M)
     >>> M @ w[0] - lmbd[0] * w[0]
     array([ 2.22044605e-16, -2.22044605e-16,  3.33066907e-16])

  """
  vals, vects = np.linalg.eig(M)
  # Round-off to zero
  vals.real = np.where(np.abs(vals.real) < eps, 0, vals.real)
  vects.real = np.where(np.abs(vects.real) < eps, 0, vects.real)
  try:
    vals.imag = np.where(np.abs(vals.imag) < eps, 0, vals.imag)
  except TypeError:
    pass
  try:
    vects.imag = np.where(np.abs(vects.imag) < eps, 0, vects.imag)
  except TypeError:
    pass
  # Sort in lexicographic order of (-|lmbd|, arg(lmbd))
  x = np.angle(vals)
  args = np.where(x < 0, x + 2 * np.pi, x)
  perron_root = np.max(vals.real) # this is resilient to numerical errors
  isnt_perron_root = (vals.real != perron_root)
  indices = np.lexsort((args, -np.abs(vals), isnt_perron_root))
  vals = vals[indices]
  vects = vects[:,indices]
  # Normalize vectors
  normed = []
  for v in vects.T:
    if np.any(v.real != 0):
      i = np.argmax(v.real != 0) # index of first non-zero entry
      v = v * np.sign(v[i].real)
    norm_1 = np.sum(np.abs(v))
    if norm_1 > eps:
      v = v / norm_1
    normed.append(v)
  # Conversion to tuple (and to real when relevant)
  vals_out = tuple([lmbd.real if lmbd.imag == 0 else lmbd for lmbd in vals])
  vects_out = tuple([v.real if np.all(v.imag == 0) else v for v in normed])
  if left:
    # Note that the eigenvalues computed from M (not M.T) are returned.
    lvals, lvects = np.linalg.eig(M.T)
    lvects.real = np.where(np.abs(lvects.real) < eps, 0, lvects.real)
    try:
      lvects.imag = np.where(np.abs(lvects.imag) < eps, 0, lvects.imag)
    except TypeError:
      pass
    # s[i] = j s.t. vals[i] ~= lvals[j]
    s = [np.argmin(np.abs(lvals - vals[i])) for i in range(len(vals))]
    lvects = lvects[:,s]
    # Normalize vectors
    normed = []
    for v in lvects.T:
      if np.any(v.real != 0):
        i = np.argmax(v.real != 0) # index of first non-zero entry
        v = v * np.sign(v[i].real)
      norm_1 = np.sum(np.abs(v))
      if norm_1 > eps:
        v = v / norm_1
      normed.append(v)
    lvects_out = tuple([v.real if np.all(v.imag == 0) else v for v in normed])
    return (vals_out, vects_out, lvects_out)
  else:
    return (vals_out, vects_out)


def is_substochastic(M):
  r"""
  Whether the matrix :math:`\mathbf{M} = (m_{ij})` is column-substochastic --
  that is, a proper submatrix of a column-stochastic matrix. In other words,
  returns ``True`` when **M** is non-negative and satisfies
  :math:`\sum_i m_{ij} \leq 1` for all *j* and
  :math:`\sum_i m_{ij} < 1` for some *j*.
  
  Note that this does not ensure that
  :math:`\mathbf{M}^t \to 0` as :math:`t \to \infty` and that
  :math:`(\mathbf{I} - \mathbf{M})^{-1}` exists. A sufficient condition for
  this would be that all columns sum to less than 1, but this condition is
  too strict for our purposes (indeed, matrix population models with a survival
  matrix having a column that sum to to 1 are sometimes encountered in
  practice).
  """
  sum_columns = np.sum(M, axis=0)  
  return (M >= 0).all() and (sum_columns <= 1).all() and (sum_columns < 1).any()


def is_primitive(M):
  r"""
  This implementation uses the fact that a non-negative square matrix **M** is
  primitive if and only if :math:`\mathbf{M}^{n^2 - 2n + 2}` is positive (see
  e.g. Corollary 8.5.8 in [HoJo13]_ or Example 8.3.4 in [Meye00]_).
  """
  ut.assert_square(M)
  ut.assert_nonnegative(M)
  n, _ = M.shape
  # We set all entries to 1 to avoid float underflow.
  # Float overflow is not a problem because np.inf > 0.
  # Using booleans is not an option due to unreliable behavior of boolean
  # matrix mutiplication depending on the version of NumPy.
  X = M.astype(bool).astype(float)
  with warnings.catch_warnings():
    warnings.simplefilter("ignore", category = RuntimeWarning)
    ans = np.all(np.linalg.matrix_power(X, n * n - 2 * n + 2) > 0)
  return ans 


def is_irreducible(M):
  r"""
  This implementation uses the fact that a non-negative square matrix **M**
  is irreducible if and only if :math:`(\mathbf{I} + \mathbf{M})^{n-1}` is
  positive (see e.g. Theorem 6.2.23 in [HoJo13]_ or Fact 2.(c) of Chapter 9.2
  in [Hogb06]_).
  """
  ut.assert_square(M)
  ut.assert_nonnegative(M)
  n, _ = M.shape
  if n == 1:
    return M[0, 0] != 0
  else:
    # See is_primitive for why we set entries to 1.
    X = (np.eye(n) + M).astype(bool).astype(float)
    with warnings.catch_warnings():
      warnings.simplefilter("ignore", category = RuntimeWarning)
      ans = np.all(np.linalg.matrix_power(X, n - 1) > 0)
    return ans 


def strongly_connected_components(M):
  r"""
  Returns the partition into strongly connected components of the
  directed graph encoded by the adjacency matrix **M**. The partition
  is represented as a list of lists of integers from 0 to *n* - 1,
  and the strongly connected components are returned in topological
  ordering (that is, if there exists an edge from a vertex of :math:`C_1` to
  a vertex of :math:`C_2`, then :math:`C_1` comes before :math:`C_2` in
  the list of components).

  The implementation uses Tarjan's algorithm [Tarj72]_ and runs
  in :math:`O(n^2)`, where *n* = dim(**M**).
  """
  ut.assert_square(M)
  ut.assert_nonnegative(M)
  n, _ = M.shape
  current_index = 0
  stack = []
  components = []
  index = [None] * n
  low_link = [None] * n
  on_stack = [False] * n
  def depth_first_search(v):
    nonlocal current_index
    index[v] = current_index
    low_link[v] = current_index
    current_index += 1
    stack.append(v)
    on_stack[v] = True
    for w in M[:, v].nonzero()[0]:  # for w successor of v
      if index[w] is None:
        depth_first_search(w)
        low_link[v] = min(low_link[v], low_link[w])
      elif on_stack[w]:
        low_link[v] = min(low_link[v], index[w])
    if low_link[v] == index[v]:
      c = []
      w = None
      while w != v:
        w = stack.pop()
        c.append(w)
        on_stack[w] = False
      components.append(c)
  for v in range(n):
    if index[v] is None:
      depth_first_search(v)
  for c in components:
    c.sort() # To keep the original order of the nodes
  components.reverse() # To get the topological sort in the correct order
  return components


def periods(M):
  r"""
  The period of *i* is the GCD of the lengths of all directed cycles (or,
  equivalently, of all closed walks) going through *i* in the graph associated
  to **M**.  If *i* is not contained in any cycle, then its period is ``None``.
  This naive implementation uses up to *n* = dim(**M**) matrix products to
  examine all paths of length at most *n*.
  """
  ut.assert_square(M)
  n, _ = M.shape
  M_bool = M.astype(bool)
  k = 0
  M_k = np.eye(n, dtype = bool)
  p = [0] * n # note: math.gcd(0, x) = x
  while k <= n and any(x != 1 for x in p):
    k += 1
    M_k = M_k @ M_bool
    for i in range(n):
      if M_k[i, i]:
        p[i] = math.gcd(p[i], k)
  return [x if x != 0 else None for x in p]


def index_of_imprimitivity(M):
  r"""
  The index of imprimitivity -- see [Gant59]_,
  [Meye00]_ -- is also referred to as the period (e.g, in [Sene06]_ and
  [Hogb06]_) or as the index of cyclicity ([HoJo13]_).

  For an irreducible matrix **M**, the index of imprimitivity *h*
  is the number of eigenvalues with maximal modulus (all of which are simple
  and correspond to the *h*-th roots of unity times the spectral radius). It is
  also equal to the greatest common divisor of the lengths of the directed
  cycles of the graph encoded by **M**.

  For a reducible matrix, it is defined as the least
  common multiple of the indices of imprimitivity of the dominant
  components (that is, the irreducible components whose spectral
  radii equal that of **M**). See [Hogb06]_, Section 9.3.

  This implementation computes the periods of each irreducible component
  by calling :func:`periods` and, if necessary, calls
  :func:`strongly_connected_components` to identify the dominant components.
  """
  p = periods(M)
  no_duplicates_or_None = list(dict.fromkeys([x for x in p if not x is None]))
  k = len(no_duplicates_or_None)
  if k == 1:
    return no_duplicates_or_None[0] 
  elif k == 0:
    if ut._ISSUE_WARNINGS:
      warnings.warn("Matrix has no cycles")
    return np.nan
  else:
    rho = spectral_radius(M)
    components = strongly_connected_components(M)
    submatrices = []
    classes = []
    for c in components:
      submat = M[c,:][:,c]
      if submat.shape != (1, 1) or submat[0, 0] != 0:
        submatrices.append(submat) 
        classes.append(c)
    periods_to_consider = []
    for k in range(len(submatrices)):
      # We allow for some numerical errors in the the eigenelements
      if math.isclose(spectral_radius(submatrices[k]), rho,
                      rel_tol = ut._REL_TOL, abs_tol = ut._ABS_TOL):
        periods_to_consider.append(p[classes[k][0]])
    return np.lcm.reduce(periods_to_consider)


def shannon_entropy(p, check = True):
  r"""
  Returns the Shannon entropy of the array *p*, that is,

  .. math::

    - \sum_i p_i \log_2 p_i,

  where the sum runs over all elements of *p* and with the convention that
  :math:`0 \log 0 = 0`.
  
  If the optional argument `check` is set to ``True``, as is the case by
  default, this will raise :exc:`ValueError` if *p* does not represent a
  probability distribution; otherwise, this will just compute the sum without
  worrying about its interpretation.
  """
  if check:
    if np.any(p < 0) or not math.isclose(np.sum(p), 1.,
                              rel_tol = ut._REL_TOL, abs_tol = ut._ABS_TOL):
      raise ValueError("Array does not represent a probability distribution")
  log_p = np.log2(p, out = np.zeros_like(p), where = (p != 0))
  return - np.sum(p * log_p)


_T_TABLE = [np.nan, 12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306,
   2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093,
   2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042]

def student_t(n) :
  r"""
  Quantile of order 0.975 for Student's distribution with *n* degrees of
  freedom. Thus, the 95% confidence interval for the mean of a sample of
  *n* normally distributed variables is
  
  .. math::
  
    \mathrm{CI}_{95} \;=\;
    \big[\hat{\mu} - \mathrm{t}_{n - 1} \hat{\sigma} / \sqrt{n},\;
     \hat{\mu} + \mathrm{t}_{n - 1} \hat{\sigma} / \sqrt{n}\big]

  where :math:`\mathrm{t}_{n - 1}` = ``student_t(n-1)`` and
  :math:`\hat{\mu}` (resp. :math:`\hat{\sigma}`) is the estimator of mean
  (resp. standard deviation) of the sample.

  Returned values are rounded-off to the third decimal, and the function
  returns 2 whenever *n* is greater than 30 (which gives conservative
  confidence intervals).
  """
  if n > 30:
    return 2. # (conservative)
  elif n <= 0:
    raise ValueError(
      "Student's t: degree of freedom must be a positive integer.")
  else:
    return _T_TABLE[n]

