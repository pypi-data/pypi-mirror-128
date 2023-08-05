"""
This module provides an interface to the 
`COMPADRE and COMADRE databases <https://www.compadre-db.org/>`_
[`Salg15 <../references.html#salg15>`_, `Salg16 <../references.html#salg15>`_].
Together, these databases contain more than 12000 models that have been curated
from the literature and annotated. The tools implemented here can also be
used to manipulate and save arbitrary collections of matrix population models. 

The central element of this module is the class :class:`MPMCollection`, which
provides a convenient interface to deal with collections of models.
MPM collections can be created manually or loaded from JSON
files. They can then be queried, iterated over, filtered,
merged and saved. See the documentation of :class:`MPMCollection`
for details.

In order to be loaded in Python, the COMPADRE / COMADRE databases -- which are
distributed as RData files -- must be converted to JSON. This can be done:

- From the R console, using the following code:

  .. code-block:: r

      library(jsonlite)
      database <- get(load("file_in.RData"))
      write(toJSON(database), "file_out.json")

- Directly from Python, using the function :func:`convert`::

    matpopmod.compadre.convert("file_in.RData")

  Note that both methods require a working R installation, and
  see also :func:`fetch` for a convenient way to download and convert
  specific versions of the database.

Alternatively, you can download the following, pre-converted versions of
the databases:

    - |COMPADRE JSON|
    - |COMADRE JSON|

These files are regularly updated using the latest version of
the databases provided on `<https://www.compadre-db.org>`_
(last update: |LONG DATE COMPADRE|).
    
Once you have an appropriate JSON file, it can be loaded
in Python using :func:`load`:

>>> db = matpopmod.compadre.load("COMPADRE_v.6.21.8.0.json")
>>> db
MPM Collection (7907 models) at 0x7fe0bfc2be10

MPM collections can for the most part be manipulated as lists of
:class:`~matpopmod.model.MPM` objects. For instance, the *i*-th
model of the collection can be accessed with ``db[i]`` and iterating
over the collection is done using the usual syntax:

>>> numpy.median([m.lmbd for m in db]) # median growth rate
0.9963973097479666

See the documentation of :class:`MPMCollection` for a complete presentation.
"""

import os
import re
import json
import inspect
import urllib.request
import warnings
import subprocess
# import glob

import numpy as np
from matpopmod.model import MPM


# Versions of the databases known to matpopmod
# Order matters: the first element is assumed to be the latest version

COMADRE_VERSIONS = [
  "4.21.8.0", "4.21.6.0", "4.21.1.0", "4.20.9.0", "4.20.8.2", 
  "4.20.8.1", "4.20.8.0", "4.20.7.0", "4.20.6.0", "4.20.5.0",
  "4.20.11.1", "4.20.11.0", "3.0.1", "3.0.0", "2.0.1", "2.0.0", "1.0.0"]
"""
Published versions of COMPADRE as of 24/09/2021.
"""

COMPADRE_VERSIONS = [
  "6.21.8.0", "6.21.6.0", "6.21.1.0", "6.20.9.0", "6.20.8.0",
  "6.20.7.0", "6.20.6.0", "6.20.5.0", "6.20.11.1", "6.20.11.0",
  "5.0.1", "5.0.0", "4.0.1", "4.0.0", "3.2.1", "3.2.0", "3.0.0"]
"""
Published versions of COMADRE as of 24/09/2021.
"""


class CompadreError(Exception):
  """Raised whenever a problem is encountered loading the database."""

def _is_2D_ndarray(M):
  """
  Internal wrapper used to determine how to print the arguments A, S and F.
  """
  return (isinstance(M, np.ndarray) and len(M.shape) == 2)

def _remove_na(mat, replace_with=None):
  """
  Replaces the string ``'NA'`` in a nested list with `replace_with`.
  """
  mat = [[x if x != 'NA' else replace_with for x in line] for line in mat]
  return np.array(mat, dtype=float)

class InvalidMPM:
  """
  Objects used by :class:`MPMCollection` to represent models that
  do not correspond to well-defined matrix population models (e.g, because some
  of the entries of projection matrix are ``nan`` or because entries that are
  supposed to correspond to survival probabilities are greater than 1).

  Invalid MPMs have the following attributes, which represent the same thing
  as for regular :class:`~matpopmod.model.MPM` objects: :attr:`A`, :attr:`S`,
  :attr:`F`, :attr:`split` and :attr:`dim`.  However, not all of these
  attributes are necessarily well-defined or of the expected type.

  In addition, Invalid MPMs have a special attribute :attr:`error` which
  explains why they are not valid MPMs. The intended use is that this
  should correspond to the exception that is raised when trying to instanciate
  a MPM with the same arguments; but users are free to store anything
  in this (non-mutable) attribute.
  """
  def __init__(self, A=None, S=None, F=None, metadata=None, error=None):

    self._A = A 
    self._F = F
    self._S = S
    if metadata is None:
      metadata = []
    self.metadata = metadata
    self._error = error
    self._split = not ((S is None) and (F is None)) 

    for M in (self._A, self._F, self._S):
      try:
        M.flags.writeable = False
      except:
        pass

  @property
  def A(self):
    return self._A

  @property
  def S(self):
    return self._S

  @property
  def F(self):
    return self._F

  @property
  def split(self):
    return self._split

  @property
  def dim(self):
    try:
      return self._A.shape[0]
    except AttributeError:
      return None

  @property
  def error(self):
    return self._error

  def __str__(self):
    if _is_2D_ndarray(self._A):
      with np.printoptions(linewidth = None, suppress = True):
        s = str(self.A)[1:-1].replace("\n ", "\n")
    else:
      s = self._A
    return f"Invalid MPM with projection matrix: \n{s}"

  def __repr__(self):
    if self.split:
      if _is_2D_ndarray(self._S):
        rprS = repr(self.S).replace("array(", "  S = ")[0:-1]
      else:
        rprS = repr(self.S)
      if _is_2D_ndarray(self._F):
        rprF = repr(self.F).replace("array(", "  F = ")[0:-1]
      else:
        rprF = repr(self.F)
      mat = rprS + ",\n" + rprF
    else:
      if _is_2D_ndarray(self._A):
        mat = repr(self.A).replace("array(", "  A = ")[0:-1]
      else:
        mat = repr(self.A)
    error = "  error = '" + str(self.error) + "'"
    if self.metadata:
      rprmeta = (
        "  metadata = {\n    " +
        ",\n    ".join(repr(key) + ": " + repr(val)
                       for (key, val) in self.metadata.items()) + "\n  }")
    else:
      rprmeta = "  metadata = {}"
    return "InvalidMPM(\n" + mat + ",\n" + error + ",\n" + rprmeta + "\n)"


class MPMCollection:
  r"""
  MPM collections provide a simple interface to manipulate sets of
  :class:`~matpopmod.model.MPM`'s.

  .. raw:: html

    <ul>
      <li><a href="#loading-collections">Loading and basic manipulation</a></li>
      <li><a href="#model-metadata">Model metadata</a></li>
      <li><a href="#matrix-id"><span class="pre">MatrixID</span>'s</a></li>
      <li><a href="#filtering">Filtering, merging and saving</a></li>
      <li><a href="#custom-collections">Manual creation</a></li>
    </ul>

  .. h3:: loading-collections Loading and basic manipulation 

  The intended way to create a MPM
  collection is to load it from a JSON file:

  >>> db = matpopmod.compadre.load("COMPADRE_v.6.21.8.0.json")

  Entries of the database that correspond to well-defined models
  are stored in the :attr:`models` attribute of the collection. If the database
  contains ill-defined models, they are stored in :attr:`invalid_models`,
  as :class:`InvalidMPM` objects. Finally, the collection has an
  attribute :attr:`info` that contains the metadata of the database.

  >>> db.info
  {'filename': 'COMPADRE_v.6.21.8.0.json',
   'Database': 'COMPADRE',
   'Version': '6.21.8.0',
   'Type': 'Release',
   'DateCreated': 'Aug_20_2021',
   'TimeCreated': '19:00',
   'Agreement': 'https://www.compadre-db.org/UserAgreement',
   'GeneratorScriptVersion': '1.3'}
  
  The attributes :attr:`models` and :attr:`invalid_models` are simply
  lists of :class:`~matpopmod.model.MPM` / :class:`InvalidMPM` objects, and
  can be manipulated as such. However, for convenience it is also possible
  to perform some of the operations on :attr:`models` directly on the MPM
  collection itself. For instance, the *i*-th model of the collection ``db``
  can be accessed using ``db[i]`` -- this is equivalent to using
  ``db.models[i]``. Similarly, ``len(db)`` is equivalent to
  ``len(db.models)`` and it is possible to iterate
  over the models using the usual syntax::

    for m in db:
        ...

  .. h3:: model-metadata Model metadata 

  Models from COMPADRE / COMADRE are extensively annotated with information
  about populations, publications and model construction.
  The fields of COMPADRE / COMADRE entries are stored in the 
  corresponding models' :attr:`metadata`:

  >>> db[0].metadata["SpeciesAccepted"]
  'Abies balsamea'

  See the `user guide of COMPADRE / COMADRE
  <https://jonesor.github.io/CompadreGuides/user-guide.html#variables-in-metadata>`_
  for the complete list of available fields and their detailed description.

  .. h3:: matrix-id MatrixID's

  Models from COMPADRE / COMADRE have unique IDs called
  "MatrixIDs". The MatrixID of a model ``m`` is in
  ``m.metadata["MatrixID"]``. To access a model from its ID, use
  :meth:`get_from_id`.

  >>> print(db.get_from_id(239145))
  MPM with projection matrix: 
  [0.    0.    0.245 2.1  ]
  [0.    0.    0.045 0.   ]
  [0.125 0.    0.091 0.   ]
  [0.125 0.    0.091 0.333]

  Note that this also returns models from the collection's
  :attr:`invalid_models`, not just from :attr:`models`. If there is no
  model with the requested ID in the collection, this will raise
  :exc:`KeyError`:

  >>> db.get_from_id(27590)
  Traceback (most recent call last):
    ...
  KeyError: "No model with metadata['MatrixID'] == 27590"
  
  When working with COMPADRE / COMADRE, MatrixIDs are numbers and
  are guaranteed to be unique. When working with custom collections, MatrixIDs 
  can be any hashable value and it is the user's responsibility to ensure
  that they are unique.

  .. h3:: filtering Filtering, merging and saving

  One of the most useful operation on MPM collections is filtering, i.e.
  removing models that do not meet certain criteria. This is done with
  :func:`filter_collection`, which works exactly like Python's
  built-in :func:`filter`:

  .. code-block::

    filter_collection(function, collection)

  will return a new collection containing the models of `collection`
  for which `function` evaluates to ``True``. For simple filters, using
  lambda expressions is convenient.

  >>> flt = matpopmod.compadre.filter_collection
  >>> split = flt(lambda x : x.split, db)
  >>> decreasing = flt(lambda x : x.lmbd < 1, db)
  >>> len(db), len(split), len(decreasing)
  (7907, 7443, 4158)

  Finally, collections can merged:
  
  >>> comadre = mpm.compadre.load("COMADRE_v.4.21.8.0.json")
  >>> both_db = matpopmod.compadre.merge(db, comadre)
  
  and saved to JSON files:

  >>> matpopmod.compadre.save(both_db, "BOTH_DB.json")
  
  .. h3:: custom-collections Manual creation 

  MPM collections can be created manually from lists of models. This can
  be useful, e.g, to save a set of MPMs.
  
  >>> eg = matpopmod.MPMCollection(matpopmod.examples.all_models)

  When doing this, the following optional arguments can be used:
  
  - `invalid_models` — a list of :class:`InvalidMPM`\ s. This is useful to
    keep information about models that failed to be instantiated.
  - `info` — a dictionary of information about the collection.
  - `check` — if ``True`` (the default), basic type checking will be performed
    when instantiating the collection.

  """
  def __init__(self, models, invalid_models=None, info=None, check=True):
    if check:
      for i,m in enumerate(models):
        if not isinstance(m, MPM):
          raise ValueError(
            f"The {i}-th element of `models` is not a MPM: {m}")
      if invalid_models is not None:
        for i,m in enumerate(invalid_models):
          if not isinstance(m, InvalidMPM):
            raise ValueError(
              f"The {i}-th element of `models` is not an InvalidMPM: {m}")
    self.models = models

    if invalid_models is not None:
      self.invalid_models = invalid_models
    else:
      self.invalid_models = []

    if info is not None:
      self.info = info
    else:
      self.info = {}

  def __getitem__(self, index):
    # Note: this is sufficient to make MPMCollection iterable
    return self.models[index]

  def __len__(self):
    return len(self.models)

  def __str__(self):
    N = len(self)
    return f"MPM Collection ({N} model{'s' if N else ''}) at {hex(id(self))}"

  def __repr__(self):
    return self.__str__()

  def get_from_id(self, ID):
    """
    TODO (say it is not very efficient)
    """
    x = next((m for m in self.models
            if "MatrixID" in m.metadata and m.metadata["MatrixID"] == ID), None)
    if x is None:
      x = next((m for m in self.invalid_models
            if "MatrixID" in m.metadata and m.metadata["MatrixID"] == ID), None)
    if x is None:
      raise KeyError(f"No model with metadata['MatrixID'] == {ID}")
    else:
      return x


def save(collection, fileout):
  """
  Save the :class:`MPMCollection` to `fileout`, in JSON format.

  The encoding is optimized for compatibility with COMPADRE /
  COMADRE, not for efficiency, and the resulting files can be large.
  Thus, when working with a very large number of models
  you may want to use another type of data serialization. For reference,
  the whole COMPADRE database, which contains about 9000 models, weighs
  ~20 Mo but only takes about one second to load / save.
  """
  db = {"metadata":[], "matrixClass":[], "mat":[]}
  db['version'] = {k:[v] for k, v in collection.info.items() if k != "filename"}
  matrixClass_keys = ["MatrixClassAuthor",
                      "MatrixClassOrganized",
                      "MatrixClassNumber"]

  for m in collection.models:
    db['metadata'].append(m.metadata)
    db['metadata'][-1]["MatrixSplit"] = "Divided" if m.split else False
    db["matrixClass"].append([
      {key:(m.metadata[key][i] if key in m.metadata else None)
       for key in matrixClass_keys}
      for i in range(m.dim)
    ])
    zeros = np.zeros((m.dim, m.dim)).tolist()
    if m.split:
      db['mat'].append({'matA': m.A.tolist(), 'matU': m.S.tolist(),
                        'matF': m.F.tolist(), 'matC': zeros})
    else:
      db['mat'].append({'matA': m.A.tolist(), 'matU': zeros,
                        'matF': zeros, 'matC': zeros})

  with open(fileout, 'w') as file:
    json.dump(db, file)


def merge(x, y, include_invalid=False, copy_info=True):
  """
  Merge the two :class:`MPMCollection`'s `x` and `y`, that is, combine them
  to form a new collection containing the models of both collections.
  If `include_invalid` is ``True`` (default: ``False``), the models
  from :attr:`invalid_models` will be included in the new collection's
  invalid models; if `copy_info` is ``True``, the :attr:`info` attributes of
  both collections will be combined in a non-destructive way.
  """
  models = list(set(x.models + y.models))
  if include_invalid :
    invalid_models = list(set(x.invalid_models + y.invalid_models))
  else:
    invalid_models = []
  if copy_info: 
    info = dict()
    keys = set(x.info).union(set(y.info))
    for k in keys:
      if k in x.info:
        if k in y.info and x.info[k] != y.info[k]:
          info[k] = (x.info[k], y.info[k])
        else:
          info[k] = x.info[k]
      else:
        info[k] = y.info[k]
  else:
    info = dict()
  return MPMCollection(models, invalid_models, info)


def filter_collection(function, collection,
                      include_invalid=False, copy_info=True):
  """
  Filters the :class:`MPMCollection` by removing models for which
  `function` evaluates to ``False``. Returns a new
  :class:`MPMCollection`.

  If `include_invalid` is ``True``, the collection's :attr:`invalid_models`
  will be included (after being filtered); if `copy_info` is ``True``, the
  collection's :attr:`info` is carried over.
  """
  if copy_info:
    info = collection.info.copy()
  else:
    info = {}
  if include_invalid:
    invalid = list(filter(function, collection.invalid_models))
  else:
    invalid = []
  return MPMCollection(list(filter(function, collection.models)),
                       invalid_models = invalid,
                       info = info,
                       check = False)


def load(filename):
  """
  Loads a :class:`MPMCollection` from a JSON file, be it:

  - The COMPADRE / COMADRE databases -- see the documentation of
    the module :mod:`~matpopmod.compadre`.
  - Files produced by :func:`save`.

  """

  models = []
  invalid_models = [] 
  info = dict()
  info["filename"] = filename

  with open(filename, 'r') as file:
    db = json.load(file)

  metadatas = db["metadata"]
  matrixClasses = db["matrixClass"]
  mats = db["mat"]
  try:
    for (x, y) in db["version"].items():
      info[x] = y[0]
  except:
    info["WARNING"] = "Could not read field 'version' of the database."

  if (len(metadatas) != len(matrixClasses)) or (len(metadatas) != len(mats)):
    raise CompadreError("Mismatching number of entries "
      "in 'metadata', 'matrixClasses' and 'mat': "
      f"{len(metadatas), len(matrixClasses), len(mats)}")

  for metadata, matrixClass, mat in zip(metadatas, matrixClasses, mats):
    A, S, F = None, None, None # For InvalidMPM, in case what follows fails
    model_metadata = dict()
    try:
      # Start with the metadata (less likely to fail)
      model_metadata.update(metadata)
      for key in ["MatrixClassAuthor",       # We also store the content of 
                  "MatrixClassOrganized",    # matrixClass in MPM.metadata
                  "MatrixClassNumber"]:
        model_metadata[key] = [entry[key] for entry in matrixClass]
      # Try to read the matrices and instanciate the model
      matA, matU, matF, matC = mat['matA'], mat['matU'], mat['matF'], mat['matC']
      A, S, F = matA, matU, matF # For InvalidMPM, in case the following fails
      if metadata["MatrixSplit"] == "Divided":
        S = _remove_na(matU)
        F = _remove_na(matF) + _remove_na(matC)
        m = MPM(S = S, F = F, metadata = model_metadata)
      else:
        A = _remove_na(matA)
        m = MPM(A, metadata = model_metadata)

      models.append(m)
    
    except Exception as ex:
      m = InvalidMPM(A=A, S=S, F=F, metadata=model_metadata, error=ex)
      invalid_models.append(m)

  return MPMCollection(models, invalid_models, info, check=False)


def convert(file_in, file_out):
  """
  Converts the RData file `file_in` to JSON and save it to `file_out`.

  This function requires a working R installation that:
  
  1. Is compatible with the
     RData file (not all versions of R can load all RData files);
  2. Either has the R package
     `jsonlite <https://CRAN.R-project.org/package=jsonlite>`_ already
     installed or can install it with `install.packages`
     (requires an Internet connection).

  If `file_out` already exists, it will be overwritten without asking
  for confirmation.

  .. note::

    Almost all versions of COMPADRE / COMADRE work out-of-the-box with
    any version of matpopmod. However, there are a few exceptions -- see `here
    <#compadre-exceptions>`_ for a list of exceptions and additional details.
    
  """
  r_snippet = inspect.cleandoc(f"""
    # Convert COMPADRE/COMADRE from RData to JSON
    # Script generated by matpopmod <https://bienvenu.gitlab.io/matpopmod>
    if(length(find.package('jsonlite', quiet=TRUE)) == 0){{install.packages('jsonlite')}}
    library(jsonlite)
    database <- get(load(file.path('{file_in}')))
    write(toJSON(database), '{file_out}')
    print('Saved to: {file_out}')
    """)
  script = f"matpopmod.compadre.convert_{os.getpid()}.R"
  if os.path.exists(script):
    raise ValueError(f"{script} already exists. Aborting.")
  with open(script, 'w') as f:
    f.write(r_snippet)
  try:
    print(f"Starting conversion of {file_in}...")
    subprocess.check_output(["Rscript", script], stderr=subprocess.STDOUT)
    print(f"Done, saved to {file_out}.")
  except subprocess.CalledProcessError as ex:
    print("R execution failed. Possible causes include:\n"
          "  - Incorrect name for the input RData file.\n"
          "  - R not being installed or not being in the PATH.\n"
          "  - The version of R being too old or too recent to read the input RData file.\n"
          "  - The R package jsonlite not being installed and R failing to install it.\n"
          "See the debugging information below.")
    print("Python exception:", ex)
    print("R error message:", ex.output)
  finally:
    os.remove(script)


def fetch(database, version="latest", save_file=True, destination="."):
  """
  Fetches any version of COMPADRE/COMADRE directly from
  `compadre-db.org <https://compadre-db.org>`_ and loads it into Python.

  .. list-table::
    :widths: 15 85

    * - `database`
      - Either ``"compadre"`` or ``"comadre"``.
    * - `version`
      - Use ``"latest"`` (the default) to get the latest version of the database,
        and a (properly formatted) version string such as ``"6.21.8.0"``
        to get a specific version.
    * - `save_file`
      - Whether to save the JSON database locally, after converting it.
    * - `destination`
      - Where to save the JSON database, if applicable.
  
  Examples of use::

    # Fetch the latest version of COMPADRE (as of 24/09/21)
    latest = matpopmod.compadre.fetch("compadre") 
    # Fetch version 6.20.5.0
    older = matpopmod.compadre.fetch("compadre", "6.20.5.0")

  .. rst-class:: nospaceafter

  Note that this requires a working and properly configured installation
  of R -- see :func:`convert` for details. If R is not available, you can
  download the following pre-converted latest versions of the databases
  (as of |SHORT DATE COMPADRE|) and load them using :func:`load`:

  - |COMPADRE JSON|
  - |COMADRE JSON|.

  """
  def aux_get_latest_db_name(dbname):
    # Getting the name of the latest version from the webpage; slightly hacky
    aux = urllib.request.urlopen("https://compadre-db.org/Data/" + dbname)
    page_source = aux.read().decode("utf-8")
    regexp_result = re.search(
      "https://compadre-db.org/Data/Download/(.*).RData", page_source)
    return regexp_result.group(1)

  base_url = "https://www.compadre-db.org/Data/Download/"
  if database in ("compadre", "COMPADRE") :
    if version == "latest":
     db_name = aux_get_latest_db_name("Compadre") # (with a capital)
    else:
      if not version in COMPADRE_VERSIONS:
        wrn_msg = (
          "Unknown version of the database.\n"
          "Either you are using a version more recent than " +
          COMPADRE_VERSIONS[0] + ",\n"
          "in which case you can ignore this message; "
          "or you have mistyped the version number.\n"
          "See matpopmod.compadre.COMPADRE_VERSIONS for a list of known versions.")
        warnings.warn(wrn_msg)
      db_name = "COMPADRE_v." + version
  elif database in ("comadre", "COMADRE"):
    if version == "latest":
      db_name = aux_get_latest_db_name("Comadre") # (with a capital)
    else:
      if not version in COMADRE_VERSIONS:
        wrn_msg = (
          "Unknown version of the database.\n"
          "Either you are using a version more recent than " +
          COMADRE_VERSIONS[0] + ",\n"
          "in which case you can ignore this message; "
          "or you have mistyped the version number.\n"
          "See matpopmod.compadre.COMADRE_VERSIONS for a list of known versions.")
        warnings.warn(wrn_msg)
      db_name = "COMADRE_v." + version
  else:
    raise ValueError("Database should be either 'compadre' or 'comadre'")
  url = base_url + db_name + ".RData"

  try:
    print(f"Trying to download {url}...")
    local_filename, _ = urllib.request.urlretrieve(url)
    print(f"Done. Temporary file stored in {local_filename}.")
    if save_file:
      file_out = os.path.join(destination, (db_name + ".json"))
    else:
      TMP_FOLDER = os.path.dirname(local_filename)
      file_out = os.path.join(TMP_FOLDER, (db_name + ".json"))

    convert(local_filename, file_out)

    print("Loading database in Python...")
    db = load(file_out) 
    print("Done.")

  except urllib.error.ContentTooShortError:
    print("Download failed. Was there a network error?")
    db = None
  except urllib.error.HTTPError as ex:
    print(f"Download failed with HTTP status code {ex.code}")
    print("See if you can download the file from www.compadre-db.org "
          "and convert it using matpopmod.compadre.convert.")
    db = None
  finally:
    try:
      os.remove(local_filename)
      if not save_file:
        os.remove(file_out)
    except:
      pass

  return db

