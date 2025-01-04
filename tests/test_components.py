import unittest
import filters.snk.tchebychev  # On importe le module complet

class TestTchebychevFilters(unittest.TestCase):
    def test_lowpass_order2(self):
        call_str = "filters.snk.tchebychev.lp.order2(f=2500, C1=1e-6, C2=2e-6)"
        print(f"\nEntrée : {call_str}")

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


if __name__ == "__main__":
    unittest.main()
