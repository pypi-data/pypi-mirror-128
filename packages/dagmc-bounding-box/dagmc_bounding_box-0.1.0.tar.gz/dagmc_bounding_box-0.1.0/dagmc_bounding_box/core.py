import trimesh
from typing import Tuple


class DagmcBoundingBox:
    def __init__(self, h5m_filename):
        """Loads the h5m file provided and provides access to the bounding box and
        related aspects of the geometry

        Args:
            expand: increase (+ve) number or decrease the offset from the
                bounding box

        Returns:
            vertices of lower left corner and upper right corner
        """

        self.h5m_filename = h5m_filename
        self.mesh_object = trimesh.load_mesh(self.h5m_filename, process=False)

    def corners(
        self, expand: Tuple[float, float, float] = None
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """Gets the lower left corner and upper right corner of the DAGMC
        geometry

        Args:
            expand:

        Returns:
            A tuple of two coordinates
        """

        vertices = self.mesh_object.bounding_box.vertices
        for vert in vertices:
            if (
                vert[0] < self.mesh_object.centroid[0]
                and vert[1] < self.mesh_object.centroid[1]
                and vert[2] < self.mesh_object.centroid[2]
            ):
                llc = (vert[0], vert[1], vert[2])
            if (
                vert[0] > self.mesh_object.centroid[0]
                and vert[1] > self.mesh_object.centroid[1]
                and vert[2] > self.mesh_object.centroid[2]
            ):
                urc = (vert[0], vert[1], vert[2])
        if expand:
            llc = (llc[0] - expand[0], llc[1] - expand[1], llc[2] - expand[2])
            urc = (urc[0] + expand[0], urc[1] + expand[1], urc[2] + expand[2])
        return llc, urc
