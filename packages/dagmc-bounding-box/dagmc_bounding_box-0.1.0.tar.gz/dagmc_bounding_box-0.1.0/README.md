
Finds the bounding box of a DAGMC geometry file.

This which is particularly useful when assigning a regular mesh tally over the entire DAGMC geometry.

# Installation

```bash
pip install dagmc_bounding_box
```

# Usage

Find the bounding box
```python
from dagmc_bounding_box import DagmcBoundingBox
my_corners = DagmcBoundingBox("dagmc.h5m").corners()
print(my_corners)
>>> ((-100, -100, -100), (100, 100, 100))
```

Extend the bounding box
```python
from dagmc_bounding_box import DagmcBoundingBox
my_corners = DagmcBoundingBox("dagmc.h5m").corners(extend=(10, 5, 2)
print(my_corners)
>>> ((-110, -105, -102), (110, 105, 102))
```
