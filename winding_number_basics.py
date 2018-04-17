from __future__ import division, print_function
from collections import namedtuple
import sys

if sys.version_info.major == 2:
    import cPickle
    from __builtin__ import raw_input as input
else:
    import pickle as cPickle




# Type definitions, see  below for more details
Geopoint = namedtuple('Geopoint', ['lat', 'long'])
Line = namedtuple('Line', ['p1', 'p2'])



"""

Mathematical basics for state determination.


###############################################################################
# Determining the inclusion of a point in a 2D planar polygon
###############################################################################

Two methods are commonly used:

    - Crossing number (cn)
    - Winding number (wn)

According to various literature, the winding number (wn) is more precise, especially in case a
polygon overlaps with itself.

A relatively simple algorithm for calculation of the winding number is shown at
    http://geomalgorithms.com/a03-_inclusion.html
and will be used in this section.

Other descriptions and explanations regarding crossing number and winding number
can be found here (German only):
    - Kreuzungszahl: http://www-lehre.informatik.uni-osnabrueck.de/~cg/2002/skript/node43.html
    - Umlaufszahl: http://www-lehre.informatik.uni-osnabrueck.de/~cg/2002/skript/node44.html
    - Punkt im Polygon: http://rw7.de/ralf/inffaq/polygon.html


For the following methods, we assume the following data types/structures:

Geopoint  - Python namedtuple, i.e.
              Point = namedtuple('Geopoint', ['lat', 'long'])
              p = Geopoint(11, 22)

Line      - Python namedtuple of two geopoints, i.e.
              Line = namedtuple('Line', ['p1', 'p2'])
              line1 = Line(Geopoint(3, 5), Geopoint(4, 2))

Polygon - Python list of Geopoints, i.e. [ Geopoint, Geopoint, Geopoint, ..., Geopoint ]


"""



#
# Tests if a point is Left|On|Right of an infinite line.
# The line is considered to be directed from the line's point1 to point2
#
#     Input:  geop   - Geopoint(lat, long)
#             line   - Line(Point(lat, long), Point(lat, long))
#     Return: >0 for point left of the line
#             =0 for point on the line
#             <0 for point right of the line
#
# Please note:  Compared to the algorithm/method at http://geomalgorithms.com/a03-_inclusion.html
#               the x and y coordinates are swapped in the common format of geocoordinates (lat = y, long = x).
#
def is_left(geop, line):

    return ( (line.p2.long - line.p1.long) * (geop.lat - line.p1.lat)
            -  (geop.long - line.p1.long) * (line.p2.lat - line.p1.lat) )



#
# Winding number (wn) test for a point in a polygon
# If wn = 0, the point is outside the polygon, otherwise it is inside
#
#     Input:  geop     - Geopoint(lat, long)
#             polygon  - List of Geopoints: [ Geopoint(lat, long), Geopoint(lat, long), ..., Geopoint(lat, long) ]
#     Return: wn       - the winding number (=0 if point is outside polygon)
#
def wn_point_polygon(geop, polygon):

    wn = 0      # winding number counter

    # loop through all edges of the polygon
    for i in range(len(polygon)):

        # Make sure that we have the two points of the edge as Geopoint type
        if not isinstance(polygon[i-1], Geopoint):
            start = Geopoint._make(polygon[i-1])
        else:
            start = polygon[i-1]

        if not isinstance(polygon[i], Geopoint):
            end = Geopoint._make(polygon[i])
        else:
            end = polygon[i]


        if start.lat <= geop.lat:                               # make sure that start y <= P.y
            if end.lat > geop.lat:                              # an upward crossing
                if is_left( geop, Line(start, end) ) > 0:       # P is left of edge
                    wn += 1                                     # a valid up intersection

        else:                                                   # start y > P.y (no test needed)
            if end.lat <= geop.lat:                             # a downward crossing
                if is_left( geop, Line(start, end) ) < 0:       # P is right of edge
                    wn -= 1                                     # a valid down intersection


    return wn




def basics_test():

    p1 = Geopoint(2,1)
    p2 = Geopoint(-2,4)
    p3 = Geopoint(1,-3)
    p4 = Geopoint(-3,-1)
    p5 = Geopoint(1,5)
    p6 = Geopoint(0,4)

    l1 = Line(Geopoint(1,4), Geopoint(3,4))
    l2 = Line(Geopoint(2,-5), Geopoint(2,-2))
    l3 = Line(Geopoint(-2,-2), Geopoint(-5,-2))
    l4 = Line(Geopoint(-3,1), Geopoint(-1,3))

    print(p1)
    print(p2)
    print(l1)

    print("P1 is_left of l1?", is_left(p1, l1))
    print("P2 is_left of l1?", is_left(p2, l1))
    print("P3 is_left of l1?", is_left(p3, l1))
    print("P4 is_left of l1?", is_left(p4, l1))
    print("P5 is_left of l1?", is_left(p5, l1))
    print("P6 is_left of l1?", is_left(p6, l1))
    print("")
    print("P1 is_left of l2?", is_left(p1, l2))
    print("P2 is_left of l2?", is_left(p2, l2))
    print("P3 is_left of l2?", is_left(p3, l2))
    print("P4 is_left of l2?", is_left(p4, l2))
    print("P5 is_left of l2?", is_left(p5, l2))
    print("P6 is_left of l2?", is_left(p6, l2))
    print("")
    print("P1 is_left of l3?", is_left(p1, l3))
    print("P2 is_left of l3?", is_left(p2, l3))
    print("P3 is_left of l3?", is_left(p3, l3))
    print("P4 is_left of l3?", is_left(p4, l3))
    print("P5 is_left of l3?", is_left(p5, l3))
    print("P6 is_left of l3?", is_left(p6, l3))
    print("")
    print("P1 is_left of l4?", is_left(p1, l4))
    print("P2 is_left of l4?", is_left(p2, l4))
    print("P3 is_left of l4?", is_left(p3, l4))
    print("P4 is_left of l4?", is_left(p4, l4))
    print("P5 is_left of l4?", is_left(p5, l4))
    print("P6 is_left of l4?", is_left(p6, l4))
    print("")


    poly1 = [p1, p2, p3, p4, p5, p6]
    print(wn_point_polygon(p1, poly1))
    print(wn_point_polygon(p2, poly1))
    print(wn_point_polygon(p3, poly1))
    print(wn_point_polygon(p4, poly1))
    print(wn_point_polygon(p5, poly1))
    print(wn_point_polygon(p6, poly1))

    print("")
    poly2 = [p1, p2, p5]
    print(wn_point_polygon(p6, poly2))
    print("")
    print("")

    poly1 = [Geopoint(1,1), Geopoint(5,1), Geopoint(5,6), Geopoint(1,6)]
    p1 = Geopoint(2,3)
    p2 = Geopoint(4,2)
    p3 = Geopoint(1,3)
    p4 = Geopoint(3,1)
    p5 = Geopoint(5,4)
    p6 = Geopoint(4,6)
    p7 = Geopoint(1,6)
    p8 = Geopoint(1,1)
    p9 = Geopoint(5,1)
    p10 = Geopoint(5,6)
    p11 = Geopoint(0,0)
    p12 = Geopoint(-2,5)
    p13 = Geopoint(4,-1)

    print("P1", wn_point_polygon(p1, poly1))
    print("P2", wn_point_polygon(p2, poly1))
    print("P3", wn_point_polygon(p3, poly1))
    print("P4", wn_point_polygon(p4, poly1))
    print("P5", wn_point_polygon(p5, poly1))
    print("P6", wn_point_polygon(p6, poly1))
    print("P7", wn_point_polygon(p7, poly1))
    print("P8", wn_point_polygon(p8, poly1))
    print("P9", wn_point_polygon(p9, poly1))
    print("P10", wn_point_polygon(p10, poly1))
    print("P11", wn_point_polygon(p11, poly1))
    print("P12", wn_point_polygon(p12, poly1))
    print("P13", wn_point_polygon(p13, poly1))




basics_test()

