import math


class LowPassFilter:
    @staticmethod
    def cutoff_frequency_order_1(R, C):
        """
        Calculate the cutoff frequency of a low-pass RLC filter order 1.

        Parameters:
        R (float): Resistance
        C (float): Capacitance

        Return:
        float: Cutoff frequency
        """

        if C <= 0 or R <= 0:
            raise ValueError("Capacitance and resistance must be positive.")
        return 1 / (2 * math.pi * R * C)

    @staticmethod
    def cutoff_frequency_order_2(R1, R2, C1, C2):
        """
        Calculate the cutoff frequency of a low-pass RLC filter order 2.

        Parameters:
        R1 (float): Resistance 1
        R2 (float): Resistance 1
        C1 (float): Capacitance 1
        C2 (float): Capacitance 2

        Return:
        float: Cutoff frequency
        """

        if R1 <= 0 or R2 <= 0 or C1 <= 0 or C2 <= 0:
            raise ValueError("Resistances and capacitances must be positive.")
        return 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))

    @staticmethod
    def cutoff_frequency_rlc(L, C):
        """
        Calculate the cutoff frequency of a low-pass RLC filter.

        Parameters:
        L (float): Inductance in henries
        C (float): Capacitance in farads

        Return:
        float: Cutoff frequency
        """
        if L <= 0 or C <= 0:
            raise ValueError("Inductance and capacitance must be positive.")
        return 1 / (2 * math.pi * math.sqrt(L * C))

    @staticmethod
    def quality_factor_rlc(R, L, C):
        """
        Calculate the quality factor of a low-pass RLC filter.

        Parameters:
        R (float): Resistance in ohms
        L (float): Inductance in henries
        C (float): Capacitance in farads

        Return:
        float: Quality factor (unitless)
        """
        if R <= 0 or L <= 0 or C <= 0:
            raise ValueError("Resistance, inductance, and capacitance must be positive.")
        return math.sqrt(L / C) / R

    @staticmethod
    def bandwidth(cutoff_frequency, quality_factor):
        """
        Calculate the bandwidth of a low-pass RLC filter (order 2).

        Parameters:
        cutoff_frequency (float): Cutoff frequency in Hz
        quality_factor (float): Quality factor (unitless)

        Return:
        float: Bandwidth in Hz
        """
        if quality_factor <= 0:
            raise ValueError("Quality factor must be positive.")
        return cutoff_frequency / quality_factor
