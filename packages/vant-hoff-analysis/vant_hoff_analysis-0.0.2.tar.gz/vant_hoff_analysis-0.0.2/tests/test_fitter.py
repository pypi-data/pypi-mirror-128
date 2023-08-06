import scipy
import numpy as np
import pytest
from vant_hoff_analysis import Fitter, PCTCurve

@pytest.fixture
def curve_a():
    curve_a_pressures = [np.exp(-1), np.exp(0), np.exp(1)]
    curve_a_concs = [0.2, 0.52, 0.85]
    curve_a_temperature = 278

    curve_a = PCTCurve(curve_a_concs, curve_a_pressures, curve_a_temperature)
    return curve_a

@pytest.fixture
def curve_b():
    curve_b_pressures = [np.exp(3), np.exp(4), np.exp(5)]
    curve_b_concs = [0.05, 0.49, 0.95]
    curve_b_temperature = 373

    curve_b = PCTCurve(curve_b_concs, curve_b_pressures, curve_b_temperature)
    return curve_b

def test_fitter(curve_a, curve_b):
    # A contrived example of fit
    fitter = Fitter()
    fit_result = fitter.fit_at_concentration(0.5, [curve_a, curve_b])
    delta_H = fit_result.to_dict()["deltaH"]
    delta_S = fit_result.to_dict()["deltaS"]

    assert delta_H == pytest.approx(4.450090593 * scipy.constants.R)
    assert delta_S == pytest.approx(15.96721097 * scipy.constants.R)

def test_from_points():
    point1 = [348, 0.193889213]
    point2 = [373, 0.563732355]
    point3 = [388, 1.061087193]

    fitter = Fitter()

    fit_result = fitter.fit_from_points([point1, point2, point3])
    delta_H = fit_result.to_dict()["deltaH"]
    delta_S = fit_result.to_dict()["deltaS"]

    assert delta_H == pytest.approx(47.4999715)
    assert delta_S == pytest.approx(122.783428)

def test_nan_case():
    points = [[2, -10], [3, 3]]

    fitter = Fitter()

    with pytest.raises(ValueError):
        fitter.fit_from_points(points)

def test_from_indices(curve_a, curve_b):
    fitter = Fitter()
    fit_result = fitter.fit_from_indices([1,1], [curve_a, curve_b])
    delta_H = fit_result.to_dict()["deltaH"]
    delta_S = fit_result.to_dict()["deltaS"]

    assert delta_H == pytest.approx(4.36606315789 * scipy.constants.R)
    assert delta_S == pytest.approx(15.7052631579 * scipy.constants.R)