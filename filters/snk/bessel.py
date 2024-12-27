import numpy as np
from scipy.signal import TransferFunction

class Lowpass:
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
        return self.BESSEL_TABLE[order]  # Retourne tous les pôles

    def sallen_key_lowpass(self, omega0, q0, cutoff_freq, r1=None, r2=None, c1=None, c2=None):
        """Calcule une cellule Sallen-Key pour un filtre passe-bas."""
        if q0 == 0:
            raise ValueError("Le facteur de qualité Q0 est nul. Vérifiez les données de la table de Bessel.")
        
        
        # Ajuster omega0 à partir de la fréquence de coupure
        omega0_real = omega0 * 2 * np.pi * cutoff_freq  # Pulsation réelle du filtre

        if c1 is not None and c2 is not None:
            # Calculer R1 et R2 à partir de C1 et C2
            if c1 <= 0 or c2 <= 0:
                raise ValueError("Les valeurs de C1 et C2 doivent être strictement positives.")
            r1_plus_r2 = 1 / (omega0_real * c2 * q0)
            r1_times_r2 = 1 / (omega0_real**2 * c1 * c2)
            a, b, c = 1, -r1_plus_r2, r1_times_r2
            discriminant = (b)**2 - (4 * a * c)
            if discriminant < 0:
                raise ValueError("C1 et C2 non valides pour calculer R1 et R2 (discriminant négatif).")
            r1 = (-b + np.sqrt(discriminant)) / (2 * a)
            r2 = (-b - np.sqrt(discriminant)) / (2 * a)

        elif r1 is not None and r2 is not None:
            # Calculer C1 et C2 à partir de R1 et R2
            if r1 + r2 == 0:
                raise ValueError("La somme R1 + R2 ne peut pas être nulle.")
            c2 = 1 / (omega0_real * q0 * (r1 + r2))
            c1 = 1 / (omega0_real**2 * r1 * r2 * c2)
            if c1 <= 0 or c2 <= 0:
                raise ValueError("R1 et R2 non valides pour calculer C1 et C2 (valeurs négatives ou nulles).")

        else:
            raise ValueError("Fournir (R1, R2) ou (C1, C2).")

        # Fonction de transfert
        num = [1]
        den = [r1 * r2 * c1 * c2, (r1 * c1 + r2 * c1), 1]

        return TransferFunction(num, den), {"R1": r1, "R2": r2, "C1": c1, "C2": c2}

    def first_order_filter(self, omega0, cutoff_freq, r=None, c=None):
        """Calcule un filtre du premier ordre."""
        omega_c = 2 * np.pi * cutoff_freq 
        if r is not None:
            c = 1 / (omega_c * r)
        elif c is not None:
            r = 1 / (omega_c * c)
        else:
            raise ValueError("Fournir R ou C.")
        num = [1]
        den = [r * c, 1]
        return TransferFunction(num, den), {"R": r, "C": c}

    def multi_stage_lowpass(self, order, cutoff_freq, components):
        """Calcule un filtre d'ordre 3 en utilisant une SNK d'ordre 1 et d'ordre 2."""
        poles = self.bessel_q0_omega0(order)
        stages = []
        params = []

        # Vérification si l'utilisateur a fourni les bons composants
        if 'r1' in components and 'r2' in components and 'r3' in components:
            # Si l'utilisateur fournit des résistances, calculer les condensateurs
            first_pole = poles[0]
            second_pole = poles[1]

            omega0_1, _ = first_pole
            tf1, param1 = self.first_order_filter(omega0_1, cutoff_freq, r=components["r1"])
            stages.append(tf1)
            params.append(param1)

            omega0_2, q0_2 = second_pole
            # Utilisation de résistances et calcul des condensateurs associés
            tf2, param2 = self.sallen_key_lowpass(omega0_2, q0_2, cutoff_freq, r1=components["r2"], r2=components["r3"])
            print(omega0_2)
            print(q0_2)
            print(cutoff_freq)
            print(components)
            stages.append(tf2)
            params.append(param2)

        elif 'c1' in components and 'c2' in components and 'c3' in components:
            # Si l'utilisateur fournit des condensateurs, calculer les résistances
            first_pole = poles[0]
            second_pole = poles[1]

            omega0_1, _ = first_pole
            tf1, param1 = self.first_order_filter(omega0_1, cutoff_freq, c=components["c1"])
            stages.append(tf1)
            params.append(param1)

            omega0_2, q0_2 = second_pole
            # Utilisation de condensateurs et calcul des résistances associés
            tf2, param2 = self.sallen_key_lowpass(omega0_2, q0_2, cutoff_freq, c1=components["c2"], c2=components["c3"])
            stages.append(tf2)
            params.append(param2)

        else:
            raise ValueError("Fournir soit (r1, r2, r3) soit (c1, c2, c3).")

        return stages, params


if __name__ == "__main__":
    lowpass_filter = Lowpass()

    # Exemple pour ordre 3 avec résistances
    order = 3
    cutoff_freq = 1000  # Fréquence de coupure
    components = {"r1": 1e3, "r2": 1e3, "r3": 1e3}  # Exemple avec R1, R2, R3

    stages, params = lowpass_filter.multi_stage_lowpass(order, cutoff_freq, components)
    print(f"Filtre d'ordre {order} avec résistances :")
    for i, (stage, param) in enumerate(zip(stages, params), 1):
        print(f"\nStage {i} :")
        print(stage)
        print("Paramètres :", param)

    # Exemple pour ordre 3 avec condensateurs
    components = {"c1": 1e-6, "c2": 1e-6, "c3": 1e-9}  # Exemple avec C1, C2, C3

    stages, params = lowpass_filter.multi_stage_lowpass(order, cutoff_freq, components)
    print(f"\nFiltre d'ordre {order} avec condensateurs :")
    for i, (stage, param) in enumerate(zip(stages, params), 1):
        print(f"\nStage {i} :")
        print(stage)
        print("Paramètres :", param)
