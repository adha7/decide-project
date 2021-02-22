import numpy as np


class Decide:
    def __init__(self, num_points, points, parameters, lcm, puv):
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
        return

    def compute_pum(self):
        return

    def compute_fuv(self):
        return

    def lic_0(self):
        return

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
