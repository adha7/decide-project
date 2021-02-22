class Parameters:
    def __init__(self, length1, radius1, epsilon, area1, q_pts, q_uads, dist, n_pts, k_pts, a_pts, b_pts, c_pts, d_pts,
                 e_pts, f_pts, g_pts, length2, radius2, area2):

        self.length1 = length1                  # Length in LICs 0, 7, 12
        self.radius1 = radius1                  # Radius in LICs 1, 8, 13
        self.epsilon = epsilon                  # Deviation from PI in LICs 2, 9
        self.area1 = area1                      # Area in LICs 3, 10, 14
        self.q_pts = q_pts                      # No. of consecutive points in LIC 4
        self.q_uads = q_uads                    # No. of quadrants in LIC 4
        self.dist = dist                        # Distance in LIC 6
        self.n_pts = n_pts                      # No. of consecutive pts. in LIC 6
        self.k_pts = k_pts                      # No. of interval points in LICs 7, 12
        self.a_pts = a_pts                      # No. of interval points in LICs 8, 13
        self.b_pts = b_pts                      # No. of interval points in LICs 8, 13
        self.c_pts = c_pts                      # No. of interval points in LIC 9
        self.d_pts = d_pts                      # No. of interval points in LIC 9
        self.e_pts = e_pts                      # No. of interval points in LICs 10, 14
        self.f_pts = f_pts                      # No. of interval points in LICs 10, 14
        self.g_pts = g_pts                      # No. of interval points in LIC 11
        self.length2 = length2                  # Maximum length in LIC 12
        self.radius2 = radius2                  # Maximum radius in LIC 13
        self.area2 = area2                      # Maximum area in LIC 14
