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
