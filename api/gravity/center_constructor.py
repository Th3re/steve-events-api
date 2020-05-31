from typing import List, Optional

from shapely.geometry import Polygon

from api.gravity.constructor import Constructor, Location


class CenterConstructor(Constructor):
    def calculate(self, vertices: List[Location]) -> Optional[Location]:
        if len(vertices) < 3:
            return None
        centroid = Polygon([v.latitude, v.longitude] for v in vertices).centroid
        return Location(latitude=centroid.x, longitude=centroid.y)