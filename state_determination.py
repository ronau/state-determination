from __future__ import division, print_function
from collections import namedtuple
from datetime import datetime
import sys

if sys.version_info.major == 2:
    import cPickle
    from __builtin__ import raw_input as input
else:
    import pickle as cPickle



"""

###############################################################################
# STATE DETERMINATION: Which state a geoposition is located in
###############################################################################

Instantiate the class by specifying the pickle-serialized file with the polygon
data for the states. See state_borders_generation.py file for details on the
format of this data structure.

Most interesting method is
    state_of_geoposition(lat, long)
which returns a string with the abbreviation (e.g. PA) of the state where the
geoposition is located in.



For the mathematical methods in this class, we assume the following data types/structures:

Geopoint  - Python namedtuple, i.e.
              Point = namedtuple('Geopoint', ['lat', 'long'])
              p = Geopoint(11, 22)

Line      - Python namedtuple of two geopoints, i.e.
              Line = namedtuple('Line', ['p1', 'p2'])
              line1 = Line(Geopoint(3, 5), Geopoint(4, 2))

Polygon - Python list of Geopoints, i.e. [ Geopoint, Geopoint, Geopoint, ..., Geopoint ]


"""
class state_determination:




    def __init__(self, state_file):

        print("Reading states border data from {0} ... ".format(state_file), end="")
        sys.stdout.flush()  # Py 2 seems to flush stdout automatically, Py 3 not
        with open(state_file, "rb") as file:
            self.states = cPickle.load(file)
        print("Done.\n")

        # Type definitions, see description above for more details
        self.Geopoint = namedtuple('Geopoint', ['lat', 'long'])
        self.Line = namedtuple('Line', ['p1', 'p2'])


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
    def is_left(self, geop, line):

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
    def wn_point_polygon(self, geop, polygon):

        wn = 0      # winding number counter

        # loop through all edges of the polygon
        for i in range(len(polygon)):

            # Make sure that we have the two points of the edge as Geopoint type
            if not isinstance(polygon[i-1], self.Geopoint):
                start = self.Geopoint._make(polygon[i-1])
            else:
                start = polygon[i-1]

            if not isinstance(polygon[i], self.Geopoint):
                end = self.Geopoint._make(polygon[i])
            else:
                end = polygon[i]


            if start.lat <= geop.lat:                               # make sure that start y <= P.y
                if end.lat > geop.lat:                              # an upward crossing
                    if self.is_left( geop, self.Line(start, end) ) > 0:       # P is left of edge
                        wn += 1                                     # a valid up intersection

            else:                                                   # start y > P.y (no test needed)
                if end.lat <= geop.lat:                             # a downward crossing
                    if self.is_left( geop, self.Line(start, end) ) < 0:       # P is right of edge
                        wn -= 1                                     # a valid down intersection


        return wn




    #
    # Returns the abbreviation of the state (e.g. PA) where the geoposition
    # (specified by lat and long) is located in.
    #
    def state_of_geoposition(self, lat, long):

        geopos = self.Geopoint(lat, long)

        for state_abbrev, state_data in self.states.items():

            # Bounding box test:
            # If the point is outside the rectangle defined by the
            # northernmost, easternmost, southernmost and westernmost point of the state,
            # then we can skip the current state, i.e. continue with next loop iteration
            #
            if (geopos.lat > state_data['rectangle']['N']
                    or geopos.lat < state_data['rectangle']['S']
                    or geopos.long > state_data['rectangle']['E']
                    or geopos.long < state_data['rectangle']['W']):
                continue

            poly_count = 0
            for poly in state_data['polygons']:
                poly_count += 1
                if self.wn_point_polygon(geopos, poly) != 0:
                    return state_abbrev




###############################################################################
###############################################################################
###############################################################################








###############################################################################
## Now some methods for testing
###############################################################################


# Query the state for a single (or a handful of) geopositions
def single_test():

    tester = state_determination("states-US-pickle2.dat")

    #p_Allentown = Geopoint(40.592930, -75.609839)
    #p_Dallas = Geopoint(32.784203, -96.819397)
    #p_Philly = Geopoint(39.9331773,-75.1594191)
    #p_Pittsburg = Geopoint(40.430237, -79.993291)
    #p_Harrisburg = Geopoint(40.254371, -76.887807)

    print(tester.state_of_geoposition(40.592930, -75.609839))
    print(tester.state_of_geoposition(32.784203, -96.819397))
    print(tester.state_of_geoposition(39.9331773,-75.1594191))
    print(tester.state_of_geoposition(40.430237, -79.993291))
    print(tester.state_of_geoposition(40.254371, -76.887807))




# Query the state of the 50 US state capitals. Repeat this n times and measure the runtime.
def fifty_test():

    capitals = []
    capitals.append((32.361538,-86.279118))       #Montgomery, Alabama
    capitals.append((58.301935,-134.419740))      #Juneau, Alaska
    capitals.append((33.448457,-112.073844))      #Phoenix, Arizona
    capitals.append((34.736009,-92.331122))       #Little Rock, Arkansas
    capitals.append((38.555605,-121.468926))      #Sacramento, California
    capitals.append((39.7391667,-104.984167))     #Denver, Colorado
    capitals.append((41.767,-72.677))             #Hartford, Connecticut
    capitals.append((39.161921,-75.526755))       #Dover, Delaware
    capitals.append((30.4518,-84.27277))          #Tallahassee, Florida
    capitals.append((33.76,-84.39))               #Atlanta, Georgia
    capitals.append((21.30895,-157.826182))       #Honolulu, Hawaii
    capitals.append((43.613739,-116.237651))      #Boise, Idaho
    capitals.append((39.783250,-89.650373))       #Springfield, Illinois
    capitals.append((39.790942,-86.147685))       #Indianapolis, Indiana
    capitals.append((41.590939,-93.620866))       #Des Moines, Iowa
    capitals.append((39.04,-95.69))               #Topeka, Kansas
    capitals.append((38.197274,-84.86311))        #Frankfort, Kentucky
    capitals.append((30.45809,-91.140229))        #Baton Rouge, Louisiana
    capitals.append((44.323535,-69.765261))       #Augusta, Maine
    capitals.append((38.972945,-76.501157))       #Annapolis, Maryland
    capitals.append((42.2352,-71.0275))           #Boston, Massachusetts
    capitals.append((42.7335,-84.5467))           #Lansing, Michigan
    capitals.append((44.95,-93.094))              #Saint Paul, Minnesota
    capitals.append((32.320,-90.207))             #Jackson, Mississippi
    capitals.append((38.572954,-92.189283))       #Jefferson City, Missouri
    capitals.append((46.595805,-112.027031))      #Helana, Montana
    capitals.append((40.809868,-96.675345))       #Lincoln, Nebraska
    capitals.append((39.160949,-119.753877))      #Carson City, Nevada
    capitals.append((43.220093,-71.549127))       #Concord, New Hampshire
    capitals.append((40.221741,-74.756138))       #Trenton, New Jersey
    capitals.append((35.667231,-105.964575))      #Santa Fe, New Mexico
    capitals.append((42.659829,-73.781339))       #Albany, New York
    capitals.append((35.771,-78.638))             #Raleigh, North Carolina
    capitals.append((48.813343,-100.779004))      #Bismarck, North Dakota
    capitals.append((39.962245,-83.000647))       #Columbus, Ohio
    capitals.append((35.482309,-97.534994))       #Oklahoma City, Oklahoma
    capitals.append((44.931109,-123.029159))      #Salem, Oregon
    capitals.append((40.269789,-76.875613))       #Harrisburg, Pennsylvania
    capitals.append((41.82355,-71.422132))        #Providence, Rhode Island
    capitals.append((34.000,-81.035))             #Columbia, South Carolina
    capitals.append((44.367966,-100.336378))      #Pierre, South Dakota
    capitals.append((36.165,-86.784))             #Nashville, Tennessee
    capitals.append((30.266667,-97.75))           #Austin, Texas
    capitals.append((40.7547,-111.892622))        #Salt Lake City, Utah
    capitals.append((44.26639,-72.57194))         #Montpelier, Vermont
    capitals.append((37.54,-77.46))               #Richmond, Virginia
    capitals.append((47.042418,-122.893077))      #Olympia, Washington
    capitals.append((38.349497,-81.633294))       #Charleston, West Virginia
    capitals.append((43.074722,-89.384444))       #Madison, Wisconsin
    capitals.append((41.145548,-104.802042))      #Cheyenne, Wyoming


    tester = state_determination("states-US-pickle2.dat")
    n = 20
    print("{0} times 50 state capitals.".format(n))

    start = datetime.now()
    print("Starting at {0}.".format(start))

    for i in range(0,n):
        for cap in capitals:
            tester.state_of_geoposition(cap[0], cap[1])

    end = datetime.now()
    print("Finished at {0}.".format(end))



# Uncomment if you want to run the tests

#single_test()
#fifty_test()

