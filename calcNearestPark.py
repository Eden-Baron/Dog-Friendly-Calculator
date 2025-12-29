
import pandas as pd
from shapely import wkt
from shapely.ops import nearest_points


def calcNearestPark():
    neighborhoods_df = pd.read_csv("data/neighborhoods.csv")
    parks_df = pd.read_csv("data/parks.csv")

    neighborhoods_geom = neighborhoods_df["geometry"].apply(wkt.loads)
    parks_geom = parks_df["geometry"].apply(wkt.loads)

    results = []

    for n_geom in neighborhoods_geom:
        #  מרכז הכובד של השכונה
        centroid = n_geom.centroid

        min_distance = float("inf")
        nearest_park_name = None

        # מעבר פארק-פארק
        for park_name, park_geom in zip(parks_df["park_name"], parks_geom):

            # מציאת הנקודה הקרובה ביותר בפארק
            p_near, park_near = nearest_points(centroid, park_geom)

            distance = centroid.distance(park_near)

            if distance < min_distance:
                min_distance = distance
                nearest_park_name = park_name

        results.append(
            {
                "nearest_park_name": nearest_park_name,
                "distance_to_park": round(min_distance, 2),
                "neighborhood_centroid": wkt.dumps(centroid),
            }
        )

    neighborhoods_df = pd.concat([neighborhoods_df, pd.DataFrame(results)], axis=1)

    neighborhoods_df.to_csv("data/neighborhoods.csv", index=False, encoding="utf-8-sig")
