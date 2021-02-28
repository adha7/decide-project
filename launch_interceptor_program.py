import numpy as np
import math
import launch_Parameters as Params
import Connector as Con
import Point2D

# Constants
PI = 3.14159265359


class Decide:
    def __init__(self, num_points, points: Point2D, parameters: Params.Parameters, lcm: Con.Connector, puv):
        self.num_points = num_points
        self.points = points
        self.parameters = parameters
        self.lcm = lcm
        self.puv = puv
        self.cmv = np.array(15, bool)        # The Conditions Met Vector (CMV), a 15-element vector.
        self.pum = np.array([15, 15], bool)  # Preliminary Unlocking Matrix (PUM), a 15x15 matrix.
        self.fuv = np.array(15, bool)        # The Final Unlocking Vector (FUV), a 15-element vector.

    def launch_decision(self):
        for count, value in enumerate(self.fuv):
            if not value:
                return 0
            
        return 1

    def compute_cmv(self):
        self.cmv[0] = self.lic_0()
        self.cmv[1] = self.lic_1()
        self.cmv[2] = self.lic_2()
        self.cmv[3] = self.lic_3()
        self.cmv[4] = self.lic_4()
        self.cmv[5] = self.lic_5()
        self.cmv[6] = self.lic_6()
        self.cmv[7] = self.lic_7()
        self.cmv[8] = self.lic_8()
        self.cmv[9] = self.lic_9()
        self.cmv[10] = self.lic_10()
        self.cmv[11] = self.lic_11()
        self.cmv[12] = self.lic_12()
        self.cmv[13] = self.lic_13()
        self.cmv[14] = self.lic_14()

    def compute_pum(self):
        for i in range(0, 15):
            for j in range(0, 15):
                if self.lcm[i][j] == Con.Connector.ANDD:
                    self.pum[i][j] = self.cmv[i] and self.cmv[j]
                elif self.lcm[i][j] == Con.Connector.ORR:
                    self.pum[i][j] = self.cmv[i] or self.cmv[j]
                else:
                    self.pum[i][j] = 1

    def compute_fuv(self):
        return

    # Return TRUE if two consecutive data points are a distance greater than the length1 apart
    def lic_0(self):

        # Check the boundaries
        if self.parameters.length1 < 0:
            return 0

        for i in range(0, self.points.length - 1):

            # Calculate the distance between point p1 and p2
            p1 = self.points[i]
            p2 = self.points[i+1]
            distance = math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))

            # Check if the distance is greater than length1 in the parameters
            if distance > self.parameters.length1:
                return 1

        return 0

    # Return TRUE if three consecutive data points are not contained within or on a circle of radius1
    def lic_1(self):

        # Check the boundaries
        if self.parameters.radius1 < 0:
            return 0

        for i in range(0, self.points.length - 2):

            # Calculate the distance between points p1, p2 and p3
            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]

            length_p12 = math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))
            length_p13 = math.sqrt(math.pow(p1.x - p3.x, 2) + math.pow(p1.y - p3.y, 2))
            length_p23 = math.sqrt(math.pow(p2.x - p3.x, 2) + math.pow(p2.y - p3.y, 2))

            # Calculating the radius of the circumcircle
            multipliedLengths = length_p12 * length_p13 * length_p23
            multipliedLengthDiffs = (length_p12 + length_p13 + length_p23) * (length_p12 + length_p13 - length_p23) * \
                                    (length_p13 + length_p23 - length_p12) * (length_p23 + length_p12 - length_p13)
            radius = multipliedLengths / math.sqrt(multipliedLengthDiffs)

            # Check if points b or c is inside or on the radius radius1 away from a
            if radius > self.parameters.radius1:
                return 1
        return 0

    # Return TRUE if three consecutive points form an angle greater than PI+epsilon or less than PI-epsilon
    def lic_2(self):

        # Check the boundaries
        if self.parameters.epsilon < 0 or self.parameters.epsilon >= PI:
            return 0

        # Iterate over all sets of three consecutive points
        for i in range(0, self.points.length - 2):

            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]

            # Calculate the two vectors using point 2 as vertex
            vector1 = (p1.x - p2.x, p1.y - p2.y)
            vector2 = (p3.x - p2.x, p3.y - p2.y)

            dotProduct = vector1[0] * vector2[0].x + vector1[1] * vector2[1]
            vector1Len = math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2))
            vector2Len = math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2))

            # If any two points coincide then move on
            if vector1Len == 0 or vector2Len == 0:
                continue

            # Obtain the angle through the definition of dot product in euclidean space
            angle = math.acos(dotProduct/(vector1Len*vector2Len))

            # Check if the angle is less than PI - epsilon
            if angle < (PI - self.parameters.epsilon):
                return 1

        return 0

    # Return TRUE if there exists a set of three consecutive points that are the vertices of a triangle with area
    # greater than parameters.area1
    def lic_3(self):

        # Check the boundaries
        if self.parameters.area1 < 0:
            return 0

        # Iterate over all sets of three consecutive points
        for i in range(0, self.points.length - 2):

            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]

            # Calculate the sides of the triangle
            length1 = math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))
            length2 = math.sqrt(math.pow(p1.x - p3.x, 2) + math.pow(p1.y - p3.y, 2))
            length3 = math.sqrt(math.pow(p2.x - p3.x, 2) + math.pow(p2.y - p3.y, 2))

            # Calculate the area of the triangle using Heron's formula
            tmp = (length1 + length2 + length3) / 2
            area = math.sqrt(tmp * (tmp - length1) * (tmp - length2) * (tmp - length3))

            if area > self.parameters.area1:
                return 1

        return 0

    # Return TRUE if there exists at least one set of Q_PTS consecutive data points that lie in more than QUADS
    # quadrants.                       2 <= Q_PTS <= NUMPOINTS, 1 <= QUADS <= 3
    def lic_4(self):

        # Check the boundaries
        if self.parameters.q_pts > self.num_points or self.parameters.q_pts < 2:
            return 0

        # Check the boundaries
        if self.parameters.q_uads > 3 or self.parameters.q_uads < 1:
            return 0

        # Iterate over all sets of qPts consecutive points
        for i in range(0, self.num_points - self.parameters.q_pts + 1):

            cons_points = []
            # Iterate q_pts steps to gather the set
            for j in range(i, self.parameters.q_pts + i):
                cons_points.append(self.points[j])

            # Keep track of visited quadrants
            num_quads = np.array(4, bool)

            for count, point in enumerate(cons_points):
                if point.x >= 0:
                    if point.y >= 0:
                        num_quads[0] = 1
                    elif point.x == 0 and point.y < 0:
                        num_quads[2] = 1
                    else:
                        num_quads[3] = 1

                else:
                    if point.y >= 0:
                        num_quads[1] = 1
                    else:
                        num_quads[2] = 1

            # Check if the set of q_pts consecutive points lie in more than q_uads quadrants
            if sum(num_quads) > self.parameters.q_uads:
                return 1

        return 0

    # Return TRUE if there exists at least one set of two consecutive data points where X[j] - X[i] < 0 (where i=j-1)
    def lic_5(self):

        # Iterate over all sets of two consecutive points
        for i in range(0, self.points.length - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]

            if (p2.x - p1.x) < 0:
                return 1

        return 0

    # Return TRUE if there exists at least one set of N PTS consecutive data points such that at least one of the points
    # lies a distance greater than DIST from the line joining the first and last of these N PTS points
    # When NUMPOINTS < 3, the condition is not met
    def lic_6(self):

        # Check the boundaries
        if self.num_points < 3:
            return 0

        if self.parameters.n_pts > self.num_points or self.parameters.n_pts < 3 or self.parameters.dist < 0:
            return 0

        # Iterate over all sets of n_pts consecutive points
        for i in range(0, self.num_points - self.parameters.n_pts + 1):

            cons_points = []
            # Iterate n_pts steps to gather the set
            for j in range(i, self.parameters.n_pts + i):
                cons_points.append(self.points[j])

            p1 = cons_points[0]
            pn = cons_points[self.parameters.n_pts - 1]

            # Check if the first and last point of these N PTS are identical
            if p1.x == pn.x and p1.y == pn.y:
                for k in range(1, self.parameters.n_pts - 1):
                    pk = cons_points[k]
                    distance = math.sqrt(math.pow(pk.y - p1.y, 2) + math.pow(pk.x - p1.x, 2))
                    if distance > self.parameters.dist:
                        return 1
            else:
                for k in range(1, self.parameters.n_pts - 1):
                    pk = cons_points[k]
                    num = abs((pn.y - p1.y) * pk.x - (pn.x - p1.x) * pk.y + pn.x * p1.y - pn.y * p1.x)
                    den = math.sqrt(math.pow(pn.y - p1.y, 2) + math.pow(pn.x - p1.x, 2))
                    distance = num / den

                    if distance > self.parameters.dist:
                        return 1
        return 0

    # Return TRUE if there exists at least one set of two data points separated by exactly K PTS consecutive intervening
    # points that are a distance greater than the length, LENGTH1, apart
    def lic_7(self):

        # Check the boundaries
        if self.num_points < 3 or self.parameters.k_pts > self.num_points - 2 or self.parameters.k_pts < 1:
            return 0

        for i in range(0, self.num_points - 1 - self.parameters.k_pts):
            p1 = self.points[i]
            p2 = self.points[i + 1 + self.parameters.k_pts]

            # Calculate the distance between the two points
            distance = math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))

            if distance > self.parameters.length1:
                return 1

        return 0


    # Return TRUE if there is at least one set of three data points separated by exactly
    # A_PTS and B_PTS consecutive intervening points, respectively, that cannot be contained
    # within or on a circle of radius RADIUS1.
    def lic_8(self):
        # Exceptional condition in case # of points are greater than 5
        if self.num_points < 5 or self.parameters.a_pts < 1 or self.parameters.b_pts < 1:
            return 0

        if self.parameters.a_pts + self.parameters.b_pts > num_points -3:
            return 0
        
        if self.parameters.radius1 < 0
            return 0

        for i in range(self.num_points - self.parameters.a_pts - self.parameters.b_pts - 2):
            Point2D p1 = self.points[i]
            Point2D p2 = self.points[i + self.parameters.a_pts + 1]
            Point2D p3 = self.points[i + self.parameters.a_pts + self.parameters.b_pts + 2]
            pointsInCircleFlag = withinCircle(p1, p2, p3, self.parameters.radius1)

            if not pointsInCircleFlag:
                return 1

        return 0

    def lic_9(self):
        return 1

    def lic_10(self):
        return 1

    def lic_11(self):
        return 1

    def lic_12(self):
        return 1

    def lic_13(self):
        return 1

    def lic_14(self):
        return 1

    # Helper functions
    def withinCircle(p1: Point2D, p2: Point2D, p3: Point2D, r):
        dist12 = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        dist23 = np.sqrt((p2.x - p3.x)**2 + (p2.y - p3.y)**2)
        dist31 = np.sqrt((p3.x - p1.x)**2 + (p3.y - p1.y)**2)

        # If all the points are in a line return true
        if (p1.y - p2.y)*(p1.x - p3.x) == (p1.y - p3.y)*(p1.x - p2.x):
            if (dist12 <= r) and (dist31 <= r) and (dist23 <= r):
                return 1

        # Calculating the radius if the circumcircle
        numerator  = dist12 * dist23 * dist31
        denomenator = (dist12 + dist31 + dist23) * (- dist12 + dist23 + dist31 ) * (dist12 - dist23 + dist31) * (dist12 + dist23 - dist31)
        # Making sure that the denominator is not zero
        if denomenator == 0:
            return 0
        r_circum = numerator / np.sqrt(denomenator)
        # Checking if a point is inside or on the circle with radius1
        if (r_circum <= r):
            return 1
        
        return 0
        

