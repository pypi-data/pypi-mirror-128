import numpy as np
from scipy import constants
from typing import List
from .pct_curve import PCTCurve
from .result import VHResult

# Steps:
# 1. From each PCT curve, note temperature, find the point nearest
# the provided X value, and grab it's pressure
# 2. For each point, convert temperature to 1/T (units 1/K) and pressure to ln(P),
# 3. Perform a regression to find line of best fit for those points.
# 4. the deltaH value will be m * R
# 5. the deltaS value will be -b * R

class Fitter:

    def fit_at_concentration(self, concentration, curves: List[PCTCurve]):
        """Given a concentration, identifies the nearest points in each curve to
        that concentration and then performs a Van't Hoff fit on those points.
        """
        points = np.array(
            list(map(lambda curve: curve.interpolate_point_at_concentration(concentration), curves)))
        xs = points.T[0]
        ys = points.T[1]
        return self.fit(xs, ys)

    def fit_from_indices(self, indices: List[int], curves: List[PCTCurve]):
        """
        Given a list of curves, and a list of indices which indicate the points on
        the curves which should be used for analysis, return the thermodynamic values
        resulting from performing that analysis.

        :param indices: A list of indices
        :param curves: The PCT c
        """
        assert len(indices) == len(curves), "Must provide one index for each curve"
        points = [(c.temperature, c.pressures[idx]) for (c, idx) in zip(curves, indices)]
        return self.fit_from_points(points)

    def fit_from_points(self, points):
        """Given (temperature, pressure) points, returns thermodynamic fit data"""
        xs = np.array([1 / point[0] for point in points])
        ys = np.array([np.log(point[1]) for point in points])
        # Check for values that resulted in NaN points - e.g. negative pressure values, which
        # invalid as inputs to logarithm.
        # probably a more elegent way to do this...
        if np.any(np.isnan(xs)) or np.any(np.isnan(ys)):
            raise ValueError("Invalid inputs detected")
        return self.fit(xs, ys)

    def fit(self, xs, ys):
        """Given 1/T, ln(pressure) points, perform a linear fit, and then
        return the thermodynamic constants.

        :param xs: A list of 1/temperature values
        :param ys: A list of log pressure values
        """
        assert len(xs) == len(ys), "x and y lists must have the same length"
        b, m = np.polynomial.polynomial.polyfit(xs, ys, deg=1)
        deltaH = -m * constants.R / 1000
        negative_deltaS = -b * constants.R
        return VHResult(deltaH, -negative_deltaS, xs.tolist(), ys.tolist(), m, b)
