import requests
import pandas as pd


def create_parks():
    url = "https://gisn.tel-aviv.gov.il/GisOpenData/service.asmx/GetLayer?layerCode=551&layerWhere=&xmin=&ymin=&xmax=&ymax=&projection="
    response = requests.get(url)
    data = response.json()
    features = data["features"]

    parks = []
    for f in features:
        attributes = f["attributes"]
        geometry = f.get("geometry", {})

        if "rings" in geometry and geometry["rings"]:
            all_points = [p for ring in geometry["rings"] for p in ring]
            x_center = sum(p[0] for p in all_points) / len(all_points)
            y_center = sum(p[1] for p in all_points) / len(all_points)
        else:
            x_center, y_center = None, None

        if attributes.get("ms_area", 0) > 10000:
            parks.append(
                {
                    "park_name": attributes.get("shem_gan"),
                    "park_size": attributes.get("ms_area"),
                    "x_center": x_center,
                    "y_center": y_center,
                }
            )

    df = pd.DataFrame(parks)
    df = (
        df.groupby("park_name")
        .agg({"park_size": "sum", "x_center": "mean", "y_center": "mean"})
        .reset_index()
    )
    df.to_csv("data/parks.csv", encoding="utf-8-sig", index=False)
