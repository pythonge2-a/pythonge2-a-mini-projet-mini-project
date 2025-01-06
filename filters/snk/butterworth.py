import numpy as np
from scipy.signal import TransferFunction

class Butterworth_LowPass:
    def __init__(self):    
        # Tableau des pulsations et facteurs de qualité des filtres passe-bas normalisés
        self.BUTTERWORTH_TABLE = {
            1: [(1.0, 0.0)],
            2: [(1.0, 0.7071)],
            3: [(1.0, 0.0), (1.0, 1.0)],
            4: [(1.0, 0.5412), (1.0, 1.3066)],
            5: [(1.0, 0.0), (1.0, 0.6180), (1.0, 1.6180)],
            6: [(1.0, 0.5176), (1.0, 0.7071), (1.0, 1.9319)],
            7: [(1.0, 0.0000), (1.0, 0.5550), (1.0, 0.8019), (1.0, 2.2470)],
            8: [(1.0, 0.5098), (1.0, 0.6013), (1.0, 0.8999), (1.0, 2.5629)],
            9: [(1.0, 0.0000), (1.0, 0.5321), (1.0, 0.6527), (1.0, 1.0), (1.0, 2.8794)],
           10: [(1.0, 0.5062), (1.0, 0.5612), (1.0, 0.7071), (1.0, 1.1013), (1.0, 3.1962)],
        }

    def components(self, order, cutoff_frequency=None, r1=None, r2=None, c1=None, c2=None, omega_Zero=None, q0=None):
        # Verifie si l'ordre du filtre est entre 1 et 10
        if order not in self.BUTTERWORTH_TABLE:
            raise ValueError(f"L'ordre {order} n'est pas supporté.")
        
        # Calul d'un filtre d'ordre 1
        if order is 1:
            if omega_Zero is None:
                omega_Zero = 1.0
            omega0 = 2 * np.pi * cutoff_frequency * omega_Zero
            if r1 is not None:
                if r1 <= 0:
                    raise ValueError("La valeur de R1 ne doit pas être nulle ou négatif.")
                c1 = 1 / (omega0 * r1)
            elif c1 is not None:
                if c1 <= 0:
                    raise ValueError("La valeur de C1 ne doit pas être nulle ou négatif.")
                r1 = 1 / (omega0 * c1)
            else:
                raise ValueError("Il faut au moin un composant comme paramètre d'entrée.")
            num = [1]
            den = [r1 * c1, 1]
            return TransferFunction(num, den), {"R": r1, "C": c1}
    
        # calcul d'un filtre d'ordre 2
        if order is 2:
            if omega_Zero is None:
                raise ValueError("Les valeurs W0 et Q0 doivent etre fournies.")
            omega0 = 2 * np.pi * cutoff_frequency * omega_Zero
            # Calcul avec C1 et C2 connus
            if c1 is not None and c2 is not None:
                if c2 <= 0 or c1 <= 0:
                    raise ValueError("Les paramètres fournis pour C1 et C2 ne doivent pas être nulls ou négatifs.")
                if q0**2 <= c1/(c2*4):
                    raise ValueError("Les paramètres fournis pour C1 et C2 ou Q0 ne permettent pas un calcul valide de R1 et R2")
                r1_plus_r2 = 1 / (omega0 * c2 * q0)
                r1_times_r2 = 1 / (omega0**2 * c1 * c2)
                b = -r1_plus_r2
                c = r1_times_r2
                discriminant = b**2 - 4 * c
                if np.sqrt(discriminant) < 0:
                    raise ValueError("Discriminant plus petit que 0.")
                r2a_Calculer = (-b + np.sqrt(discriminant)) / 2
                r2b_Calculer = (-b - np.sqrt(discriminant)) / 2
                r1a_Calculer = r1_plus_r2 - r2a_Calculer
                r1b_Calculer = r1_plus_r2 - r2b_Calculer
                num = [1]
                den1 = [r1a_Calculer * r2a_Calculer * c1 * c2, (r2a_Calculer + r2a_Calculer) * c2, 1]
                den2 = [r1b_Calculer * r2b_Calculer * c1 * c2, (r1b_Calculer + r2b_Calculer) * c2, 1]
                tf1 = TransferFunction(num, den1)
                tf2 = TransferFunction(num, den2)
                return [
                    {"tf": tf1, "params": {"R1": r1a_Calculer, "R2": r2a_Calculer, "C1": c1, "C2": c2}},
                    {"tf": tf2, "params": {"R1": r1b_Calculer, "R2": r2b_Calculer, "C1": c1, "C2": c2}},
                ]
            # Calcul avec R1 et R2 connues
            if r1 is not None and r2 is not None:
                if r2 <= 0 or r1 <= 0:
                    raise ValueError("Les paramètres fournis pour C1 et C2 ne doivent pas être nulls ou négatifs.")
                c2_Calculer = 1/((r1 + r2)*omega_Zero*q0)
                c1_Calculer = (r1 + r2)*q0 / (r1 * r2 * omega_Zero)
                num = [1]
                den = [r1 * r2 * c1_Calculer * c2_Calculer, (r1 + r2) * c2_Calculer, 1]
                tf = TransferFunction(num, den)
                return [{"tf": tf, "params": {"R1": r1, "R2": r2, "C1": c1_Calculer, "C2": c2_Calculer}}]
            else:
                raise ValueError("Veuillez fournir C1 et C2 ou R1 et R2.")
            
        # Calcul d'un filtre d'ordre supérieur à 2 avec des cellules du 1er et 2ème ordre
        if order > 2:
            poles = self.BUTTERWORTH_TABLE[order]
            stages = []
            num_combined, den_combined = [1], [1]

            num_stages = order // 2 + (order % 2)
            num_elements = 2 * num_stages

            if r_vals is None:
                r_vals = [None] * num_elements
            if c_vals is None:
                c_vals = [None] * num_elements

            if len(r_vals) < num_elements:
                r_vals.extend([None] * (num_elements - len(r_vals)))
            if len(c_vals) < num_elements:
                c_vals.extend([None] * (num_elements - len(c_vals)))

            for i, (omega0_norm, q0) in enumerate(poles):
                if q0 == 0.0:
                    tf, params = self.first_order_highpass(
                        cutoff_freq, r=r_vals[i], c=c_vals[i], omega0_norm=omega0_norm
                    )
                else:
                    idx = 2 * i
                    tf_data = self.sallen_key_highpass(
                        order=2,
                        cutoff_freq=cutoff_freq,
                        r1=r_vals[idx],
                        r2=r_vals[idx + 1],
                        c1=c_vals[idx],
                        c2=c_vals[idx + 1],
                        omega0_norm=omega0_norm,
                        q0=q0,
                    )
                    tf = tf_data[0]["tf"]
                    params = tf_data[0]["params"]

                num_combined = np.polymul(num_combined, tf.num)
                den_combined = np.polymul(den_combined, tf.den)
                stages.append({"tf": tf, "params": params})

                combined_tf = TransferFunction(num_combined, den_combined)
                return combined_tf, stages
    
class HighPass:
    def __init__(self,order,cutoff_frequency):
        self.order = order
        self.cutoff_frequency = cutoff_frequency

    def transfer_function(self, frequency):
        w0 = 2 * math.pi * self.cutoff_frequency
        return 1 / math.sqrt(1 + (frequency / w0) ** (2*self.order))

class BandPass:
    def __init__(self,order,cutoff_frequency):
        self.order = order
        self.cutoff_frequency = cutoff_frequency

    def transfer_function(self, frequency):
        w0 = 2 * math.pi * self.cutoff_frequency
        return 1 / math.sqrt(1 + (frequency / w0) ** (2*self.order))