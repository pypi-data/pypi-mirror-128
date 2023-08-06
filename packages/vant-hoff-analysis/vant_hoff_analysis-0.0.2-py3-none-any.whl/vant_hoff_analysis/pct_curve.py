import numpy as np
import csv

class PCTCurve:
    """Simple representation of a PCT curve."""

    @classmethod
    def from_csv(cls, temperature: float, csv_path: str = None, csv_file = None):
        """
        Given the path to a CSV file, instantiate a PCTCurve assuming that the
        first column in the CSV is a list of concentrations, and the second
        column is a list of pressures.

        :param csv_path: A file path to the CSV containing the PCTCurve
        :param temperature: The temperature at which the measurement was taken
        """
        concentrations = []
        pressures = []

        if csv_path is not None:
            with open(csv_path, "r", newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    concentrations.append(float(row[0]))
                    pressures.append(float(row[1]))
        elif csv_file is not None:
            reader = csv.reader(csv_file)
            for row in reader:
                concentrations.append(float(row[0]))
                pressures.append(float(row[1]))

        return cls(concentrations, pressures, temperature)

    def __init__(self, concentrations: list, pressures: list, temperature: float):
        self.concentrations = np.array(concentrations)
        self.pressures = np.array(pressures)
        self.temperature = temperature

    def get_closest_vant_hoff_point(self, target_concentration: float):
        """
        Given a target concentration, finds the nearest measured point on
        the curve, and then returns a van't hoff point associated with
        that measured point
        """
        distances = np.abs(self.concentrations - target_concentration)
        closest_point_idx = np.argmin(distances)
        pressure = self.pressures[closest_point_idx]
        return np.array([1 / self.temperature, np.log(pressure)])

    def interpolate_point_at_concentration(self, concentration: float):
        distances = self.concentrations - concentration
        above = np.where(distances > 0)[0][0]
        below = np.where(distances <= 0)[0][-1]
        total_difference = self.concentrations[above] - self.concentrations[below]
        weighted_upper_pressure = self.pressures[above] * (concentration - self.concentrations[below])
        weighted_lower_pressure = self.pressures[below] * (self.concentrations[above] - concentration)
        avg_pressure = ( weighted_upper_pressure + weighted_lower_pressure ) / total_difference
        return np.array([1 / self.temperature, np.log(avg_pressure)])

    def get_vant_hoff_values_at_idx(self, idx: int):
        """
        Given the index of a point, returns the van't hoff
        values at that point.
        """
        pressure = self._pressures[idx]
        return np.array([1 / self.temperature, np.log(pressure)])
