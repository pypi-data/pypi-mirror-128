import unittest

import matplotlib.pyplot as plt
import numpy as np

import GooseMPL as gplt


class Test_ticks(unittest.TestCase):
    """
    Functions generating ticks.
    """

    def test_log_ticks(self):

        ticks, labels = gplt.log_ticks((0, 3))
        self.assertEqual(list(ticks), [1, 10, 100, 1000])
        self.assertEqual(labels, [r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"])

        ticks, labels = gplt.log_ticks((0, 3), keep=[0, -1])
        self.assertEqual(list(ticks), [1, 10, 100, 1000])
        self.assertEqual(labels, [r"$10^{0}$", "", "", r"$10^{3}$"])

    def test_log_ticks_plot(self):

        fig, ax = plt.subplots()

        ax.set_xlim([1, 1000])
        ax.set_ylim([10, 1000])

        ticks, labels = gplt.log_xticks()
        self.assertEqual(list(ticks), [1, 10, 100, 1000])
        self.assertEqual(labels, [r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"])

        ticks, labels = gplt.log_yticks()
        self.assertEqual(list(ticks), [10, 100, 1000])
        self.assertEqual(labels, [r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"])

        plt.close(fig)

    def test_log_minorticks(self):

        ticks, labels = gplt.log_minorticks((1, 10), integer=True)
        self.assertEqual(list(ticks), [2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(labels, ["2", "3", "4", "5", "6", "7", "8", "9"])

    def test_log_minorticks_plot(self):

        fig, ax = plt.subplots()

        ax.set_xlim([1, 10])
        ax.set_ylim([0.01, 1])

        ticks, labels = gplt.log_minorxticks(integer=True)
        self.assertEqual(list(ticks), [2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(labels, ["2", "3", "4", "5", "6", "7", "8", "9"])

        ticks, labels = gplt.log_minoryticks()
        self.assertTrue(
            np.allclose(
                ticks,
                [
                    0.02,
                    0.03,
                    0.04,
                    0.05,
                    0.06,
                    0.07,
                    0.08,
                    0.09,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                    0.6,
                    0.7,
                    0.8,
                    0.9,
                ],
            )
        )
        self.assertEqual(
            labels,
            [
                "0.02",
                "0.03",
                "0.04",
                "0.05",
                "0.06",
                "0.07",
                "0.08",
                "0.09",
                "0.2",
                "0.3",
                "0.4",
                "0.5",
                "0.6",
                "0.7",
                "0.8",
                "0.9",
            ],
        )

        plt.close(fig)


class Test_fit_powerlaw(unittest.TestCase):
    def test_prefactor_exponent(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))

    def test_prefactor(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y, exponent=3.4)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))

    def test_exponent(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y, prefactor=1.2)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))


class Test_histogram_bin_edges_integer(unittest.TestCase):
    def test_front(self):

        a = [0, 0.5, 1.5, 2.5]
        b = [0, 1.5, 2.5]
        self.assertTrue(np.allclose(gplt.histogram_bin_edges_integer(a), b))

    def test_middle(self):

        a = [0, 1.5, 1.6, 2.5]
        b = [0, 1.6, 2.5]
        self.assertTrue(np.allclose(gplt.histogram_bin_edges_integer(a), b))

    def test_back(self):

        a = [0, 1.5, 2.5, 2.6]
        b = [0, 1.5, 2.6]
        self.assertTrue(np.allclose(gplt.histogram_bin_edges_integer(a), b))


if __name__ == "__main__":

    unittest.main()
