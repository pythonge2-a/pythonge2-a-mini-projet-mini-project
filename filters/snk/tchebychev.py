class Tchebychev:
    def __init__(self):
        self.lowpass = self.LowPass()
        self.highpass = self.HighPass()

    class LowPass:
        def __init__(self):
            self.orders = {}

        def __getattr__(self, order):
            if not order.isdigit():
                raise AttributeError(f"L'ordre '{order}' n'est pas valide.")
            order = int(order)
            if order not in self.orders:
                self.orders[order] = self.FilterOrder(order)
            return self.orders[order]

        class FilterOrder:
            def __init__(self, order):
                self.order = order

            def components(self, r1, r2, c1, c2):
                r1 *= 2
                r2 *= 2
                c1 *= 2
                c2 *= 2
                print(f"Ordre {self.order} : R1={r1}, R2={r2}, C1={c1}, C2={c2}")
                return {"R1": r1, "R2": r2, "C1": c1, "C2": c2}

    class HighPass:
        def __init__(self):
            self.orders = {}

        def __getattr__(self, order):
            if not order.isdigit():
                raise AttributeError(f"L'ordre '{order}' n'est pas valide.")
            order = int(order)
            if order not in self.orders:
                self.orders[order] = self.FilterOrder(order)
            return self.orders[order]

        class FilterOrder:
            def __init__(self, order):
                self.order = order

            def components(self, r1, r2, c1, c2):
                r1 *= 3
                r2 *= 3
                c1 *= 3
                c2 *= 3
                print(f"Ordre {self.order} (HighPass) : R1={r1}, R2={r2}, C1={c1}, C2={c2}")
                return {"R1": r1, "R2": r2, "C1": c1, "C2": c2}
