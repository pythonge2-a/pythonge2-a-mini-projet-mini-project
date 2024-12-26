class Tchebychev:
    def __init__(self):
        # Initialisation dynamique des ordres
        self.orders = {}

    def __getattr__(self, name):
        # Permet d'accéder dynamiquement à "2", "3", etc.
        if name.isdigit():
            order = int(name)
            if order not in self.orders:
                self.orders[order] = FilterOrder(order)
            return self.orders[order]
        raise AttributeError(f"{name} n'est pas un attribut valide.")

class FilterOrder:
    def __init__(self, order):
        self.order = order

    def components(self, r1, r2, c1, c2):
        r1 *= self.order
        r2 *= self.order
        c1 *= self.order
        c2 *= self.order
        return {"R1": r1, "R2": r2, "C1": c1, "C2": c2}