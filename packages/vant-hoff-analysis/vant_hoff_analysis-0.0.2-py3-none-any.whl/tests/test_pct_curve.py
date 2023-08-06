import vant_hoff_analysis as vh
import numpy as np


CSV_PATH = "tests/data/des1_348K.csv"

def test_pct_get_point():
    concentrations = [1, 2.4, 3.6, 4.8, 5.9]
    pressures = [1.1, 2.2, 3.3, 5.5, 6.7]
    temperature = 100
    curve = vh.PCTCurve(concentrations, pressures, temperature)
    pt = curve.get_closest_vant_hoff_point(4)
    assert pt[0] == 1 / 100
    assert pt[1] == np.log(3.3)


def test_curve_a():
    curve_a_pressures = [np.exp(-1), np.exp(0), np.exp(1)]
    curve_a_concs = [0.2, 0.52, 0.85]
    curve_a_temperature = 278

    curve_a = vh.PCTCurve(curve_a_concs, curve_a_pressures, curve_a_temperature)
    pt = curve_a.get_closest_vant_hoff_point(0.5)
    assert pt[0] == 1/278
    assert pt[1] == 0

def test_curve_b():
    curve_b_pressures = [np.exp(3), np.exp(4), np.exp(5)]
    curve_b_concs = [0.05, 0.49, 0.95]
    curve_b_temperature = 373

    curve_b = vh.PCTCurve(curve_b_concs, curve_b_pressures, curve_b_temperature)
    pt = curve_b.get_closest_vant_hoff_point(0.5)
    assert pt[0] == 1/373
    assert pt[1] == 4

def test_from_csv():
    curve = vh.PCTCurve.from_csv(348, csv_path=CSV_PATH)
    assert curve.temperature == 348
    assert curve.concentrations[0] == 0.8309570766512838
    assert curve.pressures[0] == 0.04403285286053071

def test_from_csv_pointer():
    with open(CSV_PATH) as f:
        curve = vh.PCTCurve.from_csv(348, csv_file=f)
        assert curve.temperature == 348
        assert curve.concentrations[0] == 0.8309570766512838
        assert curve.pressures[0] == 0.04403285286053071
