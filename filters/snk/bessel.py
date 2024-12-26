import numpy as np
from scipy.signal import TransferFunction


BESSEL_TABLE = {
    1: [(1.0, 0.0)],
    2: [(1.732, 0.577)],
    3: [(2.322, 0.805), (1.0, 0.0)],
    4: [(2.896, 0.867), (1.361, 0.618)],
}

def bessel_q0_omega0(order):
    """
    Récupère les valeurs normalisées Omega0 et Q0 depuis la table Bessel.
    """
    if order not in BESSEL_TABLE:
        raise ValueError(f"L'ordre {order} n'est pas supporté.")
    return BESSEL_TABLE[order][0]  # On prend les valeurs du premier pôle

def sallen_key_lowpass(order, cutoff_freq, r1=None, r2=None, c1=None, c2=None):
    """
    Génère un filtre passe-bas Bessel avec une cellule Sallen-Key.
    L'utilisateur peut fournir :
    - (R1, R2) pour calculer C1 et C2
    - (C1, C2) pour calculer R1 et R2
    """
    if order < 1 or order > 10:
        raise ValueError("Ordre non supporté. Maximum : 10, minimum : 1.")

    # Récupérer Omega0 et Q0 normalisés
    omega0_norm, q0 = bessel_q0_omega0(order)
    print(q0)
    omega0 = 2 * np.pi * cutoff_freq *omega0_norm

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
        # Exemple avec R1 et R2
        order = 2
        cutoff_freq = 1000  # Hz
        r1 = 1e3  # Ohms
        r2 = 1e3  # Ohms

        tf, params = sallen_key_lowpass(order, cutoff_freq, r1=r1, r2=r2)
        print("Fonction de transfert avec R1 et R2 :")
        print(tf)
        print("Paramètres calculés :", params)
       

        # Exemple avec C1 et C2
        c1 = 1.59e-6  # F
        c2 = 1.59e-9  # F

        tf, params = sallen_key_lowpass(order, cutoff_freq, c1=c1, c2=c2)
        print("\nFonction de transfert avec C1 et C2 :")
        print(tf)
        print("Paramètres calculés :", params)

    except ValueError as e:
        print("Erreur:", e)