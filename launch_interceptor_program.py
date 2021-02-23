import numpy as np
import math
import launch_Parameters as Params

# Constants
PI = 3.14159265359


class Decide:
    def __init__(self, num_points, points, parameters: Params.Parameters, lcm, puv):
        self.num_points = num_points
        self.points = points
        self.parameters = parameters
        self.lcm = lcm
        self.puv = puv
        self.cmv = np.array(15, bool)        # The Conditions Met Vector (CMV), a 15-element vector.
        self.pum = np.array([15, 15], bool)  # Preliminary Unlocking Matrix (PUM), a 15x15 matrix.
        self.fuv = np.array(15, bool)        # The Final Unlocking Vector (FUV), a 15-element vector.

    def launch_decision(self):
        return

    def compute_cmv(self):
        self.cmv[0] = self.lic_0()
        self.cmv[1] = self.lic_1()
        self.cmv[2] = self.lic_2()
        self.cmv[3] = self.lic_3()
        return

    def compute_pum(self):
        return

    def compute_fuv(self):
        return

    # Return TRUE if two consecutive data points are a distance greater than the length1 apart
    def lic_0(self):

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

        # Iterate over all sets of three consecutive points
        for i in range(0, self.points.length - 2):

            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]

            # Calculate the two vectors using point 2 as vertex
            vector1 = (p1.x - p2.x, p1.y - p2.y)
            vector2 = (p3.x - p2.x, p3.y - p2.y)

            dotProduct = vector1[0]*vector2[0].x + vector1[1]*vector2[1]
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

        # Iterate over all sets of three consecutive points
        for i in range(0, self.points.length - 2):

            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]

            # Calculate the sides of the triangle
            length1 = math.sqrt(math.pow(p1.x-p2.x, 2)+math.pow(p1.y-p2.y, 2))
            length2 = math.sqrt(math.pow(p1.x-p3.x, 2)+math.pow(p1.y-p3.y, 2))
            length3 = math.sqrt(math.pow(p2.x-p3.x, 2)+math.pow(p2.y-p3.y, 2))

            # Calculate the area of the triangle using Heron's formula
            tmp = (length1+length2+length3)/2
            area = math.sqrt(tmp*(tmp-length1)*(tmp-length2)*(tmp-length3))

            if area > self.parameters.area1:
                return 1

        return 0

    def lic_4(self):
        return

    def lic_5(self):
        return

    def lic_6(self):
        return

    def lic_7(self):
        return

    def lic_8(self):
        return

    def lic_9(self):
        return

    def lic_10(self):
        return

    def lic_11(self):
        return

    def lic_12(self):
        return

    def lic_13(self):
        return

    def lic_14(self):
        return
