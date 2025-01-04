import math
import csv
import os

_PARAM_TABLE = {}

def _load_csv_params():
    # On part du principe que le CSV est dans docs/table.csv
    csv_path = os.path.join("docs", "table.csv")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if not row:
                continue
            try:
                ordre = int(row[0])
            except ValueError:
                continue

            # On lit dans les 2 dernières colonnes => Tchebychev (r=1 dB) wk/wr, Qk
            wkwr_str = row[-2].strip()
            qk_str   = row[-1].strip()

            if wkwr_str not in ["-", ""] and qk_str not in ["-", ""]:
                try:
                    wkwr_val = float(wkwr_str)
                    qk_val   = float(qk_str)
                    _PARAM_TABLE[ordre] = {"wkwr": wkwr_val, "qk": qk_val}
                except ValueError:
                    pass

def get_params_for_order(ordre):
    """
    Renvoie { "wkwr": <float>, "qk": <float> } pour l'ordre demandé.
    Lève KeyError si l'ordre n'est pas dans _PARAM_TABLE.
    """
    return _PARAM_TABLE[ordre]

# On charge le CSV dès l'import
_load_csv_params()


class FilterType:
    def __init__(self, filter_type):
        self.filter_type = filter_type
        self.orders = {}

    def __getattr__(self, name):
        if name.startswith("order"):
            suffix = name[len("order"):]
            if suffix.isdigit():
                order = int(suffix)
                if 1 <= order <= 10:
                    if order not in self.orders:
                        self.orders[order] = FilterOrder(self.filter_type, order)
                    return self.orders[order]
                raise AttributeError(f"'{name}' => ordre {suffix} invalide (1..10).")
            else:
                raise AttributeError(f"'{name}' doit se terminer par un chiffre.")
        raise AttributeError(f"Attribut '{name}' inconnu pour FilterType({self.filter_type}).")


class FilterOrder:
    def __init__(self, filter_type, order):
        self.filter_type = filter_type
        self.order = order

    def __call__(self, f, **kwargs):
        # Récupération depuis le CSV
        params = get_params_for_order(self.order)
        wkwr = params["wkwr"]  # ex: 1.1589
        qk   = params["qk"]    # ex: 1.0785

        # Inversion si le filtre est "hp"
        if self.filter_type == "hp":
            wkwr = 1 / wkwr

        # Arrondi de wkwr à 4 décimales
        wkwr = round(wkwr, 4)

        # Calcul de la pulsation
        wa = 2 * math.pi * f * wkwr

        provided_res = [k for k in kwargs if k.startswith("R")]
        provided_caps = [k for k in kwargs if k.startswith("C")]

        if provided_res and provided_caps:
            raise ValueError("Ne mélangez pas R* et C* dans le même appel.")

        if len(provided_caps) == self.order:
            C_values = [kwargs[f"C{i}"] for i in range(1, self.order + 1)]
            C1, C2 = C_values
            R1 = 1 / (qk * wa * (C1 + C2))
            R2 = 1 / ((wa ** 2) * C1 * C2 * R1)
            calc_res = {f"R{i+1}": (R1 if i == 0 else R2) for i in range(self.order)}
            components = {**kwargs, **calc_res}

        elif len(provided_res) == self.order:
            R_values = [kwargs[f"R{i}"] for i in range(1, self.order + 1)]
            R1, R2 = R_values
            C1 = 1 / (qk * wa * R1)
            C2 = 1 / ((wa ** 2) * R1 * R2)
            calc_caps = {f"C{i+1}": (C1 if i == 0 else C2) for i in range(self.order)}
            components = {**kwargs, **calc_caps}

        else:
            raise ValueError("Nombre de R* ou C* fourni incorrect pour un ordre=2.")

        return {
            "order": self.order,
            "filter_type": self.filter_type,
            "frequency": f,
            "wkwr_used": wkwr,  # on renvoie la valeur arrondie
            "qk": qk,
            "components": components
        }


# Singletons
lp = FilterType("lp")
hp = FilterType("hp")
