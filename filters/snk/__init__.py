# __init__.py
import butterworth as bt
import bessel as bl

class SallenAndKey:
    def __init__(self):
        self.lowpass = bl.Lowpass()  # Initialiser une instance de Lowpass
        return None

    def test_des_functions(self):
        bt.Butterworth_LowPass.components(1, "200k")
        return None

# Point d'entrée
if __name__ == "__main__":
    highpass = bl.Highpass()

    # Exemple avec R1 et R2 fournis
    results = highpass.sallen_key_highpass(2, 2000, r1=1000, r2=2200)

    # Affichage des résultats
    for i, result in enumerate(results):
        print(f"Solution {i + 1}:")
        print("Fonction de transfert :", result["tf"])
        print("Paramètres calculés :", result["params"])

