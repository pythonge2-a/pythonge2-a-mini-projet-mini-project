import numpy as np
from scipy.signal import TransferFunction

class Bessel:
    def __init__(self):
        """Initialisation de la classe Bessel avec des données par défaut."""
        self.BESSEL_TABLE = {
            1: [(1.0, 0.0)],
            2: [(1.2723, 0.577)],
            3: [(1.3225, 0.0), (1.4474, 0.691)],
            4: [(1.431, 0.5219), (1.6043, 0.8055)],
        }

    def bessel_q0_omega0(self, order):
        """Retourne les valeurs de pulsation normalisée et de facteur de qualité pour un ordre donné."""
        if order not in self.BESSEL_TABLE:
            raise ValueError(f"L'ordre {order} n'est pas supporté.")
        return self.BESSEL_TABLE[order][0]  # Retourner omega0_norm et q0

    def sallen_key_lowpass(self, order, cutoff_freq, r1=None, r2=None, c1=None, c2=None):
        """Calcule la fonction de transfert Sallen-Key pour un filtre passe-bas Bessel."""
        if order < 1 or order > 10:
            raise ValueError("Ordre non supporté. Maximum : 10, minimum : 1.")

        # Récupérer Omega0 et Q0 normalisés
        omega0_norm, q0 = self.bessel_q0_omega0(order)
        print(f"Omega0_norm: {omega0_norm}, Q0: {q0}")
        omega0 = 2 * np.pi * cutoff_freq * omega0_norm

        if c1 is not None and c2 is not None:
            # Calculer R1 et R2 à partir de C1 et C2
            r1_plus_r2 = 1 / (omega0 * c2 * q0)
            r1_times_r2 = 1 / (omega0**2 * c1 * c2)

            # Résolution quadratique
            a = 1
            b = -r1_plus_r2
            c = r1_times_r2

            discriminant = (b)**2 - (4 * a * c)
            if discriminant < 0:
                raise ValueError("Les paramètres fournis pour C1 et C2 ne permettent pas un calcul valide de R1 et R2.")

            r1 = (-b + np.sqrt(discriminant)) / (2 * a)
            r2 = (-b - np.sqrt(discriminant)) / (2 * a)

        elif r1 is not None and r2 is not None:
            # Calculer C1 et C2 à partir de R1 et R2
            c2 = 1 / (omega0 * q0 * (r1 + r2))
            c1 = 1 / (omega0**2 * r1 * r2 * c2)
            if c1 <= 0 or c2 <= 0:
                raise ValueError("Les paramètres fournis pour R1 et R2 ne permettent pas un calcul valide de C1 et C2.")
        else:
            raise ValueError("Veuillez fournir soit (C1, C2), soit (R1, R2).")

        # Construire la fonction de transfert
        num = [1]
        den = [r1 * r2 * c1 * c2, (r1 * c1 + r2 * c1), 1]

        return TransferFunction(num, den), {"R1": r1, "R2": r2, "C1": c1, "C2": c2}


if __name__ == "__main__":
    try:
        # Initialisation de l'objet Bessel avec les données par défaut
        bessel = Bessel()

        # Exemple avec R1 et R2
        order = 2
        cutoff_freq = 1000  
        r1 = 1e3  
        r2 = 1e3  

        tf, params = bessel.sallen_key_lowpass(order, cutoff_freq, r1=r1, r2=r2)
        print("Fonction de transfert avec R1 et R2 :")
        print(tf)
        print("Paramètres calculés :", params)
       
        # Exemple avec C1 et C2
        c1 = 1.59e-6  
        c2 = 1.59e-9  

        tf, params = bessel.sallen_key_lowpass(order, cutoff_freq, c1=c1, c2=c2)
        print("\nFonction de transfert avec C1 et C2 :")
        print(tf)
        print("Paramètres calculés :", params)

    except ValueError as e:
        print("Erreur:", e)
