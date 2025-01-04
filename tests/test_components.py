import unittest

##from filters import Filters
from filters.passives import BandPassFilter


class TestComponents(unittest.TestCase):

    def setUp(self):
        self.filters = Filters()

    def test_tchebychev_order_2(self):
        # Définitions des entrées
        r1, r2, c1, c2 = 1000, 2000, 1e-6, 2e-6
        print(f"\nFonction : filters.snk.tchebychev.2.components")
        print(f"Entrée : r1={r1}, r2={r2}, c1={c1}, c2={c2}")

        # Appel de la méthode
        result = getattr(self.filters.snk.tchebychev, "2").components(r1, r2, c1, c2)
        print(f"Sortie : {result}\n")

        # Résultat attendu
        expected_result = {"R1": 2000, "R2": 4000, "C1": 2e-06, "C2": 4e-06}
        self.assertEqual(result, expected_result)

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
