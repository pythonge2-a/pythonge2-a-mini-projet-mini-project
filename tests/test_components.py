import unittest
<<<<<<< HEAD
import filters.snk.tchebychev  # On importe le module complet

class TestTchebychevFilters(unittest.TestCase):
    def test_lowpass_order2(self):
        call_str = "filters.snk.tchebychev.lp.order2(f=2500, C1=1e-6, C2=2e-6)"
        print(f"\nEntrée : {call_str}")
=======

##from filters import Filters
from filters.passives import BandPassFilter


class TestComponents(unittest.TestCase):

    def setUp(self):
        self.filters = Filters()
>>>>>>> aa374c32ceb40b83f37cfd087a3ad5fa299573a8

        result = filters.snk.tchebychev.lp.order2(
            f=2500,
            C1=1e-6,
            C2=2e-6
        )
        print("Sortie :", result)

        self.assertEqual(result["order"], 2)
        self.assertEqual(result["filter_type"], "lp")
        self.assertIn("components", result)

    def test_highpass_order2(self):
        call_str = "filters.snk.tchebychev.hp.order2(f=5000, C1=1e-6, C2=1.5e-6)"
        print(f"\nEntrée : {call_str}")

        result = filters.snk.tchebychev.hp.order2(
            f=5000,
            C1=1e-6,
            C2=1.5e-6
        )
        print("Sortie :", result)

        self.assertEqual(result["order"], 2)
        self.assertEqual(result["filter_type"], "hp")
        self.assertIn("components", result)


    def test_band_pass(self):
        # Définitions des entrées
        L = 10e-3  # Inductance en henrys
        C = 1e-6  # Capacité en farads
        R = 1000  # Résistance en ohms

        print(f"\nTest BandPassFilter :\nEntrées : L={L}, C={C}, R={R}")

        try:
            # Calculs pour le filtre passe-bande
            resonant_frequency = BandPassFilter.resonant_frequency(L, C)
            quality_factor = BandPassFilter.quality_factor(R, L, C)
            bandwidth = BandPassFilter.bandwidth(resonant_frequency, quality_factor)

            # Résultats attendus
            print(
                f"Résultats calculés :\n"
                f"- Fréquence de résonance : {resonant_frequency:.2f} Hz\n"
                f"- Facteur de qualité : {quality_factor:.2f}\n"
                f"- Bande passante : {bandwidth:.2f} Hz"
            )

            # Assertions
            self.assertAlmostEqual(resonant_frequency, 159.15, places=2)
            self.assertAlmostEqual(quality_factor, 3.16, places=2)
            self.assertAlmostEqual(bandwidth, 50.37, places=2)

        except ValueError as e:
            self.fail(f"Erreur inattendue : {e}")


if __name__ == "__main__":
    unittest.main()
