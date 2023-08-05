"""
This module provides functions to plot various quantities associated
to matrix population models, including:

- The  :func:`life cycle<life_cycle>`  graph.
- The :func:`eigenvalues <eigenvalues>` of the projection matrix.
- Trajectories, both :func:`deterministic <trajectory>` and
  :func:`stochastic <multiple_trajectories>`.
- :func:`Genealogies <genealogies>` of individual-based simulations
  *(coming in v0.2.0)*.
- Various :func:`matrices <matrices>`.

By default, each function of this module will create a new figure when
called.  If you want to draw the life-cycle graph as a subplot of an existing
figure, you can do so by providing an existing matplolib :class:`Axes` with the
argument `ax`.

The matplotlib :class:`Axes` used to draw the figure will be returned.
This is useful if you want to combine plots or to if you want to customize
them beyond what is possible with the arguments of the functions; otherwise,
you can ignore it.

Note that, unless you are in a Jupyter / IPython notebook, after
calling a plotting function you need to call either :func:`show` or
:func:`savefig` to show (resp. save) the figure that was produced.
"""

import itertools
import collections
import operator
import warnings
import math

import numpy as np
import matpopmod.utils as ut

try:
  import matplotlib.pyplot as plt
  import matplotlib.patches as mpatches
  import matplotlib.path as mpath
  import matplotlib.transforms
  mPath = mpath.Path
  import matplotlib.colors as mcolors
  import matplotlib.cm
  from matplotlib.axes._base import _process_plot_format
except Exception as ex:
  print("The matplotlib package is required to use the module plot.")
  raise ex


# Fields from the metadata attribute of a MPM object that contain
# the names of the different classes of the model (by increasing priority)
_METADATA_FIELDS_CLASSNAMES = ("MatrixClassAuthor", "Classes")

##### MATPLOTLIB ALIASES
show = plt.show
savefig = plt.savefig


def colors_deep(n):
  if n <= 6:
    return ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974", "#64B5CD"]
  else :
    return ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
            "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

def colors_muted(n):
  if n <= 6:
    return ["#4878D0", "#6ACC64", "#D65F5F", "#956CB4", "#D5BB67", "#82C6E2"]
  else:
    return ["#4878D0", "#EE854A", "#6ACC64", "#D65F5F", "#956CB4",
            "#8C613C", "#DC7EC0", "#797979", "#D5BB67", "#82C6E2"]

def set_colors(ax, colors, n):
  if colors is None:
    pass
  elif colors == "deep":
    ax.set_prop_cycle(color = colors_deep(n))
  elif colors == "muted":
    ax.set_prop_cycle(color = colors_muted(n))
  elif colors in ('Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                  'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'):
    ax.set_prop_cycle(color = plt.cm.get_cmap(colors).colors)
  else:
    try:
      ax.set_prop_cycle(color = colors)
    except:
      raise ValueError(f"Invalid argument colors: {colors}")


def trajectory(traj, log = False, second_order = False,
               rescale = False, show_classes = False,
               stacked = False, show_period = False,
               colors = None, plot_style = None,
               show_legend = None, title = None, ax = None):
  r"""
  Plots the trajectory `traj`.
  The following plotting options are available:

  .. list-table::
    :widths: 15 85

    * - `log`
      - Whether to use a logarithmic scale for the *y*-axis. Not compatible
        with `stacked`. This will automatically fall back to using a "symlog"
        scale whenever the plot contains zero or negative values
        (as can happen with `show_classes` or `second_order`).
    * - `second_order`
      - Whether to plot the second order of the population dynamics, that is,

        .. math::

          \tilde{\mathbf{n}}(t) = \mathbf{n}(t) -
          \mathbf{v} \mathbf{n}(0) \lambda^t \mathbf{w} \, .

        This is useful, e.g, to study the transient regime.
    * - `rescale`
      - Whether to divide the population size by :math:`\lambda^t`. If
        `second_order` is set, it will be divided by :math:`|\lambda_2|^t`
        instead, where :math:`\lambda_2` is the maximum modulus of the
        subdominant eigenvalues instead (see e.g.
        :attr:`~matpopmod.model.MPM.damping_ratio`).

        This option can be used to illustrate the convergence to the steady
        regime (though the resulting plot will be less informative than the one
        obtained with `second_order`). Used in conjunction with `second_order`,
        it can be used to show the periodicity of the second-order
        oscillations.
    * - `show_classes`
      - .. rst-class:: nospaceafter

        Whether to display the abundance of each class or only the
        total population size, and which classes to show:

        * ``False`` --- plot the total population size.
        * ``True`` or ``"all"`` --- plot the abundance of each class separately
        * ``[i1, ..., ik]``  --- show classes :math:`i_1, \ldots, i_k`, where
          the classes are numbered from 0. It is possible to group classes.
          For instance, ``[0, [1, 3]]`` will plot two curves:
          the number of individuals in class 0 and the number of individuals
          in class 1 or 3.

    * - `stacked`
      - If `show_classes`, whether to display the abundance of
        each class as a separate curve or using a "stacked plot" (making it
        easier to track the total population size and the relative contributions
        of each class).
    * - `show_period`
      - Whether to show the period of second-order oscillations, if it exists.
    * - `colors`
      - The colors to use for the classes. Can be either a list of colors,
        combining any format known to matplotlib, as in

        .. code-block::

          colors = ["r", "##3333CC", "C2", (0, 153, 51)]

        or the name of a `matplotlib color palette
        <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_, such
        as ``"tab10"`` or ``"Paired"``. In addition to these, we
        provide two `Seaborn color palettes
        <https://seaborn.pydata.org/tutorial/color_palettes.html>`_:
        ``"muted"`` and ``"deep"``. The default, ``None``, is to use
        ``"muted"`` but let it be over-ridden by `plot_style`.

        For a more drastic relooking of the plot, see `plot_style`.
    * - `plot_style`
      - If provided, the name of the `style-sheet
        <https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html>`_
        to use for the plot. We recommend trying out ``"seaborn"`` and
        ``"ggplot"``. Unless it is ``None``, `colors` takes precedence
        over `plot_style` for the colors of the classes of the model.
    * - `show_legend`
      - Whether to display the name of each class on the plot.
        If so, the names given in the ``"Classes"`` (or, if absent,
        ``"MatrixClassAuthor"``) field of `model.metadata` will be used.

        Optionally, you can specify the position of the legend by using one of
        the string arguments supported by `matplotlib's loc parameter
        <https://matplotlib.org/stable/api/legend_api.html#matplotlib.legend.Legend>`_,
        e.g, ``"upper right"``. Otherwise, ``"best"`` will be used by default.
    * - `title`
      - The title of the plot.

  For further customization of the plot (changing axis labels, etc),
  you can work directly on the returned matplotlib :class:`Axes` object.
  """

  if log:
    if show_classes and stacked:
      raise ValueError("log is not compatible with stacked")

  model = traj.model
  timescale = traj.timescale

  if rescale:
    if second_order:
      Y = traj.rescaled_second_order_Y
      label_Y = (
        r"$(\mathbf{n}(t) - \langle \mathbf{v}, \mathbf{n}(0)\rangle"
        r"\; \lambda^t \; \mathbf{w}) \;/\; |\lambda_2|^t$"
        ) if show_classes else (
        r"$(n(t) - \langle \mathbf{v}, \mathbf{n}(0)\rangle"
        r"\; \lambda^t) \;/\; |\lambda_2|^t$")
    else:
      Y = traj.rescaled_Y
      label_Y = (r"$\mathbf{n}(t) \;/\; \lambda^t$"
        ) if show_classes else (
        r"$n(t) \;/\; \lambda^t$")
  else:
    if second_order:
      Y = traj.second_order_Y
      label_Y = (
        r"$\mathbf{n}(t) - \langle \mathbf{v}, \mathbf{n}(0)\rangle"
        r"\; \lambda^t \; \mathbf{w}$"
        ) if show_classes else (
        r"$n(t) - \langle \mathbf{v}, \mathbf{n}(0)\rangle"
        r"\; \lambda^t$")
    else:
      Y = traj.Y
      label_Y = "Class abundances" if show_classes else "Population size"

  if show_classes:
    if show_classes not in (True, "all"):
      try:
        if all(isinstance(i, int) for i in show_classes):
          Y = Y[:, show_classes]
        else:
          aux = np.empty((len(timescale), len(show_classes)))
          for i, x in enumerate(show_classes):
            if isinstance(x, int):
              aux[:, i] = Y[:, x]
            else:
              aux[:, i] = np.sum(Y[:, x], axis = 1)
          Y = aux
      except:
        raise ValueError(f"Invalid argument show_classes: {show_classes})")
    number_colors = Y.shape[1]
  else:
    Y = np.sum(Y, axis = 1)
    number_colors = 1

  log_or_symlog = "symlog" if np.any(Y <= 0) else "log"

  if stacked:
    if np.any(Y < 0):
      raise ValueError("Cannot use a stacked plot with negative values.")

  actually_show_period = False
  if show_period:
    if model.second_order_period is np.nan: # /!\ np.nan == np.nan is False
      if ut._ISSUE_WARNINGS:
        warnings.warn("No second-order oscillations, ignoring show_period.")
    else:
      actually_show_period = True

  def aux_plot(ax):
    if log:
      plt.yscale(log_or_symlog)
    ax.set_ylabel(label_Y)
    if show_classes and stacked:
      handles = ax.stackplot(timescale, Y.T)
    else:
      handles = ax.plot(timescale, Y)
    if actually_show_period:
      for k in range(1, int(timescale[-1] / model.second_order_period) + 1):
        ax.axvline(x=k*model.second_order_period, lw=1, ls=":", color="#808080")
    ax.set_xlabel("time $t$")
    ax.set_xlim(timescale[0], timescale[-1])
    if title is not None:
      ax.set_title(title)
    if show_legend and show_classes:
      all_labels = None
      for key in _METADATA_FIELDS_CLASSNAMES:
        if key in model.metadata:
          all_labels = model.metadata[key]
      if show_classes not in (True, "all") and all_labels is not None:
        if all(isinstance(i, int) for i in show_classes):
          labels = [all_labels[i]
                    for i in range(1, len(all_labels)) if i in show_classes]
        else:
          labels = []
          for i, x in enumerate(show_classes):
            if isinstance(x, int):
              labels.append(str(x))
            else:
              try:
                labels.append(str(x)[1:-1])
              except:
                raise ValueError("Problem with argument show_classes: "
                  f"could not figure out how to label the composite class {x}.")
      else:
        labels = all_labels
      if labels is not None:
        if isinstance(show_legend, str):
          allowed_locs = ['best', 'upper right', 'upper left', 'lower left',
            'lower right', 'right', 'center left', 'center right',
            'lower center', 'upper center', 'center']
          if show_legend in allowed_locs:
            ax.legend(reversed(handles), reversed(labels), loc = show_legend)
          else:
            raise ValueError(f"Unknown value of show_legend: {show_legend}")
        else:
          ax.legend(reversed(handles), reversed(labels), loc = "best")
    return handles

  if plot_style is None:
    if ax is None:
      _, ax = plt.subplots()
    set_colors(ax, colors if colors is not None else "muted", number_colors)
    aux_plot(ax)
  else:
    try:
      with plt.style.context(plot_style):
        if ax is None:
          _, ax = plt.subplots()
        set_colors(ax, colors, number_colors)
        aux_plot(ax)
    except OSError:
      raise ValueError(f"Invalid argument plot_style: {plot_style}")

  return ax


def _short_representation(classes):
  if classes == "all":
    return "all"
  else:
    if len(classes) == 1:
      return f"Class {classes[0]}"
    else:
      ranges = []
      for _, g in itertools.groupby(enumerate(classes), lambda x : x[0] - x[1]):
        group = list(map(int, map(operator.itemgetter(1), g)))
        if group[0] == group[-1]:
          ranges.append(f"{group[0]}")
        else:
          ranges.append(f"{group[0]}-{group[-1]}")
    return "Classes " + ", ".join(ranges)


def multiple_trajectories(trajs, classes = "all",
      log=False, center = False, rescale = False, second_order = False,
      alpha=0.1, traj_style = "default",
      show_expectation = True, show_average = False,
      show_quantiles = False, quantiles = (10, 90), show_std = False,
      plot_style = None, title = None, ax = None):
  r"""
  Plots the trajectories contained in `trajs`, overlaying them.
  This is especially useful to show several realizations of stochastic
  trajectories, for instance:
  
  .. plot::
    :include-source: 

    orcas = mpm.examples.orcinus_orca
    trajs = orcas.stochastic_trajectories(
      n0=[10, 0, 0, 0],
      t_max=100,
      reps=1000,
      reproduction="bernoulli")
    mpm.plot.multiple_trajectories(trajs)

  The following plotting options are available:

  .. list-table::
    :widths: 15 85

    * - `classes`
      - The classes to plot, as a list of integers from 0 to *n*-1. The
        abundances of the classes will be summed: for instance, ``[0, 1]``
        will plot the number of individuals that are in class 0 or 1.
        The default, ``"all"``, is to plot the total population size.
    * - `log`
      - Whether to use a logarithmic scale for the *y*-axis.
        A "symlog" scale will be used if one of the trajectories contains zeros
        or negative values.
    * - `center`
      - Whether to subtract the expected value of each trajectory, so as
        to show only their stochastic component.
    * - `rescale`
      - Whether to rescale the trajectories, see :func:`trajectory`.
    * - `second_order`
      - Whether to subtract the first-order term of each trajectory, see
        :func:`trajectory`.
    * - `alpha`
      - The opacity of each trajectory, between 0 and 1.
    * - `traj_style`
      - The color and style of each trajectory, either as a matplotlib
        `fmt` string or, for more flexibility, as a dictionary of keyword
        arguments. Defaults to thin solid black lines.
    * - `show_expectation`
      - Whether to show the expected value of the trajectories. Can only
        be used if all trajectories correspond to the same model. If ``True``,
        a solid red line will be used. If a matplotlib `fmt` string or
        a dictionary, will be used to set the style and color of
        the curve.
    * - `show_average`
      - Whether to show the empirical average of the plotted trajectories.
        If ``True``, a solid purple line will be used. Can be a matplotlib
        `fmt` string or a dictionary to set the style and color of the curve.
    * - `show_quantiles`
      - Whether to show the empirical quantiles of the plotted trajectories.
        If ``True``, dashed red lines will be used. Can be a matplotlib
        `fmt` string or a dictionary to set the style and color of the curve.
    * - `quantiles`
      - If `show_quantiles`, which quantiles should be displayed, as a
        list of integers between 0 and 100. The default, ``(10, 90)``, is to
        show the 10% and 90% quantiles.
    * - `show_std`
      - Whether to show the average +/- the empirical standard deviation of the
        plotted trajectories. If ``True``, dotted red lines will be used.
        Can be a matplotlib `fmt` string or a dictionary to set the style and
        color of the curve.
    * - `plot_style`
      - If provided, the name of the `style-sheet
        <https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html>`_
        to use for the plot; see :func:`trajectory`.
    * - `title`
      - The title of the plot.

  """
  try:
    m = trajs[0].model
  except IndexError:
    raise ValueError("You need to provide at least one trajectory")
  except:
    raise ValueError("Incorrect argument trajs: should be "
      f"a list of trajectories, got {trajs}.")

  same_model = all(t.model == m for t in trajs)
  if not same_model:
    if ut._ISSUE_WARNINGS:
      warnings.warn(
        "Not all trajectories plotted together correspond to the same model")

  if not classes == "all":
    if not same_model:
      raise ValueError("Cannot use a value of classes different from 'all' "
        "when plotting trajectories corresponding to different models.")
    if any(i < 0 or i >= m.dim for i in classes):
      raise ValueError("Invalid argument classes: the classes should be "
        "represented by integers between 0 and n - 1.")

  if plot_style is None:
    if ax is None:
      _, ax = plt.subplots()
  else:
    try:
      with plt.style.context(plot_style):
        if ax is None:
          _, ax = plt.subplots()
    except OSError:
      raise ValueError(f"Invalid argument plot_style: {plot_style}")
    
  def aux_set_sty(default, sty, name):
    if sty == True or sty == "default":
      return default
    else:
      try:
        if isinstance(sty, str):
          linestyle, marker, color = _process_plot_format(sty)
          return {"linestyle": linestyle, "marker": marker, "color": color}
        else:
          return sty
      except:
        raise ValueError(f"Invalid style for {name}: {sty}.")

  tj_sty = aux_set_sty(
    {"color": "k", "linestyle": "solid", "linewidth": 0.5},
    traj_style, "traj_style")

  plotted_Y = []
  t_min, t_max = float("+inf"), float("-inf")
  log_or_symlog = "log"
  for t in trajs:
    Y = t._get_Y(center, rescale, second_order)
    if classes == "all":
      Y = np.sum(Y, axis = 1) 
    else:
      Y = np.sum(Y[:, classes], axis = 1)
    if log:
      if np.any(Y <= 0):
        log_or_symlog = "symlog"
    ax.plot(t.timescale, Y, alpha = alpha, **tj_sty)
    plotted_Y.append(Y)
    t_min = min(t_min, t.timescale[0])
    t_max = max(t_max, t.timescale[-1])

  ax.set_xlabel("time $t$")
  ax.set_xlim(t_min, t_max)

  classes_lab = _short_representation(classes)
  if classes_lab == f"{0}-{m.dim-1}" or classes_lab == "all":
    classes_lab = "Population size"
  if rescale:
    if center:
      suffix = f" (centered and rescaled)"
    elif second_order:
      suffix = f" (second order rescaled)"
    else:
      suffix = f" (rescaled)"
  else:
    if center:
      suffix = f" (centered)"
    if second_order:
      suffix = f" (second order)"
    else:
      suffix = ""
  ax.set_ylabel(classes_lab + suffix)

  if log:
    plt.yscale(log_or_symlog)

  if (show_average or show_quantiles or show_std or show_expectation):
    time_ref = trajs[0].timescale
    same_timescale = all(np.array_equal(t.timescale, time_ref) for t in trajs)

  shared_error_msg = ("Cannot plot {} for trajectories defined on "
    "different timescales. See common_timescale to put the trajectories "
    "on the same timescale.")

  if show_average:
    if not same_timescale:
      raise ValueError(shared_error_msg.format("the mean"))
    avg_sty = aux_set_sty(
      {"color": "C4", "linestyle": "solid"},
      show_average, "show_average")
    # works because we only do linear transformations to get plotted_Y
    Y_mean = np.mean(plotted_Y, axis = 0)
    ax.plot(t.timescale, Y_mean, **avg_sty)

  if show_std:
    if not same_timescale:
      raise ValueError(shared_error_msg.format("the standard deviation"))
    std_sty = aux_set_sty(
      {"color": "C3", "linestyle": "dotted", "linewidth": 1},
      show_std, "show_std")
    Y_mean = np.mean(plotted_Y, axis = 0)
    Y_std = np.std(plotted_Y, axis = 0)
    ax.plot(t.timescale, Y_mean + Y_std, **std_sty)
    ax.plot(t.timescale, Y_mean - Y_std, **std_sty)

  if show_quantiles:
    if not same_timescale:
      raise ValueError(shared_error_msg.format("the quantiles"))
    quant_sty = aux_set_sty(
      {"color": "C3", "linestyle": "dashed", "linewidth": 1},
      show_quantiles, "show_quantiles")
    quants = np.percentile(plotted_Y, quantiles, axis = 0)
    for Yquant in quants:
      ax.plot(t.timescale, Yquant, **quant_sty)

  if show_expectation:
    if not same_timescale:
      raise ValueError(shared_error_msg.format("the expected value"))
    if not same_model:
      raise ValueError("Cannot plot the expected value "
        "for trajectories corresponding to different models.")
    expec_sty = aux_set_sty(
      {"color": "C3", "linestyle": "solid"},
      show_expectation, "show_expectation")

    n0 = np.mean([tj.Y[0] for tj in trajs], axis = 0)
    T = t_max - t_min
    et = m.trajectory(n0, t_max = T)
    if t_min != 0:
      et.set_timescale(et.timescale + t_min)
    expec_Y = et._get_Y(center, rescale, second_order)
    expec_Y = (np.sum(expec_Y, axis = 1) if classes == "all" else
              np.sum(expec_Y[:, classes], axis = 1))
    ax.plot(et.timescale, expec_Y, **expec_sty)

  return ax



def eigenvalues(model, log=False,
                grid_slices=16, grid_circles=4, grid_radius="auto",
                style_eig=None, style_grid=None, title=None, ax=None):
  r"""
  Plots the eigenvalues of the projection matrix of `model` in the complex
  plane. Non-simple eigenvalues are annotated with their algebraic multiplicity.

  .. list-table::
    :widths: 15 85

    * - `log`
      - Whether to use a logarithmic scale for the modulus in polar coordinates.
    * - `grid_slices`
      - The number of "slices" of the polar grid. The default,
        16, corresponds to slices of
        :math:`2\pi / 16 \, \mathrm{rad} = 22.5^\circ`.
    * - `grid_circles`
      - The number of concentric circles of the polar grid.
    * - `grid_radius`
      - The radius of the polar grid. The default, ``"auto"``, is to use *λ*.
    * - `style_eig`
      - The dictionary of styling elements to use to plot the eigenvalues.
    * - `style_grid`
      - The dictionary of styling elements to use for the polar grid.
    * - `title`
      - The title of the plot.
  """

  if ax is None:
    _, ax = plt.subplots()

  ax.set_aspect("equal")

  eigenval = list(frozenset(model.eigenvalues))
  multiplicity = collections.Counter(model.eigenvalues)

  eig_style = dict(color='k')
  if style_eig is not None:
    eig_style.update(style_eig)

  def modified_log_transform(a, b, log):
    def aux_log(x):
      if log:
        if x < -ut._ABS_TOL:
          raise ValueError(f"x = {x} < 0")
        elif x < 0:
          return 0
        elif x < a:
          return x / (a * math.log(b))
        else:
          return (1 + math.log(x / a)) /  math.log(b)
    if log:
      return aux_log
    else:
      return lambda x: x

  if grid_radius == "auto":
    mx = model.lmbd
  elif grid_radius > 0:
    mx = grid_radius
  else:
    raise ValueError(f"Invalid argument grid_radius: {grid_radius}")

  a = min(min([abs(x) for x in model.eigenvalues if abs(x) > ut._ABS_TOL]),
          mx * 2**(-grid_circles + 1))

  f = np.vectorize(modified_log_transform(a, 2, log))
  fmx = f(mx)

  # Plot the grid
  grid_style = dict(color='k', alpha=0.5, linewidth=0.5, linestyle=':')
  if style_grid is not None:
    grid_style.update(style_grid)
  if grid_circles:
    if log:
      ticks = [f(mx / 2**k) for k in range(grid_circles)]
    else:
      ticks = np.linspace(0, mx, grid_circles + 1)
    for t in ticks:
      ax.add_patch(mpatches.Circle([0,0], t, fc='none', **grid_style))
  if grid_slices:
    ticks_angles = np.linspace(0, 2*np.pi, grid_slices + 1)
    for t in ticks_angles:
      ax.plot([0, fmx*np.cos(t)], [0, fmx*np.sin(t)], **grid_style)

  # Plot the eigenvalues
  if log:
    abs_eig = np.abs(eigenval)
    angle_eig = np.angle(eigenval)
    X = np.real(f(abs_eig) * np.exp(1j * angle_eig))
    Y = np.imag(f(abs_eig) * np.exp(1j * angle_eig))
  else:
    X, Y = np.real(eigenval), np.imag(eigenval)

  ax.scatter(X, Y, **eig_style)
  for x,y in zip(*(X, Y)):
    ax.plot([0, x], [0, y], **eig_style)

  lim = fmx if mx > model.lmbd else 1.1 * f(model.lmbd)
  ax.set(xlim=[-lim, lim], ylim=[-lim, lim])
  if log:
    ax.set_xticks(ticks)
    ax.set_xticks([-fmx / 2], minor=True)
    r = r"\lambda" if mx == model.lmbd else "R"
    ax.set_xticklabels([f"\n${r}$ = {mx}"], minor = True)
    ax.tick_params(which='minor', length=0)
    ticklabs = ([f"${r}$"] +
      [f"$\\frac{{{r}}}{{{int(2**k)}}}$" for k in range(1, grid_circles)])
    ax.set_xticklabels(ticklabs)
    ax.set_yticks([])
    ax.set_yticks([], minor=True)
  else:
    ax.set(xlabel="Real", ylabel="Imaginary")

  for e, n in multiplicity.items():
    if n > 1:
      if e == model.lmbd and mx == model.lmbd:
        lim = fmx if mx > model.lmbd else 1.15 * f(model.lmbd)
        ax.set(xlim=[-lim, lim], ylim=[-lim, lim])
      a = np.angle(e) + np.pi/4
      r = fmx*0.1
      if log:
        plt.text(np.real(f(np.abs(e)) * np.exp(1j * np.angle(e))) + r*np.cos(a),
                 np.imag(f(np.abs(e)) * np.exp(1j * np.angle(e))) + r*np.sin(a),
                 n, verticalalignment='center', horizontalalignment='center')
      else:
        plt.text(np.real(e) + r*np.cos(a), np.imag(e) + r*np.sin(a),
                 n, verticalalignment='center', horizontalalignment='center')

  if title is not None:
    ax.set_title(title)

  return ax



##### LIFE-CYCLE GRAPH ########################################################

def _edge_style(model, i, j, style_survival, style_mixed, style_fertilities):
  """
  Get the style (linestyle, color, ...) that should be applied to the
  edge `(i, j)` in `model`. Returns the style of the body of the edge and
  of its head.
  """
  arrow_prop = {"lw":1, "ec":"none", "fc":"k",
                "arrowstyle":"<|-", "mutation_scale":10}
  line_prop = {"lw":1, "fc":"none", "ec":"k"}
  style = style_survival # draw edges as survival by default
  if model.split:
    if model.F[i, j] != 0:
      if model.S[i, j] != 0:
        style = style_mixed
      else:
        style = style_fertilities
  try:
    arrow_prop.update(style)
    line_prop.update(style)
    for k in ["arrowstyle", "mutation_scale"]:
      if k in line_prop:
        del line_prop[k]
  except ValueError:
    linestyle, _, color = _process_plot_format(style)
    arrow_prop.update({"fc": color if color is not None else "k",
                       "ec": color if color is not None else "k"})
    line_prop.update({"linestyle": linestyle, "fc": "none",
                      "ec": color if color is not None else "k"})

  if (i-j) > 1 and model.A[i,j] != 0 and model.A[j,i] !=0:
    if model.split and (style_fertilities != style_survival and j < i and
         (model.F[j,i] != 0 and model.S[i,j] != 0) or
         (model.F[i,j] != 0 and model.S[j,i] != 0)) :
      line_prop.update({"linestyle": (0, (4, 4))})

  arrow_prop["linestyle"] = "-"
  line_prop["capstyle"] = "round"
  line_prop["fc"] = "none"

  return line_prop, arrow_prop


def _split_cubic_bezier(control_points, z):
  """
  Splits a cubic bezier curve in two cubic bezier curves at
  curvilinear abscissa `z` in (0,1). Returns the control points
  of the two new curves.
  """
  if z < 0 or z > 1:
    raise ValueError
  P = np.array(control_points)
  split_point = z**3*P[3]-3*z**2*(z-1)*P[2]+3*z*(z-1)**2*P[1]-(z-1)**3*P[0]
  points_1 = [P[0],
              z*P[1]-(z-1)*P[0],
              z**2*P[2]-2*z*(z-1)*P[1]+(z-1)**2*P[0],
              split_point]
  points_2 = [split_point,
              z**2*P[3]-2*z*(z-1)*P[2]+(z-1)**2*P[1],
              z*P[3]-(z-1)*P[2],
              P[3]]
  return points_1, points_2


def _draw_edge(ax, from_vertex, to_vertex, vertex_positions,
               r, arrow_prop=None, line_prop=None, label=None,
               reverse_exists=False):
  """Draw an edge from a vertex to another in the lifecycle graph."""
  if arrow_prop is None:
    arrow_prop = {"ec":"none", "fc":"k", "arrowstyle":"<|-", "mutation_scale":10}
  if line_prop is None:
    line_prop = {"lw": 1, "fc": "none", "ec":"k", "capstyle": "round"}

  x = vertex_positions[from_vertex]
  y = vertex_positions[to_vertex]
  distance = abs(from_vertex-to_vertex)
  left = to_vertex < from_vertex
  cubic_bezier = [mPath.MOVETO, mPath.CURVE4, mPath.CURVE4, mPath.CURVE4]
  text_color = line_prop["ec"] if "ec" in line_prop else "k"
  text_patch = None

  # The location of the split between the arrow and line patches
  # in curvilinear coordinates.
  split_loc = 0.02

  #---- adjacent nodes -----
  if distance == 1:
    split_loc = 0.1
    if reverse_exists:
      a1 = 11*np.pi/12 if left else 23*np.pi/12
      a2 = np.pi/12 if left else 13*np.pi/12
    else:
      a1, a2 = (np.pi, 0) if left else (0, np.pi)
    points = [[x + 1.1*r*np.cos(a1), 0.5 + 1.1*r*np.sin(a1)],
              [y + 1.1*r*np.cos(a2), 0.5 + 1.1*r*np.sin(a2)]]
    points_arrow = [x.copy() for x in points]
    points_line = [x.copy() for x in points]
    split_x = points[0][0] + split_loc*(points[1][0]-points[0][0])
    points_line[0][0] = split_x
    points_arrow[1][0] = split_x

    if label is not None:
      text_patch = ax.text((points[0][0] + points[1][0])/2,
                     (points[0][1] + points[1][1])/2 - .2*(-r if left else r),
                     label,
                     color=text_color,
                     horizontalalignment='center',
                     verticalalignment=('bottom' if left else 'top'))
    arrow_patch = mpatches.FancyArrowPatch(
      path=mPath(points_arrow, [mPath.MOVETO, mPath.LINETO]),
      zorder=1, **arrow_prop)
    line_patch = mpatches.PathPatch(
      path=mPath(points_line, [mPath.MOVETO, mPath.LINETO]),
      zorder=0, **line_prop)

  else:
    #---- self-loop -----
    if distance == 0:
      a1 = 10*np.pi/6
      a3 = 8*np.pi/6
      points = [(x + 1.1*r*np.cos(a1), 0.5 + 1.1*r*np.sin(a1)),
                (x + 3*r*np.cos(a1), 0.5 + 3*r*np.sin(a1)),
                (x + 3*r*np.cos(a3), 0.5 + 3*r*np.sin(a3)),
                (y + 1.1*r*np.cos(a3), 0.5 + 1.1*r*np.sin(a3))]
      points_arrow, points_line = _split_cubic_bezier(points, split_loc)

      if label is not None:
        text_patch = _label_cubic(points, label, text_color, ax, va="self-loop")

    #---- other arrows -----
    else:
      p = distance/(len(vertex_positions)-1)
      a1 = (3 - 2*(1-p)*(-1 if left else 1))*np.pi/6
      a2 = (3 + 2*(1-p)*(-1 if left else 1))*np.pi/6
      points = [(x + 1.1*r*np.cos(a1), 0.5 + 1.1*r*np.sin(a1)),
                (x + 0.5*p*np.cos(a1), 0.5 + 0.5*p*np.sin(a1)),
                (y + 0.5*p*np.cos(a2), 0.5 + 0.5*p*np.sin(a2)),
                (y + 1.1*r*np.cos(a2), 0.5 + 1.1*r*np.sin(a2))]

      if label is not None:
        vertical_alignment = "bottom"
        if reverse_exists:
          line_prop["capstyle"] = "butt"
          if left:
            vertical_alignment = "top"
            label += "→"
          else:
            label =  "←" + label
        text_patch = _label_cubic(points, label, text_color, ax,
                                  va=vertical_alignment)

      points_arrow, points_line = _split_cubic_bezier(points, split_loc)
      if reverse_exists:
        points_line, _ = _split_cubic_bezier(points_line, 1-2*split_loc)

    line_patch = mpatches.PathPatch(
      path=mPath(points_line, cubic_bezier),
      zorder=0, **line_prop)
    arrow_patch = mpatches.FancyArrowPatch(
      path=mPath(points_arrow, cubic_bezier),
      zorder=1, **arrow_prop)

  ax.add_patch(arrow_patch)
  ax.add_patch(line_patch)

  if text_patch is not None:
    return (line_patch, arrow_patch, text_patch)
  return (line_patch, arrow_patch)

def _draw_vertices(ax, vertex_positions, labels, r=None,
                   node_colors="k", fill_nodes=False, node_fontsize="adaptive"):
  """ Draw the vertices of the life-cycle graph."""
  N = len(vertex_positions)
  patches = []
  if r is None:
    r = abs(np.min(vertex_positions)-np.max(vertex_positions))/(2.5*N)
  try:
    edge_colors = [node_colors[i] for i in range(N)]
  except IndexError:
    edge_colors = [node_colors]*N
  try:
    fill_colors = [
      "none" if not fill_nodes[i] else edge_colors[i] for i in range(N)]
  except (TypeError, IndexError):
    fill_colors = [
      "none" if not fill_nodes else edge_colors[i] for i in range(N)]
  for n, x in enumerate(vertex_positions):
    circle = mpatches.Circle((x, 0.5), r, lw=1,
                    facecolor=fill_colors[n], edgecolor=edge_colors[n])
    ax.add_patch(circle)
    if _is_dark(fill_colors[n]):
      label_color = "w"
    else:
      label_color = "k"
    if node_fontsize == "adaptive":
      if all(len(str(l)) == 1 for l in labels if not "$" in str(l)):
        node_fontsize = 16
      else:
        node_fontsize = 14
    text = ax.text(x, 0.5 - 0.1*r,
                   labels[n],
                   fontdict = {'family': 'monospace', 'color':  label_color,
                               'weight': 'normal', 'size': node_fontsize},
                   horizontalalignment='center',
                   verticalalignment='center')
    patches.append(circle)
    patches.append(text)
  return patches

def _label_cubic(points, text, color, ax, t=0.5, va='bottom'):
  """
  Label a cubic bezier curve defined by `points` with `text` at the
  curvilinear abscissa `t` on the matplotlib axis object `ax` with
  vertical alignment `va`.
  """
  P = lambda t, a, b, c, d : a*(1-t)**3+3*b*(1-t)**2*t+3*c*(1-t)*t**2+d*t**3
  ty = P(t, *[y for _, y in points])
  tx = P(t, *[x for x, _ in points])
  if va == "top":
    ty -= 0.01
  elif va == "self-loop":
    ty -= 0.03
    va = "top"
  txt = ax.text(tx, ty, text, color = color,
                zorder=2,
                bbox = dict(boxstyle="round4, pad=0.3", color="w"),
                horizontalalignment="center",
                verticalalignment=va)
  return txt

def _parse_classnames(class_names, ignore_if_startswithnumber=True):
  """
  Extract unique labels for the node of the life-cycle graph, directly
  from the names of the classes.

  The first letter of each class is used. If there are ambiguities, the
  second letter is added. If there are still ambiguities, a number is
  used instead of the second letter.

  If `ignore_if_startswithnumber` is true (default), the index of
  the class will be used for classes whose name starts with a numerical
  character.

  Return two lists: the list of labels and that of legends.
  """

  letters = []
  letters_2 = []
  legends = []
  labels = []

  for x in class_names:
    if len(x.split(":", 1)) == 2 and len(x.split(":", 1)[0].strip()) <= 2:
      letter, legend = x.split(":", 1)
    elif len(x.split("(", 1)) == 2 and len(x.split("(", 1)[0].strip()) <= 2:
      letter, legend = x.split("(", 1)
    elif len(x.split(" ", 1)) == 2 and len(x.split(" ", 1)[0].strip()) <= 2:
      letter, legend = x.split(" ", 1)
    else:
      letter, legend = x[0], x

    clean = lambda s: "".join(filter(str.isalnum, s.strip()))
    letters.append(clean(letter))
    if len(clean(legend)) > 1:
      letters_2.append(clean(letter) + clean(legend)[1])
    else:
      letters_2.append(clean(letter) + " ")
    legends.append(legend.strip())

  count = collections.Counter(itertools.chain(letters, letters_2))
  current = {x:0 for x in letters}

  # For letters that are found multiple times, try to use
  # the second letter; if that does not work, use a number
  for letter, letter_2 in zip(letters, letters_2):
    if count[letter] == 1:
      labels.append(letter)
    elif count[letter_2] == 1:
      labels.append(letter_2)
    else:
      current[letter] += 1
      labels.append("{}{}".format(letter, current[letter]))

  if ignore_if_startswithnumber:
    legends = [leg if (lab and not lab[0].isnumeric()) else cn
      for n, (lab,leg,cn) in enumerate(zip(labels, legends, class_names))]
    labels = [lab if (lab and not lab[0].isnumeric()) else n
      for n, lab in enumerate(labels)]
  return labels, legends


def _label_classes(node_labels, model):
  """Extract class labels and legends from a model."""
  class_names = None
  if node_labels == 'numbers':
    labels = ["{}".format(n) for n in range(model.dim)]
    legends = None
  elif node_labels == 'none' or node_labels is None:
    labels, legends = None, None
  else:
    if node_labels == 'auto':
      for key in _METADATA_FIELDS_CLASSNAMES:
        if key in model.metadata:
          class_names = model.metadata[key]
      if class_names is not None:
        labels, legends = _parse_classnames(class_names)
      else:
        labels = ["{}".format(n) for n in range(model.dim)]
        legends = None
    else:
      if all(":" in l for l in node_labels):
        labels = [l.split(":", 1)[0].strip() for l in node_labels]
        legends = [l.split(":", 1)[1].strip() for l in node_labels]
      else:
        labels, legends = node_labels, None

  return labels, legends

def _is_dark(color):
  r"""
  Whether a color is "dark" by (1) converting it to gray using
  the so-called luminosity method (where RGB components are weighted
  by their wavelength and average) and (2) using an arbitrary threshold.
  """
  if color == "none":
    return False
  (r, g, b) = tuple(mcolors.to_rgb(color))
  gray = 0.299 * r + 0.587 * g  + 0.114 * b
  return gray < 0.75 # completely arbitrary threshold.


def life_cycle(model, node_labels="auto", edge_labels="{:.2f}",
               fertilities="C3-", survival="k-", mixed="C4-",
               node_colors="k", fill_nodes=False, node_size=0.7,
               node_fontsize="adaptive", show_legend=False,
               title=None, ax=None):
  r"""
  Plots the life-cycle graph of the :class:`~matpopmod.MPM` `model`.
  The following options are available for customization:

  .. list-table::
    :widths: 15 85

    * - `node_labels`
      - .. rst-class:: nospaceafter

        The labels to use for the classes, using one of the
        following:

        * ``None`` or ``"none"`` --- do not display any label.
        * ``"numbers"`` --- use the indices of the classes.
        * ``"auto"`` (default) --- determine the labels automatically from
          the ``"Classes"`` (or ``"MatrixClassAuthor"``) field of
          ``model.metadata``. If neither of those fields exists, numbers
          will be used.
        * `custom` --- the list of labels to use. If *every* label
          contains a semicolon, then only the parts that precede those
          semicolons will be used as labels; the rest will be used in the
          legend.  Otherwise, the whole entries will be used as labels and
          there will be no legend.
    * - `edges_labels`
      - The format of the weight of the edges, as a Python format string. The
        default, ``"{:.2f}"``, stands for floating point with two decimals. If
        ``None`` is given, then the edges will not be labeled. Trailing zeros are
        removed for multiples of ten.
    * - `fertilities`
      - The line color and style to use for fertilities, either
        as a matplotlib format string or, for more control, as a dictionary of
        arguments. For instance, ``"r--"`` is equivalent to ``{"color" : "r",
        "linestyle": "--"}`` and stands for "red dashed". Defaults to solid red.
    * - `survival`
      - The line color and style to use for survival transitions.
        Defaults to solid black.
    * - `mixed`
      - The line color and style for mixed (= survival or fertility)
        transitions. Default to solid purple.
    * - `node_colors`
      - List of colors to use for each node. If a single value
        is given, it will be applied to all nodes. Defaults to black.
    * - `fill_nodes`
      - List of booleans indicating whether each node should be
        filled. If a single boolean is given, it will be used for every node.
    * - `size`
      - The size of nodes, in inches. Defaults to 0.7. Use `None` to determine
        it based on matplotlib's default figure size.
    * - `node_fontsize`
      - The font size for the labels of the classes, in points.
        Defaults to 16 if every label is one-letter long and 14 if at least
        one label is longer.
    * - `show_legend`
      - Whether to display a legend giving the full name of the
        classes. The model needs to have appropriate metadata for this.
        Optionally, the vertical alignment of the legend can be specified by
        using one of `"top"`, `"bottom"` or `"center"`.
    * - `title`
      - The title of the plot.
  """
  if ax is None:
    fig, ax = plt.subplots()
  else:
    fig = ax.get_figure()
  renderer = _find_renderer(fig)

  ax.set_aspect('equal')
  ax.axis('off')

  # the vertices are drawn on [0,1].
  xspan = np.linspace(0, 1, model.dim)
  r = 1.0 / (model.dim*2.5)
  r_inner = 0.8*r

  artists = []
  bbox = None

  def fmt_label(x):
    s = edge_labels.format(x)
    if (x / 10).is_integer():
      s = s.rstrip("0").rstrip(".")
    return s

  # --- Draw the edges --- #
  for i, j in zip(*np.where(model.A)):
    line_prop, arrow_prop = _edge_style(
      model, i, j,
      survival, mixed, fertilities)
    patches = _draw_edge(
      from_vertex=i, to_vertex=j, vertex_positions=xspan, r=r,
      arrow_prop=arrow_prop, line_prop=line_prop,
      reverse_exists=(model.A[j,i] != 0),
      label=fmt_label(model.A[i,j]) if edge_labels else None,
      ax=ax)
    artists += patches
    for p in patches:
      bbox = _update_bbox(bbox, renderer, p, ax)

  # --- Extract labels and legend from the model --- #
  labels, legends = _label_classes(node_labels, model)

  # --- Draw the vertices --- #
  patches = _draw_vertices(labels=labels, node_colors=node_colors,
                           fill_nodes=fill_nodes,
                           r=r_inner, node_fontsize=node_fontsize,
                           vertex_positions=xspan, ax=ax)
  artists += patches
  for p in patches:
    bbox = _update_bbox(bbox, renderer, p, ax)
  
  # --- Write the legend --- #
  if show_legend:
    if legends is None:
      if ut._ISSUE_WARNINGS:
        warnings.warn("No suitable metadata in the model. "
                      "Ignoring argument show_legend.")
    else:
      if show_legend == "center":
        y_legend = (bbox.y1 + bbox.y0) / 2
      elif show_legend == "bottom":
        y_legend = bbox.y0
      else:
        show_legend = "top"
        y_legend = bbox.y1
      mx_label = np.max([len(str(label)) for label in labels])
      legend_fmt = "{{0:{0}}}: {{1}}".format(mx_label)
      txt = "\n".join([legend_fmt.format(str(u), v)
                       for u, v in zip(labels, legends)])
      legend_text = ax.text(1 + 2*r, y_legend, txt,
                            clip_on=False,
                            fontdict={'family' : 'monospace'},
                            horizontalalignment='left',
                            verticalalignment=show_legend,
                            bbox={'lw':0, 'fc':'none'})
      artists.append(legend_text)
      bbox = _update_bbox(bbox, renderer, legend_text, ax)

  # --- Configure the Axes --- #
  fig.set_size_inches(node_size*bbox.width/(2*r_inner),
                      node_size*bbox.height/(2*r_inner))

  if show_legend:
  # We need to recompute the global bounding box and readjust the
  # figure size because changing the figure size changes the size of the
  # text elements.
    for p in artists:
      bbox = _update_bbox(bbox, renderer, p, ax)
    fig.set_size_inches(node_size*bbox.width/(2*r_inner),
                        node_size*bbox.height/(2*r_inner))

  # Add padding to avoid clipping
  xspan = bbox.x1 - bbox.x0
  yspan = bbox.y1 - bbox.y0
  q = 4. if show_legend else 1.
  ax.set_xlim(bbox.x0 - xspan/100, bbox.x1 + q * xspan/100)
  ax.set_ylim(bbox.y0 - yspan/100, bbox.y1 + yspan/100)

  if title is not None:
    ax.set_title(title)
  return ax


def _find_renderer(fig):
  """Get the current renderer. See matplotlib backend_bases.py print_figure()."""
  if hasattr(fig.canvas, "get_renderer"):
    renderer = fig.canvas.get_renderer()
  else:
    import io
    fig.canvas.print_pdf(io.BytesIO())
    renderer = fig._cachedRenderer
  return renderer


def _update_bbox(bbox, renderer, artist, ax):
  """Update the global bounding box bbox, by adding the bbox of
  a new artist object"""
  transf = ax.transData.inverted()
  try:
    path = artist.get_path()
    transform = artist.get_transform()
    bbox_artist = path.get_extents().transformed(transform)
  except AttributeError:
    bbox_artist = artist.get_window_extent(renderer = renderer)

  bbox_artist = bbox_artist.transformed(transf)

  #----- For debugging: uncommenting draws the bbox -----#
  #bba = bbox_artist
  #ax.vlines([bba.x0, bba.x1], bba.y0, bba.y1, color='C1', zorder=10)
  #ax.hlines([bba.y0, bba.y1], bba.x0, bba.x1, color='C0', zorder=10)

  if bbox is None:
    return bbox_artist
  else:
    return matplotlib.transforms.Bbox.union([bbox, bbox_artist])


##### MATRICES ########################################################

def matrices(matrices, plot_type="bubbles", same_scale=False,
             class_labels=None, matrix_names=None, show_entries=False,
             colors=None, plot_style=None,
             title=None, ax=None):
  r"""
  Graphical representation non-negative matrices.

  .. list-table::
    :widths: 15 85

    * - `matrices`
      - The list (or tuple) of matrices to plot. If a single matrix is to
        be plotted, it can be passed directly instead of as a one-element list.
        All matrices must be square, non-negative, and have the same dimensions.
    * - `plot_type`
      - .. rst-class:: nospaceafter

        The type of plot:

        * ``"bars"`` --- the value of entries are represented by
          the heights of bars.
        * ``"bubbles"`` --- the value of entries are represented by the radius
          of circles.
        * ``"heatmap"`` --- the value of entries are represented by a color.
          Only one matrix can be displayed with this option.
    * - `same_scale`
      - When plotting several matrices, whether to use
        the same scale for all matrices. This makes direct comparison between
        matrices possible, but can make patterns harder to see. 
        The default is ``False``.
    * - `class_labels`
      - The labels of the classes, as a list of strings. For models
        from COMPADRE/COMADRE, the ``"MatrixClassAuthor"`` of the model
        ``metadata`` can be used. If ``None``, integers will be used.
    * - `matrix_names`
      - The names of the matrices plotted, as a list of strings. If ``None``
        (the default), no legend will be shown. 
    * - `show_entries`
      - Whether to display the numerical value of non-zero matrix entries.
    * - | `colors`
        | `plot_style`
        | `title`
      - See the documentation of :func:`trajectory`.
  """

  if (not isinstance(matrices, list)) and (not isinstance(matrices, tuple)):
    matrices = [matrices]

  number = len(matrices)
  if number == 0:
    raise ValueError("Incorrect argument matrices: you should provide at "
      "least one matrix. Got an empty list.")
  width = 1/number

  for mat in matrices:
    if not isinstance(mat, np.ndarray):
      raise ValueError(f"Expected a NumPy array, got {mat}")
    ut.assert_square(mat)
    ut.assert_nonnegative(mat)
    ut.assert_same_dimensions(matrices[0], mat)
  N = matrices[0].shape[0]

  labels = class_labels # (can't be bother to change it everywhere)
  if labels is not None:
    if not all(isinstance(lab, str) for lab in labels):
      raise ValueError("Incorrect argument labels: "
        f"should be a list of strings, got {labels}")
    if len(labels) != N:
      raise ValueError("Incorrect argument labels: the number of labels "
        f"provided ({len(labels)}) does not match the dimension "
        f"of the matrices ({N})")

  if matrix_names:
    if not all(isinstance(name, str) for name in matrix_names):
      raise ValueError("Incorrect argument matrix_names: "
        f"should be a list of strings, got {matrix_names}")
    if len(matrix_names) != number:
      raise ValueError("Incorrect argument matrix_names: the number of names "
        f"provided ({len(matrix_names)}) does not match "
        f"the number of matrices ({number}).")

  if plot_type not in ["bars", "bubbles", "heatmap"]:
      raise ValueError(f"Unknown plot_type: {plot_type}. Should be one of: "
        "'bars', 'bubbles', 'heatmatp'.")

  if plot_type == 'heatmap' and number > 1:
    raise ValueError("plot_type='heatmap' can only with one matrix, "
      f"here {number} matrices were provided.")

  if show_entries and number > 1:
    raise ValueError("Cannot show numerical values of entries "
      "for more than one matrix.")

  if show_entries:
    if show_entries == True:
      entries_fmt = "{:.2f}"
    else:
      try:
        show_entries.format(1.0)
      except:
        raise ValueError("Incorrect format string for matrix entries: "
          f"{show_entries}.")
      entries_fmt = show_entries

  if plot_style is None:
    if ax is None:
      fig, ax = plt.subplots(1,1, constrained_layout=True)
    else:
      fig = ax.get_figure()
    set_colors(ax, colors if colors is not None else "muted", number)
  else:
    try:
      with plt.style.context(plot_style):
        if ax is None:
          fig, ax = plt.subplots(1,1,)
        else:
          fig = ax.get_figure()
      set_colors(ax, colors, number)
    except OSError:
      raise ValueError(f"Invalid argument plot_style: {plot_style}")

  classes = list(range(N))

  if labels is not None:
    short_labels, long_labels = _parse_classnames(labels)
    for i in range(len(short_labels)):
      long_labels[i] += (" ({})".format(short_labels[i]))
  else:
    short_labels = [str(i) for i in range(N)]
    long_labels = [str(i) for i in range(N)]

  prop_cycler = ax._get_lines.prop_cycler

  if same_scale:
    mx = max(mat.max() for mat in matrices)

  for n, mat in enumerate(matrices):

    color = next(prop_cycler)["color"]

    if matrix_names:
      ax.plot([None,None], [None,None], color=color, label=matrix_names[n])
    else:
      ax.plot([None,None], [None,None], color=color)

    if not same_scale:
      mx = mat.max()

    if plot_type == 'heatmap':
      cmap = plt.cm.get_cmap('viridis', 12)
      norm = matplotlib.colors.Normalize(mat.min(), mat.max())
      fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

    for i in classes:
      for j in classes:
        labcolor = 'k'
        posy = N - 1 - j
        posx = i

        if mat[j,i]>0:
          if plot_type=='bars':
            posx = i + (-0.5 + 0.5*width if number > 1 else 0)
            ax.bar(posx + n*width,
                   mat[j,i]/mx, bottom=posy-0.5,
                   width=width, color=color)
          elif plot_type=='bubbles':
            ax.add_patch(
              mpatches.Circle([posx, posy], 0.025 + 0.45*(mat[j,i]/mx),
                              color=color, alpha=0.5))
          elif plot_type=='heatmap':
            color = cmap(mat[j,i]/mx)
            ax.bar(posx, 1, bottom=posy-0.5, width=1, color=color)
            labcolor = 'w' if _is_dark(cmap(mat[j,i]/mx)) else 'k'

          if show_entries:
            ax.text(posx, posy, entries_fmt.format(mat[j,i]),
                    horizontalalignment='center',
                    color=labcolor,
                    verticalalignment='center')
        else:
          if plot_type=="heatmap":
            ax.bar(i, 1, bottom=posy-0.5, width=1, color=cmap(0))


  if matrix_names and plot_type!='heatmap':
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)

  if plot_type=='bars':
    ax.vlines(np.array(classes)+0.5, -1, N, color='k', lw=0.1)
    ax.hlines(np.array(classes)+0.5, -1, N, color='k', lw=0.1)
  elif plot_type=='bubbles':
    ax.hlines(np.array(classes), -1, N, color='k', lw=0.1, zorder=0)
    ax.vlines(np.array(classes), -1, N, color='k', lw=0.1, zorder=0)
    for side in ('left','right','top','bottom'):
      ax.spines[side].set_visible(False)
  ax.set(xticks = classes, yticks=classes[::-1],
         xticklabels=short_labels, yticklabels=long_labels)
  ax.xaxis.tick_top()
  ax.tick_params(which='both', length=0)
  ax.set_aspect('equal')
  ax.set(xlim=(-0.5, N - 0.5), ylim=(-0.5, N - 0.5))

  if title is not None:
    ax.set_title(title)

  return ax

