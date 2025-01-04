import unittest
from filters.passives import BandPassFilter

 # ENCORE AJOUTER LES TESTS POUR LES AUTRES METHODES DE LA CLASSE
class TestBandPassFilter(unittest.TestCase):

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
            self.assertAlmostEqual(resonant_frequency, 1591.55, places=2)
            self.assertAlmostEqual(quality_factor, 0.1, places=2)
            self.assertAlmostEqual(bandwidth, 15915.49, places=2)

        except ValueError as e:
            self.fail(f"Erreur inattendue : {e}")
