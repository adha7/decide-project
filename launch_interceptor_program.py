import numpy as np
import math
import launch_Parameters as Params
import Connector as Con
import Point2D
import Vector as Vec

# Constants
PI = 3.14


class Decide:
    def __init__(self, num_points, points: Point2D, parameters: Params.Parameters, lcm: Con.Connector, puv):
        self.num_points = num_points
        self.points = points
        self.parameters = parameters
        self.lcm = lcm
        self.puv = puv
        self.cmv = np.zeros(15)              # The Conditions Met Vector (CMV), a 15-element vector.
        self.pum = np.array([15, 15], bool)  # Preliminary Unlocking Matrix (PUM), a 15x15 matrix.
        self.fuv = np.zeros(15)              # The Final Unlocking Vector (FUV), a 15-element vector.

    def launch_decision(self):
        for count, value in enumerate(self.fuv):
            if not value:
                return 0

        return 1

    def compute_cmv(self):
        self.cmv[0] = self.lic_0()
        self.cmv[1] = self.lic_1()
        self.cmv[2] = self.lic_2(0, PI)
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
        pum_rows, pum_columns = self.pum.shape
        for i in range(0, pum_rows):
            for j in range(0, pum_columns):
                if self.lcm[i][j] == Con.Connector.ANDD:
                    self.pum[i][j] = self.cmv[i] and self.cmv[j]
                elif self.lcm[i][j] == Con.Connector.ORR:
                    self.pum[i][j] = self.cmv[i] or self.cmv[j]
                else:
                    self.pum[i][j] = 1

    def compute_fuv(self):
        fuv_length = len(self.fuv)
        for i in range(0, fuv_length):
            if not(self.puv[i]) or sum(self.pum[i]) == len(self.pum[i]):
                self.fuv[i] = True
            else:
                self.fuv[i] = False

    # Return TRUE if two consecutive data points are a distance greater than the length1 apart
    def lic_0(self):

        # Check the boundaries
        if self.parameters.length1 < 0:
            return 0

        for i in range(0, len(self.points) - 1):

            # Calculate the distance between point p1 and p2
            p1 = self.points[i]
            p2 = self.points[i + 1]
            distance = self.calculate_distance(p2, p1)

            # Check if the distance is greater than length1 in the parameters
            if distance > self.parameters.length1:
                return 1

        return 0

    # Return TRUE if three consecutive data points are not contained within or on a circle of radius1
    def lic_1(self):

        # Check the boundaries
        if self.parameters.radius1 < 0:
            return 0

        for i in range(0, len(self.points) - 2):

            # Calculate the distance between points p1, p2 and p3
            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]

            # Check if points b or c is inside or on the radius radius1 away from a
            if self.within_circle(p1, p2, p3, self.parameters.radius1):
                return 0
        return 1

    def calculate_distance(self, point_1, point_2):
        length = math.sqrt(math.pow(point_1.x - point_2.x, 2) + math.pow(point_1.y - point_2.y, 2))
        return length

    # Return TRUE if three consecutive points form an angle greater than PI+epsilon or less than PI-epsilon
    def lic_2(self, lower_limit, upper_limit):

        # Check the boundaries
        if self.parameters.epsilon < lower_limit or self.parameters.epsilon >= upper_limit:
            return 0

        # Iterate over all sets of three consecutive points
        for i in range(0, len(self.points) - 2):

            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]

            # Calculate the two vectors using point 2 as vertex
            vector1 = Vec.Vector(p2, p1)
            vector2 = Vec.Vector(p2, p3)

            dotProduct = vector1.x * vector2.x + vector1.y * vector2.y
            vector1Len = math.sqrt(math.pow(vector1.x, 2) + math.pow(vector1.y, 2))
            vector2Len = math.sqrt(math.pow(vector2.x, 2) + math.pow(vector2.y, 2))

            # If any two points coincide then move on
            if vector1Len == 0 or vector2Len == 0:
                continue

            # Obtain the angle through the definition of dot product in euclidean space
            angle = math.acos(dotProduct / (vector1Len * vector2Len))

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
        for i in range(0, len(self.points) - 2):

            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]

            # Calculate the sides of the triangle
            length1 = self.calculate_distance(p1, p2)
            length2 = self.calculate_distance(p1, p3)
            length3 = self.calculate_distance(p2, p3)

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
            num_quads = [False, False, False, False]

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
        for i in range(0, len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]

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
            distance = self.calculate_distance(p2, p1)

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

        if self.parameters.a_pts + self.parameters.b_pts > self.num_points - 3:
            return 0

        if self.parameters.radius1 < 0:
            return 0

        for i in range(self.num_points - self.parameters.a_pts - self.parameters.b_pts - 2):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.a_pts + 1]
            p3 = self.points[i + self.parameters.a_pts + self.parameters.b_pts + 2]
            pointsInCircleFlag = self.within_circle(p1, p2, p3, self.parameters.radius1)

            if not pointsInCircleFlag:
                return 1

        return 0

    # Return TRUE if there is at least one set of three data points separated by exactly
    # C_PTS and D_PTS consecutive intervening points, respectively, that form an angle
    def lic_9(self):
        if self.num_points < 5 or self.parameters.c_pts < 1 or self.parameters.d_pts < 1:
            return 0

        if self.parameters.c_pts + self.parameters.d_pts > self.num_points - 3:
            return 0

        for i in range(self.num_points - self.parameters.c_pts - self.parameters.d_pts - 2):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.c_pts + 1]
            p3 = self.points[i + self.parameters.c_pts + self.parameters.d_pts + 2]

            # Taking point 2 as vertex, finding the vectors to create an angle
            v1 = (p1.x - p2.x, p1.y - p2.y)
            v2 = (p3.x - p2.x, p3.y - p2.y)

            # The cosine of the angle between two vectors is equal to the dot product
            # of this vectors divided by the product of vector magnitude.
            v1Len = math.sqrt(math.pow(v1[0], 2) + math.pow(v1[1], 2))
            v2Len = math.sqrt(math.pow(v2[0], 2) + math.pow(v2[1], 2))

            if (v1Len == 0) or (v2Len == 0):
                continue

            angle = math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (v1Len * v2Len))

            if angle < (PI - self.parameters.epsilon):
                return 1

        return 0

        # Return TRUE if there is at least one set of three data points separated by exactly

    # E_PTS and F_PTS consecutive intervening points, respectively, that they are the
    # vertices of a triange with area greater than AREA1. 

    def lic_10(self):
        if self.num_points < 5 or self.parameters.e_pts < 1 or self.parameters.f_pts < 1:
            return 0

        if self.parameters.e_pts + self.parameters.f_pts > self.num_points - 3:
            return 0

        for i in range(self.num_points - self.parameters.e_pts - self.parameters.f_pts - 2):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.e_pts + 1]
            p3 = self.points[i + self.parameters.e_pts + self.parameters.f_pts + 2]

            # Finding the vectors to create an triangle
            v1 = (p1.x - p2.x, p1.y - p2.y)
            v2 = (p3.x - p1.x, p3.y - p1.y)
            v3 = (p2.x - p3.x, p2.y - p3.y)

            # Calculating the length of sides of the triangle
            v1Len = math.sqrt(math.pow(v1[0], 2) + math.pow(v1[1], 2))
            v2Len = math.sqrt(math.pow(v2[0], 2) + math.pow(v2[1], 2))
            v3Len = math.sqrt(math.pow(v3[0], 2) + math.pow(v3[1], 2))

            # Calculating the are of the triangle 
            semi_perimeter = (v1Len + v2Len + v3Len) / 2
            area = math.sqrt(
                semi_perimeter * (semi_perimeter - v1Len) * (semi_perimeter - v2Len) * (semi_perimeter - v3Len))
            print("Area",area)
            if area > self.parameters.area1:
                return 1

        return 0

    # Return TRUE if there is at least one set of two data points separated by exactly
    # G_PTS consecutive intervening points, such that X[j] - X[i] < 0.

    def lic_11(self):
        if self.num_points < 3 or self.parameters.g_pts < 1 or self.num_points - 2 < 1:
            return 0

        for i in range(self.num_points - self.parameters.g_pts - 1):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.g_pts + 1]

            if p2.x - p1.x < 0:
                return 1

        return 0

    # Return TRUE if there is at least one set of two data points separated by exactly
    # G_PTS consecutive intervening points, which are a distance greater than the length,
    # LENGTH1, apart and if there is at least one set of two data points, separated by 
    # exactly K_PTS consecutive intervening points, that are a distance less than the 
    # length, LENGTH2, apart.

    def lic_12(self):
        if self.num_points < 3 or self.parameters.length2 < 0:
            return 0

        flag1 = 0
        flag2 = 0

        for i in range(self.num_points - self.parameters.k_pts - 1):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.k_pts + 1]

            # Calculate the distance between two points
            dist = self.calculate_distance(p2, p1)

            if dist > self.parameters.length1:
                flag1 = 1

            if dist < self.parameters.length2:
                flag2 = 1

            if flag1 and flag2:
                return 1

        return 0

    # Return TRUE if there is at least one set of three data points separated by exactly
    # A_PTS and B_PTS consecutive intervening points, respectively, that cannot be 
    # contained within or on a circle of radius RADIUS1 and if there is at least one set of  
    # three data points separated by exactly A_PTS and B_PTS consecutive intervening points,
    # respectively, that can be contained in or on a circle of radius RADIUS2.

    def lic_13(self):
        if self.num_points < 5 or self.parameters.radius2 < 0:
            return 0

        for i in range(self.num_points - self.parameters.a_pts - self.parameters.b_pts - 2):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.a_pts + 1]
            p3 = self.points[i + self.parameters.a_pts + self.parameters.b_pts + 2]

            if not self.within_circle(p1, p2, p3, self.parameters.radius1) and self.within_circle(p1, p2, p3, self.parameters.radius2):
                return 1

        return 0

    # Return TRUE if there is at least one set of three data points separated by exactly
    # E PTS and F PTS consecutive intervening points, respectively, that are the vertices
    # of a triangle with area greater than AREA1 and if there is at least one set of  
    # three data points separated by exactly E PTS and F PTS consecutive intervening points,
    # respectively, that are the vertices of a triangle with area less than AREA2. 

    def lic_14(self):
        if self.num_points < 5 or self.parameters.area2 < 0:
            return 0

        flag1 = 0
        flag2 = 0

        for i in range(self.num_points - self.parameters.e_pts - self.parameters.f_pts - 2):
            p1 = self.points[i]
            p2 = self.points[i + self.parameters.e_pts + 1]
            p3 = self.points[i + self.parameters.e_pts + self.parameters.f_pts + 2]

            # Calculating the length of sides of the triangle
            v1Len = self.calculate_distance(p1, p2)
            v2Len = self.calculate_distance(p1, p3)
            v3Len = self.calculate_distance(p2, p3)

            # Calculating the are of the triangle 
            semi_perimeter = (v1Len + v2Len + v3Len) / 2
            area = math.sqrt(
                semi_perimeter * (semi_perimeter - v1Len) * (semi_perimeter - v2Len) * (semi_perimeter - v3Len))

            if area > self.parameters.area1:
                flag1 = 1

            if area < self.parameters.area2:
                flag2 = 1

            if flag1 and flag2:
                return 1

        return 0

    # Helper functions
    def within_circle(self, p1: Point2D, p2: Point2D, p3: Point2D, r):
        dist12 = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
        dist23 = np.sqrt((p2.x - p3.x) ** 2 + (p2.y - p3.y) ** 2)
        dist31 = np.sqrt((p3.x - p1.x) ** 2 + (p3.y - p1.y) ** 2)

        # If all the points are in a line return true
        if (p1.y - p2.y) * (p1.x - p3.x) == (p1.y - p3.y) * (p1.x - p2.x):
            if (dist12 <= r) and (dist31 <= r) and (dist23 <= r):
                return 1

        # Calculating the radius if the circumcircle
        numerator = dist12 * dist23 * dist31
        denominator = (dist12 + dist31 + dist23) * (- dist12 + dist23 + dist31) * (dist12 - dist23 + dist31) * (
                    dist12 + dist23 - dist31)
        # Making sure that the denominator is not zero
        if denominator == 0:
            return 0
        r_circum = numerator / np.sqrt(denominator)
        # Checking if a point is inside or on the circle with radius1
        if r_circum <= r:
            return 1

        return 0
