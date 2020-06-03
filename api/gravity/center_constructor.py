from typing import List, Optional

from shapely.geometry import Polygon

from api.gravity.constructor import Constructor, Location


class CenterConstructor(Constructor):
    def calculate(self, vertices: List[Location]) -> Optional[Location]:
        if len(vertices) == 0:
            return None
        while len(vertices) < 3:
            last_vertex = vertices[-1]
            vertices.append(last_vertex)
        centroid = Polygon([v.latitude, v.longitude] for v in vertices).centroid
        return Location(latitude=centroid.x, longitude=centroid.y)
