# AnnotationExport - Neubias-WG5

Library containing annotation export tools. 

## Annotation slice

The `AnnotationSlice` class represents a 2D annotation with additional metadata when relevant:

- _shape_: encoded as a polygon
- _label_: label associated to the annotation
- _index_: for 3D volumes, the depth index
- _time_: for time volumes, the time index

## From masks to objects

See file `mask_to_objects.py`. All function take a multi-dimensional array as input and output AnnotationSlice
- 2D: `mask_to_objects_2d `
- 3D/2D+t: `mask_to_objects_3d`
- 3D+t: `mask_to_objects_3dt`

## From masks to points

See file `mask_to_points.py`:

- 2D: `mask_to_points_2d`
