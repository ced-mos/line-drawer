from dataclasses import dataclass
import math

# Example how to disable linter features
# pylint: disable=R0902

# Tolerances
TOL_DIST = 1e-5
TOL_ZERO_DIV = 1e-5


@dataclass
class Point:
    x: float
    y: float

    def as_tuple(self) -> tuple:
        return (self.x, self.y)

    def equals(self, other, tol=TOL_DIST):
        return math.isclose(self.x, other.x, abs_tol=tol) and math.isclose(self.y, other.y, abs_tol=tol)

    def __add__(self, other):
        """Adds two points like a vector addition.

        Args:
            other (Point): Point to add

        Returns:
            Point: summation of two points
        """
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """Equals operator to compare if point is as similar position
        using a standard tolerances.


        Args:
            other (Point): Other point

        Returns:
            bool: return true if point is as same position.
        """
        return self.equals(other)

    def as_PointInt(self):
        return PointInt(int(self.x), int(self.y))

@dataclass
class PointInt(Point):
    x: int
    y: int


class LineSegment:
    """
    A geometric line segment defined by two points.
    """

    def __init__(self, p_1, p_2):
        self.p_1 = p_1
        self.p_2 = p_2

    def is_intersecting(self, l):
        return bool(len(self.intersection_with_line_segment(l)))

    def intersection_with_line_segment(self, l):
        """Returns list with intersection point with other line segments.
        Returns empty list if no intersection happened.

        Intersection points are determined according to two define Lines in terms
        of first degree Bézier parameters (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection).

        Args:
            l_2 (LineSegment): Line segment used to check for intersection

        Returns:
            list: List of intersection point
        """

        r_intersection_points = []

        x_1, y_1 = self.p_1.as_tuple()
        x_2, y_2 = self.p_2.as_tuple()
        x_3, y_3 = l.p_1.as_tuple()
        x_4, y_4 = l.p_2.as_tuple()

        den = (x_1-x_2)*(y_3-y_4) - (y_1-y_2)*(x_3-x_4)

        # Is line parallel or coincindent?
        if math.isclose(den, 0.0, abs_tol=TOL_ZERO_DIV):
            return r_intersection_points

        t_nom = (x_1-x_3)*(y_3-y_4) - (y_1-y_3)*(x_3-x_4)
        u_nom = - ((x_1-x_2)*(y_1-y_3) - (y_1-y_2)*(x_1-x_3))

        t = t_nom / den
        u = u_nom / den

        # Is intersection within the two line segments?
        if 0.0 <= t and t <= 1.0 and 0.0 <= u and u <= 1.0:
            p_x = x_1 + t * (x_2 - x_1)
            p_y = y_1 + t * (y_2 - y_1)
            r_intersection_points.append(Point(p_x, p_y))

        return r_intersection_points


    def intersection_with_line(self, l):
        """Returns list with intersection point with other line segments.
        Returns empty list if no intersection happened.

        Intersection points are determined according to two defined lines in terms
        of first degree Bézier parameters (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection).

        Args:
            l_2 (LineSegment): Line segment used to check for intersection

        Returns:
            list: List of intersection point
        """

        r_intersection_points = []

        x_1, y_1 = self.p_1.as_tuple()
        x_2, y_2 = self.p_2.as_tuple()

        line_segment = l.as_line_segment()
        x_3, y_3 = line_segment.p_1.as_tuple()
        x_4, y_4 = line_segment.p_2.as_tuple()

        den = (x_1-x_2)*(y_3-y_4) - (y_1-y_2)*(x_3-x_4)

        # Is line parallel or coincindent?
        if math.isclose(den, 0.0, abs_tol=TOL_ZERO_DIV):
            return r_intersection_points

        t_nom = (x_1-x_3)*(y_3-y_4) - (y_1-y_3)*(x_3-x_4)

        t = t_nom / den

        # Not relevant, because we only want to know if intersection is within the 
        # line segment exists and not within the whole line.
        #u_nom = - ((x_1-x_2)*(y_1-y_3) - (y_1-y_2)*(x_1-x_3))
        #u = u_nom / den

        # Is intersection within the two line segments?
        if 0.0 <= t and t <= 1.0:
            p_x = x_1 + t * (x_2 - x_1)
            p_y = y_1 + t * (y_2 - y_1)
            r_intersection_points.append(Point(p_x, p_y))

        return r_intersection_points


class Line():
    """
    A geometric line defined by a point and direction.
    """

    def __init__(self, point, direction):
        self.point = point
        
        # TODO: Normalize vector
        self.direction = direction

    def as_line_segment(self):
        """Returns infinite line as a line segment.

        Returns:
            LineSegment: Line segment which lies on line
        """
        return LineSegment(self.point, self.point + self.direction)

    def is_intersecting(self, other):
        return bool(len(self.intersection_with_line(other)))

    def intersection_with_line(self, other):
        """Returns list with intersection point with other line.
        Returns empty list if no intersection happened.

        Intersection points are determined according to two defined lines in terms
        of first degree Bézier parameters (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection).

        Args:
            other (Line): Line used to check for intersection,

        Returns:
            list: List of intersection point
        """      
        x_1, y_1 = self.point.as_tuple()
        x_2, y_2 = (self.point+self.direction).as_tuple()
        x_3, y_3 = other.point.as_tuple()
        x_4, y_4 = (other.point+other.direction).as_tuple()

        den = (x_1-x_2)*(y_3-y_4) - (y_1-y_2)*(x_3-x_4)

        # Is line parallel or coincindent?
        if math.isclose(den, 0.0, abs_tol=TOL_ZERO_DIV):
            return []

        t_nom = (x_1-x_3)*(y_3-y_4) - (y_1-y_3)*(x_3-x_4)
        u_nom = - ((x_1-x_2)*(y_1-y_3) - (y_1-y_2)*(x_1-x_3))

        t = t_nom / den
        u = u_nom / den

        p_x = x_1 + t * (x_2 - x_1)
        p_y = y_1 + t * (y_2 - y_1)

        return [Point(p_x, p_y)]

class Rectangle():
    """
    A rectangle defined by the bottom left point, width and height.
    """
    def __init__(self, width, height, bl_pos=Point(0,0)):
        self.p_bl = Point(bl_pos.x,bl_pos.y)
        self.p_br = Point(bl_pos.x + width, bl_pos.y)
        self.p_tr = Point(bl_pos.x + width, bl_pos.y + height)
        self.p_tl = Point(bl_pos.x, bl_pos.y + height)

        self.s_b = LineSegment(self.p_bl, self.p_br)
        self.s_r = LineSegment(self.p_br, self.p_tr)
        self.s_t = LineSegment(self.p_tr, self.p_tl)
        self.s_l = LineSegment(self.p_tl, self.p_bl)

        self.line_segments = ( self.s_b, self.s_r, self.s_t, self.s_l)

    def intersection_with_line(self, line):
        """Returns all intersection points between rectangle and given line.

        Args:
            line (Line): Line object

        Returns:
            list: List with intersection points
        """

        intersections = []

        for line_segment in self.line_segments:
            temp_intersection = line_segment.intersection_with_line(line)
            if len(temp_intersection) > 0:
                intersections = intersections + temp_intersection

        # Clean twin points at edges.
        cleaned_intersections = []
        if len(intersections):
            for intersection in intersections:
                if intersection not in cleaned_intersections:
                    cleaned_intersections.append(intersection)

        return cleaned_intersections
