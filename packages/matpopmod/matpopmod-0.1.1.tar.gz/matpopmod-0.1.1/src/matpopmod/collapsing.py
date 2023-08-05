"""
This module provides functions to reduce the number of classes of a model
by merging some of them, as described in [BALM17]_.
Two methods are available:

.. rst-class:: spaced

- **Individualistic collapsing.** This method, first studied in [Hool00]_,
  amounts to what we would get if we were to rebuild the model by counting
  individuals while being unable to distinguish between subclasses of a merged
  class. The advantage of the method is thus that it has a straightforward
  interpretation. However, it does a poor job at preserving many of the
  properties of the original model.

- **Genealogical collapsing.** This method, introduced in [BALM17]_, aims at
  preserving properties of the genealogy of individuals. It usually
  does a better job at preserving the properties of the original model.
  One major drawback of the method, though, is that it lacks a clear
  interpretation. In particular, applying it to a survival matrix can yield a
  matrix with entries that are greater than one.

Which method is better will depend on the model at hand and on what one wants
to do with it. In general, if it can be used then genealogical collapsing
should be more useful.
"""

import warnings

import numpy as np
from matpopmod.model import MPM
import matpopmod.utils as ut


def collapsing_matrix(cv):
  r"""
  Given an iterable collapsing vector `cv` representing which classes
  should be merged together, returns the :math:`m \times n` matrix
  :math:`\boldsymbol \Phi = (\phi_{ij})` defined by:
  
  .. math::

    \phi_{ik} = \begin{cases}
      1 & \text{ if } k \text{ is a subclass of } i. \\
      0 & \text{ otherwise}.
    \end{cases}

  More specifically, `cv` should be an iterable representing a partition of
  :math:`\{0, \ldots, n-1\}` into *m* = `len(cv)` subclasses in such a way
  that `cv[i]` is the set of indices of the subclasses composing the collapsed
  class *i*, and :math:`\phi_{ik} = \mathbf{1}_{\{k \in \mathrm{cv}[i]\}}`.
  
  If `cv` does not represent a valid partition of :math:`\{0, \ldots, n-1\}`,
  ``ValueError`` is raised.

  The collapsing matrix makes it easy to sum over subclasses that have to
  be collapsed together. For instance, the vector :math:`\tilde{\mathbf{x}} =
  (x_i)` defined by :math:`x_i = \sum_{k \subset i} x_k` is
  :math:`\tilde{\mathbf{x}} = \boldsymbol \Phi \mathbf{x}` and the matrix
  :math:`\tilde{\mathbf{M}} = (\tilde{m}_{ij})` defined by
  :math:`\tilde{m}_{ij} = \sum_{k \subset i}\sum_{\ell \subset j} m_{k\ell}` is
  :math:`\tilde{\mathbf{M}} = \boldsymbol \Phi \mathbf{M}
  \boldsymbol\Phi^\top`.
  """
  m = len(cv)
  # Check that cv represents a partition of {0, ..., n-1}
  flat = [k for block in cv for k in block]
  flat.sort()
  n = len(flat)
  if flat != [k for k in range(n)]:
    raise ValueError("Incorrect collapsing vector.")
  aux = [[k in cv[i] for k in range(n)] for i in range(m)]
  return np.array(aux, dtype = float)


def individualistic_collapsing(m, cv):
  r"""
  Returns the individualistically collapsed version of `m`, i.e. the
  model whose projection matrix :math:`\hat{\mathbf{A}} = (\hat{a}_{ij})` is
  given by

  .. math::

    \hat{a}_{ij} =
    \frac{\sum\limits_{k \subset i} \sum\limits_{\ell \subset j} a_{k\ell} \,
    w_\ell}{\sum\limits_{\ell \subset j} w_\ell}

  where :math:`k \subset i` indicates that the (original) class *k* is a
  subclass of the (collapsed) class *i*. If the **A** = **S** + **F**
  decomposition is available, then this formula is applied separately
  to the matrices **S** and **F**.

  Specifying which classes should be merged together is done thanks to
  the collapsing vector `cv`, whose *i*-th entry is the list of subclasses
  of the collapsed class *i*. *The classes of a model should always be numbered
  from* :math:`0` *to* :math:`n - 1`.
  
  For instance, consider the model
  :data:`~matpopmod.examples.dipsacus_sylvestris` from the module
  :mod:`~matpopmod.examples`:

  .. plot::
    :include-source:

    >>> from matpopmod.examples import dipsacus_sylvestris
    >>> matpopmod.plot.life_cycle(dipsacus_sylvestris)

  To merge the two seed classes (0 and 1) into a single class and the
  three rosette classes (2--4) into another one, use


    >>> m = individualistic_collapsing(
    ...         dipsacus_sylvestris, [[0, 1], [2, 3, 4], [5]])
    >>> matpopmod.plot.life_cycle(m)

  .. plot::

    from matpopmod.examples import dipsacus_sylvestris
    from matpopmod.collapsing import individualistic_collapsing
    m = individualistic_collapsing(dipsacus_sylvestris, [[0, 1], [2, 3, 4], [5]])
    matpopmod.plot.life_cycle(m)

  Note that the metadata of the model are not copied.

  Individualistic collapsing guarantees that the growth rate and stable
  class distributions are preserved. However, most other descriptors are
  expected to be different (unless the classes that are collapsed together have
  identical reproductive values).


  >>> dipsacus_sylvestris.lmbd, m.lmbd
  (2.333880171440902, 2.3338801714408994)
  >>> dipsacus_sylvestris.T_a, m.T_a
  (2.9095973630611565, 2.3784561962530835)
  >>> dipsacus_sylvestris.R0, m.R0
  (14.375518834698335, 11.351604517163121)

  """
  Phi = collapsing_matrix(cv) 
  _, n = Phi.shape
  if n != m.dim:
    raise ValueError("Incorrect collapsing vector.")
  if m.split:
    S_hat = (Phi @ (m.S * m.w) @ Phi.T) / (Phi @ m.w)
    F_hat = (Phi @ (m.F * m.w) @ Phi.T) / (Phi @ m.w)
    return MPM(S = S_hat, F = F_hat)
  else:
    A_hat = (Phi @ (m.A * m.w) @ Phi.T) / (Phi @ m.w)
    return MPM(A = A_hat)


def genealogical_collapsing(m, cv):
  r"""
  Returns the genealogically collapsed version of `m`, i.e. the model whose
  projection matrix :math:`\mathbf{A}^\star = (a^\star_{ij})` is given by

  .. math::

    a^\star_{ij} = \frac{\sum\limits_{k \subset i} \sum\limits_{\ell \subset j}
    v_k \, a_{k\ell}\, w_\ell}{\left(\frac{\sum_{k \subset i}
    v_k w_k}{\sum_{k \subset i} w_k}\right)
    \sum\limits_{\ell \subset j} w_\ell} \, .

  See the documentation of :func:`individualistic_collapsing` for details
  about the notation and the argument `cv`.

  In addition to preserving the asymptotic growth rate and the stable class
  structure, genealogical collapsing preserves the reproductive values, the
  elasticities and the generation time :math:`T_a`. Overall, the descriptors of
  the genealogically collapsed model are expected to better match the
  descriptors of the original model than those of the individualistically
  collapsed one.

  >>> mi = individualistic_collapsing(
  ...          dipsacus_sylvestris, [[0, 1], [2, 3], [4], [5]])
  >>> mg = genealogical_collapsing(
  ...          dipsacus_sylvestris, [[0, 1], [2, 3], [4], [5]])
  >>> dipsacus_sylvestris.T_a, mi.T_a, mg.T_a
  (2.9095973630611565, 3.0291753555161596, 2.9095973630611573)
  >>> dipsacus_sylvestris.R0, mi.R0, mg.R0
  (14.375518834698335, 20.204098421369117, 14.211167697833941)

  However, a major shortcoming of genealogical collapsing is that the
  interpretation of the entries of the projection matrix is somewhat lost.
  In particular, it is possible for the sum of the columns of the survival
  matrix to exceed 1, contradicting their interpretation as survival
  probabilities. When this happens, a warning is issued and a model based
  on the projection matrix **A** only (that is, without a survival and
  fertility matrix) is returned. For instance, compare

  >>> m1 = genealogical_collapsing(
  ...          dipsacus_sylvestris, [[0, 1], [2, 3], [4], [5]])
  >>> m1.split
  True
  >>> m2 = genealogical_collapsing(
  ...          dipsacus_sylvestris, [[0, 1], [2, 3, 4], [5]])
  UserWarning: Genealogical collapsing yields survival
  probabilities > 1. A non-split model is returned.
  >>> m2.split
  False

  """
  Phi = collapsing_matrix(cv) 
  _, n = Phi.shape
  if n != m.dim:
    raise ValueError("Incorrect collapsing vector.")
  w_star = Phi @ m.w
  x = (Phi @ (m.v * m.w)) / w_star
  if m.split:
    vsw = ((m.S * m.w).T * m.v).T
    vfw = ((m.F * m.w).T * m.v).T
    S_star = (((Phi @ vsw @ Phi.T) / w_star).T / x).T
    try:
      ut.assert_substochastic(S_star)
      F_star = (((Phi @ vfw @ Phi.T) / w_star).T / x).T
      return MPM(S = S_star, F = F_star)
    except ut.InadequateMatrix:
      if ut._ISSUE_WARNINGS:
        warnings.warn("Genealogical collapsing yields survival "
          "probabilities > 1. A non-split model is returned.")
  vaw = ((m.A * m.w).T * m.v).T
  A_star = (((Phi @ vaw @ Phi.T) / w_star).T / x).T
  return MPM(A = A_star)


#  Finally, note that letting :math:`\boldsymbol \Phi`
#  be the :func:`collapsing_matrix` and letting :math:`\otimes`
#  and :math:`\oslash` denote NumPy's ``*`` and ``/`` operators, the
#  collapsed matrix :math:`\hat{\mathbf{A}}` can be expressed in matrix
#  form as
#
#  .. math::
#
#    \hat{\mathbf{A}} =
#    \big(\boldsymbol\Phi (\mathbf{A} \otimes \mathbf{w}) \boldsymbol\Phi^\top\big)
#    \;\oslash\; (\boldsymbol\Phi \mathbf{w}) \,.
#

