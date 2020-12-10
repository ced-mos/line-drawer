import unittest


# class TestGeometry(unittest.TestCase):
#     def test_ole(self):
#         self.assertEqual(1,1)

from src.geometry import Point, LineSegment, Line, Rectangle


class TestGeometryPoint(unittest.TestCase):
    
    def test_as_tuple(self):
        p_as_tupple = (3.0, 1.0)
        self.assertEqual(
            Point(p_as_tupple[0], p_as_tupple[1]).as_tuple(), p_as_tupple)

    def test_equals(self):
        p_1, p_2 = (Point(0.0, 1.0), Point(0.0, 1.0))
        self.assertTrue(p_1.equals(p_2))

        p_1, p_2 = (Point(0.0, 0.0), Point(0.0, 0.1))
        self.assertFalse(p_1.equals(p_2))

        p_1, p_2 = (Point(0.0, 0.0), Point(0.0, 1e-5))
        self.assertTrue(p_1.equals(p_2))


class TestGeometryLineSegment(unittest.TestCase):

    def test_is_intersecting(self):

        l_1 = LineSegment(Point(0.0, 0.0), Point(0.0, 1.0))
        l_2 = LineSegment(Point(0.0, 0.0), Point(1.0, 0.0))
        l_3 = LineSegment(Point(0.0, 2.0), Point(1.0, 2.0))

        self.assertTrue(l_1.is_intersecting(l_2))
        self.assertFalse(l_1.is_intersecting(l_3))

    def test_intersection_with_line_segment__edge_case(self):
        p_1 = Point(0.0, 0.0)
        l_1 = LineSegment(p_1, Point(0.0, 1.0))
        l_2 = LineSegment(p_1, Point(1.0, 0.0))

        intersection = l_1.intersection_with_line_segment(l_2)
        self.assertTrue(len(intersection) == 1)
        self.assertTrue(intersection[0].equals(p_1))

    def test_intersection_with_line_segment__center_case(self):
        intersection_point = Point(0.5, 0.5)
        l_1 = LineSegment(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = LineSegment(Point(0.0, 1.0), Point(1.0, 0.0))

        intersection = l_1.intersection_with_line_segment(l_2)
        self.assertTrue(len(intersection) == 1)
        self.assertTrue(intersection[0].equals(intersection_point))

    def test_intersection_with_line_segment__no_intersection_case(self):
        l_1 = LineSegment(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = LineSegment(Point(-2.0, -2.0), Point(-3.0, -3.0))

        intersection = l_1.intersection_with_line_segment(l_2)
        self.assertTrue(len(intersection) == 0)

    def test_intersection_with_line_segment__parallel_case(self):
        l_1 = LineSegment(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = LineSegment(Point(0.0, 0.0), Point(1.0, 1.0))

        intersection = l_1.intersection_with_line_segment(l_2)
        self.assertTrue(len(intersection) == 0)


class TestGeometryLine(unittest.TestCase):

    def test_is_intersecting(self):

        l_1 = Line(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = Line(Point(-2.0, 2.0), Point(1.0, -1.0))
        l_3 = Line(Point(2.0, 2.0), Point(1.0, 1.0))

        self.assertTrue(l_1.is_intersecting(l_2))
        self.assertFalse(l_1.is_intersecting(l_3))

    def test_intersection_with_line__edge_case(self):
        p_1 = Point(0.0, 0.0)
        l_1 = Line(p_1, Point(0.0, 1.0))
        l_2 = Line(p_1, Point(1.0, 0.0))

        intersection = l_1.intersection_with_line(l_2)
        self.assertTrue(len(intersection) == 1)
        self.assertTrue(intersection[0].equals(p_1))

    def test_intersection_with_line__center_case(self):
        intersection_point = Point(0.5, 0.5)
        l_1 = Line(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = Line(Point(0.0, 1.0), Point(1.0, -1.0))

        intersection = l_1.intersection_with_line(l_2)
        self.assertTrue(len(intersection) == 1)
        self.assertTrue(intersection[0].equals(intersection_point))

    def test_intersection_with_line__no_intersection_case(self):
        l_1 = Line(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = Line(Point(0.0, 0.0), Point(1.0, 1.0))

        intersection = l_1.intersection_with_line(l_2)
        self.assertTrue(len(intersection) == 0)

    def test_intersection_with_line__parallel_case(self):
        l_1 = Line(Point(0.0, 0.0), Point(1.0, 1.0))
        l_2 = Line(Point(1.0, 1.0), Point(1.0, 1.0))

        intersection = l_1.intersection_with_line(l_2)
        self.assertTrue(len(intersection) == 0)


class TestGeometryRectangle(unittest.TestCase):

    def test_intersection_with_line__two_intersections_with_one_edge_intersection(self):
        start_point = Point(-1, -1)
        direction = Point(1, 1)
        test_line = Line(start_point, direction)
        test_rectangle = Rectangle(30, 40)
        intersections = test_rectangle.intersection_with_line(test_line)
        self.assertTrue(len(intersections) == 2)

        # Check if all testpoints are available.
        test_points = ( Point(0.0, 0.0), Point(30.0,30.0) )
        for test_point in test_points:
            self.assertTrue(test_point in intersections)

    def test_intersection_with_line__no_intersection(self):
        start_point = Point(-1, -1)
        direction = Point(1, -1)
        test_line = Line(start_point, direction)
        test_rectangle = Rectangle(40, 30)
        intersections = test_rectangle.intersection_with_line(test_line)
        self.assertTrue(len(intersections) == 0)

    def test_intersection_with_line__one_intersection(self):
        start_point = Point(-1, -1 + 30)
        direction = Point(1, 1)
        test_line = Line(start_point, direction)
        test_rectangle = Rectangle(40, 30)
        intersections = test_rectangle.intersection_with_line(test_line)
        self.assertTrue(len(intersections) == 1)

        # Check if all testpoints are available.
        test_point = Point(0,30.0)
        self.assertTrue(test_point in intersections)
            

        


if __name__ == '__main__':
    unittest.main()
