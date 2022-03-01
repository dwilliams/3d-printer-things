#! /usr/bin/env python3

### IMPORTS ###
import cadquery
import logging

### GLOBALS ###
# NOTE: all dimensions in mini-meters (mm)
LARGE_OUTER_DIAMETER = 37.5
LARGE_OUTER_THICKNESS = 6.0
LARGE_INNER_DIAMETER = 31.5
LARGE_INNER_THICKNESS = 5.0

SMALL_OUTER_DIAMETER = 30.75
SMALL_OUTER_THICKNESS = 5.0
SMALL_INNER_DIAMETER = 24.5
SMALL_INNER_THICKNESS = 6.0 # FIXME: Is this one necessary?

CHAMFER_THICKNESS_Y = 2.0
CHAMFER_THICKNESS_X = 1.0

CUT_RADIUS = (SMALL_INNER_DIAMETER / 2.0) + 1.5
CUT_ARC_LENGTH = 22.5 # Degrees # Not sure if this is the correct value.

#OVERALL_THICKNESS = 11.0 # FIXME: Is this one necessary?

### FUNCTIONS ###

### CLASSES ###

### MAIN ###
def main():
    # Setup Logging
    log_format = "%(asctime)s:%(levelname)s:%(name)s.%(funcName)s: %(message)s"
    logging.basicConfig(format = log_format, level = logging.DEBUG)

    logging.debug("Creating the outer cylinders")

    # result = cadquery.Workplane("XY").cylinder(LARGE_OUTER_THICKNESS, LARGE_OUTER_DIAMETER / 2.0)
    # result = result.faces("<Z").workplane().cylinder(LARGE_OUTER_THICKNESS + SMALL_OUTER_THICKNESS, SMALL_OUTER_DIAMETER / 2.0)
    # result = result.faces(">Z").workplane().cboreHole(SMALL_INNER_DIAMETER, LARGE_INNER_DIAMETER, LARGE_INNER_THICKNESS)
    # result = result.edges(">Z").

    ring_polygon_points = [
        (LARGE_OUTER_DIAMETER / 2.0, 0),
        (LARGE_OUTER_DIAMETER / 2.0, LARGE_OUTER_THICKNESS),
        (SMALL_OUTER_DIAMETER / 2.0, LARGE_OUTER_THICKNESS),
        (SMALL_OUTER_DIAMETER / 2.0, LARGE_OUTER_THICKNESS + SMALL_OUTER_THICKNESS),
        (SMALL_INNER_DIAMETER / 2.0, LARGE_OUTER_THICKNESS + SMALL_OUTER_THICKNESS),
        (SMALL_INNER_DIAMETER / 2.0, LARGE_INNER_THICKNESS),
        (LARGE_INNER_DIAMETER / 2.0, LARGE_INNER_THICKNESS),
        (LARGE_INNER_DIAMETER / 2.0, CHAMFER_THICKNESS_Y),
        ((LARGE_INNER_DIAMETER / 2.0) + CHAMFER_THICKNESS_X, 0)
    ]
    ring_sketch = cadquery.Sketch().polygon(ring_polygon_points)

    result = cadquery.Workplane("XY").placeSketch(ring_sketch).revolve(360, (0, 0, 0), (0, 1, 0))

    cut_polygon_points = [
        (0, 0),
        ((SMALL_INNER_DIAMETER / 2.0) + 2.0, 0),
        ((SMALL_INNER_DIAMETER / 2.0) + 2.0, LARGE_OUTER_THICKNESS + SMALL_OUTER_THICKNESS),
        (0, LARGE_OUTER_THICKNESS + SMALL_OUTER_THICKNESS)
    ]
    cut_sketch = cadquery.Sketch().polygon(cut_polygon_points)

    result = result.workplane().placeSketch(cut_sketch).revolve(45, (0, 0, 0), (0, 1, 0), "cut")

    cadquery.exporters.export(result, "corolla-maf-sensor-spacer.stl")
    cadquery.exporters.export(result, "corolla-maf-sensor-spacer.svg")

if __name__ == "__main__":
    main()
