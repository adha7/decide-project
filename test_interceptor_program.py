import pytest
import Point2D
import launch_interceptor_program as lip
import launch_Parameters as Params
import Connector as Con

# Constants
PI = 3.14


# TEST LIC0
@pytest.mark.parametrize("length1,expected", [
    (4, 1),
    (6, 1),
    (10, 1),
    (20, 0),
])
# lic0 returns TUE if two consecutive data point are a greater distance than the length length1
def test_lic0(length1, expected):
    num_points = 5
    points = [Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(3.0, 5.0),
              Point2D.Point2D(10.0, 10.0), Point2D.Point2D(20.0, 20.0)]

    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.length1 = length1
    assert interceptor_system.lic_0() == expected


# TEST LIC1
@pytest.mark.parametrize("points,radius1,expected", [
    # Testing the boundaries
    ([Point2D.Point2D(-1.0, 0.0), Point2D.Point2D(0.0, 1.0), Point2D.Point2D(1.0, 0.0)], -1, 0),
    # Testing if LIC1 returns FALSE if three consecutive data points are within the circle
    ([Point2D.Point2D(-1.0, 0.0), Point2D.Point2D(0.0, 1.0), Point2D.Point2D(1.0, 0.0)], 1.5, 0),
    # Testing if LIC1 returns TRUE if three consecutive data points are outside of the circle
    ([Point2D.Point2D(-2.0, 0.0), Point2D.Point2D(0.0, 2.0), Point2D.Point2D(2.0, 0.0)], 1.5, 1),
    # Testing if LIC1 returns FALSE if three consecutive data points are within the circle of radius 10
    ([Point2D.Point2D(-2.0, 0.0), Point2D.Point2D(0.0, 2.0), Point2D.Point2D(0.0, 0.0)], 10, 0),
])
# lic1 returns TRUE if three consecutive data points are not all contained within or on a circle of radius radius1
def test_lic1(points, radius1, expected):
    num_points = 3
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.radius1 = radius1
    assert interceptor_system.lic_1() == expected


# TEST LIC2
@pytest.mark.parametrize("epsilon,expected", [
    # Testing if LIC2 returns TRUE if three consecutive points form an angle greater than 180 + epsilon=10 degrees
    (PI / 18.0, 1),
    # Testing if LIC2 returns TRUE if three consecutive points form an angle greater than 180 + epsilon=89 degrees
    (PI * 0.499, 1),
    # Testing if LIC2 returns FALSE if three consecutive points form an angle not greater than 180 + epsilon=90 degrees
    (PI * 0.50, 0),
])
# Return TRUE if three consecutive points form an angle greater than PI+epsilon or less than PI-epsilon
def test_lic2(epsilon, expected):
    num_points = 4
    points = [Point2D.Point2D(-1.0, -1.0), Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),
              Point2D.Point2D(1.0, -1.0)]
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.epsilon = epsilon
    assert interceptor_system.lic_2() == expected


# TEST LIC3
@pytest.mark.parametrize("area1,expected", [
    # Testing if LIC3 returns FALSE if area1 is less than 0
    (-2, 0),
    # Testing if LIC3 returns TRUE if three consecutive points are the vertices of a triangle with area > 2
    (2, 1),
    # Testing if LIC3 returns FALSE if three consecutive points are the vertices of a triangle with area < 5
    (5, 0),
])
# Return TRUE if there exists a set of three consecutive points that are the vertices of a triangle with area
# greater than parameters.area1
def test_lic3(area1, expected):
    num_points = 5
    points = [Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, 0.0), Point2D.Point2D(0.0, 0.0),
              Point2D.Point2D(-3.0, 3.0), Point2D.Point2D(-3.0, 0.0)]
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.area1 = area1
    assert interceptor_system.lic_3() == expected


# TEST LIC4
@pytest.mark.parametrize("q_pts,q_uads,expected", [
    # Testing if LIC4 returns FALSE if two consecutive points do not lie in more than 2 quadrants
    (2, 2, 0),
    # Testing if LIC4 returns TRUE if three consecutive points lie in more than 2 quadrants
    (3, 2, 1),
    # Testing if LIC4 returns FALSE if q_pts is less than 2
    (1, 3, 0),
    # Testing if LIC4 returns FALSE if two consecutive points do not lie in more than 3 quadrants
    (2, 3, 0),
])
# Return TRUE if there exists at least one set of Q_PTS consecutive data points that lie in more than QUADS
# quadrants.                       2 <= Q_PTS <= NUMPOINTS, 1 <= QUADS <= 3
def test_lic4(q_pts, q_uads, expected):
    num_points = 4
    points = [Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, -1.0), Point2D.Point2D(-1.0, 1.0),
              Point2D.Point2D(-1.0, -1.0)]
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.q_pts = q_pts
    interceptor_system.parameters.q_uads = q_uads
    assert interceptor_system.lic_4() == expected


# TEST LIC5
@pytest.mark.parametrize("points,num_points,expected", [
    # Testing if LIC5 returns FALSE if there do not exists two consecutive data points where X[j] - X[i] < 0
    ([Point2D.Point2D(0.0, 0.0)], 1, 0),
    # Testing if LIC5 returns FALSE if there do not exists two consecutive data points where X[j] - X[i] < 0
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0)], 2, 0),
    # Testing if LIC5 returns FALSE if there do not exists two consecutive data points where X[j] - X[i] < 0
    ([Point2D.Point2D(0.0, 1.0), Point2D.Point2D(0.0, 1.0)], 2, 0),
    # Testing if LIC5 returns TRUE if there exists two consecutive data points where X[j] - X[i] < 0
    ([Point2D.Point2D(1.0, 0.0), Point2D.Point2D(0.0, 0.0)], 2, 1),
])
# Return TRUE if there exists at least one set of two consecutive data points where X[j] - X[i] < 0 (where i=j-1)
def test_lic5(points, num_points, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)
    assert interceptor_system.lic_5() == expected


# TEST LIC6
@pytest.mark.parametrize("points,num_points,n_pts,dist,expected", [
    # Testing if LIC6 returns FALSE if there do not exist at least one point of the set of 2 consecutive data points
    # that lie a distance greater than 1
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(0.0, 0.0)], 2, 1, 1, 0),
    # Testing if LIC6 returns FALSE if there do not exist at least one point of the set of 3 consecutive data points
    # that lie a distance greater than 3
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 2.0), Point2D.Point2D(3.0, 0.0)], 3, 3, 3, 0),
    # Testing if LIC6 returns TRUE if there exist at least one point of the set of 3 consecutive data points that lie a
    # distance greater than 0
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 2.0), Point2D.Point2D(3.0, 0.0)], 3, 3, 0, 1),
    # Testing if LIC6 returns TRUE if there exist at least one point of the set of 3 consecutive data points that lie a
    # distance greater than 1
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(2.0, 2.0), Point2D.Point2D(0.0, 0.0)], 3, 3, 1, 1),
])
# Return TRUE if there exists at least one set of N PTS consecutive data points such that at least one of the points
# lies a distance greater than DIST from the line joining the first and last of these N PTS points
# When NUMPOINTS < 3, the condition is not met
def test_lic6(points, num_points, n_pts, dist, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.n_pts = n_pts
    interceptor_system.parameters.dist = dist
    assert interceptor_system.lic_6() == expected


# TEST LIC7
@pytest.mark.parametrize("points,num_points,k_pts,length1,expected", [
    # Testing if LIC7 returns FALSE if there do not exist one set of two data points separated by exactly 1
    # consecutive intervening points that are on a distance greater than 1
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 1.0)], 1, 1, 1, 0),
    # Testing if LIC7 returns FALSE if there do not exist one set of two data points separated by exactly 1
    # consecutive intervening points that are  on a distance greater than 2
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0), Point2D.Point2D(0.0, 1.0)], 3, 1, 2, 0),
    # Testing if LIC7 returns TRUE if there exist one set of two data points separated by exactly 1
    # consecutive intervening points that are  on a distance greater than 2
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(3.0, 0.0), Point2D.Point2D(5.0, 0.0)], 3, 1, 2, 1),
])
# Return TRUE if there exists at least one set of two data points separated by exactly K PTS consecutive intervening
# points that are a distance greater than the length, LENGTH1, apart
def test_lic7(points, num_points, k_pts, length1, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.k_pts = k_pts
    interceptor_system.parameters.length1 = length1
    assert interceptor_system.lic_7() == expected


# TEST COMPUTE CMV
def test_compute_cmv():
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    num_points = 5
    points = [Point2D.Point2D(0.0, 1.0), Point2D.Point2D(1.0, 0.0), Point2D.Point2D(2.0, 0.0),
              Point2D.Point2D(3.0, 0.0), Point2D.Point2D(3.0, 4.0)]

    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.radius2 = 10
    interceptor_system.parameters.radius2 = 1.5
    interceptor_system.parameters.nPTS = 5
    interceptor_system.parameters.dist = 1.5
    interceptor_system.parameters.area2 = 4
    expected = [True, True, True, True, False, False, False, True, True, True, True, False, False, False, False]

    # Testing if all cmv values are correctly set
    interceptor_system.compute_cmv()
    assert sum(interceptor_system.cmv) == sum(expected)


# TEST DECIDE
# Testing if Decide() returns TRUE if all values in FUV are true, false otherwise
def test_decide():
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(0, None, parameters, Con.Connector.ANDD, None)
    interceptor_system.fuv = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]

    assert interceptor_system.launch_decision()

# TEST LIC8
@pytest.mark.parametrize("points,num_points,a_pts,b_pts,radius1,expected", [
    ####################################  SMALL RADIUS THAT CAN FIT THE DATA POINTS  ###############################
    # Tests if LIC8 returns TRUE if there exist one set of three data points separated by exactly 2 and 1
    # consecutive intervening points , that cannot be contained within or on a circle of radius 0.5
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.5, 0.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 0.5, 1),
    ####################################  LARGE RADIUS THAT CAN NOT FIT THE DATA POINTS  ###########################
    # Tests if LIC8 returns FALSE if there exist one set of three data points separated by exactly 2 and 1
    # consecutive intervening points , that cannot be contained within or on a circle of radius 3
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.5, 0.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 3, 0),
    ####################################  CORNER CONDITIONS/ EXCEPTIONS  ###########################################
    # Tests if LIC8 returns FALSE if the number of points are less than 5
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0), Point2D.Point2D(0.0, 1.0)], 3, 1, 2, 2, 0),
    # Tests if LIC8 returns FALSE if there exist one set of three data points separated by exactly 2 and 2 (corner condition)
    # consecutive intervening points that cannot be contained within or on a circle of radius 0.5
    ([Point2D.Point2D(-1.0, 0.0), Point2D.Point2D(1.5, 0.5),Point2D.Point2D(1.5, -0.5), Point2D.Point2D(0.0, 1.0), Point2D.Point2D(-1.5, 0.5), Point2D.Point2D(1.0, 0.0)], 6, 2, 2, 0.5, 0),
])
# Return TRUE if there is at least one set of three data points separated by exactly
# A_PTS and B_PTS consecutive intervening points, respectively, that cannot be contained
# within or on a circle of radius RADIUS1.
def test_lic8(points, num_points, a_pts, b_pts, radius1, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.a_pts = a_pts
    interceptor_system.parameters.b_pts = b_pts
    interceptor_system.parameters.radius1 = radius1
    assert interceptor_system.lic_8() == expected

# TEST LIC9
@pytest.mark.parametrize("points,num_points,c_pts,d_pts,epsilon,expected", [
    ####################################  ANGLE IS LESS THAN PI - EPSILON  ###############################
    # Tests if LIC9 returns TRUE if there exist one set of three data points separated by exactly 1 and 1
    # consecutive intervening points , that form an angle such that forms an angle < (PI−1.5)
    ([Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(0.0, 0.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-1.5, -1.0), Point2D.Point2D(0.0, 1.5)], 6, 1, 1, 1.5, 1),
    ####################################  ANGLE IS GREATER THAN PI - EPSILON ###########################
    # Tests if LIC9 returns FALSE if there exist one set of three data points separated by exactly 2 and 1
    # consecutive intervening points , that form an angle such that forms an angle > (PI−3.4)
    ([Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(0.0, 0.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-1.5, -1.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 3.4, 0),
    ####################################  CORNER CONDITIONS/ EXCEPTIONS  ###########################################
    # Tests if LIC9 returns FALSE if the number of points are less than 5
    ([Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(0.0, 0.0)], 3, 1, 2, 2, 0),
    # Tests if LIC9 returns FALSE if either the first point or the last point (or both) coincide with the vertex, the
    # angle is undefined and the LIC is not satisfied by those three points. (either c_pts or d_pts are 0)
    ([Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(0.0, 0.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-1.5, -1.0), Point2D.Point2D(0.0, 1.5)], 6, 0, 1, 1.5, 0),
])
# Return TRUE if there is at least one set of three data points separated by exactly
# C_PTS and D_PTS consecutive intervening points, respectively, that form an angle < (PI-Epsilon)
# or angle > (PI+Epsilon).
def test_lic9(points, num_points, c_pts, d_pts, epsilon, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.c_pts = c_pts
    interceptor_system.parameters.d_pts = d_pts
    interceptor_system.parameters.epsilon = epsilon
    assert interceptor_system.lic_9() == expected


# TEST LIC10
@pytest.mark.parametrize("points,num_points,e_pts,f_pts,area1,expected", [
    ####################################  AREA OF THE TRIANGLE LESS THAN 8  ###############################
    # Tests if LIC10 returns TRUE if there exist one set of three data points separated by exactly 1 and 2
    # consecutive intervening points , that are the vertices of a triangle with area greater than 7 (actual area is 8)
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(11.0, 6.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-4.5, -1.0), Point2D.Point2D(13.0, 3.0)], 6, 1, 2, 7, 1),
    ####################################  AREA OF THE TRIANGLE EQUAL TO 8 ###########################
    # Tests if LIC10 returns FALSE if there exist one set of three data points separated by exactly 1 and 2
    # consecutive intervening points , that are the vertices of a triangle with area equal to 8
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(11.0, 6.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-4.5, -1.0), Point2D.Point2D(13.0, 3.0)], 6, 1, 2, 8, 0),
    ####################################  CORNER CONDITIONS/ EXCEPTIONS  ###########################################
    # Tests if LIC10 returns FALSE if the number of points are less than 5
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(11.0, 6.0)], 3, 1, 2, 2, 0),
    ####################################  AREA OF THE TRIANGLE LESS THAN 8 ###########################
    # Tests if LIC10 returns FALSE if there exist one set of three data points separated by exactly 1 and 2
    # consecutive intervening points , that are the vertices of a triangle with area less than 9
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(11.0, 6.0), Point2D.Point2D(-1.0, 1.0), Point2D.Point2D(-4.5, -1.0), Point2D.Point2D(13.0, 3.0)], 6, 1, 2, 9, 0),
])
# Return TRUE if there is at least one set of three data points separated by exactly
# E_PTS and F_PTS consecutive intervening points, respectively, that they are the
# vertices of a triangle with area greater than AREA1.
def test_lic10(points, num_points, e_pts, f_pts, area1, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.e_pts = e_pts
    interceptor_system.parameters.f_pts = f_pts
    interceptor_system.parameters.area1 = area1
    assert interceptor_system.lic_10() == expected


# TEST LIC11
@pytest.mark.parametrize("points,num_points,g_pts,expected", [
    ####################################  X[j] - X[i] < 0  ###############################
    # Tests if LIC11 returns TRUE if there exist one set of two data points separated by exactly 1
    # consecutive intervening points , such that X[j] - X[i] < 0.
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(1.0, 6.0)], 3, 1, 1),
    ####################################  X[j] - X[i] > 0 ###########################
    # Tests if LIC11 returns FALSE if there exist one set of three data points separated by exactly 1 and 2
    # consecutive intervening points , that are the vertices of a triangle with area equal to 8
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(13.0, 3.0), Point2D.Point2D(11.0, 6.0)], 3, 1, 0),
    ####################################  CORNER CONDITION ###########################
    # Tests if the number of points is less than 3
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(13.0, 3.0)], 2, 1, 0),
])
# Return TRUE if there is at least one set of two data points separated by exactly
# G_PTS consecutive intervening points, such that X[j] - X[i] < 0.
def test_lic11(points, num_points, g_pts, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.g_pts = g_pts
    assert interceptor_system.lic_11() == expected


# TEST LIC12
@pytest.mark.parametrize("points,num_points,k_pts,length1,length2,expected", [
    ##########################  distance greater than the length1 and less than length2  ############################
    # Tests if LIC12 returns TRUE if there exist one set of two data points separated by exactly 2
    # consecutive intervening points , such that distance greater than the length1 and less than length2.
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(1.0, 6.0), Point2D.Point2D(11.0, 4.0)], 4, 2, 2, 5, 1),
    ################################  distance greater than the length1 and length2  ################################
    # Tests if LIC12 returns FALSE if there exist one set of three data points separated by exactly 2
    # consecutive intervening points , such that distance greater than the length1 and length2.
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(1.0, 6.0), Point2D.Point2D(11.0, 4.0)], 4, 2, 2, 1, 0),
    ################################  distance less than the length1 and length2  ################################
    # Tests if LIC12 returns FALSE if there exist one set of three data points separated by exactly 2
    # consecutive intervening points , such that distance greater than the length1 and length2.
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(2.0, 3.0),Point2D.Point2D(1.0, 6.0), Point2D.Point2D(11.0, 6.0)], 4, 2, 5, 6, 0),
    # Tests if the number of points is less than 3
    ([Point2D.Point2D(7.0, 4.0), Point2D.Point2D(13.0, 3.0)], 2, 1, 1, 1, 0),
])
# Return TRUE if there is at least one set of two data points separated by exactly
# K_PTS consecutive intervening points, which are a distance greater than the length,
# LENGTH1, apart and if there is at least one set of two data points, separated by
# exactly K_PTS consecutive intervening points, that are a distance less than the
# length, LENGTH2, apart.
def test_lic12(points, num_points, k_pts, length1, length2, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.k_pts = k_pts
    interceptor_system.parameters.length1 = length1
    interceptor_system.parameters.length2 = length2
    assert interceptor_system.lic_12() == expected


# TEST LIC13
@pytest.mark.parametrize("points,num_points,a_pts,b_pts,radius1,radius2,expected", [
    ##########################  distance greater than the length1 and less than length2  ############################
    # Tests if LIC13 returns TRUE if there exist one set of three data points separated by exactly 2 and 1
    # consecutive intervening points , that cannot be contained within or on a circle of radius 0.5 and can be
    # contained within or on a circle of radius 2.
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.5, 0.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 0.5, 2, 1),
    ################################  distance greater than the length1 and length2  ################################
	# Tests if LIC13 returns FALSE if there exist one set of three data points separated by exactly 2 and 1
	# consecutive intervening points , that cannot be contained within or on a circle of radius 0.5 and of radius 0.6.
	([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.5, 0.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 0.5, 0.6, 0),
	################################  distance less than the length1 and length2  ################################
	# Tests if LIC13 returns FALSE if there exist one set of three data points separated by exactly 2 and 1
	# consecutive intervening points , that can be contained within or on a circle of radius 2 and of radius 5.
	([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0), Point2D.Point2D(1.0, 1.0), Point2D.Point2D(1.5, 0.0), Point2D.Point2D(0.0, 1.5)], 6, 2, 1, 2, 5, 0),
    # Tests if the number of points is less than 3
    ([Point2D.Point2D(0.0, 0.0), Point2D.Point2D(1.0, 0.0),Point2D.Point2D(1.0, 0.0)], 3, 1, 1, 1, 3, 0),
])
# Return TRUE if there is at least one set of three data points separated by exactly
# A_PTS and B_PTS consecutive intervening points, respectively, that cannot be
# contained within or on a circle of radius RADIUS1 and if there is at least one set of
# three data points separated by exactly A_PTS and B_PTS consecutive intervening points,
# respectively, that can be contained in or on a circle of radius RADIUS2.

def test_lic13(points, num_points, a_pts, b_pts, radius1, radius2, expected):
    parameters = Params.Parameters(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    interceptor_system = lip.Decide(num_points, points, parameters, Con.Connector.ANDD, None)

    interceptor_system.parameters.a_pts = a_pts
    interceptor_system.parameters.b_pts = b_pts
    interceptor_system.parameters.radius1 = radius1
    interceptor_system.parameters.radius2 = radius2
    assert interceptor_system.lic_13() == expected

