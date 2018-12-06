import unittest
from curvy import axis
import datetime

class TestAxisMethods(unittest.TestCase):

    def test_da_date(self):
        self.assertEqual(
            axis.da_date(datetime.datetime.today()),
            datetime.date.today() + datetime.timedelta(days=1)
        )

    def test_bom_dates(self):
        self.assertEqual(
            axis.bom_dates(datetime.datetime(2018, 11, 26)),
            [
                datetime.date(2018, 11, 28),
                datetime.date(2018, 11, 29),
                datetime.date(2018, 11, 30),
            ]
        )

    def test_date_ranges(self):
        self.assertEqual(
            axis.date_ranges(datetime.datetime(2018, 11, 26), 1),
            [
                [datetime.date(2018, 11, 27)],
                [datetime.date(2018, 11, 28), datetime.date(2018, 11, 29), datetime.date(2018, 11, 30)],
                [datetime.date(2018, 12, 1), datetime.date(2018, 12, 2),
                datetime.date(2018, 12, 3), datetime.date(2018, 12, 4),
                datetime.date(2018, 12, 5), datetime.date(2018, 12, 6),
                datetime.date(2018, 12, 7), datetime.date(2018, 12, 8),
                datetime.date(2018, 12, 9), datetime.date(2018, 12, 10),
                datetime.date(2018, 12, 11), datetime.date(2018, 12, 12),
                datetime.date(2018, 12, 13), datetime.date(2018, 12, 14),
                datetime.date(2018, 12, 15), datetime.date(2018, 12, 16),
                datetime.date(2018, 12, 17), datetime.date(2018, 12, 18),
                datetime.date(2018, 12, 19), datetime.date(2018, 12, 20),
                datetime.date(2018, 12, 21), datetime.date(2018, 12, 22),
                datetime.date(2018, 12, 23), datetime.date(2018, 12, 24),
                datetime.date(2018, 12, 25), datetime.date(2018, 12, 26),
                datetime.date(2018, 12, 27), datetime.date(2018, 12, 28),
                datetime.date(2018, 12, 29), datetime.date(2018, 12, 30),
                datetime.date(2018, 12, 31)]
            ]
        )

        self.assertEqual(
            axis.date_ranges(datetime.datetime(2018, 11, 29), 1),
            [[datetime.date(2018, 11, 30)],
            [datetime.date(2018, 12, 1), datetime.date(2018, 12, 2),
             datetime.date(2018, 12, 3), datetime.date(2018, 12, 4),
             datetime.date(2018, 12, 5), datetime.date(2018, 12, 6),
             datetime.date(2018, 12, 7), datetime.date(2018, 12, 8),
             datetime.date(2018, 12, 9), datetime.date(2018, 12, 10),
             datetime.date(2018, 12, 11), datetime.date(2018, 12, 12),
             datetime.date(2018, 12, 13), datetime.date(2018, 12, 14),
             datetime.date(2018, 12, 15), datetime.date(2018, 12, 16),
             datetime.date(2018, 12, 17), datetime.date(2018, 12, 18),
             datetime.date(2018, 12, 19), datetime.date(2018, 12, 20),
             datetime.date(2018, 12, 21), datetime.date(2018, 12, 22),
             datetime.date(2018, 12, 23), datetime.date(2018, 12, 24),
             datetime.date(2018, 12, 25), datetime.date(2018, 12, 26),
             datetime.date(2018, 12, 27), datetime.date(2018, 12, 28),
             datetime.date(2018, 12, 29), datetime.date(2018, 12, 30),
             datetime.date(2018, 12, 31)]
            ]
        )

    def test_price_ranges(self):
        self.assertEqual(
            axis.price_ranges([[1,2,3]], [4]), 
            [[4,4,4]]
        )

        self.assertEqual(
            axis.price_ranges([[1,2,3], [4,5,6]], [1,2]),
            [[1,1,1],[2,2,2]]
        )

        with self.assertRaises(ValueError):
            self.assertEqual(
                axis.price_ranges([[1,2,3], [4,5,6]], [1,2,3]),
                [[1,1,1],[2,2,2]]
            )

    def test_flatten_ranges(self):
        self.assertEqual(
            axis.flatten_ranges([[1]]),
            [1]
        )

        self.assertEqual(
            axis.flatten_ranges([[1,2], [3,4,5]]),
            [1,2,3,4,5]
        )

        self.assertEqual(
            axis.flatten_ranges([[1,2,3], [3,4,5]], no_overlap=True),
            [1,2,3,4]
        )

    def test_midpoint_values(self):
        self.assertEqual(
            axis.midpoint_values([[3,5,7]]),
            [5]
        )

        self.assertEqual(
            axis.midpoint_values([[3,5,7], [3,1,8,7]]),
            [5,8]
        )


    def test_midpoint_relative_index(self):
        self.assertEqual(
            axis.midpoint_relative_index([[3]]),
            [0]
        )

        self.assertEqual(
            axis.midpoint_relative_index([[3,5,6,3], [3,1,8,7,8]]),
            [2,2]
        )

    def test_midpoint_absolute_index(self):
        self.assertEqual(
            axis.midpoint_absolute_index([[1]]),
            [0]
        )

        self.assertEqual(
            axis.midpoint_absolute_index([[3,5,6], [3,1,8,7]]),
            [1,5]
        )

    def test_start_end_absolute_index(self):
        self.assertEqual(
            axis.start_end_absolute_index([[3,5,6],[3,1,8,7]]),
            [[0,2],[3,6]]
        )

        self.assertEqual(
            axis.start_end_absolute_index([[3,5,6],[3,1,8,7]], overlap=1),
            [[0,3],[3,7]]
        )


    def test_full_index(self):
        self.assertEqual(
            axis.full_index([[0,1]]),
            [[0,1]]
        )

        self.assertEqual(
            axis.full_index([[0,2],[3,7]]),
            [[0,1,2], [3,4,5,6,7]]
        )

        self.assertEqual(
            axis.full_index([[0,3],[3,7]]),
            [[0,1,2,3], [3,4,5,6,7]]
        )

    def test_knot_index(self):
        self.assertEqual(
            axis.knot_index([[1,2],[2,6],[6,10]]),
            [2,6]
        )

        with self.assertRaises(ValueError):
            self.assertEqual(
                axis.knot_index([[1,2]]),
                [2]
            )

    def test_get_ranges(self):
        with self.assertRaises(ValueError):
            self.assertEqual(
                axis.get_ranges(datetime.datetime.now(), [1]),
                []
            )

        x, y, dr, pr = axis.get_ranges(datetime.datetime(2018, 11, 26), [1, 2, 3])
        self.assertEqual(
            dr,
            [
                [datetime.date(2018, 11, 27)],
                [datetime.date(2018, 11, 28), datetime.date(2018, 11, 29), datetime.date(2018, 11, 30)],
                [datetime.date(2018, 12, 1), datetime.date(2018, 12, 2),
                datetime.date(2018, 12, 3), datetime.date(2018, 12, 4),
                datetime.date(2018, 12, 5), datetime.date(2018, 12, 6),
                datetime.date(2018, 12, 7), datetime.date(2018, 12, 8),
                datetime.date(2018, 12, 9), datetime.date(2018, 12, 10),
                datetime.date(2018, 12, 11), datetime.date(2018, 12, 12),
                datetime.date(2018, 12, 13), datetime.date(2018, 12, 14),
                datetime.date(2018, 12, 15), datetime.date(2018, 12, 16),
                datetime.date(2018, 12, 17), datetime.date(2018, 12, 18),
                datetime.date(2018, 12, 19), datetime.date(2018, 12, 20),
                datetime.date(2018, 12, 21), datetime.date(2018, 12, 22),
                datetime.date(2018, 12, 23), datetime.date(2018, 12, 24),
                datetime.date(2018, 12, 25), datetime.date(2018, 12, 26),
                datetime.date(2018, 12, 27), datetime.date(2018, 12, 28),
                datetime.date(2018, 12, 29), datetime.date(2018, 12, 30),
                datetime.date(2018, 12, 31)]
            ]
        )

        self.assertEqual(
            pr,
            [
                [1],
                [2] * 3,
                [3] * 31
            ]
        )

        self.assertEqual(
            x,
            [
                datetime.date(2018, 11, 27), datetime.date(2018, 11, 28),
                datetime.date(2018, 11, 29), datetime.date(2018, 11, 30),
                datetime.date(2018, 12, 1), datetime.date(2018, 12, 2),
                datetime.date(2018, 12, 3), datetime.date(2018, 12, 4),
                datetime.date(2018, 12, 5), datetime.date(2018, 12, 6),
                datetime.date(2018, 12, 7), datetime.date(2018, 12, 8),
                datetime.date(2018, 12, 9), datetime.date(2018, 12, 10),
                datetime.date(2018, 12, 11), datetime.date(2018, 12, 12),
                datetime.date(2018, 12, 13), datetime.date(2018, 12, 14),
                datetime.date(2018, 12, 15), datetime.date(2018, 12, 16),
                datetime.date(2018, 12, 17), datetime.date(2018, 12, 18),
                datetime.date(2018, 12, 19), datetime.date(2018, 12, 20),
                datetime.date(2018, 12, 21), datetime.date(2018, 12, 22),
                datetime.date(2018, 12, 23), datetime.date(2018, 12, 24),
                datetime.date(2018, 12, 25), datetime.date(2018, 12, 26),
                datetime.date(2018, 12, 27), datetime.date(2018, 12, 28),
                datetime.date(2018, 12, 29), datetime.date(2018, 12, 30),
                datetime.date(2018, 12, 31)
            ]
        )

        self.assertEqual(
            y,
            [1] + [2] * 3 + [3] * 31
        )

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()