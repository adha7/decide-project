import pytest
import Point2D
import launch_interceptor_program as lip
import launch_Parameters as Params
import Connector as Con


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
