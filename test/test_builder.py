import unittest
from curvy import builder, axis
import datetime
import numpy as np

taus = [[2,5],[5,7],[7,11]]
prices = [3,5,4]
knots = [5,7]

class TestBuilderMethods(unittest.TestCase):

    def test_calc_H(self):
        H = np.load('test/test_files/H.npy')
        np.testing.assert_array_equal(
            builder.calc_H(2, 5),
            H
        )

    def test_calc_big_H(self):
        big_H = np.load('test/test_files/big_H.npy')
        np.testing.assert_array_equal(
            builder.calc_big_H(taus),
            big_H
        )

    def test_avg_constraint(self):
        avg_constraint = np.load('test/test_files/avg_constraint.npy')
        np.testing.assert_array_equal(
            builder.calc_avg_constraint(2,5),
            avg_constraint
        )

    def test_calc_constraints(self):
        constraints = np.load('test/test_files/constraints.npy')
        np.testing.assert_array_equal(
            builder.calc_constraints(5),
            constraints
        )

    def test_calc_big_A(self):
        big_A = np.load('test/test_files/big_A.npy')
        np.testing.assert_array_equal(
            builder.calc_big_A(knots, taus),
            big_A
        )

    def test_calc_B(self):
        B = np.load('test/test_files/B.npy')
        np.testing.assert_array_equal(
            builder.calc_B(prices, taus),
            B
        )

    def test_solve_lineq(self):
        lineq_ans = np.load('test/test_files/lineq_ans.npy')
        lineq_ans = [arr for arr in lineq_ans]

        np.testing.assert_array_almost_equal(
            builder.solve_lineq(
                builder.calc_big_H(taus),
                builder.calc_big_A(knots, taus),
                builder.calc_B(prices, taus)
            ),
            lineq_ans
        )

        lineq_ans_no_split = np.load('test/test_files/lineq_ans_no_split.npy')
        np.testing.assert_array_almost_equal(
            builder.solve_lineq(
                builder.calc_big_H(taus),
                builder.calc_big_A(knots, taus),
                builder.calc_B(prices, taus),
                split=False
            ),
            lineq_ans_no_split
        )

    def test_smfc(self):
        self.assertEqual(
            builder.smfc(2, [2,3,4,5,6]),
            88
        )

        self.assertEqual(
            builder.smfc(11, [5,2,9,5,4]),
            77015
        )

    def test_curve_values(self):
        curve_values = np.load('test/test_files/curve_values.npy')
        curve_values_flat = np.load('test/test_files/curve_values_flat.npy')
        H = builder.calc_big_H(taus)
        A = builder.calc_big_A(knots, taus)
        B = builder.calc_B(prices, taus)
        X = builder.solve_lineq(H, A, B)

        np.testing.assert_array_almost_equal(
            builder.curve_values(taus, X, builder.smfc),
            curve_values
        )

        np.testing.assert_array_almost_equal(
            builder.curve_values(taus, X, builder.smfc, flatten=True),
            curve_values_flat
        )

    def test_calc_smfc(self):
        prices2 = [2,4,7,5,4,3,2]
        dr = axis.date_ranges(datetime.datetime(2018,11,26), 5)
        curve_values = np.load('test/test_files/curve_values2.npy')
        curve_values_flat = np.load('test/test_files/curve_values2_no_flat.npy').tolist()

        np.testing.assert_array_almost_equal(
            builder.calc_smfc(dr, prices2),
            curve_values
        )

        test_curve_values = builder.calc_smfc(dr, prices2, flatten=False)
        for i in range (0, len(test_curve_values)):
            np.testing.assert_array_almost_equal(test_curve_values[i], curve_values_flat[i])

    #### This one might be harder to test 
    #
    # def test_build_smfc_curve(self):
    #     curve_values = np.load('test/test_files/curve_values3.npy')
    #     curve_values_flat = np.load('test/test_files/curve_values3_no_flat.npy')

    #     test_curve_values = builder.build_smfc_curve(
    #         prices,
    #         start_date=datetime.datetime(2018,11,26)
    #     )

    #     test_curve_values_no_flat = builder.build_smfc_curve(
    #         prices,
    #         start_date=datetime.datetime(2018,11,26),
    #         flatten=False
    #     )

    #     for i in len(curve_values):
    #         np.testing.assert_array_equal(
    #             curve_values
    #         )

if __name__ == '__main__':
    unittest.main() 