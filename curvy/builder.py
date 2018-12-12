import numpy as np
import numpy.matlib as npm
from scipy.linalg import block_diag
from curvy import axis
from datetime import datetime

def calc_H(tau_b, tau_e):
    return np.matrix([
        [(144 / 5) * (tau_e**5 - tau_b**5),    18 * (tau_e**4 - tau_b**4),    8 * (tau_e**3 - tau_b**3), 0, 0],
        [       18 * (tau_e**4 - tau_b**4),    12 * (tau_e**3 - tau_b**3),    6 * (tau_e**2 - tau_b**2), 0, 0],
        [        8 * (tau_e**3 - tau_b**3),     6 * (tau_e**2 - tau_b**2),    4 * (tau_e**1 - tau_b**1), 0, 0],
        [                   0,                0,               0, 0, 0],
        [                   0,                0,               0, 0, 0],
    ])

def calc_big_H(taus):
    h_matrices = []
    for i in range(0, len(taus)):
        tau_b, tau_e = taus[i]
        h_matrices.append(calc_H(tau_b, tau_e))
    return block_diag(*h_matrices)

def calc_avg_constraint(tau_b, tau_e):
    return np.matrix([(tau_e**5 - tau_b**5) / 5, (tau_e**4 - tau_b**4) / 4, (tau_e**3 - tau_b**3) / 3, (tau_e**2 - tau_b**2) / 2, tau_e - tau_b])

def calc_constraints(u_j):
    # Using the four contraints: connectivity, continuous, smooth and maintaining the average.
    # Excluding the requirement for the line to be zero at the end.
    return np.matrix([
        [     u_j**4,     u_j**3,     u_j**2, u_j**1,   1],
        [ 4 * u_j**3, 3 * u_j**2, 2 * u_j**1,      1,   0],
        [12 * u_j**2, 6 * u_j**1,          2,      0,   0]
    ])

def calc_big_A(knots, taus):
    A = npm.zeros((4 * len(knots) + 1, 5 * len(knots) + 5))
    for i, knot in enumerate(knots):
        tau_b, tau_e = taus[i]
        c1 = calc_constraints(knot)
        c2 = calc_avg_constraint(tau_b, tau_e)
        A[(4 * i):(4 * i + 3), (5 * i):(5 * i + 5)] = c1
        A[(4 * i):(4 * i + 3), (5 * i + 5):(5 * i + 10)] = - c1
        A[(4 * i + 3), (5 * i):(5 * i + 5)] = c2
    # Last line only subject to the average constraint.
    tau_b, tau_e = taus[-1]
    A[-1, -5:] = calc_avg_constraint(tau_b, tau_e)
    return A

def calc_B(prices, taus):
    B = npm.zeros(4 * len(taus) - 3)
    for i in range(0, len(taus) - 1):
        tau_b, tau_e = taus[i]
        B[:, 4 * i + 3] = prices[i] * (tau_e - tau_b)
    tau_b, tau_e = taus[-1]
    B[:, -1] = prices[-1] * (tau_e - tau_b)
    return B.T

# Solves the linear equation and return only the x values (scraps lambda).
# By default it splits the x-matrix into a list of numpy arrays, each containing
# the a, b, c, d and e variables for each line segment.
def solve_lineq(H, A, B, split=True, num_params=5):
    top = np.concatenate((2 * H, A.T), axis=1)
    btm = np.concatenate((A, np.zeros((A.shape[0], A.T.shape[1]))), axis=1)
    A_merged = np.concatenate((top, btm), axis=0)
    B_merged = np.concatenate(
        (
            npm.zeros(top.shape[1] - B.shape[0]).T,
            B
        ), axis=0)
    X = np.squeeze(np.array(np.linalg.solve(A_merged,B_merged)[:A.shape[1]]))
    if split:
        if X.shape[0] % num_params != 0:
            raise ValueError('The split of the x-matrix is not even. Set "num_params" to the correct value to fix this')
        return np.split(X, np.arange(num_params, X.shape[0], num_params))
    else:
        return X

def smfc(u, params):
    return params[0] * u**4 + params[1] * u**3 + params[2] * u**2 + params[3] * u + params[4]

def curve_values(ranges, X, curve_func, flatten=False):
    if len(ranges) != len(X):
        raise ValueError('Arrays do not match in length')
    ranges_se = axis.start_end_absolute_index(ranges)
    x_index = axis.full_index(ranges_se)
    x_ranges = []
    for i, r in enumerate(x_index):
        x_ranges.append(curve_func(np.array(r, dtype='int64'), X[i]))
    if flatten:
        return np.concatenate(x_ranges)
    else:
        return x_ranges

def calc_smfc(dr, prices, flatten=True):
    taus = axis.start_end_absolute_index(dr, overlap=1)
    knots = axis.knot_index(taus)
    H = calc_big_H(taus)
    A = calc_big_A(knots, taus)
    B = calc_B(prices, taus)
    X = solve_lineq(H, A, B)
    return curve_values(dr, X, smfc, flatten=flatten)

def build_smfc_curve(prices, start_date=None, flatten=True):
    if start_date is None:
        start_date = datetime.now()
    x, y, dr, pr = axis.get_ranges(start_date, prices)
    y_smfc = calc_smfc(dr, prices, flatten)

    return x, y, dr, pr, y_smfc