import pandas as pd
import math

def calculate_distance(neighborhood, park):
    return math.sqrt((neighborhood[0] - park[0]) ** 2 + (neighborhood[1] - park[1]) ** 2)

def calcNearestPark():
    neighborhoods_df = pd.read_csv("data/neighborhoods.csv")
    parks_df = pd.read_csv("data/parks.csv")

    nearest_parks = []

    for _, n_row in neighborhoods_df.iterrows():
        neighborhoods_center = [n_row["x_center"], n_row["y_center"]]
        min_distance = float("inf")
        nearest_park = None

        for _, p_row in parks_df.iterrows():
            park_center = [p_row["x_center"], p_row["y_center"]]

            distance = calculate_distance(neighborhoods_center, park_center)
            if distance < min_distance:
                min_distance = distance
                nearest_park = p_row["park_name"]

        nearest_parks.append({
            "nearest_park_name": nearest_park,
            "distance_to_park": round(min_distance)
        })

    neighborhoods_df = pd.concat([neighborhoods_df, pd.DataFrame(nearest_parks)], axis=1)
    neighborhoods_df.to_csv("data/neighborhoods.csv", index=False, encoding="utf-8-sig")

