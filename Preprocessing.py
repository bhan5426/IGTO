import numpy as np
import pytest

class Inputs():
    '''
    A geometry class with NURBS parameter as the method
    Methods:
        crtpts_coordinates : generate control points along with weights 

        knot_vector :generates knot vector based on control points generated from crtpts_coordinates and degree

        knotconnect : other parameter required for assembly like span, unique knots.
        
    '''

    def __init__(self, length=1, height=1, width=1, nx=1, ny=1, nz=1, xidegree=1, etadegree=1, netadegree=1):
        self.length = length
        self.height = height
        self.width = width
        self.nx = nx - 1
        self.ny = ny - 1
        self.nz = nz - 1
        self.n = nx
        self.p = ny
        self.q = nz
        self.xidegree = xidegree
        self.etadegree = etadegree
        self.netadegree = netadegree

    def crtpts_coordinates(self):
        '''
        A Method which return the control point co-ordinates


        Test case
        ------
        Test command -  
                        pytest test_Inputs.py::test__controlpoints_coordinates_true
        '''
        beam_coordinates = []
        index = 0
        for i in range(self.nz + 1):
            for j in range(self.ny + 1):
                for k in range(self.nx + 1):
                    beam_coordinates.append(
                        [(k) * (self.length / self.nx), j * (self.height / self.ny), i * (self.width / self.nz), 1,
                         index])
                    index += 1
        return np.array(beam_coordinates)

    def knot_vector(self, n, degree):
        '''
        This function return knotvector based on the number of control points and degree of Bspline
        Parameters
        ----------
        control_points : int
            number of points along with weights.
        degree : int
            order of B-splines  0-constant, 1-linear, 2-quadratic, 3-cubic.

        Returns
        -------
        KNOTVECTOR - an array containing knots based on control points

        Test case
        ------
        test command - 
                        pytest test_Inputs.py::test__knotvector_true
        '''
        size = n + degree + 1
        self.knotvector = np.zeros(size)
        if n >= (degree):
            for i in range(size):
                if i <= degree:
                    self.knotvector[i] = 0
                elif i > degree and i < (size - degree):
                    value = i - degree
                    self.knotvector[i] = value
                else:
                    self.knotvector[i] = n - degree
        elif n == 2 and degree == 1:
            self.knotvector = [0, 0, 1, 1]
        elif n == 2 and degree == 2:
            self.knotvector = [0, 0, 0, 1, 1, 1]
        else:
            raise Exception('Require more control points to define the knotvector')
        self.knotvector = self.knotvector / self.knotvector[-1]
        return self.knotvector

    #knot vector are generated along xi, eta ,neta direction based on n - no of control points and degree of knotvector
    def xi_knotvector(self):
        self.xikntvtr = self.knot_vector(self.n, self.xidegree)
        return self.xikntvtr

    def eta_knotvector(self):
        self.etakntvtr = self.knot_vector(self.p, self.etadegree)
        return self.etakntvtr

    def neta_knotvector(self):
        self.netakntvtr = self.knot_vector(self.q, self.netadegree)
        return self.netakntvtr

    def knotconnect(self, n, degree):
        '''
        This function generates a parameters used to build the connectivity matrix
         Parameters
        ----------
        n : int
            length of the knot vector
        degree : int
            order of B-splines  0-constant, 1-linear, 2-quadratic, 3-cubic.

        Returns
        -------
        span - span of each element generated based on degree and length of knotvector.
                            Ex-[0,0,0.25,0.5,0.75,1,1,1]
                                degree:2
                                span: [[0,0.25,0.5],
                                        [0.5,0.75,1]]
        knotconnectivity - a 2d array containing the spans of all the elements number as index of poistion of knotvector
                                knotconnectivity:[[0,1,2],
                                                    [2,3,4]]
        uniknots - an array of unique knots
                            Ex-[0,0.25,0.5,0.75,1]
        n - length of knot vector

        Test case
        ------
        test command -
                        pytest test_Inputs.py::test__knotconnect_span_true
        '''
        knot = self.knot_vector(n, degree)
        uniknots = np.unique(knot)
        n = len(uniknots) - 1
        span = np.zeros((n, 2))
        elindex = np.zeros((n, 2))
        knotconnectivity = np.zeros((n, degree + 1))
        index = 0
        for i in range(0, n):
            if uniknots[i] != uniknots[i + 1]:
                elindex[index, :] = [i + degree, i + 1 + degree]
                span[index, :] = [uniknots[i], uniknots[i + 1]]
                index += 1
        j = 0
        while j < n:
            knotconnectivity[j, :] = np.arange(elindex[j, 0] - degree, elindex[j, 0] + 1)
            j += 1
        knotconnectivity = knotconnectivity.astype(int)
        return span, knotconnectivity, uniknots, n

    # knot parameters for each knot vector xi, eta, neta are generated below
    def xi_knotspan(self):
        self.xi_span, self.xiknotconnectivity, self.xiuniknots, self.nXi = self.knotconnect(self.n, self.xidegree)
        return self.xi_span, self.xiknotconnectivity, self.xiuniknots, self.nXi

    def eta_knotspan(self):
        self.eta_span, self.etaknotconnectivity, self.etauniknots, self.nEta = self.knotconnect(self.p, self.etadegree)
        return self.eta_span, self.etaknotconnectivity, self.etauniknots, self.nEta

    def neta_knotspan(self):
        self.neta_span, self.netaknotconnectivity, self.netauniknots, self.nNeta = self.knotconnect(self.q,
                                                                                                    self.netadegree)
        return self.neta_span, self.netaknotconnectivity, self.netauniknots, self.nNeta

