import pandas as pd
import random


def generate_dogs(neighborhoods_df, num_dogs=10000):
    neighborhoods = neighborhoods_df["neighborhoodName"].tolist()

    dogs_data = {
        "dog_name": [f"dog_{i}" for i in range(1, num_dogs + 1)],
        "neighborhood": [random.choice(neighborhoods) for _ in range(num_dogs)],
    }

    dogs_df = pd.DataFrame(dogs_data)

    dogs_by_neighborhood = (
        dogs_df.groupby("neighborhood").size().reset_index(name="dogsByNeighborhood")
    ).sort_values(by="neighborhood")

    dogs_by_neighborhood.to_csv(
        "data/dogs_by_neighborhood.csv", index=False, encoding="utf-8-sig"
    )
