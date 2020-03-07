import math

import googlemaps
import polyline


class PathPlotter:
    # todo: typing
    fixed_distance = 1500  # in meters
    key = None

    def find_point_from_line(self, x1, y1, x2, y2, dt, d):
        t = dt / d
        return (((1 - t) * x1) + (t * x2)), (((1 - t) * y1) + (t * y2))

    def calculate_geo_distance(self, prev_location, new_location):
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

    def calculate_points(self, prev_location, new_location, fixed_distance_remaining=0):
        new_points = []
        geo_distance = self.calculate_geo_distance(prev_location, new_location)
        while geo_distance > fixed_distance_remaining:
            new_points.append(self.find_point_from_line(x1=prev_location[0], y1=prev_location[1], x2=new_location[0],
                                                        y2=new_location[1], dt=fixed_distance_remaining,
                                                        d=geo_distance))
            # Initialize the fixed_distance_remaining
            geo_distance -= fixed_distance_remaining
            fixed_distance_remaining = self.fixed_distance

        fixed_distance_remaining -= geo_distance

        return new_points, fixed_distance_remaining

    def plot_path(self, origin, destination):
        gmaps = googlemaps.Client(key=self.key)
        resp = gmaps.directions(origin=origin, destination=destination)

        # Combine all the steps to get the whole polyline
        p_line = []
        for i in resp[0]['legs'][0]['steps']:
            p_line.extend(polyline.decode(i['polyline']['points']))

        # Main code
        result_points = [p_line[0]]  # Start with first point
        prev_location = p_line[0]
        fixed_distance_remaining = self.fixed_distance  # Start with full fixed distance
        for new_location in p_line[1:]:
            new_points, fixed_distance_remaining = self.calculate_points(prev_location, new_location,
                                                                         fixed_distance_remaining)
            result_points.extend(new_points)
            prev_location = new_location

        if fixed_distance_remaining and fixed_distance_remaining != self.fixed_distance:
            # Append last point if trail was remaining
            result_points.append(p_line[-1])

        return result_points


# Driver program
pp = PathPlotter()
results = pp.plot_path(origin=(12.94523, 77.61896), destination=(12.95944, 77.66085))
for i in results:
    print("{0},{1},".format(i[0], i[1]))
