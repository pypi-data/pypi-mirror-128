"""
This module implements the class :class:`MPM` used to represent matrix
population models. It provides a flexible way to create matrix population
models and a high-level interface to study their mathematical properties and
biological descriptors (growth rate, stable distribution, reproductive
values, etc).  The descriptors are computed when they are first needed, and
then stored as immutable attributes.

>>> m = MPM(A = "0.1 2; 0.4 0.8")
>>> m.primitive # is the projection matrix primitive?
True
>>> m.lmbd # asymptotic growth rate
1.4104686356149274
>>> m.w # stable distribution
array([0.60414407, 0.39585593])
>>> m.lmbd = 0 # trying to change a descriptor throws an error.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute

In order to be computed, many descriptors require knowing which entries of the
projection matrix correspond to survival probabilities and which correspond to
fertilities, i.e. its decomposition into the survival matrix **S** and the
fertility matrix **F**. Trying to access such descriptors without having
specified the matrices **S** and **F** when creating the model will raise
:class:`~matpopmod.utils.NotAvailable`:

>>> m1 = MPM(A = "0.1 2; 0.4 0.8")
>>> m1.lmbd
1.4104686356149274
>>> m1.R0
Traceback (most recent call last):
  ...
matpopmod.utils.NotAvailable: 'A = S + F decomposition required.'
>>> m2 = MPM(S = "0.1 0; 0.4 0.8", F = "0 2; 0 0")
>>> m2.lmbd
1.4104686356149274
>>> m2.R0
4.4444444444444455

"""

import math, cmath
import warnings
import pathlib
import itertools

import numpy as np
import matpopmod.utils as ut
import matpopmod.mathtools as mt
import matpopmod.trajectories as tj


_WARNING_MSG_QUASIPRIMITIVE = (
  "A is not quasi-primitive. Most descriptors "
  "are ill-defined. They will be set to NaN.")


class MPM:
  """
  A matrix population model is defined by its projection matrix **A**.
  Some descriptors (such the growth rate, the stable distribution or
  the reproductive values) can be computed directly from this projection
  matrix. However, other ones (such as the net reproductive rate or
  the generation time) can be computed only if the **A** = **S** + **F**
  decomposition of the projection matrix into its survival and fertility
  components is known. Thus, there are two ways to create a matrix
  population model:

  - Using the projection matrix **A** only::
  
      MPM(A = "0.1 2; 0.4 0.8")

    If the model is created that way, trying to access descriptor that
    require knowing **S** and **F** will raise
    :class:`~matpopmod.utils.NotAvailable`.

  - By specifying any two of the three matrices **A**, **S** and **F**, for
    instance::

      MPM(S = "0.1 0; 0.4 0.8", F = "0 2; 0 0")

    If the three matrices are given, **A** will be silently ignored (that is,
    only **S** and **F** will be used, without checking whether
    **A** = **S** + **F**).

    For convenience, instead of specifying two matrices it is also possible to
    provide **A** and the list of entries that correspond to reproduction.
    This is done with the `fertility` argument::
    
      MPM(A = "0.1 2; 0.4 0.8", fertilities = [(0, 1)])

    However this is less flexible, since this does not allow for overlapping
    entries between **S** and **F**. Note that the indexing of the entries
    starts at 0.

  In addition to this, there are several ways to specify any of the matrices
  in the arguments:

  - Using a string, as we saw in the examples above. Rows have to be
    separated by a semicolon and columns by a space and/or a comma.

  - Using Python iterables, such as a list of lists::
  
      MPM(A = [[0.1, 2], [0.4, 0.8]])
  
    Valid arguments are the same as for NumPy's :func:`array` function.
    In particular, NumPy arrays can be used.

  - Reading the matrix from a text file. In that case, the name
    of the file containing the matrix must be passed as a
    :class:`~pathlib.Path` from Python's :mod:`pathlib` module. ::

      file_A = pathlib.Path("~/myfolder/myfile.txt")
      MPM(A = file_A)

    Valid files contain one row of the matrix per line, with columns separated
    by whitespace (the character separating columns can be specified
    using the `delimiter` argument -- use ``","`` to load
    CSV files). Lines starting with ``#``, ``%`` or ``//`` are ignored.
  """


  def __init__(self, A = None, S = None, F = None,
               fertilities = None, delimiter = None, metadata = None):

    # Use to store information about the model. Mutable.
    if metadata is None:
      metadata = dict()
    self.metadata = metadata

    # Hidden attributes
    self._A = None
    self._dim = None
    self._split = True
    self._S = None
    self._F = None
    self._irreducible = None
    self._irreducible_components = None
    self._normal_form = None
    self._periods = None
    self._index_of_imprimitivity = None
    self._primitive = None
    self._quasi_irreducible = None
    self._quasi_primitive = None
    self._eigenvalues = None
    self._warning_w = False
    self._right_eigenvectors = None
    self._left_eigenvectors = None
    self._w = None
    self._v = None
    self._damping_ratio = None
    self._second_order_period = None
    self._sensitivities = None
    self._elasticities = None
    self._P = None
    self._Ps = None
    self._Pf = None
    self._G = None
    self._N = None
    self._NPs = None
    self._entropy_rate = None
    self._postrepro = None
    self._leslie = None
    self._usher = None
    self._nu = None
    self._class_of_birth = None
    self._T_a = None
    self._T_R0 = None
    self._T_G = None
    self._mu1 = None
    self._R0 = None
    self._cohort_R0 = None
    self._total_reproductive_output = None
    self._w_G = None
    self._v_G  = None
    self._fertility_excess = None
    self._survival_excess = None
    self._LAST_COMPUTED_MEAN_AGE_REPRO = None
    self._LAST_COMPUTED_LE_REPRO = None
    self._proba_repro = None
    self._life_expectancy_repro = None
    self._remaining_life_expectancy_repro = None
    self._lifetable_entropy = None
    self._mean_age_class = None
    self._mean_age_population = None
    self._proportion_newborns = None

    def get_matrix(arg, name=""):
      if isinstance(arg, pathlib.Path):
        a = np.loadtxt(arg.expanduser(), delimiter, comments = ("#", "%", "//"))
      elif isinstance(arg, str):
        a = np.array(ut.parse_array_string(arg))
      else:
        a = np.array(arg)
      ut.assert_square(a, name)
      ut.assert_nonnegative(a, name)
      return a

    if not S is None:
      self._S = get_matrix(S, "S")
      if not F is None:
        self._F = get_matrix(F, "F")
        ut.assert_same_dimensions(self._S, self._F, "S", "F")
        self._A = self._S + self._F
      elif not A is None:
        self._A = get_matrix(A, "A")
        ut.assert_same_dimensions(self._S, self._A, "S", "A")
        self._F = self._A - self._S
      else:
        raise ut.MissingArguments("Specifying S is not sufficient.")
    elif not F is None:
      if not A is None:
        self._F, self._A = get_matrix(F,"F"), get_matrix(A,"A")
        ut.assert_same_dimensions(self._F, self._A, "F", "A")
        self._S = self._A - self._F
      else:
        raise ut.MissingArguments("Specifying F is not sufficient.")
    elif not A is None:
      self._A = get_matrix(A, "A")
      if not fertilities is None:
        self._F = np.zeros(self._A.shape)
        for i, j in fertilities:
          self._F[i, j] = self._A[i, j]
          self._S = self._A - self._F
      else:
        self._split = False
    else:
      raise ut.MissingArguments("You have to specify some matrix.")

    if self._S is not None:
      ut.assert_substochastic(self._S, "S")

    self._dim = self._A.shape[0]

    self._A.flags.writeable = False
    if self._split:
      self._F.flags.writeable = False
      self._S.flags.writeable = False


  def __str__(self):
    with np.printoptions(linewidth = None, suppress = True):
      s = str(self.A)[1:-1].replace("\n ", "\n")
      return f"MPM with projection matrix: \n{s}"


  def __repr__(self):
    if self.split:
      rprS = repr(self.S).replace("array(", "  S = ")[0:-1]
      rprF = repr(self.F).replace("array(", "  F = ")[0:-1]
      mat = rprS + ",\n" + rprF
    else:
      mat = repr(self.A).replace("array(", "  A = ")[0:-1]
    if self.metadata:
      rprmeta = (
        "  metadata = {\n    " +
        ",\n    ".join(repr(key) + ": " + repr(val)
                       for (key, val) in self.metadata.items()) + "\n  }")
    else:
      rprmeta = "  metadata = {}"
    return "MPM(\n" + mat + ",\n" + rprmeta + "\n)"


  def _repr_latex_(self):
    out = r"$$ \text{" + ("MPM") + r":} \; \left ["

    def nparray_to_latex(mat):
      tex = r"\begin{pmatrix}"
      tex += repr(mat).replace("array(", "")[0:-1]
      tex = tex.replace("],", r"\\")
      tex = tex.replace(",", "&")
      tex = tex.replace("[", "")
      tex = tex.replace("]", "")
      tex += r"\end{pmatrix}"
      return tex

    if self.split:
      rprS = r"\mathbf{S} = " + nparray_to_latex(self.S)
      rprF = r"\mathbf{F} = " + nparray_to_latex(self.F)
      mat = rprS + r",\;" + rprF
    else:
      mat = r"\mathbf{A} = " + nparray_to_latex(self.A)
    out += mat + r"\right ] $$"
    return out


  def _repr_html_(self):
    out = self._repr_latex_()
    if self.metadata:
      out += '<div style="max-height:10em;overflow-y:scroll;margin:5px"><table>'
      for k, v in self.metadata.items():
        val = str(v).replace('\n','<br/>')
        out += "<tr><td><strong>{}</strong></td><td>{}<td></tr>".format(k, val)
      out += "</div></table>"
    return out


  @property
  def dim(self):
    """The number of classes of the model."""
    return self._dim


  @property
  def split(self):
    """
    Whether the **A** = **S** + **F** decomposition of the projection matrix
    into survival probabilities vs fertilities is available.  Note that many
    descriptors of matrix population models require this decomposition in order
    to be computed.
    """
    return self._split


  @property
  def A(self):
    r"""
    The projection matrix :math:`\mathbf{A} = (a_{ij})`, where :math:`a_{ij}`
    is the expected per-capita contribution of individuals of class *j* to the
    abundance of class *i* at the next time-step.
    """
    return self._A


  @property
  def S(self):
    r"""
    The survival matrix :math:`\mathbf{S} = (s_{ij})`, where :math:`s_{ij}` is
    the probability that an individual of class *j* survives and goes to
    class *i* at the next time-step. See also :attr:`F` and :attr:`split`.
    """
    if self._split:
      return self._S
    else:
      raise ut.NotAvailable("A = S + F decomposition required.")


  @property
  def F(self):
    r"""
    The fertility matrix :math:`\mathbf{F} = (f_{ij})`, where :math:`f_{ij}` is
    the expected number of offspring of class *i* of an individual in class *j*.
    See also :attr:`S` and :attr:`split`.
    """
    if self._split:
      return self._F
    else:
      raise ut.NotAvailable("A = S + F decomposition required.")


  @property
  def irreducible(self):
    r"""
    Whether the projection matrix **A** is irreducible, meaning for any two
    classes *i* and *j*, there exists a directed path from *i* to *j* in
    the life-cycle graph.  Equivalently, a non-negative matrix **A** is
    irreducible if and only if for all *i*, *j* there exists *k* such that the
    (*i*, *j*)-th entry of :math:`\mathbf{A}^k` is positive.

    See :func:`~matpopmod.mathtools.is_irreducible` from the module
    :mod:`~matpopmod.mathtools` for a function that can be used on any NumPy
    array and for details about the implementation.
    """
    if self._irreducible is None:
      self._irreducible = mt.is_irreducible(self._A)
    return self._irreducible


  @property
  def irreducible_components(self):
    r"""
    The decomposition of the projection matrix **A** into irreducible
    components, as a couple (`submatrices`, `classes`) where
    `submatrix[k]` is the submatrix of **A** that corresponds to the
    *k*-th irreducible component and `classes[k][i]` is the class of **A** that
    corresponds to the *i*-th class of that component.
    Example:

    >>> m = MPM(A = "1 0 0 0; 2 0 3 0; 0 4 0 0; 0 0 5 0")
    >>> m.A
    array([[1, 0, 0, 0],
           [2, 0, 3, 0],
           [0, 4, 0, 0],
           [0, 0, 5, 0]])
    >>> m.irreducible_components
    ([array([[1]]), array([[0, 3], [4, 0]])], [[0], [1, 2]])

    Note that classes are indexed from 0 to *n* - 1, where *n* = dim(**A**),
    and that classes that do not belong to any directed cycle (as is the case
    above with class ``3``) are not part of any irreducible component.

    See :func:`~matpopmod.mathtools.strongly_connected_components` from the
    module :mod:`~matpopmod.mathtools` for a function that can be used on any
    NumPy array and for details about the implementation. See also
    :func:`normal_form` for an alternative representation of the decomposition
    that retains the transitions between the classes.
    """
    if self._irreducible_components is None:
      components = mt.strongly_connected_components(self._A)
      submatrices = []
      classes = []
      for c in components:
        submat = self._A[c,:][:,c]
        if submat.shape != (1, 1) or submat[0, 0] != 0:
          submatrices.append(submat) 
          classes.append(c)
      self._irreducible_components = (submatrices, classes)
    return self._irreducible_components


  @property
  def normal_form(self):
    r"""
    A normal form of the projection matrix **A** is obtained by reordering its
    classes so as to get a projection matrix of the form

    .. math::

      \begin{pmatrix}
      \mathbf{A}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
      \mathbf{A}_{21} & \mathbf{A}_{22} & \ddots & \vdots \\
      \vdots & \vdots & \ddots & \mathbf{0} \\
      \mathbf{A}_{2m} & \mathbf{A}_{2m} & \cdots & \mathbf{A}_{mm}
      \end{pmatrix} , 

    where each of the diagonal blocks
    :math:`\mathbf{A}_{11}, \ldots, \mathbf{A}_{mm}`
    is either an irreducible matrix or a null matrix --
    see e.g. Chapter XIII, §4 of [Gant59]_.
    
    The new matrix is returned with a NumPy array `permutation`
    representing the reordering of the classes: `permutation[i]`
    is the index of the row/column of **A** that corresponds to the *i*-th
    row/column in the normal form. Indexing starts at 0. Example:

    >>> m = MPM(A = "1 0 2 0; 3 0 0 4; 5 0 0 0; 0 6 7 0")
    >>> m.A
    array([[1, 0, 2, 0],
           [3, 0, 0, 4],
           [5, 0, 0, 0],
           [0, 6, 7, 0]])
    >>> m.normal_form
    (array([[1, 2, 0, 0],
            [5, 0, 0, 0],
            [3, 0, 0, 4],
            [0, 7, 6, 0]]), array([0, 2, 1, 3]))
    
    Note that the normal form is not unique, as we can reorder the classes
    inside each irreducible component to get a different one (if
    some of the blocks under the diagonal are null, we may also be able to
    permutate the irreducible blocks). This implementation tries to preserve
    the original order of the classes. Also note that several authors (e.g,
    [Varg00]_ and [HoJo13]_) define the normal form to be block
    upper-triangular, rather than block lower-triangular. However, this is at
    odds with the usage in matrix population models, where projection matrices
    are typically lower-triangular (e.g, Leslie matrices).

    See :attr:`irreducible_components` for a function that extracts the
    submatrices corresponding to the irreducible components.
    """
    if self._normal_form is None:
      components = mt.strongly_connected_components(self._A)
      permut = np.fromiter(itertools.chain.from_iterable(components), dtype=int)
      matrix = self._A[:, permut][permut, :]
      self._normal_form = (matrix, permut)
      for entry in self._normal_form:
        entry.flags.writeable = False

    return self._normal_form


  @property
  def periods(self):
    """
    The vector of periods of the projection matrix **A**. The
    period of the class *i* is the greatest common divisor of the lengths
    of the cycles goings through the corresponding vertex in the life-cycle
    graph (if there is no such cycle, then it is ``None``).
    See also :attr:`index_of_imprimitivity` for the greatest common divisor of
    the periods the classes.

    See :func:`~matpopmod.mathtools.periods` from the
    :mod:`~matpopmod.mathtools` module for a function that can be used on any
    NumPy array and for details about the implementation.
    """
    if self._periods is None:
      self._periods = mt.periods(self._A)
    return self._periods


  @property
  def index_of_imprimitivity(self):
    r"""
    The index of imprimitivity of the projection matrix **A**, also known
    as its period.

    When **A** is irreducible, the coefficient of imprimitivity is both the
    greatest common divisor of the lengths of the cycles in the life-cycle
    graph and the number of eigenvalues whose modulus is equal to the
    asymptotic growth rate *λ*. It corresponds to the period of the asymptotic
    oscillations of the population structure.
    
    When **A** is reducible, the coefficient of imprimitivity is defined as
    the least common multiple of the periods of its dominant components
    (see the documentation of the function
    :func:`~matpopmod.mathtools.index_of_imprimitivity` from the module
    :mod:`~matpopmod.mathtools` for details). It corresponds to the longest
    possible period of the asymptotic oscillations: if we start from
    |any*| population vector with individuals in every classes, there
    will be asymptotic oscillations whose period is the coefficient of
    imprimitivity; but some initial population vectors can produce asymptotic
    oscillations with a period that is a divisor of the index of imprimitivity.
    
    When the index of imprimitivity is equal to 1, the population structure
    can never exhibit asymptotic oscillations and **A** is said to be
    :attr:`aperiodic`.
    """
    if self._index_of_imprimitivity is None:
      self._index_of_imprimitivity = mt.index_of_imprimitivity(self._A)
    return self._index_of_imprimitivity


  @property
  def aperiodic(self):
    r"""
    Whether the projection matrix **A** is aperiodic, i.e. whether the
    index of imprimitivity is equal to 1. Aperiodicity is a necessary
    condition for the convergence of the population structure: otherwise, it
    can exhibit asymptotic oscillations (see :attr:`index_of_imprimitivity` for
    details).
    """
    return self.index_of_imprimitivity == 1 # No need to cache ;)


  @property
  def primitive(self):
    r"""
    Whether the projection matrix **A** is primitive, meaning that there exists
    an integer *k* such that :math:`\mathbf{A}^k` is positive.
    Equivalently, a non-negative matrix is primitive if and only if it is
    irreducible and aperiodic.

    Primitivity is a central notion of the Perron-Frobenius theory. It ensures
    that, as :math:`t \to \infty`,

    .. math::

      \frac{\mathbf{A}^t}{\lambda^t} \to \mathbf{w v} , 
    
    with *λ* the dominant eigenvalue of **A**, **v** and **w** 
    the corresponding left and right eigenvectors (scaled so that
    **vw** = 1), and **wv** the matrix :math:`(w_i v_j)`. As a result,
    for |any*| initial population vector :math:`\mathbf{n}(0)`,
    :math:`\mathbf{n}(t) / \lambda^t \to c \mathbf{w}`, where
    :math:`c = \mathbf{vn}(0)`.
    Note that these conclusions also hold if **A** is :attr:`quasi_primitive`.

    See :func:`~matpopmod.mathtools.is_primitive` from the module
    :mod:`~matpopmod.mathtools` for a function that can be used on any NumPy
    array and for details about the implementation.
    """
    if self._primitive is None:
      self._primitive = mt.is_primitive(self._A)
    return self._primitive


  @property
  def quasi_irreducible(self):
    r"""
    Whether the projection matrix **A** is quasi-irreducible, i.e. whether
    it has only one irreducible component whose dominant eigenvalue is
    equal to *λ*.
    
    Unlike irreducibility, quasi-irreducibility is not a standard
    notion. However, it is useful to treat models with post-reproductive
    classes or metapopulation models with uni-directional migration: indeed,
    the vast majority of matrix population are quasi-irreducible, and many of
    the results for irreducible matrices are easily adapted to
    quasi-irreducible ones. See :attr:`quasi_primitive` for more information.
    """
    if self._quasi_irreducible is None:
      submatrices, _ = self.irreducible_components
      number_dominant_components = 0
      for B in submatrices:
        if math.isclose(mt.spectral_radius(B), self.lmbd,
                        rel_tol = ut._REL_TOL, abs_tol = ut._ABS_TOL):
          number_dominant_components += 1
      if number_dominant_components == 0:
        raise ValueError("No dominant component found. "
          "Either the projection matrix is unsuitable (e.g, nilpotent) "
          "or something went wrong with the calculation of the eigenvalues.")
      else:
        self._quasi_irreducible = (number_dominant_components == 1)
    return self._quasi_irreducible


  @property
  def quasi_primitive(self):
    r"""
    Whether the projection matrix **A** is quasi-primitive, i.e.
    quasi-irreducible and aperiodic. Equivalently, a non-negative matrix
    is quasi-primitive if and only if it has a single eigenvalue of maximum
    modulus and this eigenvalue has algebraic multiplicity 1.

    Quasi-primitivity is not a standard notion, but it is a useful relaxation
    of primitivity when working with matrix population models.
    Indeed, like primitivity it ensures that
    :math:`\mathbf{A}^t / \lambda^t \to \mathbf{w v}` 
    as :math:`t \to \infty`. The only difference with the primitive case is
    that the dominant eigenvectors **v** and **w** are allowed to have entries
    that are equal to zero (corresponding to "sink" classes for **v** and to
    "source" ones for **w**).

    Further generalizations are possible -- see e.g. [Roth81]_ -- but they
    are more technical and typically not useful for matrix population models,
    where the structure of matrices is subject to biological constraints.
    See Section 9.3 of [Hogb06]_ for an overview of Perron-Frobenius
    theory for reducible matrices.
    """
    if self._quasi_primitive is None:
      if self.dim == 1:
        self._quasi_primitive = (self.A[0, 0] != 0)
      else:
        # Recall that the eigenvalues are sorted by decreasing modulus
        self._quasi_primitive = (
        not math.isclose(abs(self.eigenvalues[0]), abs(self.eigenvalues[1]),
                         rel_tol = ut._REL_TOL, abs_tol = ut._ABS_TOL))
    return self._quasi_primitive


  def __compute_all_eigen_elements(self):
    r"""
    Internal function that computes and stores all eigen-elements at once.
    Should not be exposed to the end-user and not documented. Calling this
    function will set the following attributes:

    - self._eigenvalues
    - self._right_eigenvectors
    - self._left_eigenvectors

    """
    vals, rvects, lvects = mt.eigen_elements(self._A, left = True)
    for v in rvects:
      v.flags.writeable = False
    for w in lvects:
      w.flags.writeable = False
    if not np.isreal(vals[0]):
      # This can only happen due to numerical errors.
      # There is not much we can do about it.
      raise ut.UnexpectedMathError(
        "Problem in the calculation of the eigen-elements: "
        "the dominant eigenvalue is not real. This indicates numerical "
        "errors in the calculations of the eigen-elements. You can either "
        "inspect the eigen-elements manually using mathtools.eigen_elements, "
        "or try modifying the entries of the projection matrix in "
        "a way that does not affect the biological relevance of the results "
        "(e.g, by adding 1e-15 to some non-zero entries).")
    self._eigenvalues = vals
    self._right_eigenvectors = rvects
    self._left_eigenvectors = lvects


  @property
  def eigenvalues(self):
    """
    The eigenvalues of the projection matrix **A**, in decreasing order of
    their modulus and repeated according to their algebraic multiplicities.
    
    See :attr:`right_eigenvectors` and :attr:`left_eigenvectors` for the
    corresponding eigenvectors, and :func:`~matpopmod.mathtools.eigen_elements`
    from the module :mod:`~matpopmod.mathtools` for details about the
    implementation.
    """
    if self._eigenvalues is None:
      self.__compute_all_eigen_elements()
    return self._eigenvalues


  @property
  def right_eigenvectors(self):
    r"""
    Right eigenvectors of the projection matrix **A**, that is,
    each :math:`\mathbf{w}^{(k)}` = `right_eigenvectors[k]` is a solution of

    .. math::

      \mathbf{A}\mathbf{w}^{(k)} = \lambda^{(k)}\,\mathbf{w}^{(k)},

    where :math:`\lambda^{(k)}` = `eigenvalues[k]`. Note that there are always
    some small errors (typically of the order of the machine epsilon, although
    there are no strict guarantees on that) in the obtention of those solutions:

    >>> m = MPM(A = "0.1 2; 0.4 0.8")
    >>> lmbd0, w0 = m.eigenvalues[0], m.right_eigenvectors[0]
    >>> m.A @ w0
    array([0.85212626, 0.55834237])
    >>> lmbd0 * w0
    array([0.85212626, 0.55834237])
    >>> m.A @ w0 - lmbd0 * w0
    array([-1.11022302e-16,  0.00000000e+00])

    Each vector is scaled so that
    
    .. math::

      \|\mathbf{w}^{(k)}\|_1 \;:=\; \sum_i |w_i^{(k)}| \;=\; 1, 

    and is chosen to be non-negative when possible.

    Importantly, note that unless **A** is diagonalizable, some of its
    eigenvectors *will* be linearly dependent (that includes the possibility
    of repeated or null eigenvectors). Thus, although :attr:`right_eigenvectors`
    will always return exactly :attr:`dim` eigenvectors (because the
    eigenvalues are repeated according to their algebraic multiplicities in
    :attr:`eigenvalues`), this should not be interpreted as meaning that **A**
    "has :attr:`dim` eigenvectors" (an abusive formulation that implicitly
    refers to linearly independent eigenvectors). If needed, functions to
    compute the geometric multiplicities and to test linear independence are
    provided in the module :mod:`mathtools`.
    """
    if self._right_eigenvectors is None:
      self.__compute_all_eigen_elements()
    return self._right_eigenvectors


  @property
  def left_eigenvectors(self):
    r"""
    Left eigenvectors of the projection matrix **A**, that is,
    each :math:`\mathbf{v}^{(k)}` = `left_eigenvectors[k]` is a solution of

    .. math::

      \mathbf{v}^{(k)} \mathbf{A} = \lambda^{(k)}\,\mathbf{v}^{(k)},

    where :math:`\lambda^{(k)}` = `eigenvalues[k]`.
    
    Note that some authors define left eigenvectors as column
    vectors, and will sometimes introduce them as *"the right eigenvectors of
    the conjugate transpose matrix* :math:`\mathbf{A}^*`\ *”*. In the context
    of matrices with real entries, all definitions are equivalent up to
    transposition, since :math:`\mathbf{A}^* = \mathbf{A}^\top` and
    :math:`(\mathbf{A}^\top \mathbf{x})^\top = \mathbf{x A}`.

    Although in our mathematical expressions we consider left eigenvectors
    as row vectors, NumPy does not make a distinction between
    row vectors and column vectors and all vectors in this library
    are represented using NumPy 1-D arrays.
    
    The left eigenvectors returned here are all scaled so that

    .. math::

      \|\mathbf{v}^{(k)}\|_1 \;:=\; \sum_i |v_i^{(k)}| \;=\; 1, 

    however note that a different scaling is used for the vector of
    reproductive values :attr:`v`.

    Finally, the comments on the accuracy of the determination of the
    eigenvectors made in the documentation of :attr:`right_eigenvectors`
    also apply here.
    """
    if self._left_eigenvectors is None:
      self.__compute_all_eigen_elements()
    return self._left_eigenvectors


  @property
  def lmbd(self):
    r"""
    The asymptotic growth rate *λ*. For large times *t*, the
    population size will grow (or decrease, if :math:`\lambda < 1`) like
    :math:`\lambda^t` times a constant that depends on the initial composition
    of the population.

    Mathematically, *λ* is the spectral radius of the projection matrix **A**,
    i.e. the maximum of the modulus of its eigenvalues. Note that
    the spectral radius of a non-negative matrix is always an eigenvalue
    of that matrix (see e.g. Section 8.3 of [Meye00]_). However, there can
    be several eigenvalues of maximum modulus; in fact, 
    *λ* is the only eigenvalue of maximum modulus if and only if **A** is
    aperiodic -- see Fact 3.(a) in Section 9.3 of [Hogb06]_.  When *λ* is the
    only eigenvalue of maximum modulus, we refer to it as the *dominant
    eigenvalue*.
    """
    return self.eigenvalues[0]


  @property
  def w(self):
    r"""
    The stable class distribution vector **w**. If the projection matrix **A**
    is primitive, then for |any*| initial population structure
    :math:`\mathbf{n}(0)` the population vector **n** will satisfy 

    .. math::

      \frac{\mathbf{n}(t)\;}{\|\mathbf{n}(t)\|_1} \to \mathbf{w} 
      \quad\text{as}\quad t \to \infty , 
    
    where :math:`\|\mathbf{n}(t)\|_1 = \sum_i |n_i(t)|` denotes the total
    population size. This convergence will also hold if **A**
    is quasi-primitive and we start with at least one individual in the
    dominant component (or one of its sources); see the documentation of
    :attr:`quasi_primitive` for details.

    Mathematically, **w** is the right eigenvector associated to the asymptotic
    growth rate *λ*.  If **A** is not quasi-primitive, then **w** is not
    well-defined (the asymptotic population structure may either depend on the
    initial one, due to reducibility; or not converge, due to periodicity).
    In that case, a vector of ``nan`` will be returned.
    """
    if self._w is None:
      if self.quasi_primitive:
        if np.any(self.right_eigenvectors[0] < 0):
          # This should never happen because if A is quasi_primitive
          # then w is well-defined and non-negative.
          raise ut.UnexpectedMathError(
            "Could not compute the Perron-Frobenius right eigenvector")
        else:
          self._w = self.right_eigenvectors[0]
      else:
        self._w = ut.vector_of_nan(self.dim)
      self._w.flags.writeable = False
    if ut._ISSUE_WARNINGS and np.isnan(self._w).any():
      warnings.warn(_WARNING_MSG_QUASIPRIMITIVE)
    return self._w


  @property
  def v(self):
    r"""
    The reproductive values vector **v**, scaled so that
    :math:`\mathbf{vw} = \sum_i v_i w_i = 1`. The term "reproductive value"
    is justified by the fact that, for quasi-primitive projection matrices,
    as :math:`t \to \infty` the population size is
    asymptotically equivalent to :math:`c\lambda^t`, where

    .. math::

      c \;=\; \mathbf{v} \mathbf{n}(0) \;=\;
      \sum_i v_i n_i(0)\,.

    Thus, :math:`v_i` is the relative contribution of an individual of
    class *i* to the composition of the population in the distant future.
    
    Mathematically, **v** is the left eigenvector associated to the asymptotic
    growth rate *λ*. If **A** is not quasi-primitive, then **v** is not
    well-defined. In that case, a vector of ``nan`` will be returned.

    Note that even though NumPy does not make a distinction between
    row vectors and column vectors (both correspond to 1-D arrays),
    in our mathematical expressions we consider **v** to be a row vector,
    This explains why we write **vw** for the scalar :math:`\sum_i v_i w_i` and
    **wv** for the matrix :math:`(v_i w_j)`.
    """
    if self._v is None:
      if self.quasi_primitive:
        v_unscaled = self.left_eigenvectors[0]
        if np.any(v_unscaled < 0):
          # This should never happen because if A is quasi_primitive
          # then v is well-defined and non-negative.
          raise ut.UnexpectedMathError(
            "Could not compute the Perron-Frobenius left eigenvector")
        else:
          # The following line will issue a warning if A is not quasi-primitive
          self._v = v_unscaled / (v_unscaled @ self.w)
      else:
        self._v = ut.vector_of_nan(self.dim)
        if ut._ISSUE_WARNINGS:
          warnings.warn(_WARNING_MSG_QUASIPRIMITIVE)
      self._v.flags.writeable = False
    else:
      if ut._ISSUE_WARNINGS and np.isnan(self._v).any():
        warnings.warn(_WARNING_MSG_QUASIPRIMITIVE)
    return self._v


  @property
  def damping_ratio(self):
    r"""
    The damping ratio of the projection matrix **A**, defined as
    the growth rate *λ* divided by the maximum of the modulus of the
    subdominant eigenvalues, that is,

    .. math::

       \frac{\lambda}{\tau} \quad\text{where}\quad
       \tau = \max\big\{|\mu| :
       \mu \text{ is an eigenvalue with } |\mu| < \lambda\big\},
      
    where :math:`\max \varnothing = 0` -- i.e. when there is no eigenvalue
    :math:`\mu` such that :math:`0 < |\mu| < \lambda`, the damping ratio is
    infinite and ``inf`` is returned.

    The damping ratio corresponds to the rate of convergence to the
    steady regime. Indeed, for primitive projection
    matrices, for any :math:`r > \tau`,

    .. math::

       \mathbf{A}^t \;=\; \lambda^t \mathbf{wv} \;+\; O(r^t)

    see e.g. Theorem 1.2 in [Sene06]_ for a slightly more precise statement.

    Note that the name "damping ratio" is now well-established in the
    literature on matrix population models (see e.g. [Casw00]_), but
    that it is slightly unfortunate since :math:`\lambda / \tau` does *not*
    correspond to the notion of damping ratio in classical physics,
    which also depends on the period of the second-order oscillations (see
    :attr:`second_order_period`). The damping ratio from matrix population
    models is actually a *geometric rate of convergence*; in all likeliness
    the confusion comes from the interpretation of the word *ratio* (which,
    in physics, refers to the ratio of the actual damping to the critical one).
    """
    if self._damping_ratio is None:
      is_subdominant = np.logical_not(np.isclose(np.abs(self.eigenvalues),
        self.lmbd, rtol = ut._REL_TOL, atol = ut._ABS_TOL))
      i = np.argmax(is_subdominant) # index of first subdominant eigenvalue 
      if i == 0:
        self._damping_ratio = float("inf")
      else:
        tau = abs(self.eigenvalues[i])
        if tau == 0:
          self._damping_ratio = float("inf")
        else:
          self._damping_ratio = self.lmbd / tau 
    return self._damping_ratio


  @property
  def second_order_period(self):
    r"""
    The period of the second-order oscillations,
    
    .. math::

       \mathcal{P} \;=\; \left|\frac{2 \pi}{\arg \lambda_2}\right|, 

    where :math:`\lambda_2` and its complex conjugate :math:`\lambda_2^*`
    are the only eigenvalues with largest modulus strictly less than *λ* (note
    that these two eigenvalues give the same :math:`\mathcal{P}` so it
    does not matter which one we choose in the definition). 
    When :math:`\lambda_2 = \lambda_2^* \geq 0`, then there are no
    oscillations associated to the eigenvalue of second-largest modulus and
    ``nan`` is returned. Note that there could still be oscillations
    associated to eigenvalues of smaller modulus. 

    In the unlikely case where there are more than two eigenvalues of
    second-largest modulus, then the corresponding oscillations are
    periodic if and only if the corresponding periods
    :math:`\mathcal{P}_1, \ldots, \mathcal{P}_q` are commensurable, i.e.
    if there exists positive integers :math:`k_1, \ldots, k_q` such that
    :math:`k_1 \mathcal{P}_1 =  \cdots = k_q \mathcal{P}_q`. The
    period is then the smallest possible such common value
    of :math:`k_i \mathcal{P}_i`. Of course,
    it does not make sense to ask if real numbers are commensurable when they
    are represented by floating point numbers. Thus, in that case we
    test if there are small integers such that the relation above holds up to
    numerical precision; otherwise a :exc:`~matpopmod.utils.CannotCompute`
    error is raised.

    The values that we compute may differ from those calculated by other
    software. Whenever we identified discrepancies, they were
    due to the fact that other software chose their arguments
    in :math:`[0, 2\pi]` or failed to take into account the possibility of more
    than two eigenvalues of second largest modulus, which are errors of
    implementation.
    """
    if self._second_order_period is None:
      is_subdominant = np.logical_not(np.isclose(np.abs(self.eigenvalues),
        self.lmbd, rtol = ut._REL_TOL, atol = ut._ABS_TOL))
      i = np.argmax(is_subdominant) # index of first subdominant eigenvalue
      if i == 0:
        if ut._ISSUE_WARNINGS:
          warnings.warn(
            "No second-order oscillations (all eigenvalues are of same modulus).")
        self._second_order_period = np.nan
      else:
        tau = abs(self.eigenvalues[i])
        def are_close(x, y):
          return math.isclose(x, y, rel_tol=ut._REL_TOL, abs_tol=ut._ABS_TOL)
        # List all periods associated to eigenvalues of second largest modulus
        aux = [mu for mu in self.eigenvalues
          if are_close(abs(mu), tau) and not are_close(cmath.phase(mu), 0)]
        snd_order_p = [abs(2*math.pi / cmath.phase(mu)) for mu in aux]
        if len(snd_order_p) == 0:
          if ut._ISSUE_WARNINGS:
            warnings.warn("No second-order oscillations "
            "(all eigenvalues of second largest modulus, if any, are positive)")
          self._second_order_period = np.nan
        elif len(snd_order_p) == 1:
          if are_close(snd_order_p[0], 2.):
            self._second_order_period = 2.
          else:
            raise ut.UnexpectedMathError(
                    "Error in the numerical calculation of eigenvalues: "
                    "complex eigenvalues are supposed to come in pairs "
                    "of complex conjugates.")
        elif len(snd_order_p) == 2:
          if are_close(snd_order_p[0], snd_order_p[1]):
            self._second_order_period = snd_order_p[0]
          else:
            raise ut.UnexpectedMathError(
                    "Error in the numerical calculation of eigenvalues: "
                    "complex eigenvalues are supposed to come in pairs "
                    "of complex conjugates.")
        else:
          no_dup = list(dict.fromkeys(snd_order_p))
          n = len(no_dup)
          # In what follows we consider each tuple (k_0, ..., k_{n-1}) of
          # positive integers <= k_max to see if the values k_i * no_dup[i]
          # are equal for all i. If such common values exist, we take the
          # smallest one. The implementation is not optimized at all.
          MAX_TUPLES_TESTED = 1e6 # In case there are a lot of eigenvalues.
          MAX_K = 120 # Long periods are not reliable or biologically relevant.
          k_max = max(1, min(int(MAX_TUPLES_TESTED ** (1. / n)), MAX_K))
          multiples_of_the_period = []
          for k in itertools.product(range(1, k_max + 1), repeat = n):
            q = [p_i * k_i for (p_i, k_i) in zip(no_dup, k)]
            mean = sum(q) / len(q)
            if all(are_close(pk, mean) for pk in q):
              multiples_of_the_period.append(mean)
          if multiples_of_the_period == []:
            raise ut.CannotCompute("Could not determine whether there exist "
                    "oscillations associated to the eigenvalues of second "
                    "largest modulus, due to numerical precision.")
          else:
            self._second_order_period = min(multiples_of_the_period)
    return self._second_order_period


  @property
  def sensitivities(self):
    r"""
    The matrix of sensitivities of the growth rate *λ* to the entries of
    the projection matrix **A**, that is,

    .. math::

      s_\lambda(a_{ij}) \;=\;
      \frac{\partial \lambda}{\partial a_{ij}} \,.

    If **A** is primitive, then

    .. math::
    
      s_\lambda(a_{ij}) \;=\; v_i w_j, 
    
    where the vector of reproductive values **v** and the
    stable class distribution **w** are such that **vw** = 1.
    In fact, this formula is valid whenever **A** is quasi-irreducible;
    however for this **v** and **w** have to be defined as the
    only non-negative eigenvectors associated to *λ*, which
    cannot necessarily be interpreted as the reproductive values and stable
    distribution.

    If **A** is not quasi-irreducible, then *λ* is not a differentiable
    function of its entries. In that case, a warning is issued and a
    matrix of ``nan`` is returned.
    
    The standard reference for the formula
    :math:`s_\lambda(a_{ij}) = v_i w_j` is
    [Casw78]_, which was the first time it appeared in  the biological
    literature.  However, this paper does not contain a mathematical proof.
    The first proof seems to have been published in the
    earlier paper [Vahr76]_. As of June 2021, this paper was cited only
    6 times.

    See Chapter 3 of [KiNe19]_ for a more general yet very accessible
    treatment.
    """
    if self._sensitivities is None:
      if self.quasi_irreducible:
        if self.quasi_primitive:
          col_v = self.v.view().reshape((self._dim, 1))
          row_w = self.w.view().reshape((1, self._dim))
        else:
          # Get the Perron vectors
          rpv = self.right_eigenvectors[0]
          lpv = self.left_eigenvectors[0]
          lpv = lpv / (lpv @ rpv)
          col_v = lpv.view().reshape((self._dim, 1))
          row_w = rpv.view().reshape((1, self._dim))
        self._sensitivities = col_v @ row_w 
      else:
        if ut._ISSUE_WARNINGS:
          warnings.warn("A is not quasi-irreducible, lambda is not "
                        "a differentiable function of its entries.")
        self._sensitivities = ut.matrix_of_nan(self._dim)
      self._sensitivities.flags.writeable = False
    return self._sensitivities


  @property
  def elasticities(self):
    r"""
    The matrix of elasticities of the growth rate *λ* to the entries of
    the projection matrix **A**, that is,

    .. math::

      e_\lambda(a_{ij}) \;=\;
      \frac{a_{ij}}{\lambda} \frac{\partial \lambda}{\partial a_{ij}} \;=\;
      \frac{\partial \log \lambda}{\partial \log a_{ij}} \,.
    
    Contrary to the sensitivities, which measure the absolute change
    in *λ* in response to an additive perturbation of the entries of **A**,
    the elasticities measure the relative change in *λ* in response to
    a multiplicative perturbation of the entries of **A**.

    The elasticities also have a simple interpretation as the
    asymptotic frequencies of the transitions of the life cycle that we
    encounter as we follow the lineage of a focal individual back in time;
    see [BALM17]_ for more on this.

    If **A** is primitive, then

    .. math::
    
      e_\lambda(a_{ij}) \;=\; v_i\,  a_{ij}\, w_j \,/\, \lambda,
    
    where the vector of reproductive values **v** and the
    stable class distribution **w** are such that **vw** = 1.
    See the documentation of :attr:`sensitivities` for details about the
    validity of this formula and for references.
    """
    if self._elasticities is None:
      self._elasticities = self.sensitivities * self._A / self.lmbd
      self._elasticities.flags.writeable = False
    return self._elasticities


  @property
  def P(self):
    r"""
    The transition of matrix of the genealogical Markov chain,
    :math:`\mathbf{P} = (p_{ij})` where

    .. math::
    
      p_{ij} = \frac{a_{ij} w_j}{\lambda w_i},

    with *λ* the asymptotic growth rate and **w** the stable distribution.

    The genealogical Markov chain describes the sequence of classes that we
    encounter as we go "up" the genealogy of the population by following the
    lineage of a focal individual backwards in time: 
    :math:`p_{ij}` is the probability that an individual in class *i*
    at time *t* was in class *j* at time *t-1* (or had its mother
    in class *j*, if the individual was not born yet at time *t-1*).

    The genealogical Markov chain was first introduced in [Deme74]_ to define
    population entropy, but has recently found its use in a variety of
    problems. See [BALM17]_ for a complete introduction.

    See also :attr:`Ps` and :attr:`Pf` for the survival and fertility
    components of **P**, and :attr:`pi` for its stationary distribution.
    """
    if self._P is None:
      self._P = (self._A.T / (self.lmbd * self.w)).T * self.w
      self._P.flags.writeable = False
    return self._P


  @property
  def Ps(self):
    r"""
    Survival component of the genealogical matrix :attr:`P`:
    :math:`p_s(i, j)` is the probability that an individual in class *i*
    at time *t* was alive in class *j* at time *t-1*.
    """
    if self._Ps is None:
      self._Ps = (self.S.T / (self.lmbd * self.w)).T * self.w
      self._Ps.flags.writeable = False
    return self._Ps


  @property
  def Pf(self):
    r"""
    Fertility component of the genealogical matrix :attr:`P`:
    :math:`p_f(i, j)` is the probability that an individual in class *i*
    has just been born to a mother from class *j*.
    """
    if self._Pf is None:
      self._Pf = (self.F.T / (self.lmbd * self.w)).T * self.w
      self._Pf.flags.writeable = False
    return self._Pf


  @property
  def pi(self):
    r"""
    The vector of class reproductive values :math:`\pi_i = v_i w_i`.
    This is also the stationary distribution of the Markov chains corresponding
    to :attr:`P`, see [BALM17]_.
    """
    # No need to store; but make read-only for consistency.
    pi = self.v * self.w
    pi.flags.writeable = False
    return pi


  @property
  def entropy_rate(self):
    r"""
    The entropy rate of the genealogical Markov chain :attr:`P`, that is

    .. math::
    
      H \;=\;
      -\sum_{i, j} \pi_{i} p_{ij} \log_2 p_{ij} .

    This measures the information density of the trajectories of the
    genealogical chain, and can therefore be seen as a measure of the complexity
    of the life cycle (although, when comparing life cycles with different
    number of classes, remember that *H* takes values in :math:`[0, \log_2 n]`,
    where *n* is the number of classes).
    Mathematically, if we let :math:`X_1, X_2, \ldots` be a trajectory of
    the genealogical chain and :math:`H(X_1, \ldots, X_t)` denote the
    joint entropy of :math:`X_1, \ldots,  X_t`, then

    .. math::

      H \;=\; \lim_{t \to \infty} \frac{1}{t} H(X_1, \ldots, X_t)

    The first use of the entropy rate of **P** in matrix population models
    is due to Demetrius in [Deme74]_, where it is refered to as
    the *population entropy*. The same terminology is used in [Tulj82]_,
    but Demetrius later changed it\ |entropy*|\ ; nowadays, :math:`H` is often
    referred to as the *evolutionary entropy*, the term population entropy
    being reserved to the quantity :math:`S = HT_a`, where :math:`T_a` is the
    generation time.
    """
    if self._entropy_rate is None:
      P = self.P
      logP = np.log2(P, out = np.zeros_like(P), where = (P != 0))
      self._entropy_rate = - np.sum(self.pi @ (P * logP))
    return self._entropy_rate


  @property
  def mixed_transitions(self):
    r"""
    Whether the model has "mixed transitions", i.e. transitions in the
    life-cycle that can correspond to both survival and reproduction.
    In other words, whether there are overlapping entries between the
    matrices **S** and **F**.
    """
    return np.any(self.S * self.F > 0)


  @property
  def fundamental_matrix(self):
    r"""
    The fundamental matrix associated to **S**, that is,
    
    .. math::
    
      \mathbf{N} = (\mathbf{I} - \mathbf{S})^{-1} \,.

    The (*i*, *j*)-th entry of **N** is the expected number of times that an
    individual from class *j* will visit the class *i* during its remaining
    lifetime.

    See e.g. Chapter III of [KeSn76]_ for more on the mathematical properties
    of **N**.
    """
    if self._N is None:
      try:
        N = np.linalg.inv(np.eye(self.dim) - self.S)
        N[np.abs(N) < ut._ABS_TOL] = 0
        if np.any(N < 0):
          raise ut.UnexpectedMathError(
            "The fundamental matrix contains negative entries. "
            "This is caused by numerical errors in the calculation "
            "of (I - S)^(-1). You can try modifying the entries of S "
            "in a way that does not affect the biological relevance "
            "of the results (e.g, by adding 1e-15 to some non-zero entries).")
        else:
          self._N = N
          self._N.flags.writeable = False
      except np.linalg.LinAlgError:
        raise ut.NonConvergentMatrix(
          "Cannot compute the fundamental matrix, most likely because "
          "the survival matrix S is not convergent (i.e. makes it possible "
          "to have immortal individuals).")
    return self._N


  @property
  def G(self):
    r"""
    The next generation matrix
    
    .. math::
    
      \mathbf{G} = \mathbf{F} (\mathbf{I} - \mathbf{S})^{-1} \,,
    
    whose (*i*, *j*)-th entry is the expected number of offspring of class *i*
    that an individual of class *j* will produce in its remaining lifetime.
    See :attr:`R0` for the dominant eigenvalue of this matrix, a 
    commonly used measure of the net reproductive rate. 
    """
    if self._G is None:
      self._G = self.F @ self.fundamental_matrix
      self._G.flags.writeable = False
    return self._G


  @property
  def fundamental_matrix_Ps(self):
    r"""
    The fundamental matrix associated to :math:`\mathbf{P}_s`, that is
    
    .. math::
    
      (\mathbf{I} - \mathbf{P}_s)^{-1} \,.

    The (*i*, *j*)-th entry of this matrix is the
    expected number of times that an individual from class *i* has been in
    class *j* in the past.
    """
    if self._NPs is None:
      try:
        NPs = np.linalg.inv(np.eye(self.dim) - self.Ps)
        NPs[np.abs(NPs) < ut._ABS_TOL] = 0
        if np.any(NPs < 0):
          raise ut.UnexpectedMathError(
            "The fundamental matrix of Ps contains negative entries. "
            "This is caused by numerical errors in the calculation "
            "of (I - Ps)^(-1). You can try modifying the entries of A "
            "in a way that does not affect the biological relevance "
            "of the results (e.g, by adding 1e-15 to some non-zero entries).")
        else:
          self._NPs = NPs
          self._NPs.flags.writeable = False
      except np.linalg.LinAlgError:
        raise ut.NonConvergentMatrix(
          "Cannot compute the fundamental matrix of Ps, most likely because "
          "the fertility matrix F is null or the survival matrix S "
          "is not convergent. ")
    return self._NPs


  @property
  def newborn_classes(self):
    r"""
    .. rst-class:: nospaceafter

    The vector whose *i*-th entry is equal to:

    - :math:`0` if no individual in class *i* is a newborn, i.e. if
      :math:`f_{ij} = 0`
      for all *j*.
    - :math:`1` if every individual in class *i* is a newborn, i.e. if 
      :math:`s_{ij} = 0` for all *j* (and there exists *j*
      such that :math:`f_{ij} > 0`).
    - ``nan`` otherwise. In that case, class *i* may or may not be considered
      newborn class, since some but not all of its individuals are newborns.

    If you want to use a different convention, you can use NumPy's
    :func:`nan_to_num` function:

    >>> m = MPM(S = "0.1 0; 0.4 0.8", F = "0 2; 0 0")
    >>> m.newborn_classes
    array([nan,  0.])
    >>> numpy.nan_to_num(m.newborn_classes, nan = 0)
    array([0., 0.])
    >>> numpy.nan_to_num(m.newborn_classes, nan = 1)
    array([1., 0.])

    (this requires NumPy ≥1.17)

    See also :attr:`proportion_newborns` for the proportion of newborns in
    each stage, and :attr:`nu` and :attr:`class_of_birth` for related
    quantities.
    """
    sF = (np.sum(self.F, axis = 1) > 0)
    sS = (np.sum(self.S, axis = 1) > 0)
    nc = sF.astype(float)
    for i in range(len(sS)):
      if sF[i] and sS[i]: 
        nc[i] = np.nan
    # No need to store; but make read-only for consistency.
    nc.flags.writeable = False
    return nc


  @property
  def unique_newborn_class(self):
    r"""
    Whether the model has a single, well-defined newborn class, i.e.
    whether the two following conditions are met: (1) all individuals
    are born in the same class and (2) all individuals in that class are
    newborns.
    """
    return np.sum(self.newborn_classes) == 1.


  @property
  def reproductive_classes(self):
    r"""
    The vector whose *i*-th entry is equal to :math:`1` if *i* is a
    reproductive class and :math:`0` otherwise.
    """
    # No need to store; but make read-only for consistency.
    repro = (np.sum(self.F, axis = 0) > 0).astype(float)
    repro.flags.writeable = False
    return repro


  @property
  def postreproductive_classes(self):
    r"""
    The vector whose *i*-th entry is equal to :math:`1` if *i* is a
    post-reproductive class and :math:`0` otherwise.

    Note that if *i* is post-reproductive then its reproductive
    value :math:`v_i` is equal to zero, but that the converse is not true:
    in a meta-population model, the classes of a sink patch can have
    :math:`v_i = 0` without being post-reproductive.
    """
    if self._postrepro is None:
      # Y_ij = 1 iff i is accessible from j through survival
      X = (np.eye(self.dim) + self.S).astype(bool).astype(float)
      Y = (np.linalg.matrix_power(X, self.dim - 1) > 0)
      self._postrepro = (self.reproductive_classes @ Y == 0).astype(float)
      self._postrepro.flags.writeable = False
    return self._postrepro


  @property
  def proportion_newborns(self):
    r"""
    The vector whose *i*-th entry is the proportion of the individuals of
    class *i* that have just been born, assuming the population is at its
    stable class distribution. That is,

    .. math::

      \sum_{j} \frac{f_{ij} w_j}{\lambda w_i} \, .

    If the proportion of newborns in the class is not defined (e.g, because
    it depends on the composition of the population and there is no
    stable class distribution), the corresponding entry is set to ``nan``.
    """
    if self._proportion_newborns is None:
      with warnings.catch_warnings():
        # to suppress RuntimeWarning raised by division by 0:
        warnings.simplefilter("ignore")
        self._proportion_newborns = (self.F @ self.w) / (self.lmbd * self.w)
      if np.isnan(self._proportion_newborns).any():
        sF = (np.sum(self.F, axis = 1) > 0)
        sS = (np.sum(self.S, axis = 1) > 0)
        for i in range(self.dim):
          if sF[i]:
            if not sS[i]:
              self._proportion_newborns[i] = 1.0
          else:
            self._proportion_newborns[i] = 0.0
      self._proportion_newborns.flags.writeable = False
    return self._proportion_newborns


  @property
  def nu(self):
    r"""
    The vector :math:`\boldsymbol\nu = (\nu_i)` giving the fraction of offspring
    produced in a given year that are born in class *i*, assuming
    the population is at its stable class distribution. That is,

    .. math::

      \boldsymbol\nu \;=\; \frac{\mathbf{Fw}}{\|\mathbf{Fw}\|_1} \,, 

    where :math:`\|\cdot\|_1` denotes the :math:`L_1`-norm (sum of the absolute
    values of the components). If there is no stable class distribution but
    all individuals are born in class *k*, then the vector
    :math:`\boldsymbol\nu = (\nu_i)`, where :math:`\nu_i = 1` if and only
    if *i* = *k*, is returned.
    """
    if self._nu is None:
      sF = (np.sum(self.F, axis = 1) > 0)
      nc = sF.astype(float)
      if np.sum(nc) == 1: # all indiv. are born in the same class:
        self._nu = nc
      else:
        self.newborn_classes
        Fw = self.F @ self.w
        self._nu = Fw / np.sum(Fw)
      self._nu.flags.writeable = False
    return self._nu


  @property
  def class_of_birth(self):
    r"""
    The matrix :math:`\mathbf{B} = (b_{ij})`
    whose (*i*, *j*)-th entry gives the probability that an
    individual currently in class *j* was born in class *i*, that is,

    .. math::

       b_{ij}
       \;&=\; \mathbb{P}(\text{born in } i \mid \text{in } j \text{ at }t = 0)\\
       \;&=\; \sum_{t \geq 0} \mathbb{P}\big(\text{born at } -t
           \,\big|\, \text{in } i \text{ at }-t\big) \, 
           \mathbb{P}\big(\text{in } i \text{ at } -t
           \,\big|\, \text{in } j \text{ at }t = 0\big) \\
       \;&=\; \sum_{t \geq 0} \sum_k p_f(i, k) \, 
           p_s^{(t)}(j, i) \,, 
    
    with :math:`\mathbf{P}_{\!f} = (p_f(i, j))` and :math:`\mathbf{P}_{\!s}^t =
    (p_s^{(t)}(i, j))` the genealogical matrices. In matrix form,

    .. math::

      \mathbf{B} \;=\;
      (\mathbf{I} - \mathbf{P}_{\!s}^\top)^{-1}
       \otimes\mathbf{P}_{\!f} \, \mathbf{E}\,

    where **E** is a square matrix of ones and :math:`\otimes` denotes
    the entry-wise product.
    """
    if self._class_of_birth is None:
      sF = (np.sum(self.F, axis = 1) > 0)
      nc = sF.astype(float)
      if np.sum(nc) == 1: # all indiv. are born in the same class:
        self._class_of_birth = np.column_stack([nc for j in range(self.dim)])
      else:
        try:
          fund_Ps = np.linalg.inv(np.eye(self.dim) - self.Ps.T)
          fund_Ps[np.abs(fund_Ps) < ut._ABS_TOL] = 0
          if np.any(fund_Ps < 0):
            raise ut.UnexpectedMathError(
              "The matrix (I - Ps^T)^(-1) contains negative entries. "
              "This is caused by numerical errors in the calculation "
              "of the inverse. You can try modifying the entries of A "
              "in a way that does not affect the biological relevance "
              "of the results (e.g, by adding 1e-15 to some non-zero entries).")
          E = np.ones(self.Pf.shape) 
          self._class_of_birth = fund_Ps * (self.Pf @ E)
          self._class_of_birth.flags.writeable = False
        except np.linalg.LinAlgError:
          raise ut.UnexpectedMathError(
            "Cannot compute (I - Ps)^(-1) due to numerical precision issues.")
    return self._class_of_birth


  @property
  def class_of_death(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # To implement this: extend the state-space to add one "dead" state by
    # class of death, and then use the classical result giving the probability
    # of being absored in a given absorbing state when starting from
    # a given transient state (see e.g. equation 11.2.11 in
    # https://stats.libretexts.org/Bookshelves/Probability_Theory/Book%3A_Introductory_Probability_(Grinstead_and_Snell)/11%3A_Markov_Chains/11.02%3A_Absorbing_Markov_Chains
    # but try to find a more conventional reference for the formula.
    raise NotImplementedError


  @property
  def leslie(self):
    r"""
    Whether the model is a Leslie model, i.e. an age-classified model with
    a projection matrix is of the form

    .. math::

      \mathbf{A} \;= \;
      \begin{pmatrix}
      \; f_1    & f_2    & \cdots   & f_{n-1}   & f_n     \\[1ex]
      \; s_1    & 0      & \cdots   & 0         & 0       \\
      \; 0      & s_2    & \ddots   &           & \vdots  \\
      \; \vdots &        & \ddots   & 0         & 0       \\
      \; 0      & 0      & \cdots   & s_{n-1}   & s_{n} \\
      \end{pmatrix}

    where :math:`s_{i}` is the probability of surviving from class *i*
    to class *i* + 1 and :math:`f_i` is the fertility of class *i*. The
    last class regroups all individuals older than a certain age.

    Note that here the classes have to be labeled by increasing age, otherwise
    the model will not be considered a Leslie model, even if the life-cycle
    graph is isomorphic to a Leslie model. You can therefore rely on the fact 
    that any model such that ``leslie == True`` is in the exact form above.
    To test whether a model is a "relabeled" Leslie model,
    see :attr:`relabeled_leslie`.

    Also note that for a model to be considered a Leslie model, the survival
    and fertility matrices have to have been provided when creating the model.
    Otherwise there simply is no way to know whether this is really a Leslie
    model and this could lead to incorrect results.

    >>> m0 = MPM(A = "0.5 1; 0.3 0.8")
    >>> m0.leslie
    Traceback (most recent call last):
      ...
    matpopmod.utils.NotAvailable: A = S + F decomposition required.
    >>> m1 = MPM(A = "0.5 1; 0.3 0.8", F = "0.5 1; 0 0")
    >>> m1.leslie
    True
    >>> m1.R0
    2.0
    >>> m2 = MPM(A = "0.5 1; 0.3 0.8", F = "0 1; 0 0")
    >>> m2.leslie
    False
    >>> m2.R0 # Different from the corresponding Leslie model m1. 
    3.0000000000000004

    """
    if self._leslie is None:
      auxF = self.F.copy()
      auxF[0,:] = 0
      if np.any(auxF > 0):
        self._leslie = False
      else:
        n = self.dim
        auxS = self.S.copy()
        r = np.arange(n - 1)
        auxS[r + 1, r] = 0
        auxS[n - 1, n - 1] = 0
        self._leslie = not np.any(auxS > 0)
    return self._leslie


  @property
  def usher(self):
    r"""
    Whether the model is an Usher model (also sometimes called "Lefkovitch
    model" or "standard size-based model"), i.e. has a projection matrix of the
    form

    .. math::

      \mathbf{A} \;= \;
      \begin{pmatrix}
      \; f_1 + r_1       & f_2    & \cdots   & f_{n-1}   & f_n     \\[1ex]
      \; g_1    & r_2    & \cdots   & 0         & 0       \\
      \; 0      & g_2    & \ddots   &           & \vdots  \\
      \; \vdots &        & \ddots   & r_{n-1}         & 0       \\
      \; 0      & 0      & \cdots   & g_{n-1}   & r_{n} \\
      \end{pmatrix}
    
    where :math:`f_i` is the fertility of class *i*,
    :math:`g_i` the probability of "growing" from class *i* to
    class *i* + 1, and :math:`r_i` the probability of surviving and
    remaining in class *i*.  Of course the term "growing" is an image, since we
    have no way to know whether the classes are actually based on size. 

    Note that, mathematically, Usher models are a generalization of Leslie
    models. Thus, every model such that ``usher == True`` is also such
    that ``leslie == True``.
    
    See also :attr:`relabeled_usher` for whether the model can be
    obtained by reordering the classes of an Usher model.
    """
    if self._usher is None:
      auxF = self.F.copy()
      auxF[0,:] = 0
      if np.any(auxF > 0):
        self._usher = False
      else:
        n = self.dim
        auxS = self.S.copy()
        r = np.arange(n - 1)
        auxS[r, r] = 0
        auxS[r + 1, r] = 0
        auxS[n - 1, n - 1] = 0
        self._usher = not np.any(auxS > 0)
    return self._usher 


  @property
  def relabeled_leslie(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def relabeled_usher(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def kemeny_constant(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def hitting_times(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def R0(self):
    r"""
    The measure of the net reproductive rate (also called net reproduction
    number) introduced by Cushing and Zhou in [CuZh94]_, namely the dominant
    eigenvalue of the next generation matrix :math:`\mathbf{G} =
    \mathbf{F}(\mathbf{I} - \mathbf{S})^{-1}`.

    .. rst-class:: nospaceafter

    Although this is a relevant measure of the net reproductive rate, 
    one should note that if there are several newborn classes then
    this does not necessarily correspond to the expected number of offspring
    that newborn will produce over the course of its life, in the usual sense. 
    This is because there are two, non-equivalent ways to choose a newborn:

    - According to the dominant eigenvector of **G**, as
      done here.
    - Uniformly among the individuals born in a given year, as done
      in :attr:`cohort_R0`.

    These two measures can differ significantly: 

    >>> mpm.examples.thalia_democratica.R0
    4.001730883164397
    >>> mpm.examples.thalia_democratica.cohort_R0
    5.222416673531082
    
    """
    if self._R0 is None:
      vals, rv, lv = mt.eigen_elements(self.G, left = True)
      if not np.isreal(vals[0]) or np.any(rv[0] < 0) or np.any(lv[0] < 0):
        # This can only happen due to numerical errors.
        # There is not much we can do about it.
        raise ut.UnexpectedMathError(
          "Problem in the calculation of the eigen-elements of G: "
          "the dominant eigenvalue is not real. This indicates numerical "
          "errors in the calculations of the eigen-elements. You can either "
          "inspect the eigen-elements manually using mathtools.eigen_elements, "
          "or try modifying the entries of the projection matrix in "
          "a way that does not affect the biological relevance of the results "
          "(e.g, by adding 1e-15 to some non-zero entries).")
      else:
        self._R0 = vals[0]
        self._w_G = rv[0]
        self._w_G.flags.writeable = False
        x = rv[0] @ lv[0]
        if abs(x) < ut._ABS_TOL:
          self._v_G = lv[0]
        else:
          self._v_G = lv[0] / x
        self._v_G.flags.writeable = False
    return self._R0


  @property
  def cohort_R0(self):
    r"""
    The net reproductive rate, as the average number of offspring that
    a newborn is expected to produce over its lifetime in the stable population.
    This is given by

    .. math::

      R_0^* \;=\; \|\mathbf{G} \boldsymbol \nu \|_1

    with **G** the next-generation matrix and
    :math:`\boldsymbol\nu = (\nu_i)`, where :math:`\nu_i` is the
    fraction of newborns that are born in class *i* when the population is
    at its stable distribution (see :attr:`nu`).
    """
    if self._cohort_R0 is None:
      self._cohort_R0 = np.sum(self.G @ self.nu)
    return self._cohort_R0


  @property
  def total_reproductive_output(self):
    r"""
    The matrix :math:`\mathbf{R} = (r_{ij})` such that
    :math:`r_{ij}` is the expected number of offspring of class *i*
    that an individual currently in class *j* is expected to produce
    over the course of its life. This includes offspring produced before
    the present:

    .. math::

      \mathbf{R} \;&=\;
      \underbrace{\sum_{t \geq 1} \mathbf{F}
      (\mathbf{P}_{\!s}^\top)^t}_{\text{before}} \;+\; 
      \underbrace{\sum_{t \geq 0} \mathbf{F} \mathbf{S}^t}_{\text{after}} \\
     \;&=\; \mathbf{F} (\mathbf{I} - \mathbf{P}_{\!s}^\top)^{-1}
     \mathbf{P}_{\!s}^\top
     \;+\; \mathbf{G}\,.

    where :math:`\mathbf{P}_{\!s}` is the survival component of the
    genealogical matrix :attr:`P`.
    """
    if self._total_reproductive_output is None:
      NPs = self.fundamental_matrix_Ps
      born_before = self.F @ NPs.T @ self.Ps.T
      self._total_reproductive_output = born_before + self.G
      self._total_reproductive_output.flags.writeable = False
    return self._total_reproductive_output


  @property
  def T_a(self):
    r"""
    The generation time, as the mean age of mothers in the stable population
    (that is, when there is a birth in the stable population we record
    the age of the mother).

    As suggested by [CoEl92]_, all births are not counted equally: instead,
    they are weighted by the reproductive value of the newborns. This
    yields a mathematically more tractable measure. In particular,
    [BiLe15]_ showed that :math:`T_a` can be interpreted as the
    expected time between two reproductive events along the ancestral
    lineage of an individual, and is given by

    .. math::
    
      T_a = \frac{\lambda}{\mathbf{vFw}} \, .
    
    See [Elln18]_ for a detailed discussion.
    """
    if self._T_a is None:
      self._T_a = self.lmbd / np.dot(self.v, np.dot(self.F, self.w))
    return self._T_a


  @property
  def T_G(self):
    r"""
    A variant of the classic "cohort generation time" :attr:`mu1`. Here
    births are weighted by the cohort reproductive values :attr:`v_G` instead
    of equally, as suggested by [StTC14]_. This yields the simple formula

    .. math::

      T_G = \mathbf{v}_G (\mathbf{I} - \mathbf{S})^{-1} \mathbf{w}_G,

    as shown by [Elln18]_. However the interpretation of this
    measure is subject to the same difficulties as that of :attr:`mu1`,
    and this should not be used as a measure of the typical age at which
    an individual is expected to reproduce.
    """
    if self._T_G is None:
      self._T_G = self.v_G @ self.fundamental_matrix @ self.w_G
    return self._T_G


  @property
  def T_R0(self):
    r"""
    The :math:`R_0` generation time, i.e. the time it takes for the population
    to grow by a factor of its net reproductive rate :math:`R_0`:

    .. math::

      T_{R_0} \;=\; \frac{\log R_0}{\log\lambda} \, .
      
    When :math:`\lambda \to 1`, :math:`T_{R_0} \to T_a`, the average age
    of mothers in the stable population; see [Elln18]_. Thus we can extend
    :math:`T_{R_0}` by continuity at :math:`\lambda = 1`.

    For coherence with the literature and other libraries,
    the dominant eigenvalue of the next generation matrix **G**
    is used to compute the net reproductive rate :math:`R_0`. However,
    the interpretation of this quantity is not as straightforward as is
    usually assumed, see :attr:`R0` for details.
    """
    if self._T_R0 is None:
      if math.isclose(self.lmbd, 1, rel_tol=ut._REL_TOL, abs_tol=ut._ABS_TOL):
        # When lmbd -> 1, T_R0 -> T_a
        self._T_R0 = self.T_a
      else:
        self._T_R0 = math.log(self.R0, self.lmbd)
    return self._T_R0


  @property
  def mu1(self):
    r"""
    The mean age of the mothers when considering all offspring produced by a
    cohort. This is sometimes referred to as the cohort generation time and
    is given by the formula

    .. math::

      \mu_1 \;=\; \frac{\mathbf{e F} (\mathbf{I} - \mathbf{S})^{-2}
      \mathbf{F w}}{\mathbf{e F} (\mathbf{I} - \mathbf{S})^{-1} \mathbf{F w}},

    where **e** is a vector of ones. See [CoEl92]_ and [Elln18]_.

    Despite the name "mean age of mothers in a cohort", this is not a good
    measure of the typical age at which an individual is expected to reproduce.
    In particular, :math:`\mu_1` can be greater than the life expectancy
    conditional on reproduction:

    >>> astrocaryum = mpm.examples.astrocaryum_mexicanum
    >>> astrocaryum.mu1
    275.1594139265308
    >>> astrocaryum.life_expectancy_repro
    232.18934046629715

    See [Bien19]_ for a detailed explanation of the problems associated
    with :math:`\mu_1`, and :meth:`mean_age_repro` for an
    alternative measure of the typical age at reproduction.
    """
    if self._mu1 is None:
      F, G, w = self.F, self.G, self.w
      num = np.sum(np.dot(G, np.dot(self._N, np.dot(F, w))))
      denom = np.sum(np.dot(G, np.dot(F, w)))
      self._mu1 = num / denom
    return self._mu1


  def _aux_mean_age_and_life_expectancy(self, mean_age_repro,
               n, reproduction, ini, target_err, return_err):
    r"""
    Internal auxilliary function used to factorize the code of
    :meth:`mean_age_repro` and :meth:`life_expectancy_repro`.
    The first argument, `mean_age_repro`, indicates which one of these
    two quantities we compute.
    """
    if not target_err is None:
      if not target_err > 0:
        raise ValueError("Incorrect argument target_err: "
          f"should be a positive number, was {target_err}.")

    if ini is None:
      ini = self.nu
    else:
      try:
        ini = np.array(ini)
      except:
        ValueError("Incorrect argument ini: "
          f"should represent a vector, was {ini}.")
    ut.assert_vector(ini, length = self.dim, name = "ini")
    if not np.all(ini >= 0): # (not x >= 0) <=/=> (x < 0)
      raise ValueError("Incorrect argument ini: "
        f"should be positive weights, was {ini}.")

    if not (isinstance(n, int) and n > 1):
      raise ValueError("Incorrect argument n: "
        f"should be an integer > 1, was {n}.")

    # The additional stage corresponds to dead individuals
    classes = tuple(range(self.dim + 1))
    proba_death = 1 - np.sum(self.S, axis=0)
    S_aux = np.vstack((self.S, proba_death)).T

    # Compute total fertility for each (non-dead) stage
    F_tot = np.sum(self.F, axis=0)

    # Saving a few RNG when choosing the newborn class
    random_newborn = (len(np.nonzero(ini)[0]) > 1)
    if not random_newborn:
      newborn_class = np.nonzero(ini)[0][0]

    obs, acc = 0, []
    keep_going = True

    # supposed to provide minor speed improvements
    choice = ut.rng.choice
    dim = self.dim
    rand = ut.rng.random

    if reproduction == "poisson":
      if mean_age_repro:
        new_offspring = ut.rng.poisson
      else:
        new_offspring = lambda x: (1 if rand() < -math.expm1(-x) else 0)
    elif reproduction == "bernoulli":
      if np.any(F_tot > 1):
        raise ValueError("Cannot use Bernoulli reproduction: the sum of "
          "one of the columns of F is greater than 1.")
      new_offspring = (lambda x: (1 if rand() < x else 0))
    else:
      raise ValueError("Invalid argument reproduction: should be either "
        f"'poisson' or 'bernoulli', was {reproduction}.")

    while keep_going:

      while obs < n:
        alive = True
        age = 1
        num_offspring, sum_ages = 0, 0
        if random_newborn:
          pos = choice(range(dim), p = ini)
        else:
          pos = newborn_class
        while alive:
          if pos == dim:
            alive = False
          else:
            if mean_age_repro:
              k = new_offspring(F_tot[pos])
              sum_ages += k * age
              num_offspring += k
            else:
              if num_offspring == 0:
                num_offspring = new_offspring(F_tot[pos])
            pos = choice(classes, p = S_aux[pos])
            age += 1
        if num_offspring > 0:
          obs += 1
          if mean_age_repro:
            acc.append(sum_ages / num_offspring)
          else:
            acc.append(age - 1)

      mean = np.mean(acc)
      err = mt.student_t(n - 1) * np.std(acc) / math.sqrt(n)
      if target_err is None:
        keep_going = False
      else:
        keep_going = (err >= target_err * mean)
        n = 2 * n

    if mean_age_repro:
      self._LAST_COMPUTED_MEAN_AGE_REPRO = (mean, n, err)
    else:
      self._LAST_COMPUTED_LE_REPRO = (mean, n, err)

    if return_err:
      return (mean, n, err)
    else:
      return mean


  def mean_age_repro(self, n=1000, reproduction="poisson", ini=None, 
                     target_err=1e-2, return_err=False):
    r"""
    *Note: unlike most descriptors, this function will return a different value
    every time it is called. This is because the numerical estimation is based
    on individual-based simulations, not an analytical formula. The last
    computed value is stored in* ``self._LAST_COMPUTED_MEAN_AGE_REPRO``.

    *Be aware that the computing time can be very long, especially when few
    newborns get to reproduce.*

    .. rst-class:: nospaceafter

    Numerical estimate of the mean age at which a typical mother produces
    offspring, using individual-based simulations. Formally, this is the
    expected age at offspring production, conditional on reproduction;
    see [Bien19]_.

    .. list-table::
      :widths: 15 85

      * - `n`
        - The number of replicates.
      * - `reproduction`
        - The distribution of the number of offspring.
          Use ``"bernoulli"`` for monotocous species and ``"poisson"`` (the
          default) otherwise.
      * - `ini`
        - The birth class of the focal individual, as a vector of weights.
          The default is to use :attr:`nu`, the stable distribution of newborns.
      * - `target_err`
        - if ``None``, this parameter will be ignored and `n`
          replicates will be used. Otherwise, the number of replicates
          will start at `n` and double that number until ``err < target_err *
          mean`` (see below).
      * - `return_err`
        - Whether to return the number of replicates used and
          :math:`\mathsf{err}=\mathrm{t}_{n-1} \hat{\sigma} / \sqrt{n}`, where
          :math:`\mathrm{t}_{n-1}` is the 0.975 quantile of the Student
          distribution with *n*-1 degrees of freedom. Thus, ``err`` is the
          half-width of the 95% confidence interval for the mean of normally
          distributed variables. If `return_err` is set, then a tuple ``(mean,
          reps, err)`` is returned; otherwise only ``mean`` is returned.
    """
    return self._aux_mean_age_and_life_expectancy(
      True, n, reproduction, ini, target_err, return_err)


  @property
  def proba_repro(self):
    r"""
    The vector whose *i*-th entry is the probability that an individual
    currently in class *i* will reproduce during its remaining lifetime. Use
    ``nu @ proba_repro`` to get the proportion of newborns that reproduce
    before dying in the stable population.

    See :attr:`life_expectancy_repro` for details on how this is calculated.
    """
    if self._proba_repro is None:
      _ = self.remaining_life_expectancy_repro 
    return self._proba_repro


  @property
  def life_expectancy_repro(self):
    r"""
    The life expectancy conditional on reproducing, assuming that the
    fertilities are Poisson-distributed. See :attr:`life_expectancy`
    for a discussion of what we mean by "life expectancy".

    To compute this quantity, we build a Markov chain tracking the movement
    of individuals in the life-cycle, with two absorbing states: corresponding
    to dead individuals that reproduced and dead individuals that did not
    reproduce. This requires knowing the probability of reproducing
    in each class of the model, which explains that we need to assume 
    that the fertilities are Poisson-distributed.

    Once we have this extended Markov chain, we condition it on absorption
    in the "died after reproducing" state (see e.g. Section 11.1.2 of [KeCa05]_,
    or Chapter III of [KeSn76]_ for a more detailed treatment)
    and compute the expected time to absorption when starting from the
    distribution of newborns in the stable population (see :attr:`nu`).
    """
    if self._life_expectancy_repro is None:
      _ = self.remaining_life_expectancy_repro 
    return self._life_expectancy_repro


  @property
  def remaining_life_expectancy_repro(self):
    r"""
    The remaining life expectancy of an individual, as a function of
    its current class and conditional on this individual reproducing in
    the future.  See :attr:`life_expectancy_repro` for details on how this is
    calculated.
    """
    if self._remaining_life_expectancy_repro is None:

      S, F, n = self.S, self.F, self.dim

      # Proba of reproducing in class i, assuming Poisson reproduction
      pr = -np.expm1(-np.sum(F, axis = 0))

      # Auxiliary transition matrix Sb
      S00 = S * (1 - pr)[:, np.newaxis]
      S10 = S * pr[:, np.newaxis]
      Z = np.zeros((n, n))
      R0 = np.hstack((S00, Z))
      R1 = np.hstack((S10, S))
      Sb = np.vstack((R0, R1))

      # Transitions to the absorbing dead states
      ps = 1 - np.sum(Sb, axis = 0)
      RM1 = np.hstack((ps[:n], np.zeros(n)))
      RM2 = np.hstack((np.zeros(n), ps[n:]))
      M = np.vstack((RM1, RM2))
      
      # Fundamental matrix
      Nb = np.linalg.inv(np.eye(2 * n) - Sb)

      # Probability of reproducing in the (remaining) lifetime
      B = M @ Nb
      b_aux = B[1,:]
      self._proba_repro = (1 - pr) * b_aux[:n] + pr
      self._proba_repro.flags.writeable = False

      # Fundamental matrix conditional on reproduction
      with warnings.catch_warnings():
        # to suppress RuntimeWarning raised by division by 0:
        warnings.simplefilter("ignore")
        N_cond = (Nb / b_aux) * b_aux[:, np.newaxis]

      # Remaining life expectancy conditional on reproduction
      rle = np.sum(N_cond, axis = 0)

      # proba of starting in the reproductive subclass of the class
      with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p1 = pr / self._proba_repro 
        p1 = np.nan_to_num(p1)
      
      # we do the following to ensure that nan * x = 0 if x = 0, nan otherwise
      aux = p1 * rle[n:]
      acc, postrepro = 0, self.postreproductive_classes
      nu_repro = (self.nu * self._proba_repro) / (self.nu @ self._proba_repro)
      for i in range(n):
        p0 = 1 - p1[i]
        if p0 > ut._ABS_TOL:
          aux[i] += (1 - p1[i]) * rle[i]
        if postrepro[i] == 0:
          acc += aux[i] * nu_repro[i]
      self._remaining_life_expectancy_repro = aux
      self._remaining_life_expectancy_repro.flags.writeable = False
      self._life_expectancy_repro = acc

    return self._remaining_life_expectancy_repro
    

  @property
  def w_G(self):
    r"""
    Cohort stable distribution (dominant right-eigenvector of :attr:`G`,
    normalized so that its entries sum to 1).
    """
    if self._w_G is None:
      _ = self.R0 # This computes and stores w_G.
    return self._w_G

  @property
  def v_G(self):
    r"""
    Cohort reproductive values (dominant left-eigenvector of :attr:`G`,
    normalized so that :math:`v_c \cdot w_c = 1`).
    """
    if self._v_G is None:
      _ = self.R0 # This computes and stores v_G.
    return self._v_G


  @property
  def proba_maturity(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # Defined has the proba of reaching a reproductive class.
    # Should be given as a vector (function of the starting class).
    raise NotImplementedError


  def class_survivorship(self, t):
    r"""
    The class-structured survivorship, which gives the probability that an
    individual survives at least *t* time steps, as a function of the current
    class of that individual. That is,

    .. math::

      \ell_i(t) \;=\; \mathbb{P}(T_i \geq t)\,, 

    where :math:`T_i` is the remaining lifespan of an individual from class *i*.
    For instance, :math:`\ell_i(1)` is the probability that the individual
    survives to the next time step. We have:

    .. math::

      \ell(t) \;=\; \mathbf{e\,S}^t\,,  

    where **S** is the survival matrix and **e** is a vector of ones.
    """
    if t < 0 or not ut.represents_integer(t):
      raise ValueError(f"t should be a nonnegative integer, was {t}")
    ans = np.sum(np.linalg.matrix_power(self.S, t), axis = 0)
    ans.flags.writeable = False # for consistency
    return ans


  def survivorship(self, t):
    r"""
    The survivorship function :math:`\ell`, which gives the probability that a
    newborn reaches age *t* in the stable population:

    .. math::

      \ell(t) \;=\; \mathbf{e\,S}^t \boldsymbol\nu \,, 

    where **S** is the survival matrix; **e** is a vector of ones; and
    :math:`\boldsymbol \nu` is the distribution of newborns in the stable
    population (see :attr:`nu`).
    """
    return self.class_survivorship(t) @ self.nu


  @property
  def conditional_life_expectancy(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # TODO
    # The matrix Lambda_{ij} of Cochran and Ellner
    raise NotImplementedError


  @property
  def remaining_life_expectancy(self):
    r"""
    The remaining life expectancy of an individual, as a function of
    its current class. See :attr:`life_expectancy` for a discussion of what
    this quantity represents. It is given by

    .. math::

      \sum_{t \geq 0} \ell_i(t)
      \;=\; \mathbf{e}(\mathbf{I} - \mathbf{S})^{-1}\,, 

    where :math:`\ell_i` is the survivorship of class *i* and **e** is a
    vector of ones.
    """
    ans = np.sum(self.fundamental_matrix, axis = 0)
    ans.flags.writeable = False # for consistency
    return ans


  @property
  def life_expectancy(self):
    r"""
    The expected number of projection intervals that an individual
    born in the stable population lives. The convention used here is to
    return 1 for annuals. For instance,

    >>> m = MPM(S = "0", F = "1.2")
    >>> m.life_expectancy
    1.0

    Note that whether this corresponds to the expected age at death depends
    on the type of census (pre-breeding, post-breeding, birth-flow...),
    as well as on when deaths occur in the projection interval. 
    It is also possible to get different results for models that describe
    the same population, if the models are build differently:
    
    >>> eg = matpopmod.examples
    >>> eg.passerine_prebreeding.life_expectancy
    1.7
    >>> eg.passerine_postbreeding.life_expectancy
    1.3399999999999999

    This is normal: individuals who die shortly after their birth are not
    taken into account in the pre-breeding model, which biases the life
    expectancy upwards.

    With our convention, the life expectancy is given by

    .. math::

      \sum_{t \geq 0} \ell(t)
      \;=\; \mathbf{e}(\mathbf{I} - \mathbf{S})^{-1} \boldsymbol\nu \,, 

    where :math:`\ell` is the :meth:`survivorship <survivorship>`, **e** is a
    vector of ones and :math:`\boldsymbol \nu` is the distribution of newborns
    in the stable population (see :attr:`nu`).
    """

    return self.remaining_life_expectancy @ self.nu


  @property
  def variance_remaining_lifespan(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # As a vector, Equation (5) of Cochran and Ellner
    raise NotImplementedError


  @property
  def variance_lifespan(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # To implement, use variance_remaining_lifespan + law of total variance. 
    raise NotImplementedError


  @property
  def mean_age_class(self):
    r"""
    The vector whose *i*-th component is the mean age in class *i*, when the
    population is at its stable structure. It is given by

    .. math::

      \mathbf{y} \;=\; \big((\mathbf{I} - \lambda^{-1} \mathbf{S})^{-2}
      \boldsymbol \nu \big) \oslash
      \big((\mathbf{I} - \lambda^{-1} \mathbf{S})^{-1} \boldsymbol \nu \big)\,, 

    where :math:`\boldsymbol\nu` is the distribution of newborns in the
    stable population and :math:`\oslash` denotes the entry-wise division --
    see e.g. Equation (23) in [CoEl92]_.

    For post-breeding models, one may want to substract 1 from this
    quantity; here individuals in newborn classes are 1 year old.
    """
    if self._mean_age_class is None:
      X = np.linalg.inv(np.eye(self.dim) - self.S / self.lmbd)
      self._mean_age_class = (X @ (X @ self.nu)) / (X @ self.nu)
      self._mean_age_class.flags.writeable = False

    return self._mean_age_class


  @property
  def mean_age_population(self):
    r"""
    The mean age in the stable population, given by
    :math:`\mathbf{y} \cdot \mathbf{w}`, where **y** is the vector whose
    *i*-th entry is the mean age in class *i* (see :attr:`mean_age_class`).

    For post-breeding models, one may want to substract 1 from this quantity.
    """
    if self._mean_age_population is None:
      self._mean_age_population = self.mean_age_class @ self.w
    return self._mean_age_population


  @property
  def variance_age_class(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # Equation (24)
    raise NotImplementedError


  @property
  def variance_age_population(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # Equation (24) + law of total variance
    raise NotImplementedError


  def age_specific_fertility(self, t):
    r"""
    The matrix :math:`\mathbf{\Phi}(t)`, whose (*i*, *j*)-th entry
    gives the expected number of class-*i* offspring produced at age *t* by an
    individual in class *j* at age 0. It is given by

    .. math::

      \mathbf{\Phi(t)} \;=\;
      \mathbf{F} \tilde{\mathbf{S}}(t) , 

    where the (*i*, *j*)-th entry
    :math:`\tilde{s}_{ij}(t)` of
    :math:`\tilde{\mathbf{S}}(t) = (\tilde{s}_{ij}(t))` is the probability
    that an individual in class *j* at time 0 is in class i at time t,
    conditional on having survived to that time:

    .. math::


      \tilde{s}_{ij}(t) \;=\;
      \frac{\mathbf{S}^t(i, j)}{\sum_{k} \mathbf{S}^t(k, j)}.

    See e.g. Section 11.3.2 of [KeCa05]_.
    """
    St = np.linalg.matrix_power(self.S, t)
    with warnings.catch_warnings():
      # to suppress RuntimeWarning raised by division by 0:
      warnings.simplefilter("ignore")
      ans = self.F @ (St / np.sum(St, axis = 0))
    return ans

  @property
  def mean_age_maturity(self):
    r"""
    *(coming in version 0.2.0)*
    """
    # Using the matrix tau_{ij} of Cochran and Ellner
    raise NotImplementedError

  @property
  def mean_age_first_repro(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def population_entropy(self):
    r"""
    The population entropy, defined by Demetrius as\ |entropy*|

    .. math::

      S = H \cdot T_a

    where *H* is the :attr:`entropy_rate` of the model and
    :math:`T_a` is the generation time, as given by the mean age of mothers
    in the stable population.

    .. rst-class:: nospaceafter

    For Leslie models, *S* has several interpretations; it corresponds to
    both:

    - The Shannon entropy of the difference of age between mothers and
      daughters in the stable population.
    - The Shannon entropy of a random trajectory in the genealogy of the
      population, which we refer to as the *genealogical entropy*.

    Moreover, for those models *S* has the following simple expression:

    .. math::

      S \;=\; -\sum_i \phi_i \lambda^{-i} \log_2 \phi_i \lambda^{-i},

    where :math:`\phi_i` is the age-specific net fertility
    and :math:`\lambda` is the asymptotic growth rate -- see [Deme74]_,
    but note that in this article Demetrius refers to *H*, not *S*, as
    the entropy of the population.

    For general projection matrices, there is no clear interpretation
    of *S* as an entropy in the usual sense.
    """
    return self.entropy_rate * self.T_a


  @property
  def birth_entropy(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def genealogical_entropy(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  @property
  def lifetable_entropy(self):
    r"""
    The life-table entropy, also known as Keyfitz's entropy to distinguish
    it from the population entropy introduced by Demetrius.
    Introduced by Keyfitz in [Keyf77]_, is defined as

    .. math::

      - \frac{1}{L} \sum_{t \geq 0} \ell(t) \log_2 \ell(t)\,, 

    where :math:`\ell` is the :meth:`survivorship <survivorship>`, that is, the
    probability of reaching age *t* and :math:`L = \sum_{t \geq 0} \ell(t)` is
    the life expectancy.

    Note that despite its accepted name, the life-table entropy is not
    an entropy in the usual sense. This makes its interpretation challenging --
    all the more so given that in the literature it is often conflated with
    Demetrius' population entropy (see e.g. Section 4.3.1 of [KeCa05]_).
    """
    if self._lifetable_entropy is None:
      ell = self.survivorship # pointless micro-optimization. :)
      log = np.log            #
      t = 1
      x = ell(t)
      xlogx = 0 if x == 0 else x * log(x)
      h = xlogx
      # We use a very naive method to compute the sum of the series,
      # but that should be sufficient in practice because ell(t) has
      # a geometric tail.
      while x > ut._ABS_TOL:
        t += 1
        x = ell(t)
        xlogx = 0 if x == 0 else x * log(x)
        h += xlogx
      self._lifetable_entropy = - h / self.life_expectancy
    return self._lifetable_entropy 


  def keyfitz_delta(self, n0):
    r"""
    Keyfitz's :math:`\Delta`, which corresponds to the
    total variation distance between the stable class distribution **w**
    and the initial class distribution
    :math:`\mathbf{x} = \mathbf{n}(0) / \|\mathbf{n}(0)\|_1`. It is given by

    .. math::

      \Delta \;=\;
      \frac{1}{2} \|\mathbf{x} - \mathbf{w}\|_1 \;=\;
      \frac{1}{2} \sum_{i} |x_i - w_i| \,.

    The factor 1/2 ensures that :math:`\Delta \in [0, 1]`.
    """
    n0 = np.array(n0)
    ut.assert_vector(n0, self.dim, name = "n0")
    ut.assert_nonnegative(n0, name = "n0")
    return 0.5 * np.linalg.norm(n0 / np.sum(n0) - self.w, 1)


  def cohen_D1(self, n0):
    r"""
    Cohen's :math:`D_1` index of cumulative distance, introduced in [Cohe79]_:

    .. math::

      D_1 = \Bigg\|\sum_{t \geq 0} \big(\mathbf{n}(t) / \lambda^t -
              \mathbf{vn}(0) \mathbf{w}\big)\Bigg\|_1 \,.

    This corresponds to accumulating the difference between
    :math:`\mathbf{n}(t) / \lambda^t` and its limit along the trajectory of
    the population, then taking sum of the absolute values of
    the entries of the resulting vector.

    What makes :math:`D_1` noteworth is that when the projection
    matrix **A** is (quasi-)primitive we have
    
    .. math::
    
      D_1 = \big(
              (\mathbf{I} + \mathbf{wv} - \lambda^{-1} \mathbf{A}) - \mathbf{wv}
            \big) \, \mathbf{n}(0), 

    which makes it straightforward to compute :math:`D_1` in practice. However,
    one of the major drawbacks of :math:`D_1` is that when
    :math:`n_i(t) / \lambda^t` fluctuates around :math:`\mathbf{vn}(0)\, w_i`,
    the terms of the time series tend to cancel out.
    For instance, consider the following situation:

    >>> dp = mpm.examples.dipsacus_sylvestris
    >>> dp.w
    array([0.63771991, 0.26395418, 0.01215485,
           0.06931315, 0.01224112, 0.00461679])
    >>> n0 = [0.2635, 0.6420, 0.0157, 0.0483, 0.0013, 0.0292]
    >>> dp.cohen_D1(n0)
    0.037129817800633416

    Here, :math:`D_1` is small even though the initial population structure
    is very different from the stable one, and the fluctuations
    of :math:`\mathbf{n}(t) / \lambda^t` around
    :math:`\mathbf{vn}(0) \mathbf{w}` are initially much larger than
    :math:`D_1`:

    >>> traj = dp.trajectory(n0, t_max=5)
    >>> numpy.sum(traj.rescaled_Y - (dp.v @ n0) * dp.w, axis=1)
    array([-1.43193488,  2.16076214, -0.48105167,
           -0.9132861 ,  1.02463032, -0.31244266])
    
    This makes the relevance of :math:`D_1` questionable.
    """
    n0 = np.array(n0)
    ut.assert_vector(n0, self.dim, name = "n0")
    ut.assert_nonnegative(n0, name = "n0")
    row_v = self.v.view().reshape((1, self._dim))
    col_w = self.w.view().reshape((self._dim, 1))
    B = col_w @ row_v
    Z = np.linalg.inv(np.eye(self.dim) + B - self.A / self.lmbd)
    return np.sum(np.abs((Z - B) @ n0))


  @property
  def fertility_excess(self):
    r"""
    The fertility excess (non-standard terminology), defined as
    the constant *c* > 0 such that
    :math:`\rho(\mathbf{S} + c^{-1} \mathbf{F}) = 1`, where :math:`\rho`
    denotes the spectral radius (i.e. the asymptotic growth rate *λ*, in
    the case of a primitive matrix). In other words, the
    fertility excess is the factor by which all fertilities must
    be rescaled to get a stationary projection matrix.
    """
    if self._fertility_excess is None:
      self._fertility_excess = _aux_excess(self.S, self.F, self.lmbd)
    return self._fertility_excess


  @property
  def survival_excess(self):
    r"""
    The survival excess (non-standard terminology), defined as
    the constant *c* > 0 such that
    :math:`\rho(c^{-1}\mathbf{S} + \mathbf{F}) = 1`, where :math:`\rho`
    denotes the spectral radius (i.e. the asymptotic growth rate *λ*, in
    the case of a primitive matrix). In other words, the
    survival excess, if it exists, is the factor by which all fertilities must
    be rescaled to get a stationary projection matrix.

    When *λ* > 1, if the spectral radius of **F** is greater than 1, then *c*
    is not defined and ``NaN`` will be returned. When *λ* < 1, the matrix
    :math:`c^{-1}\mathbf{S}` can have columns that sum to more than 1.
    This means that the original model is such that it is impossible to get a
    sationary projection matrix by increasing survival by a common factor, even
    though *c* is mathematically well-defined.
    """
    if self._survival_excess is None:
      try:
        self._survival_excess = _aux_excess(self.F, self.S, self.lmbd)
      except ut.InadequateMatrix:
        if ut._ISSUE_WARNINGS:
          warnings.warn(
            "F has a growth rate >= 1, the survival excess is not defined.")
        self._survival_excess = np.nan
    return self._survival_excess


  @property
  def theta(self):
    r"""
    *(coming in version 0.2.0)*
    """
    raise NotImplementedError


  def population_momentum(self, n0, auto=True):
    r"""
    Population momentum is the name given by Keyfitz in [Keyf71]_ to the
    following phenomenon: when a population undergoes a demographic transition,
    it can keep growing even after its asymptotic growth rate has become
    equal to 1. The reason for this is that the population is not at its stable
    structure, and that the increase / decrease that we see corresponds to the
    transient regime.

    The standard way to quantify this is to use the following quantity,
    often referred to as the momentum of the population:

    .. math::

      M = \lim_{t \to +\infty} \frac{\|\mathbf{n}(t)\|_1}{\|\mathbf{n}(0)\|_1}, 

    where *t* = 0 is the time at which the asymptotic growth rate of the
    population becomes equal to 1. For (quasi-)primitive, stationary
    projection matrices, this limit always exists and is given by

    .. math::

      M = \frac{\mathbf{vn}(0)}{\|\mathbf{n}(0)\|_1}, 

    where **v** is the vector of reproductive values of the projection matrix,
    rescaled so that **vw** = 1.

    Computing the population momentum requires knowing two things: (1) the
    population vector at the time *t* = 0 of the transitions and (2) the
    projection matrix after the transition; specifying the projection
    matrix before the transition is not sufficient. Therefore,
    this function makes the following assumptions:

    - If *λ* = 1, we assume that the projection matrix of the model
      describes the dynamics of the population after the demographic
      transition, and we return :math:`\mathbf{vn}(0) / \|\mathbf{n}(0)\|_1`. 

    - If *λ* ≠ 1, we do not know what projection matrix should be used after
      the transition, so :class:`~matpopmod.utils.NotAvailable` is raised.
      However, if `auto` is ``True``, then instead of raising an error we
      assume that the projection matrix after the transition is

      .. math::

        \mathbf{A}' = \mathbf{S} + c^{-1} \mathbf{F}

      where *c* is the :attr:`fertility_excess`, i.e.
      the constant such that
      :math:`\lambda(\mathbf{S} + c^{-1} \mathbf{F}) = 1`.
      This corresponds to Keyfitz's original idea of assuming that all
      fertilities get reduced by the same factor during the demographic
      transition.

    """
    if math.isclose(self.lmbd, 1, rel_tol=ut._REL_TOL, abs_tol=ut._ABS_TOL):
      return (self.v @ n0) / np.sum(n0)
    else:
      if auto:
        m = MPM(S = self.S, F = self.F / self.fertility_excess)
        return (m.v @ n0) / np.sum(n0)
      else:
        raise ut.NotAvailable("The projection matrix is not stationary. "
          "You need to either specify the transition matrix after the "
          "demographic transition or use auto = True to use the default one.")


  def trajectory(self, n0, t_max, step=1):
    r"""
    The trajectory of the population vector associated to
    the initial condition `n0`, up to time *t* = `t_max`.
    This is the solution of
  
    .. math::
  
      \mathbf{n}(t+1) \;=\; \mathbf{A} \mathbf{n}(t)\,,
      \quad t = 0, \ldots, t_{\max}.
  
    The population vector will only be computed for multiples of the optional
    argument `step`. For instance, use `step = 3` to get the population vector
    at times :math:`t= 0, 3, 6, \ldots`
  
    Returns a :class:`~matpopmod.trajectories.Trajectory` object. Trajectories
    have a set of methods that facilitate their study and can be plotted using
    the function :func:`~matpopmod.plot.trajectory` from the module
    :mod:`~matpopmod.plot`.
    """
    return tj.compute_trajectory(self, n0, t_max, step=1)


  def stochastic_trajectories(self, n0, t_max, reps,
                              reproduction = "poisson", Z = None):
    r"""
    Returns a list of `reps` independent stochastic trajectories
    corresponding to the matrix population model. Each trajectory
    starts at time *t* = 0 from the integer-valued population vector `n0`,
    and ends at time *t* = `t_max`.

    In ecological terms, those stochastic trajectories account for
    *demographic stochasticity* -- that is, the randomness stemming
    from the variation in the realizations of the demographic rates of the
    individuals (as opposed to randomness in the environment affecting
    the demographic rates population-wide).
    
    Formally, the trajectories are realizations of a multitype Galton--Watson
    process whose types correspond to the classes of the model. At
    each time-step, each class-*j* individual *x*:

    .. rst-class:: spaced

    - produces a random number :math:`F_{ij}(x)` of class-*i*
      individuals, where :math:`\mathbb{E}(F_{ij}(x)) = f_{ij}`, the
      (*i*, *j*)-th entry of the fertility matrix **F**;

    - survives and goes to class *i* with probability :math:`s_{ij}`,
      the (*i*, *j*)-th entry of the survival matrix **S**.

    What happens to individuals is independent of what happens to other
    individuals or of anything that happened in the past.
    This crucial assumption is the cornerstone of the link between multitype
    Galton--Watson processes and matrix population models. It ensures
    that :math:`\mathbf{n}(t)`, the expected value of the (integer-valued)
    vector tracking the number of individuals in each class of the
    stochastic process, satisfies the linear equation

    .. math::

      \mathbf{n}(t+1) = \mathbf{A} \mathbf{n}(t)

    with **A** = **S** + **F** is the projection matrix of the matrix
    population model.

    Each Galton--Watson process corresponds to a single matrix population model,
    but there are an infinity of Galton--Watson processes for a given
    matrix population model. To fully specify a Galton--Watson process, one
    needs to provide the joint law of the family :math:`(S_{ij}, F_{ij})_i`, for
    every *j*.  Two standard sets of assumptions can be selected via
    the argument `reproduction`:

    .. rst-class:: spaced


    - ``"poisson"`` ---
      for all *j*, :math:`(F_{ij})_i` are independent
      Poisson variables with respective parameters :math:`f_{ij}`, and are
      independent of the family :math:`(S_{ij})_i`. If the
      survival and fertility matrices are not available, instead of
      the model described above we simply take the number of 
      class-*i* individuals that a class-*j* individual leaves at the next
      time-step to follow a :math:`\mathrm{Poisson}(a_{ij})` distribution
      (instead of
      :math:`\mathrm{Bernoulli}(s_{ij}) + \mathrm{Poisson}(f_{ij})` in the
      more detailed model).

      This is the assumption that we recommend using in the absence of
      additional information.

    - ``"bernoulli"`` ---
      for all *j*, :math:`(F_{ij})_i` are incompatible Bernoulli variables
      that are independent of :math:`(S_{ij})_i`.
      In other words, each class-*j* individual produces an
      offspring with probability :math:`\sum_k f_{kj} \leq 1`, and that
      offspring is produced in class *i* with probability
      :math:`f_{ij} / \sum_k f_{kj}`. If the survival and fertility
      matrices are not available or if
      :math:`\sum_k f_{kj} > 1`, an error will be raised.

      This assumption is what we recommend using for monotocous species.

    Alternatively, one can use a custom Galton--Watson process by specifying
    the argument `Z`. In that case, `Z` should be a random Python function
    such that the dynamics of the population vector :math:`N(t)` is defined
    by:

    .. math::

      N(t+1) = Z\big(\mathbf{F}, \mathbf{S}, N(t)\big)

    if **S** and **F** are known,
    and :math:`N(t+1) = Z(\mathbf{A}, \mathrm{None}, N(t))` otherwise.

    Because this function focuses on efficiency,
    it is not possible to specify :math:`(S_{ij}, F_{ij})_i` only; the
    user has to use them to work out how to sample *Z*. 
    See the module :mod:`~matpopmod.ibm` to generate
    stochastic trajectories directly from :math:`(S_{ij}, F_{ij})_i`.
    """
    return tj.compute_stochastic_trajectories(
             self, n0, t_max, reps, reproduction, Z = None)


def _aux_excess(X, Y, lmbd_ini):
  r"""
  Internal function used in :attr:`fertility_excess` and
  :attr:`survival_excess`. Returns *c* such that the spectral radius of
  :math:`X + c^{-1} Y` is equal to 1, assuming that **X** and **Y** are
  non-negative matrices and that the spectral radius of **X** is smaller than 1.
  If the spectral radius of **X** is greater than or equal to 1 (which cannot
  happen if **X** is the survival matrix of a :class:`MPM`; and should rarely
  happen if it is a fertility matrix), then this will raise
  :exc:`InadequateMatrix`.
  """
  if mt.spectral_radius(X) >= 1 - ut._ABS_TOL:
    raise ut.InadequateMatrix("X should have a spectral radius < 1")
  if math.isclose(lmbd_ini, 1, rel_tol=ut._REL_TOL, abs_tol=ut._ABS_TOL):
    return 1.
  if lmbd_ini < 1.:
    a, b = 0., 1.
  else:
    a, b = 1., 2.
    while mt.spectral_radius(X + Y / ((a + b) / 2)) > 1.:
      b *= 2.
  while not math.isclose(a, b, rel_tol=ut._REL_TOL, abs_tol=ut._ABS_TOL):
    c = (a + b) / 2.
    if mt.spectral_radius(X + Y / c) < 1.:
      b = c 
    else:
      a = c
  return c


#### OLD CODE #####

# The following function is not listed in the documentation.
# We only keep it for testing.

def _life_expectancy_repro_IBM(m, n=1000, reproduction="poisson", ini=None, 
                          target_err=1e-2, return_err=False):
  r"""
  *Note: unlike most descriptors, this function will return a different value
  every time it is called. This is because the numerical estimation is based
  on individual-based simulations, not an analytical formula. The last
  computed value is stored in* ``self._LAST_COMPUTED_LE_REPRO``.

  *Be aware that the computing time can be long, especially when few
  newborns get to reproduce.*

  .. rst-class:: nospaceafter

  Numerical estimate of life expectancy conditional on reproduction,
  using individual-based simulations.

  .. list-table::
    :widths: 15 85

    * - `n`
      - The number of replicates.
    * - `reproduction`
      - The distribution of the number of offspring.
        Use ``"bernoulli"`` for monotocous species and ``"poisson"`` (the
        default) otherwise.
    * - `ini`
      - The birth class of the focal individual, as a vector of weights.
        The default is to use :attr:`nu`, the stable distribution of newborns.
    * - `target_err`
      - if ``None``, this parameter will be ignored and `n`
        replicates will be used. Otherwise, the number of replicates
        will start at `n` and double that number until ``err < target_err *
        mean`` (see below).
    * - `return_err`
      - Whether to return the number of replicates used and
        :math:`\mathsf{err}=\mathrm{t}_{n-1} \hat{\sigma} / \sqrt{n}`, where
        :math:`\mathrm{t}_{n-1}` is the 0.975 quantile of the Student
        distribution with *n*-1 degrees of freedom. Thus, ``err`` is the
        half-width of the 95% confidence interval for the mean of normally
        distributed variables. If `return_err` is set, then a tuple ``(mean,
        reps, err)`` is be returned; otherwise only ``mean`` is returned.
  """
  return m._aux_mean_age_and_life_expectancy(
    False, n, reproduction, ini, target_err, return_err)


