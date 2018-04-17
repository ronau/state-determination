State Determination
===================

Determine which US state a geoposition is located in.


Usage
-----

**state_determination.py**

Instantiate the `state_determination` class by specifying the pickle-serialized file with the polygon data for the states. See state_borders_generator.py for details on the format of this data structure.

Most interesting method is `state_of_geoposition(lat, long)` which returns a string with the abbreviation (e.g. PA) of the state where the
geoposition is located in.

**state_borders_generator.py**

Generates a Python pickle file containing information about borders of all US states.<br>
State borders data has been downloaded from https://www.census.gov/geo/maps-data/data/tiger-line.html<br>
The Shapefiles (.shp) from there have been imported with Google Earth Pro and then exported again as .kml file.
This script transforms the .kml file to a dictionary structure which is - at the end - serialized again using Python pickle library.
The pickle file can then be used in other scripts.

**winding_number_basics.py**

Contains the mathematical basics including simple cases in a test.


The Math
--------

**Mathematical problem: Determining the inclusion of a point in a 2D planar polygon**

Two methods are commonly used:

- Crossing number (cn)
- Winding number (wn)

According to various literature, the winding number (wn) is more precise, especially in case a polygon overlaps with itself.

A relatively simple algorithm for calculation of the winding number is shown at http://geomalgorithms.com/a03-_inclusion.html (or theory/Inclusion-point-in-polygon-pdf) and will be used here.

Other descriptions and explanations regarding crossing number and winding number can be found here (German only):

- Kreuzungszahl: http://www-lehre.informatik.uni-osnabrueck.de/~cg/2002/skript/node43.html (theory/Kreuzungszahl.pdf)
- Umlaufszahl: http://www-lehre.informatik.uni-osnabrueck.de/~cg/2002/skript/node44.html (theory/Umlaufszahl.pdf)
- Punkt im Polygon: http://rw7.de/ralf/inffaq/polygon.html (theory/Punkt-im-Polygon.pdf)


Data Types/Structures
---------------------

For the mathematical methods in this class, the following data types/structures are used:

- **Geopoint**  - Python namedtuple, i.e.

    ```python
    Point = namedtuple('Geopoint', ['lat', 'long'])
    p = Geopoint(11, 22)
    ```

- **Line** - Python namedtuple of two geopoints, i.e.

    ```python
    Line = namedtuple('Line', ['p1', 'p2'])
    line1 = Line(Geopoint(3, 5), Geopoint(4, 2))
    ```

- **Polygon** - Python list of Geopoints, i.e. [ Geopoint, Geopoint, Geopoint, ..., Geopoint ]