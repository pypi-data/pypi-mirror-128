r"""
This module provides ready-made models that can be used to get familiar
with the library or for pedagogical purposes.

>>> from matpopmod.examples import orcinus_orca
>>> orcinus_orca
MPM(
  S = [[0.    , 0.    , 0.    , 0.    ],
       [0.9775, 0.9111, 0.    , 0.    ],
       [0.    , 0.0736, 0.9534, 0.    ],
       [0.    , 0.    , 0.0452, 0.9804]],
  F = [[0.    , 0.0043, 0.1132, 0.    ],
       [0.    , 0.    , 0.    , 0.    ],
       [0.    , 0.    , 0.    , 0.    ],
       [0.    , 0.    , 0.    , 0.    ]],
  metadata = {
    'ModelName': 'orcinus_orca',
    'Species': 'Orcinus orca',
    'CommonName': 'Killer whale',
    'Classes': ['Newborns', 'Juveniles', 'Reproductive adults',
'Post-reproductive adults'],
    'Source': 'Example 5.1 from Caswell H. (2000). Matrix
Population Models: Construction, Analysis, and Interpretation.',
    'Comments': 'The projection matrix is not irreducible due
to the presence of a post-reproductive class.\n\nExample of a
K-strategy, with high survival and low fertility.'
  }
)

Only a handful of models of specific interest are given.
For a much larger collection of models, see the module
:mod:`~matpopmod.compadre`, which provides an interface to the
COMPADRE and COMADRE databases.
"""


from matpopmod.model import MPM


orcinus_orca = MPM(
  S = [[0.    , 0.    , 0.    , 0.    ],
       [0.9775, 0.9111, 0.    , 0.    ],
       [0.    , 0.0736, 0.9534, 0.    ],
       [0.    , 0.    , 0.0452, 0.9804]],
  F = [[0.    , 0.0043, 0.1132, 0.    ],
       [0.    , 0.    , 0.    , 0.    ],
       [0.    , 0.    , 0.    , 0.    ],
       [0.    , 0.    , 0.    , 0.    ]],
  metadata = {
    'ModelName': 'orcinus_orca',
    'Species': 'Orcinus orca',
    'CommonName': 'Killer whale',
    'Classes': ['Newborns', 'Juveniles', 'Reproductive adults', 'Post-reproductive adults'],
    'Source': 'Example 5.1 from Caswell H. (2000). Matrix Population Models: Construction, Analysis, and Interpretation.',
      'Comments': 'The projection matrix is not irreducible due to the presence of a post-reproductive class.\n\nExample of a K-strategy, with high survival and low fertility.'
  }
)
r"""
Stage-based model for the killer whale *Orcinus orca* (Example 5.1 in [Casw00]_,
based on data from [BrCa93]_). The projection matrix is

.. math::

  \mathbf{A} =
    \begin{pmatrix}
       0      & 0.0043 & 0.1132 & 0    \\
       0.9775 & 0.9111 & 0      & 0    \\
       0      & 0.0736 & 0.9534 & 0    \\
       0      & 0      & 0.0452 & 0.9804
    \end{pmatrix},

and the classes correspond to newborns, juveniles, reproductive adults
and post-reproductive adults. This is an example of what refer to as an Usher
model, that is, the survival probabilities are on the diagonal and subdiagonal
entries of the projection matrix, and the fertilities on its first row.

>>> orcinus_orca.usher
True

An interesting feature of the model is that it is reducible due to the presence
of a post-reproductive class:

>>> orcinus_orca.irreducible
False
>>> orcinus_orca.postreproductive_classes
array([0., 0., 0., 1.])
>>> orcinus_orca.v # reproductive values
array([ 1.14163164,  1.19762278,  1.79386902, -0.        ])

It also is an example of a *K*-strategy, i.e. of a life-cycle with a very high
survival and a low fertility.  This results in long lifespans, but because
individuals do not reproduce during their whole life the generation time
remains comparatively short.

>>> orcinus_orca.life_expectancy
69.41056244644568
>>> orcinus_orca.T_a # generation time (mean age of mothers)
23.69204811243964
>>> orcinus_orca.T_R0 # R0 generation time
27.850790932634087

"""


bernardelli_beetle = MPM(
  S = [[0  , 0  , 0  ],
       [1/2, 0  , 0  ],
       [0  , 1/3, 0  ]],
  F = [[0, 0, 6],
       [0, 0, 0],
       [0, 0, 0]],
  metadata = {
    'ModelName': 'bernardelli_beetle',
    'Source': 'Bernardelli H. (1941). Population waves. Journal of the Burma Research Society, 31(1):3--18.',
    'Comments': 'Fictitious population of beetles imagined by Bernardelli in 1941.\n\nFirst published example of a periodic matrix population model: the index of imprimitivity is equal to 3.'
  }
)
r"""
The famous model for Bernardelli's fictitious beetle, from [Bern41]_ (partially
reprinted in [SmKe77]_). In this influential paper, Bernardelli imagined
a population of beetles whose dynamics are governed by the projection
matrix

.. math::

  \mathbf{A} =
    \begin{pmatrix}
      0           &  0             &  6 \\
      \frac{1}{2} &  0             &  0 \\
      0           &  \frac{1}{3}   &  0
    \end{pmatrix},

(although he does point out that the numerical values are irrelevant), and
showed that the population would be subject to sustained oscillations, which he
termed *"population waves"*. And, indeed::

  traj = bernardelli_beetle.trajectory([100, 0, 0], 40)
  matpopmod.plot.trajectory(traj) 

.. plot::

  from matpopmod.examples import bernardelli_beetle
  traj = bernardelli_beetle.trajectory([100, 0, 0], 40)
  matpopmod.plot.trajectory(traj) 

This is because the projection matrix is periodic,
with index of imprimitivity 3:

>>> bernardelli_beetle.aperiodic
False
>>> bernardelli_beetle.index_of_imprimitivity
3

As a result, there is no stable distribution in the usual sense. However,
since the projection matrix is irreducible, it has a well-defined
Perron vector (that is, a unique non-negative eigenvector associated
to *λ*) and it remains possible to compute quantities such as the
elasticities.

>>> bernardelli_beetle.w
UserWarning: A is not quasi-primitive. Most descriptors are
ill-defined. They will be set to NaN.
array([nan, nan, nan])
>>> bernardelli_beetle.right_eigenvectors[0]
array([0.6, 0.3, 0.1])
>>> bernardelli_beetle.elasticities
array([[0.        , 0.        , 0.33333333],
       [0.33333333, 0.        , 0.        ],
       [0.        , 0.33333333, 0.        ]])

"""


passerine_postbreeding = MPM(
  S = [[0.  , 0.  , 0.  ],
       [0.2 , 0.  , 0.  ],
       [0.  , 0.35, 0.5 ]],
  F = [[0.7  , 1.225, 1.75 ],
       [0.   , 0.   , 0.   ],
       [0.   , 0.   , 0.   ]],
  metadata = {
    'ModelName': 'passerine_postbreeding',
    'Classes':['Newborns', 'Yearlings', 'Adults'],
    'Source': 'Model passa_0 shipped with the ULM software.',
    'Comments': 'Generic post-breeding census model for passerine birds.\n\nCan be compared with the corresponding pre-breeding census model, passerine_prebreeding.'
  }
)
r"""
A generic model for passerine birds, using a post-breeding census. The
projection matrix is

.. math::

  \mathbf{A} =
    \begin{pmatrix}
      \sigma s_0 f_1     & \sigma s f_2  &  \sigma \nu f_2 \\
             s_0         &  0            &  0              \\
             0           &  s            &  \nu
    \end{pmatrix},

where :math:`s_0` (resp. :math:`s`, :math:`\nu`) is the survival probability
of newborns (resp. yearlings, adults); :math:`f_1` (resp. :math:`f_2`)
is the fecundity of female yearlings (resp. adults), i.e. the expected
number of chicks they produce; and :math:`\sigma` is the primary sex ratio,
i.e. the proportion of females at birth. The numerical values
used here are from the model `passa_0` shipped with the
`ULM software <https://www.biologie.ens.fr/~legendre/ulm/ulm.html>`_.

The output of this model can be compared with that of the corresponding
pre-breeding model, :const:`passerine_prebreeding`.

>>> passerine_postbreeding.w # stable distribution
array([0.77777778, 0.14077741, 0.08144481])
>>> passerine_prebreeding.w
array([0.63349835, 0.36650165])
>>> passerine_postbreeding.elasticities
array([[0.37947486, 0.12019835, 0.09934154],
       [0.21953989, 0.        , 0.        ],
       [0.        , 0.09934154, 0.08210381]])
>>> passerine_prebreeding.elasticities
array([[0.37947486, 0.21953989],
       [0.21953989, 0.18144535]])

"""


passerine_prebreeding = MPM(
  S = [[0.  , 0.  ],
       [0.35, 0.5 ]],
  F = [[0.7, 0.7],
       [0. , 0. ]],
  metadata = {
    'ModelName': 'passerine_prebreeding',
    'Classes':['Yearlings', 'Adults'], 
    'Source': 'Model pass_0 shipped with the ULM software.',
    'Comments': 'Generic pre-breeding census model for passerine birds.\n\nCan be compared with the corresponding post-breeding census model, passerine_postbreeding.'
  }
)
r"""
A generic model for passerine birds, using a pre-breeding census. The
projection matrix is

.. math::

  \mathbf{A} =
    \begin{pmatrix}
      \sigma s_0 f_2  & \sigma s_0 f_2 \\
                   s  &            \nu
    \end{pmatrix}.

See :const:`passerine_postbreeding` for more information.
"""


dipsacus_sylvestris = MPM(
  S = [[0.   , 0.   , 0.   , 0.   , 0.   , 0.   ],
       [0.966, 0.   , 0.   , 0.   , 0.   , 0.   ],
       [0.013, 0.01 , 0.125, 0.   , 0.   , 0.   ],
       [0.007, 0.   , 0.125, 0.238, 0.   , 0.   ],
       [0.008, 0.   , 0.038, 0.245, 0.167, 0.   ],
       [0.   , 0.   , 0.   , 0.023, 0.75 , 0.   ]],
  F = [[  0.   ,   0.   ,   0.   ,   0.   ,   0.   , 322.38 ],
       [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   0.   ],
       [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   3.448],
       [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,  30.17 ],
       [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   0.862],
       [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   0.   ]],
  metadata = {
    'ModelName': 'dipsacus_sylvestris',
    'Species': 'Dipsacus fullonum',
    'CommonName': 'Teasel',
    'Classes':['S1: First-year dormant seeds', 'S2: Second-year dormant seeds', 'R1: Small rosettes', 'R2: Medium rosettes', 'R3: Rosettes', 'F: Flowering plants'],
    'Source': 'Example 5.2 from Caswell H. (2000). Matrix Population Models: Construction, Analysis, and Interpretation.',
    'Comments': 'The teasel Dipsacus fullonum is referred to as Dipsacus sylvestris by most publications citing this model.\n\nExample of a complex life-cycle with ill-defined newborn classes.'
  }
)
r"""
Complex life-cycle for the common teasel *Dipsacus fullonum* (also referred to
as *Dispacus sylvestris* by most publications citing this model) from
[Casw00]_, Example 5.2. Based on the original publication [CaWe78]_.

.. code-block::

  matpopmod.plot.life_cycle(dipsacus_sylvestris)

.. plot::

  from matpopmod.examples import dipsacus_sylvestris
  matpopmod.plot.life_cycle(dipsacus_sylvestris)


The classes are, from 0 to 5: first-year dormant seeds, second-year dormant
seeds, small rosettes, medium rosettes, rosettes and flowering plants.

This is an example of a model with ill-defined newborn classes: classes 3,
4 and 5 can be reached either by following a reproductive transition or
by following a survival one. As a result, it is not possible to know if
individuals in those classes are newborns or not.

>>> dipsacus_sylvestris.newborn_classes
array([ 1.,  0., nan, nan, nan,  0.])

However, this does not affect the calculation of the descriptors implemented
in this library. It is also possible to compute the fraction of individuals
that are newborns in each class in the stable class structure population:

>>> dipsacus_sylvestris.proportion_newborns
array([1.        , 0.        , 0.5611508 ,
       0.86103652, 0.139299  , 0.        ])

"""


homo_sapiens_USA = MPM(
  S = [[0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.9967 , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.99837, 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.9978 , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.99672, 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.99607, 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.99472, 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.9924 ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.98867, 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.98274, 0.     ]],
  F = [[0.     , 0.00102, 0.08515, 0.30574, 0.40002, 0.28061, 0.1526 ,
        0.0642 , 0.01483, 0.00089],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ],
       [0.     , 0.     , 0.     , 0.     , 0.     , 0.     , 0.     ,
        0.     , 0.     , 0.     ]],
  metadata = {
    'ModelName': 'homo_sapiens_USA',
    'Species': 'Homo sapiens',
    'Classes': ['{}-{} years'.format(x,x+4) for x in range(0,50,5)],
    'ProjectionInterval': 5.0,
    'Source': 'Example 7.2 from Keyfitz N. and Caswell H. (2005). Applied mathematical demography.',
    'Comments': 'Leslie model with a 5-year projection interval for the population of the United States in 1966.'
  }
)
r"""
Leslie model with a 5-year projection interval for the population of the United
States in 1966, from [KeCa05]_, Example 7.2. (also in [Casw00]_ and based on
[KeFl71]_). The life-table is:

=========  ====================  =========
Age class  Survival probability  Fertility
=========  ====================  =========
0--4       0.99670               0
5--9       0.99837               0.00102
10--14     0.99780               0.08515   
15--19     0.99672               0.30574   
20--24     0.99607               0.40002   
25--29     0.99472               0.28061   
30--34     0.99240               0.15260   
35--39     0.98867               0.06420   
40--44     0.98274               0.01483   
45--49     --                    0.00089
=========  ====================  =========

Because the projection interval is 5 years, one must be careful when
interpreting the descriptors.
For instance, the *yearly* growth rate is
:math:`\sqrt[5]{\lambda} \approx 1.01`, and not :math:`\lambda \approx 1.05`:
    
>>> PI = homo_sapiens_USA.metadata["ProjectionInterval"]
>>> PI
5.0
>>> homo_sapiens_USA.lmbd
1.0497530435202165
>>> homo_sapiens_USA.lmbd ** (1 / PI)
1.0097582926164328

Similarly, quantities such as the generation time should be multiplied by
the length of the projection interval.

>>> homo_sapiens_USA.T_a * PI
25.935182726205607
>>> homo_sapiens_USA.T_R0 * PI
26.14245390652162
"""


thalia_democratica = MPM(
  S = [[0.7939, 0.    , 0.    , 0.    ],
       [0.1994, 0.55  , 0.    , 0.    ],
       [0.    , 0.    , 0.8162, 0.    ],
       [0.    , 0.    , 0.1791, 0.7458]],
  F = [[0.    , 0.    , 0.    , 4.233 ],
       [0.    , 0.    , 0.    , 0.    ],
       [0.2034, 0.    , 0.    , 0.    ],
       [0.    , 0.    , 0.    , 0.    ]],
  metadata = {
    'ModelName': 'thalia_democratica',
    'Species': 'Thalia democratica',
    'CommonName': 'Salp',
    'Classes': ['Females >1mm', 'Males >4mm', 'Juvenile oozoids <10mm', 'Post-release oozoids >10mm'],
    'Source': 'Henschke et al. (2015). Population drivers of a Thalia democratica swarm: insights from population modelling. Journal of Plankton Research, 37(5):1074–1087.',
    'Comments': 'Two-sex model.\n\nAlthough males are tracked, they have no impact on the population dynamics as they correspond, mathematically to a post-reproductive class.\n\nExample of a model for which there is a significant difference between r0 and cohort_r0.'
  }
)
"""
Two-sex model for the small salp *Thalia democratica*, from [HSES15]_.

.. plot::

  from matpopmod.examples import thalia_democratica
  matpopmod.plot.life_cycle(thalia_democratica)

The classes are, from 1 to 4: females (>1 mm), males (>4 mm),
juvenile oozoids (3-10 mm) and post-release oozoids (>10 mm).

Despite the name "two-sex model", males have no impact on the dynamics of
the population. Mathematically, they correspond to a post-reproductive
class. It is never possible to have a two-sex matrix population model where
the frequency of males and females influences the dynamics of the population.
This is because this would require introducing non-linearities, whereas
matrix population models are by definition linear.

This is an example of a model where the classic measure of :math:`R_0` --
namely, the dominant eigenvalue of the next generation matrix -- and its
usual interpretation (the expected per-capita reproductive output of a cohort
of newborns at the stable class distribution) differ markedly:

>>> thalia_democratica.R0
4.001730883164397
>>> thalia_democratica.cohort_R0
5.222416673531084

The reason for this discrepancy is that at the stable stage distribution,
28% of the new individuals produced in a year are juvenile oozoids and
72% are females. By contrast, if we sample a newborn
according to the dominant eigenvector of next generation matrix, it only has
a 20% chance of being a juvenile oozoid. Since juvenile oozoids have a higher
reproductive value than females, this explains that a stable cohort of
newborns will have a higher expected reproductive output.
"""


astrocaryum_mexicanum = MPM(
  S = [[0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
        0.      , 0.      , 0.      , 0.      ],
       [0.037349, 0.83093 , 0.      , 0.      , 0.      , 0.      ,
        0.      , 0.      , 0.      , 0.      ],
       [0.      , 0.015881, 0.89666 , 0.      , 0.      , 0.      ,
        0.      , 0.      , 0.      , 0.      ],
       [0.      , 0.      , 0.048969, 0.95944 , 0.      , 0.      ,
        0.      , 0.      , 0.      , 0.      ],
       [0.      , 0.      , 0.      , 0.029778, 0.90496 , 0.      ,
        0.      , 0.      , 0.      , 0.      ],
       [0.      , 0.      , 0.      , 0.      , 0.082074, 0.91348 ,
        0.      , 0.      , 0.      , 0.      ],
       [0.      , 0.      , 0.      , 0.      , 0.      , 0.08652 ,
        0.90553 , 0.      , 0.      , 0.      ],
       [0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
        0.094467, 0.87733 , 0.      , 0.      ],
       [0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
        0.      , 0.0882  , 0.88642 , 0.      ],
       [0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
        0.      , 0.      , 0.11358 , 0.995   ]],
  F = [[ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  1.4792,  8.156 ,
         9.9513, 14.259 , 23.594 ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ],
       [ 0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,  0.    ,
         0.    ,  0.    ,  0.    ]],
  metadata = {
    'ModelName': 'astrocaryum_mexicanum',
    'Species': 'Astrocaryum mexicanum',
    'CommonName': 'Chocho palm',
    'Classes': ['Fruits', 'Infants', 'Juveniles', 'Immature adults', 'Mature adults 1', 'Mature adults 2', 'Mature adults 3', 'Mature adults 4', 'Mature adults 5', 'Mature adults 6'],
    'Source': 'Table A2 from Cochran and Ellner. (1992). Simple methods for calculating age‐based life history parameters for stage‐structured populations. Ecological monographs, 62(3):345--364.',
    'Comments': 'The three classic measures of generation time (mu1, the mean age of parents of offspring produced by a cohort, also frequently referred to as the cohort generation time; T_a, the mean age of mothers in the stable population; and T_R0, the R0 generation time) differs greatly.\n\nmu1 is greater than the expected lifespan conditional on reproduction -- showing that, contrary to what is often claimed, it cannot be interpreted as the "mean age at reproduction".'
  }
)
r"""
Usher model for the palm tree *Astrocaryum mexicanum* (Table A2 in [CoEl92]_,
based on data from [PiMS84]_). 

  .. plot::

    from matpopmod.examples import astrocaryum_mexicanum
    matpopmod.plot.life_cycle(astrocaryum_mexicanum)

The stages are, from 1 to 10: fruits, infants, juveniles, immature adults,
mature adults 1--6.

This is an example of a model where the three classic measures of generation
time :math:`(\mu_1`, the mean age of parents of offspring produced by a cohort,
also frequently referred to as the cohort generation time; :math:`T_a`, the
mean age of mothers in the stable population; and :math:`T_{R_0}`, the
:math:`R_0` generation time) differs greatly.

>>> astrocaryum_mexicanum.mu1
275.1594139265308
>>> astrocaryum_mexicanum.T_a
152.5908805755843
>>> astrocaryum_mexicanum.T_R0
197.61963152089652

This models highlights problems with the interpretation of :math:`\mu_1` (and of
the related measure :math:`T_G` introduced by [StTC14]_). Indeed,
:math:`\mu_1` is often claimed to be a measure of the mean age at reproduction
for a typical individual, but in reality it systematically overestimates it,
as explained in [Bien19]_. In fact, :math:`\mu_1` differs can even exceed
the life expectancy conditional on reproduction, as is the case here:

>>> astrocaryum_mexicanum.mu1
275.1594139265308
>>> mpm.set_rng_seed(0) # for reproducibility
>>> astrocaryum_mexicanum.mean_age_repro() # ~20 mins 
152.61792711532627
>>> astrocaryum_mexicanum.life_expectancy_repro
232.18934046629712
"""


second_order_oscillations = MPM(
  A = [[  0,    2,    2,    1],
       [1/4,    0,    0,    0],
       [  0,  3/4,    0,    0],
       [  0,    0,  2/3,    0]],
  metadata = {
    'ModelName': 'second_order_oscillations',
    'Source': 'matpopmod',
    'Comments': 'Fictitious projection matrix illustrating how to compute the period of the second order oscillations.\n\nThere are three eigenvalues on the second spectral circle: one with period 2 and two with period 3. Since 2 and 3 are commensurable, the second-order dynamics is periodic, with period lcm(2, 3) = 6.'
  }
)
r"""
An example of a projection matrix with non-trivial second order oscillations:

.. math::

  \mathbf{A} = \begin{pmatrix}
    0 & 2 & 2 & 1 \\
    \frac{1}{4} & 0 & 0 & 0 \\
    0 & \frac{3}{4} & 0 & 0 \\
    0 & 0 & \frac{2}{3}  & 0 \\
  \end{pmatrix}

The eigenvalues of **A** are :math:`\big\{1, -\frac{1}{2}, \frac{1}{2} e^{2i\pi/3},
\frac{1}{2} e^{-2i\pi/3}\big\}`. Thus, there are three eigenvalues on the
second spectral circle: :math:`-\frac{1}{2}` generates oscillations with
period 2 and the pair :math:`(\frac{1}{2} e^{2i\pi/3}, \frac{1}{2} e^{-2i\pi/3})`
generates oscillations with period 3. Since there exist positive integers
:math:`(k, k')` such that :math:`2k = 3 k'`, the second-order dynamic
of this model is periodic, with period :math:`\mathrm{lcm}(2, 3) = 6`.

>>> second_order_oscillations.transient_period
5.999999999999999

The periodic component of the second-order dynamics can be illustrated by
plotting it. Note that here we rescale the second order term by :math:`1/2^t`
to compensate the damping of the oscillations and make the periodicity
more apparent.

.. code-block::

  traj = second_order_oscillations.trajectory(
    n0 = [1, 1, 1, 1],
    t_max = 30 
  )

  matpopmod.plot.trajectory(
    traj,
    second_order = True,
    rescale = True,
    show_period = True
  )

.. plot::

  from matpopmod.examples import second_order_oscillations 
  traj = second_order_oscillations.trajectory(
    n0 = [1, 1, 1, 1],
    t_max = 30 
  )
  matpopmod.plot.trajectory(
    traj,
    second_order = True,
    rescale = True,
    show_period = True
  )

"""


all_models = [
  orcinus_orca,
  bernardelli_beetle,
  passerine_postbreeding,
  passerine_prebreeding,
  dipsacus_sylvestris,
  homo_sapiens_USA,
  thalia_democratica,
  astrocaryum_mexicanum,
  second_order_oscillations
]


#### MATRICES DIPSACUS IN LATEX #####
#
#.. math::
#
#  \mathbf{S} =
#  \begin{pmatrix}
#     0    & 0    & 0      & 0      & 0      & 0  \\
#     0.966& 0    & 0      & 0      & 0      & 0  \\
#     0.013& 0.01 & 0.125  & 0      & 0      & 0  \\
#     0.007& 0    & 0.125  & 0.238  & 0      & 0  \\
#     0.008& 0    & 0.038  & 0.245  & 0.167  & 0  \\
#     0    & 0    & 0      & 0.023  & 0.75   & 0
#  \end{pmatrix}
#
#.. math::
#
#  \mathbf{F} =
#  \begin{pmatrix}
#    0   &   0   &   0   &   0   &   0   & 322.38  \\
#    0   &   0   &   0   &   0   &   0   &   0    \\
#    0   &   0   &   0   &   0   &   0   &   3.448 \\
#    0   &   0   &   0   &   0   &   0   &  30.17  \\
#    0   &   0   &   0   &   0   &   0   &   0.862 \\
#    0   &   0   &   0   &   0   &   0   &   0   
#  \end{pmatrix}
#
