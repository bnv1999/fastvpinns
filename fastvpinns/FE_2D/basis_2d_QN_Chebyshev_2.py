# Purpose: Defines the basis functions for a 2D Q1 element.
# Reference: ParMooN -  File: BF_C_Q_Q1_2D.h
# Author: Thivin Anandh D
# Date: 30/Aug/2023

## NOTE : TEST FUNCTIONS AND DERIVATIVES INFERED FROM https://github.com/ehsankharazmi/hp-VPINNs/
## Cite: hp-VPINNs: Variational Physics-Informed Neural Networks With Domain Decomposition Ehsan Kharazmi et.al

# import the legendre polynomials
from scipy.special import jacobi

import numpy as np
from .basis_function_2d import BasisFunction2D


class Basis2DQNChebyshev2(BasisFunction2D):
    """
    This class defines the basis functions for a 2D Q1 element.
    """

    def __init__(self, num_shape_functions: int):
        super().__init__(num_shape_functions)

    def jacobi_wrapper(self, n, a, b, x):
        """
        Evaluate the Jacobi polynomial of degree n with parameters a and b at the given points x.

        Parameters:
            n (int): Degree of the Jacobi polynomial.
            a (float): First parameter of the Jacobi polynomial.
            b (float): Second parameter of the Jacobi polynomial.
            x (array_like): Points at which to evaluate the Jacobi polynomial.

        Returns:
            array_like: Values of the Jacobi polynomial at the given points x.
        """
        x = np.array(x, dtype=np.float64)
        return jacobi(n, a, b)(x)

    ## Helper Function
    def test_fcnx(self, n_test, x):
        """
        Compute the x-component of the test functions for a given number of test functions and x-coordinates.

        Parameters:
            n_test (int): Number of test functions.
            x (array_like): x-coordinates at which to evaluate the test functions.

        Returns:
            array_like: Values of the x-component of the test functions.
        """
        test_total = []
        for n in range(1, n_test + 1):
            test = self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, x) / self.jacobi_wrapper(
                n + 1, -1 / 2, -1 / 2, 1
            ) - self.jacobi_wrapper(n - 1, -1 / 2, -1 / 2, x) / self.jacobi_wrapper(
                n - 1, -1 / 2, -1 / 2, 1
            )
            test_total.append(test)
        return np.asarray(test_total, np.float64)

    def test_fcny(self, n_test, y):
        """
        Compute the y-component of the test functions for a given number of test functions and y-coordinates.

        Parameters:
            n_test (int): Number of test functions.
            y (array_like): y-coordinates at which to evaluate the test functions.

        Returns:
            array_like: Values of the y-component of the test functions.
        """
        test_total = []
        for n in range(1, n_test + 1):
            test = self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, y) / self.jacobi_wrapper(
                n + 1, -1 / 2, -1 / 2, 1
            ) - self.jacobi_wrapper(n - 1, -1 / 2, -1 / 2, y) / self.jacobi_wrapper(
                n - 1, -1 / 2, -1 / 2, 1
            )
            test_total.append(test)
        return np.asarray(test_total, np.float64)

    def dtest_fcn(self, n_test, x):
        """
        Compute the first and second derivatives of the test function.

        Parameters:
        - n_test (int): The number of test functions.
        - x (float): The input value.

        Returns:
        - d1test_total (ndarray): Array of first derivatives of the test function.
        - d2test_total (ndarray): Array of second derivatives of the test function.
        """
        d1test_total = []
        d2test_total = []
        for n in range(1, n_test + 1):
            if n == 1:
                d1test = (
                    ((n + 1) / 2)
                    * self.jacobi_wrapper(n, 1 / 2, 1 / 2, x)
                    / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1)
                )
                d2test = (
                    ((n + 2) * (n + 1) / (2 * 2))
                    * self.jacobi_wrapper(n - 1, 3 / 2, 3 / 2, x)
                    / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1)
                )
                d1test_total.append(d1test)
                d2test_total.append(d2test)
            elif n == 2:
                d1test = ((n + 1) / 2) * self.jacobi_wrapper(
                    n, 1 / 2, 1 / 2, x
                ) / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1) - (
                    (n - 1) / 2
                ) * self.jacobi_wrapper(
                    n - 2, 1 / 2, 1 / 2, x
                ) / self.jacobi_wrapper(
                    n - 1, -1 / 2, -1 / 2, 1
                )
                d2test = (
                    ((n + 2) * (n + 1) / (2 * 2))
                    * self.jacobi_wrapper(n - 1, 3 / 2, 3 / 2, x)
                    / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1)
                )
                d1test_total.append(d1test)
                d2test_total.append(d2test)
            else:
                d1test = ((n + 1) / 2) * self.jacobi_wrapper(
                    n, 1 / 2, 1 / 2, x
                ) / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1) - (
                    (n - 1) / 2
                ) * self.jacobi_wrapper(
                    n - 2, 1 / 2, 1 / 2, x
                ) / self.jacobi_wrapper(
                    n - 1, -1 / 2, -1 / 2, 1
                )
                d2test = ((n + 2) * (n + 1) / (2 * 2)) * self.jacobi_wrapper(
                    n - 1, 3 / 2, 3 / 2, x
                ) / self.jacobi_wrapper(n + 1, -1 / 2, -1 / 2, 1) - (
                    (n) * (n - 1) / (2 * 2)
                ) * self.jacobi_wrapper(
                    n - 3, 3 / 2, 3 / 2, x
                ) / self.jacobi_wrapper(
                    n - 1, -1 / 2, -1 / 2, 1
                )
                d1test_total.append(d1test)
                d2test_total.append(d2test)
        return np.asarray(d1test_total), np.asarray(d2test_total)

    def value(self, xi, eta):
        """
        This method returns the values of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        test_x = self.test_fcnx(num_shape_func_in_1d, xi)
        test_y = self.test_fcny(num_shape_func_in_1d, eta)
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                test_x[i, :] * test_y
            )

        return values

    def gradx(self, xi, eta):
        """
        This method returns the x-derivatives of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the x-derivatives of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        grad_test_x = self.dtest_fcn(num_shape_func_in_1d, xi)[0]
        test_y = self.test_fcny(num_shape_func_in_1d, eta)
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                grad_test_x[i, :] * test_y
            )

        return values

    def grady(self, xi, eta):
        """
        This method returns the y-derivatives of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the y-derivatives of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        test_x = self.test_fcnx(num_shape_func_in_1d, xi)
        grad_test_y = self.dtest_fcn(num_shape_func_in_1d, eta)[0]
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                test_x[i, :] * grad_test_y
            )

        return values

    def gradxx(self, xi, eta):
        """
        This method returns the xx-derivatives of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the xx-derivatives of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        grad_grad_x = self.dtest_fcn(num_shape_func_in_1d, xi)[1]
        test_y = self.test_fcny(num_shape_func_in_1d, eta)
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                grad_grad_x[i, :] * test_y
            )

        return values

    def gradxy(self, xi, eta):
        """
        This method returns the xy-derivatives of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the xy-derivatives of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        grad_test_x = self.dtest_fcn(num_shape_func_in_1d, xi)[0]
        grad_test_y = self.dtest_fcn(num_shape_func_in_1d, eta)[0]
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                grad_test_x[i, :] * grad_test_y
            )

        return values

    def gradyy(self, xi, eta):
        """
        This method returns the yy-derivatives of the basis functions at the given (xi, eta) coordinates.

        Parameters:
            xi (array_like): x-coordinates at which to evaluate the basis functions.
            eta (array_like): y-coordinates at which to evaluate the basis functions.

        Returns:
            array_like: Values of the yy-derivatives of the basis functions.
        """
        num_shape_func_in_1d = int(np.sqrt(self.num_shape_functions))
        test_x = self.test_fcnx(num_shape_func_in_1d, xi)
        grad_grad_y = self.dtest_fcn(num_shape_func_in_1d, eta)[1]
        values = np.zeros((self.num_shape_functions, len(xi)), dtype=np.float64)

        for i in range(num_shape_func_in_1d):
            values[num_shape_func_in_1d * i : num_shape_func_in_1d * (i + 1), :] = (
                test_x[i, :] * grad_grad_y
            )

        return values
