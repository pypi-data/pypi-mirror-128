"""
This module implements the class :class:`Trajectory`. Instances of this class
are returned by :meth:`MPM.trajectory <matpopmod.model.MPM.trajectory>` and
taken as argument by :func:`plot.trajectory <matpopmod.plot.trajectory>`.
"""

import math

import numpy as np
import matpopmod.utils as ut


class Trajectory:
  """
  High-level representation of population trajectories.

  The main purpose of this class is simply to bundle the various
  data needed to plot population trajectories. Thus, 
  :class:`Trajectory` objects are mostly meant to be passed around by the
  user, as in

  .. code-block::

    orca = matpopmod.examples.orcinus_orca
    traj = orca.trajectory([0, 10, 0, 0], t_max=100)
    matpopmod.plot.trajectory(traj)
  
  rather than manipulated directly. However, the interface of the class
  also makes it easy for users to use trajectories in numerical calculations.
  """

  def __init__(self, timescale, Y, model, stochastic=False):

    try:
      (n, ) = timescale.shape
    except:
      raise ValueError("Incorrect argument timescale: "
        f"expected a 1D NumPy array, got {timescale}.")

    try:
      nY, nClasses = Y.shape
      if nY != n:
        raise ValueError(
          f"timescale and Y have incompatible lengths ({n} vs {nY}).")
      if nClasses != model.dim:
        raise ValueError(
          "The number of classes of Y is not compatible with that of model.")
    except:
      raise ValueError("Incorrect argument Y:"
        f"expected a {n}x{model.dim} NumPy array, got {Y}.")

    timescale.flags.writeable = False
    self._timescale = timescale
    Y.flags.writeable = False
    self._Y = Y
    self._model = model
    self._stochastic = stochastic
    self._centered_Y = None

  @property
  def timescale(self):
    """
    The vector of times at which the population is observed.
    That is, ``timescale[k]`` is the absolute time corresponding to the
    *k*-th step of the trajectory.

    This is a read-only NumPy array. Use :meth:`set_timescale` to modify it.
    """
    return self._timescale

  @property
  def Y(self):
    """
    The 2D array of population vectors. That is, ``Y[k]`` is the population
    vector at time ``timescale[k]``.
    
    This is a read-only NumPy array. See :meth:`centered_Y`, 
    :meth:`rescaled_Y` and other methods below for common transformations
    of the population vector.
    """
    return self._Y

  @property
  def model(self):
    """
    The :class:`~matpopmod.model.MPM` associated with the trajectory (for
    stochastic trajectories, this is the matrix population model giving
    the expected value of the population vector).
    """
    return self._model

  @property
  def stochastic(self):
    """
    Whether the trajectory is a realization of a multitype Galton--Watson
    process, or simply the deterministic trajectory of the associated matrix
    population model.
    """
    return self._stochastic

  @property
  def centered_Y(self):
    r"""
    The trajectory minus its expected value, that is,

    .. math::

      \mathbf{Y}(t) - \mathbf{A}^{\!t\,} \mathbf{Y}(0).

    For deterministic trajectories, this is not relevant as it is always zero.
    For stochastic trajectories, this is what is known in the ecological
    literature as the *demographic stochasticity*.
    """
    if self._centered_Y is None:
      timescale = self.timescale
      EY = np.empty((len(timescale), self.model.dim))
      EY[0] = self.Y[0]
      # basic memoization
      POWER_OF_A = {}
      def aux_A_pow(dt):
        nonlocal POWER_OF_A
        try:
          return POWER_OF_A[dt]
        except KeyError:
          A_dt = np.linalg.matrix_power(self.model.A, dt)
          POWER_OF_A[dt] = A_dt
          return A_dt
      for k in range(len(timescale) - 1):
        dt = timescale[k + 1] - timescale[k]
        EY[k + 1] = aux_A_pow(dt) @ EY[k]
      self._centered_Y = self.Y - EY
    return self._centered_Y

  @property
  def rescaled_Y(self):
    r"""
    The trajectory rescaled by its (expected) order of magnitude, that is,
    
    .. math::

      \mathbf{Y}(t) \; / \; \lambda^t, 

    where :math:`\lambda` is the asymptotic growth rate (for stochastic
    trajectories, this is the expected asymptotic growth rate; trajectories
    that go extinct have an asymptotic growth rate of 0 and trajectories
    conditioned on not going extinct have a larger asymptotic
    growth rate).
    """
    # Legend has it that float division is slower than float multiplication.
    # However, I suspect it might be more precise to divide a large number
    # by another large one than to multiply it by a number close to zero.
    svect = self.model.lmbd ** self.timescale
    smat = svect.reshape((-1, 1)) @ np.ones((1, self.model.dim))
    return self.Y / smat

  @property
  def rescaled_centered_Y(self):
    r"""
    The fluctuations of the trajectory around its mean, rescaled by their
    expected order of magnitude:

    .. math::

      \big(\mathbf{Y}(t) - \mathbf{A}^{\!t\,} \mathbf{Y}(0)\big) \;/\; \lambda^t.
     
    """
    svect = self.model.lmbd ** self.timescale
    smat = svect.reshape((-1, 1)) @ np.ones((1, self.model.dim))
    return self.centered_Y / smat

  @property
  def second_order_Y(self):
    r"""
    The trajectory minus its (expected) first-order dynamics, that is,

    .. math::

      \mathbf{Y}(t) - \mathbf{v} \mathbf{Y}(0) \, \lambda^t \, \mathbf{w}.

    For deterministic trajectories, this shows the second-order dynamics, i.e.
    the dynamics associated with the largest subdominant eigenvalue(s).
    For stochastic trajectories, this mostly shows the fluctuations around
    the mean (because those are on the same scale as the first-order dynamics,
    whereas the second-order dynamics are on a smaller scale).
    """
    aux = (self.model.v @ self.Y[0]) * (self.model.lmbd ** self.timescale)
    first_order = aux.reshape((-1, 1)) @ self.model.w.reshape((1, -1))
    return self.Y - first_order

  @property
  def rescaled_second_order_Y(self):
    r"""
    The trajectory minus its first-order dynamics, rescaled by the order
    of magnitude of the second-order dynamics, that is,

    .. math::

      \big(\mathbf{Y}(t) - \mathbf{v} \mathbf{Y}(0) \,\lambda^t\, \mathbf{w}
      \big) \;/\; \tau^t, 

    where :math:`\tau`, if it exists and is non-zero, is the largest
    modulus of the subdominant eigenvalues (as in the definition of the
    damping ratio, :math:`\rho = \lambda / \tau`).

    With deterministic trajectories, this is useful to show the periodic
    component of the second-order dynamics.
    """
    dr = self.model.damping_ratio
    if math.isinf(dr):
      raise ValueError(
        "Cannot rescale the second-order dynamics (infinite damping ratio).")
    tau = self.model.lmbd / dr
    svect = tau ** self.timescale
    smat = svect.reshape((-1, 1)) @ np.ones((1, self.model.dim))
    return self.second_order_Y / smat

  def set_timescale(self, new_timescale):
    """
    Replaces :attr:`timescale` with `new_timescale`.
    """
    ut.assert_vector(new_timescale, len(self.timescale), "new_timescale")
    new_timescale.flags.writeable = False
    self._timescale = new_timescale

  def _get_Y(self, center = False, rescale = False, second_order = False):
    """
    Internal function to access the correct attribute 
    from boolean optional arguments. Used for plotting.
    """
    if center and second_order:
      raise ValueError("Cannot combine 'center' and 'second_order'")
    if rescale:
      if center:
        return self.rescaled_centered_Y
      elif second_order:
        return self.rescaled_second_order_Y
      else:
        return self.rescaled_Y
    else:
      if center:
        return self.centered_Y
      elif second_order:
        return self.second_order_Y
      else:
        return self.Y


"""
TEMPORARY

  pair of NumPy arrays `(t, n)` such that
  `n[k]` = :math:`\mathbf{n}(t_k)` is the population vector at
  time :math:`t_k` = `t[k]` (that is, `n[k,i]` is the abundance
  of class *i* at that time).

  If `second_order` is ``True``, then the first-order term will be
  substracted from the trajectory -- that is, the function will return

  .. math::

    \tilde{\mathbf{n}}(t) \;=\; \mathbf{n}(t) - \mathbf{v}\mathbf{n}(0) \,
    \lambda^t\, \mathbf{w}.

  using matplotlib.
"""

def compute_trajectory(model, n0, t_max, step=1):
  r"""
  Internal implementation of the method :meth:`~matpopmod.model.MPM.trajectory`
  of :class:`~matpopmod.model.MPM`. Refer to the documentation of that
  method for a more detailed description.

  - `model`: the :class:`~matpopmod.model.MPM` whose trajectory we want to
    compute.
  - `n0`: the initial population vector.
  - `t_max`: the maximal time.
  - `step`: the time-step of the trajectory.

  Returns a :class:`~matpopmod.trajectories.Trajectory`.
  """
  n0 = np.array(n0)
  ut.assert_vector(n0, model.dim, name = "n0")
  ut.assert_nonnegative(n0, name = "n0")
  ut.assert_positive_integer(step, name = "step")
  ut.assert_nonnegative_number(t_max, name = "t_max")
  timescale = np.arange(0, t_max + 1, step)
  Y = np.empty((len(timescale), model.dim))
  Y[0] = n0
  A_step = np.linalg.matrix_power(model.A, step)
  for k in range(len(timescale) - 1):
    Y[k + 1] = A_step @ Y[k]
  return Trajectory(timescale, Y, model) 


def compute_stochastic_trajectories(
      model, n0, t_max, reps, reproduction = "poisson", Z = None):
  r"""
  Internal implementation of the method
  :meth:`~matpopmod.model.MPM.stochastic_trajectories`
  of :class:`~matpopmod.model.MPM`. Refer to the documentation of that
  method for a more detailed description.

  - `model`: the :class:`~matpopmod.model.MPM` parametrizing the trajectories.
  - `n0`: the (deterministic) initial population vector.
  - `t_max`: the maximal time.
  - `reps`: the number of independent replicates.
  - `reproduction`: the offspring distribution. Should be either
    ``"poisson"`` or, for monotocous species, ``"bernoulli"``. Note that
    this is the law of the number of offspring in the biological sense,
    not in the "Galton--Watson" one. This argument is ignored if
    `Z` is supplied.
  - `Z`: the random variable such that
    :math:`\mathbf{Y}(t+1) =  Z(\mathbf{F}, \mathbf{S}, \mathbf{Y}(t))` if
    the **A** = **S** + **F** decomposition is available, and
    :math:`\mathbf{Y}(t+1) =  Z(\mathbf{A}, \mathrm{None}, \mathbf{Y}(t))`
    otherwise.


  Returns a list of :class:`~matpopmod.trajectories.Trajectory` objects.
  """
  n0 = np.array(n0)
  ut.assert_vector(n0, model.dim, name = "n0")
  ut.assert_nonnegative(n0, name = "n0")
  if n0.dtype != int: # I think this is equivalent to != np.int_
    raise ValueError(f"Incorrect argument n0: should be integer-valued")
  ut.assert_nonnegative_number(t_max, name = "t_max")
  ut.assert_positive_integer(reps, name = "reps")

  if Z is None:
      
    def poisson_reproduction(F, nt):
      return ut.rng.poisson(F @ nt)

    def bernoulli_reproduction(F_ber, nt):
      # A special format is used for the matrix fertility matrix
      # in order to factorize some of the calculations; see below.
      newborns = np.zeros(model.dim, dtype = int)
      for j in range(model.dim):
        newborns += ut.rng.multinomial(nt[j], F_ber[j])[:-1]
      return newborns

    if reproduction == "poisson":
      F_aux = model.F if model.split else model.A
      repro = poisson_reproduction
    elif reproduction == "bernoulli":
      F = model.F if model.split else model.A
      proba_repro = np.sum(model.F, axis =  0)
      if np.any(proba_repro > 1):
        raise ut.InadequateMatrix(
          ("Inadequate fertility matrix F for Bernoulli reproduction: "
           "some of the columns sum to more than 1.") if model.split else
          ("Inadequante projection matrix A for Bernoulli scheme: "
           "some of the columns sum to more than 1."))
      F_aux = np.vstack([F, (1 - proba_repro)]).T
      repro = bernoulli_reproduction
    else:
      raise ValueError(f"Incorrect argument reproduction = {reproduction}. "
        "Should be either 'poisson' or 'bernoulli'")

    if model.split:
      proba_survival = np.sum(model.S, axis =  0)
      S_aux = np.vstack([model.S, (1 - proba_survival)]).T

      def survival(S_aux, nt):
        # Again, using a special matrix S to factorize calculations
        survivors = np.zeros(model.dim, dtype = int)
        for j in range(model.dim):
          survivors += ut.rng.multinomial(nt[j], S_aux[j])[:-1]
        return survivors
      Z = lambda F_aux, S_aux, nt : repro(F_aux, nt) + survival(S_aux, nt)

    else:
      S_aux = None
      Z = lambda F_aux, S_aux, nt : repro(F_aux, nt)

  else: # i.e. if Z is specified
    if model.split:
      F_aux = model.F
      S_aux = model.S
    else:
      F_aux = model.A
      S_aux = None 

  trajectories = []
  timescale = np.arange(0, t_max + 1)  # Trajectories can safely have shared
                                       # timescales because they are immutable
  for k in range(reps):
    t = 0
    Y = np.zeros((t_max + 1, model.dim), dtype = int)
    Y[0] = n0
    while t < t_max and np.any(Y[t] > 0):
      Y[t + 1] = Z(F_aux, S_aux, Y[t])
      t += 1
    trajectories.append(Trajectory(timescale, Y, model, stochastic = True))

  return trajectories 

