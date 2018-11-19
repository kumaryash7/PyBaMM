#
# Tests for the electrolyte class
#
import pybamm

import numpy as np
from numpy.linalg import norm

import unittest


class TestElectrolyte(unittest.TestCase):
    def test_cation_conservation_finite_volumes_convergence(self):
        electrolyte = pybamm.Electrolyte()

        # Finite volume only has h**2 convergence if the mesh is uniform?
        uniform_lengths = {"Ln": 1e-3, "Ls": 1e-3, "Lp": 1e-3}
        param = pybamm.Parameters(optional_parameters=uniform_lengths)

        # Test convergence
        ns = [100, 200, 400]
        errs = [0] * len(ns)
        for i, n in enumerate(ns):
            # Set up
            mesh = pybamm.Mesh(param, n)
            param.set_mesh_dependent_parameters(mesh)
            c0 = np.cos(2 * np.pi * mesh.xc)
            operators = {"xc": pybamm.Operators("Finite Volumes", "xc", mesh)}
            lbc = np.array([0])
            rbc = np.array([0])
            dcdt_exact = -4 * np.pi ** 2 * c0

            # Calculate solution and errors
            electrolyte.set_simulation(param, operators, mesh)

            dcdt = electrolyte.cation_conservation(c0, 0, (lbc, rbc))
            errs[i] = norm(dcdt - dcdt_exact) / norm(dcdt_exact)

        # Expect h**2 convergence
        [
            self.assertLess(errs[i + 1] / errs[i], 0.26)
            for i in range(len(errs) - 1)
        ]


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()
