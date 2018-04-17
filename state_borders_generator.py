"""

Generates a Python pickle file containing information about borders of all US states.
State borders data has been downloaded from https://www.census.gov/geo/maps-data/data/tiger-line.html
The Shapefiles (.shp) from there have been imported with Google Earth Pro and then exported again as .kml file.
This script transforms the .kml file to a dictionary structure which is - at the end - serialized again using Python pickle library.
The pickle file can then be used in other scripts.

"""

from __future__ import division, print_function

import xml.etree.ElementTree as etree
import sys

if sys.version_info.major == 2:
    import cPickle
else:
    import pickle as cPickle



kml_ns = "{http://www.opengis.net/kml/2.2}"

placemarks = etree.parse("USA.kml").getroot().findall(".//{ns}Placemark".format(ns=kml_ns))
print("Found {0} /Placemark items in the file.".format(len(placemarks)))

usa_states = dict()

for pm in placemarks:
    state = dict()
    abbrev = pm.find("{ns}name".format(ns=kml_ns)).text
    polygon_elems = pm.findall(".//{ns}Polygon".format(ns=kml_ns))
    print(abbrev, len(polygon_elems))

    polygons = []
    rectangle = {'N':None, 'E':None, 'S':None, 'W':None}

    for poly_elem in polygon_elems:

        # the current polygon we are working on, will be collected as a list
        poly = []

        # Get the coordinates element within the polygon element
        coordinates_elem = poly_elem.find(".//{ns}coordinates".format(ns=kml_ns))

        # Take the text of this coordinates element, split it at whitespace characters.
        #   Then we have a list of strings where each string is a geoposition in format
        #   long,lat,height (Note this special order in kml files).
        geopositions = coordinates_elem.text.split()

        # Go through that list of geoposition strings
        for geopos in geopositions:
            lat = float(geopos.split(',')[1])       # Grab the first two values only (lat and long)
            long = float(geopos.split(',')[0])

            # Check and store if lat is the northernmost or southernmost lat we have so far
            if rectangle['N'] == None or lat > rectangle['N']:
                rectangle['N'] = lat
            if rectangle['S'] == None or lat < rectangle['S']:
                rectangle['S'] = lat

            # Check and store if long is the easternmost or westernmost long we have so far
            if rectangle['E'] == None or long > rectangle['E']:
                rectangle['E'] = long
            if rectangle['W'] == None or long < rectangle['W']:
                rectangle['W'] = long

            # Wrap lat and long as tuple (that's the parantheses) and append to our current polygon
            poly.append( (lat, long) )

        # add current polygon to our list of polygons
        polygons.append(poly)


    # Now we are done processing all polygons for the current placemark.

    # We add the polygons and the surrounding rectangle to the current state dictionary
    state['polygons'] = polygons
    state['rectangle'] = rectangle

    # and add the current state to our big dictionary of states
    usa_states[abbrev] = state


# Loop through all placemark elements is finished here



# This is for plausibility, we just count again the items we now have
print("\n\nUSA states dictionary content:\n")
for k, v in sorted(usa_states.items()):
    print(k, len(v['polygons']), v['rectangle'])



# Now we store everything into a file using pickle library
filename = "states-US-pickle2.dat"
print("Writing to file {0} ... ".format(filename), end="")
file = open(filename, "wb")
cPickle.dump(usa_states, file, 2)
file.close()
print("Done.")



