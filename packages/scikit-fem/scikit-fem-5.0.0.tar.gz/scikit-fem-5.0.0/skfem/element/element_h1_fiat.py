"""Wrapper around FIAT elements.

from skfem import *
from skfem.element.element_h1_fiat import ElementH1FIAT
from skfem.models import laplace
import FIAT

m = MeshTri()
e = ElementH1FIAT(FIAT.Lagrange(FIAT.reference_element.UFCTriangle(), 2))
basis = Basis(m, e)
A = laplace.assemble(basis)

"""

import numpy as np
from .element_h1 import ElementH1
from ..refdom import *
from ..generic_utils import hash_args


class ElementH1FIAT(ElementH1):
    """WIP: Supports only UFCTriangle."""

    def __init__(self, elem):
        self.elem = elem
        self.maxdeg = elem.degree()
        self.nodal_dofs = len(elem.entity_dofs()[0][0])
        self.facet_dofs = len(elem.entity_dofs()[1][0])
        self.interior_dofs = len(elem.entity_dofs()[2][0])
        self.refdom = {
            'UFCTriangle': RefTri
        }[elem.get_reference_element().__class__.__name__]
        self._cache = {}

    def lbasis(self, X, i):
        Xh = hash_args(X)
        if Xh not in self._cache:
            self._cache[Xh] = self.elem.tabulate(1, X.T)
        tab = self._cache[Xh]

        # flip facet dof indices
        if (i >= self.refdom.nnodes * self.nodal_dofs
            and i < (self.refdom.nnodes * self.nodal_dofs
                     + self.refdom.nfacets * self.facet_dofs)):
            j = i - self.refdom.nnodes * self.nodal_dofs
            j = np.floor(j / self.facet_dofs)
            if j == 0:
                i = i + 2 * self.facet_dofs
            else:
                i = i - self.facet_dofs

        return tab[(0, 0)][i], np.array([tab[(1, 0)][i], tab[(0, 1)][i]])
