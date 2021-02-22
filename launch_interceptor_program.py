import numpy as np
import math
import launch_Parameters as Params


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
        return

    def compute_pum(self):
        return

    def compute_fuv(self):
        return

    # Return TRUE if two consecutive data points are a distance greater than the length1 apart, else return FALSE
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

    def lic_1(self):
        return

    def lic_2(self):
        return

    def lic_3(self):
        return

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
