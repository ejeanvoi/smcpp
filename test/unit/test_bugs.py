import numpy as np
import scipy.integrate

from smcpp import _smcpp, model, util, estimation_tools


def test_bug1():
    d = {'class': 'SMCModel', 'spline_class': 'PChipSpline', 'y': [-2.433625923004, -4.6051701859880909, 3.6726078178617159, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'knots': [0.02, 0.031697863849222269, 0.050237728630191596, 0.079621434110699482, 0.12619146889603869, 0.20000000000000004, 0.31697863849222285, 0.50237728630191625, 0.79621434110699474, 1.2619146889603867, 2.0], 's': [0.02, 0.0030956396937891623, 0.0035747889494773186, 0.0041281018779233576, 0.0047670576795886162, 0.0055049123283644683, 0.0063569735840901878, 0.0073409185720541212, 0.0084771605180803608, 0.0097892722475999561, 0.011304475234748909, 0.013054204347456175, 0.0150747600048972, 0.017408061277172454, 0.020102515551248895, 0.0232140228055219, 0.026807135327986953, 0.030956396937891623, 0.0357478894947732, 0.041281018779233569, 0.047670576795886155, 0.055049123283644696, 0.063569735840901809, 0.073409185720541281, 0.084771605180803622, 0.097892722475999561, 0.11304475234748901, 0.13054204347456178, 0.15074760004897203, 0.17408061277172449, 0.2010251555124889, 0.23214022805521917, 0.26807135327986908]}
    model1 = model.SMCModel.from_dict(d)
    eta = _smcpp.PyRateFunction(model1, [])
    t1 = 0.0
    t2 = 0.02
    K = 10
    for t, Rt in eta.random_coal_times(t1, t2, K):
        assert t1 < t < t2

def test_bug2():
    model1 = model.PiecewiseModel([1.], [1.], [])
    eta = _smcpp.PyRateFunction(model1, [0.0, 1.0, 2.0, np.inf])
    assert eta.R(2.0) == 2.0
    n = 5
    raw_sfs = _smcpp.raw_sfs(model1, n - 2, 0., np.inf).astype('float')
    undist = util.undistinguished_sfs(raw_sfs)
    assert np.allclose(undist[1:], 2. / np.arange(1, n))
    ts = [0.0, 0.5, 1.0, 2.0, np.inf]
    for t1, t2 in zip(ts[:-1], ts[1:]):
        q = scipy.integrate.quad(lambda t: t * np.exp(-t), t1, t2)
        ans = q[0]
        ans /= np.exp(-t1) - np.exp(-t2)
        for n in [0, 2, 10, 20]:
            raw_sfs = _smcpp.raw_sfs(model1, n, t1, t2)
            np.testing.assert_allclose(raw_sfs.sum(axis=1)[1], 2. * ans)

def test_bug3():
    np.testing.assert_equal(
            [[3,0,0,0]],
            estimation_tools.compress_repeated_obs([[1,0,0,0],[2,0,0,0]])
            )

def test_bug4():
    a = np.array([
        [3314,    0,    0,    0],
        [   1,    1,    0,    0],
        [6685,    0,    0,    0]], dtype=np.int32)
    b = estimation_tools.thin_dataset([a], 2)[0]
    np.testing.assert_equal(a, b)
