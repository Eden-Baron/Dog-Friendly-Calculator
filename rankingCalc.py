# חישוב דירוג
# חישוב יחס מספר כלבים לשכונה לעומת השטח של השכונה
# חישוב המרחק בין השכונה לפארק ביחס לגודלו של הפארק
# ככל שהמרחק קטן לפארק גדול ויחס הכלבים לשטח קטן כך הדירוג גבוה יותר ומקבל ניקוד בין 1-10

import pandas as pd


def ranking_neighborhoods():
    dogs = pd.read_csv("data/dogs_by_neighborhood.csv")
    neighborhoods = pd.read_csv("data/neighborhoods.csv")
    parks = pd.read_csv("data/parks.csv")

    densities = []

    for dog_row, n_row in zip(dogs.itertuples(), neighborhoods.itertuples()):
        density = dog_row.dogsByNeighborhood / n_row.Shape_Area
        densities.append(density)

    neighborhoods["density"] = densities

    def normalize(values, reverse=False):
        min_val = min(values)
        max_val = max(values)
        norm = [
            (v - min_val) / (max_val - min_val) if max_val > min_val else 0
            for v in values
        ]
        if reverse:
            norm = [1 - v for v in norm]
        return norm

    # נרמול כל פרמטר
    norm_density = normalize(neighborhoods["density"])
    norm_distance = normalize(neighborhoods["distance_to_park"], reverse=True)

    park_sizes = dict(zip(parks["park_name"], parks["park_size"]))
    nearest_park_sizes = neighborhoods["nearest_park_name"].map(park_sizes)
    norm_park_size = normalize(nearest_park_sizes)

    # חישוב דירוג סופי 1-10 והוספה לעמודה
    rating = [
        round(2 + 8 * (0.4 * d + 0.3 * p + 0.3 * r))
        for d, p, r in zip(norm_density, norm_park_size, norm_distance)
    ]

    rank_df = pd.DataFrame(
        {"neighborhoodName": neighborhoods["neighborhoodName"], "rating": rating}
    ).sort_values(by="neighborhoodName")

    rank_df.to_csv("data/rank_for_neighborhoods.csv", index=False, encoding="utf-8-sig")
