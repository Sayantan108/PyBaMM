#
# Tests for the lithium-ion DFN model
#
import pybamm
import unittest


class TestDFN(unittest.TestCase):
    def test_well_posed(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_2plus1D(self):
        options = {"current collector": "potential pair", "dimensionality": 1}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

        options = {"current collector": "potential pair", "dimensionality": 2}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

        options = {"bc_options": {"dimensionality": 5}}
        with self.assertRaises(pybamm.OptionError):
            model = pybamm.lithium_ion.DFN(options)

    def test_lumped_thermal_model_1D(self):
        options = {"thermal": "x-lumped"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_x_full_thermal_model(self):
        options = {"thermal": "x-full"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_x_full_Nplus1D_not_implemented(self):
        # 1plus1D
        options = {
            "current collector": "potential pair",
            "dimensionality": 1,
            "thermal": "x-full",
        }
        with self.assertRaises(NotImplementedError):
            pybamm.lithium_ion.DFN(options)
        # 2plus1D
        options = {
            "current collector": "potential pair",
            "dimensionality": 2,
            "thermal": "x-full",
        }
        with self.assertRaises(NotImplementedError):
            pybamm.lithium_ion.DFN(options)

    def test_lumped_thermal_1plus1D(self):
        options = {
            "current collector": "potential pair",
            "dimensionality": 1,
            "thermal": "lumped",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_lumped_thermal_2plus1D(self):
        options = {
            "current collector": "potential pair",
            "dimensionality": 2,
            "thermal": "lumped",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_thermal_1plus1D(self):
        options = {
            "current collector": "potential pair",
            "dimensionality": 1,
            "thermal": "x-lumped",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_thermal_2plus1D(self):
        options = {
            "current collector": "potential pair",
            "dimensionality": 2,
            "thermal": "x-lumped",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_particle_uniform(self):
        options = {"particle": "uniform profile"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_particle_quadratic(self):
        options = {"particle": "quadratic profile"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_particle_quartic(self):
        options = {"particle": "quartic profile"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_particle_shape_user(self):
        options = {"particle shape": "user"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_loss_active_material(self):
        options = {
            "loss of active material": "none",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_loss_active_material_negative(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "negative",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_loss_active_material_positive(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "positive",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_loss_active_material_both(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "both",
        }
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_surface_form_differential(self):
        options = {"surface form": "differential"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_surface_form_algebraic(self):
        options = {"surface form": "algebraic"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_electrolyte_options(self):
        options = {"electrolyte conductivity": "integrated"}
        with self.assertRaisesRegex(pybamm.OptionError, "electrolyte conductivity"):
            pybamm.lithium_ion.DFN(options)


class TestDFNWithSEI(unittest.TestCase):
    def test_well_posed_constant(self):
        options = {"sei": "constant"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_reaction_limited(self):
        options = {"sei": "reaction limited"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_reaction_limited_average_film_resistance(self):
        options = {"sei": "reaction limited", "sei film resistance": "average"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_solvent_diffusion_limited(self):
        options = {"sei": "solvent-diffusion limited"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_electron_migration_limited(self):
        options = {"sei": "electron-migration limited"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_interstitial_diffusion_limited(self):
        options = {"sei": "interstitial-diffusion limited"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_ec_reaction_limited(self):
        options = {"sei": "ec reaction limited", "sei porosity change": "true"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()


class TestDFNWithCrack(unittest.TestCase):
    def test_well_posed_none_crack(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "none"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_no_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "no cracking"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_negative_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "negative"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_positive_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "positive"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_both_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "both"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()


class TestDFNWithPlating(unittest.TestCase):
    def test_well_posed_none_plating(self):
        options = {"lithium plating": "none"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_reversible_plating(self):
        options = {"lithium plating": "reversible"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()

    def test_well_posed_irreversible_plating(self):
        options = {"lithium plating": "irreversible"}
        model = pybamm.lithium_ion.DFN(options)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
