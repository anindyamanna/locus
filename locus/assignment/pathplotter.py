import math

import googlemaps
import polyline


class PathPlotter:
    fixed_distance = 100  # in meters
    key = None

    @staticmethod
    def find_point_from_line(x1, y1, x2, y2, dt, d):
        """
        Used for finding a point along a line a certain distance away from another point!
        :return: The resulting point in x, y format
        """
        t = dt / d
        return (((1 - t) * x1) + (t * x2)), (((1 - t) * y1) + (t * y2))

    @staticmethod
    def calculate_geo_distance(prev_location, new_location):
        """
        Used to find the distance between two lat-long coordinates
        :return: Distance in meters
        """
        R = 6373000.0  # Earth's radius in meters
        lat1 = math.radians(prev_location[0])
        lon1 = math.radians(prev_location[1])
        lat2 = math.radians(new_location[0])
        lon2 = math.radians(new_location[1])

        # Change in coordinates
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Haversine formula
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def calculate_points(self, prev_location, new_location, fixed_distance_remaining):
        """
        Purpose of this function is to check and find fixed points between the two given locations. If not found the
        fixed_distance_remaining is reduced by the distance between these points.
        :return: Tuple of new points (Can be an empty list) and resulting fixed distance remaining
        """
        new_points = []
        geo_distance = self.calculate_geo_distance(prev_location, new_location)
        while geo_distance > fixed_distance_remaining:
            # Keep looping if more points can be extracted
            new_points.append(self.find_point_from_line(x1=prev_location[0], y1=prev_location[1], x2=new_location[0],
                                                        y2=new_location[1], dt=fixed_distance_remaining,
                                                        d=geo_distance))
            # Initialize the fixed_distance_remaining
            geo_distance -= fixed_distance_remaining
            fixed_distance_remaining = self.fixed_distance

        fixed_distance_remaining -= geo_distance

        return new_points, fixed_distance_remaining

    def plot_path(self, origin, destination):
        # Query google maps directions API to get the response
        gmaps = googlemaps.Client(key=self.key)
        resp = gmaps.directions(origin=origin, destination=destination)

        # Combine all the steps to get the whole polyline for the route
        p_line = []
        for i in resp[0]['legs'][0]['steps']:
            p_line.extend(polyline.decode(i['polyline']['points']))

        # Main code
        result_points = [p_line[0]]  # Start with first point
        prev_location = p_line[0]
        fixed_distance_remaining = self.fixed_distance  # Start with full fixed distance
        for new_location in p_line[1:]:
            # Loop through the polyline and try to find points of the fixed distance
            new_points, fixed_distance_remaining = self.calculate_points(prev_location, new_location,
                                                                         fixed_distance_remaining)
            result_points.extend(new_points)
            prev_location = new_location    # Update the current point so It becomes prev_location for next iteration.

        if fixed_distance_remaining and fixed_distance_remaining != self.fixed_distance:
            # Append last point if trail was remaining
            result_points.append(p_line[-1])

        return result_points


# Driver program
pp = PathPlotter()
results = pp.plot_path(origin=(12.94523, 77.61896), destination=(12.95944, 77.66085))
for i in results:
    print("{0},{1},".format(i[0], i[1]))
