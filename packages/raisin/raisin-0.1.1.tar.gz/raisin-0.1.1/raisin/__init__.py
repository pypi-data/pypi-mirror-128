#!/usr/bin/env python3

r"""
** Raisin: To perform cluster work easily! **
---------------------------------------------

The main aim of project *raisin* is to **share physical resources** of your laptop
with a community.
In counterpart, you can **benefit from the community resources**.

Notes
-----
* To generate the documentation, you have to install the package *pdoc3* with *pip* for example.
    Then, you just have to type the following command to generate the html files:
    * ``pdoc3 raisin/ -c latex_math=True --force --html``
* To run the test benches, you have to install the package *pytest* with *pip* for example.
    Then you have to type the following command:
    * ``clear && python3 -m pytest --doctest-modules raisin/``
* Docstrings respect the following convention:
    * ``https://numpydoc.readthedocs.io/en/latest/format.html``
"""

import inspect

from raisin.serialization import (deserialize, dump, dumps, load,
    loads, serialize)


__version__ = '3.0.0'
__author__  = 'Robin RICHARD (robinechuca) <raisin@ecomail.fr>'
__license__ = 'GNU Affero General Public License v3 or later (AGPLv3+)'
__all__ = ['deserialize', 'dump', 'dumps', 'load', 'loads', 'serialize']
__pdoc__ = {obj: 'Alias to ``raisin.{}.{}``'.format(
            (inspect.getsourcefile(globals()[obj]).split('raisin/')[-1][:-3]
            ).replace('/', '.').replace('.__init__', ''),
            obj) for obj in __all__}
__pdoc__ = {**__pdoc__, **{f'{cl}.{meth}': False
            for cl in __all__ if globals()[cl].__class__.__name__ == 'type'
            for meth in globals()[cl].__dict__ if not meth.startswith('_')}}


class _Temprep:
    """
    cree puis detruit un dossier temporaire
    la representation de cet objet est le chemin absolu de ce repertoire
    """
    def __init__(self, destroy=True):
        self.destroy = destroy              # True imposse de supprimer le repertoir a la fin, False le laisse en vie
        self.temprep = None                 # creation du repertoire contenant tous les droits

    def __call__(self):
        if self.temprep is None:
            from tempfile import mkdtemp
            self.temprep = mkdtemp()
        return self.temprep

    def __repr__(self):
        return self.__call__()

    def __str__(self):
        return self.__call__()

    def __del__(self):
        if self.destroy and self.temprep:
            try:
                shutil.rmtree(self.temprep)
            except KeyboardInterrupt as err:
                raise err from err
            except Exception as err:
                try:
                    from importlib import reload
                    import shutil
                    reload(shutil)
                    shutil.rmtree(self.temprep)
                except Exception as err:
                    pass

TEMPREP = _Temprep()
