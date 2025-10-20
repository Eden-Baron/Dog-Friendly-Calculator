import pandas as pd
import requests


def calculate_center(rings):
    x_coords = [pt[0] for ring in rings for pt in ring]
    y_coords = [pt[1] for ring in rings for pt in ring]
    return [sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)]


def create_neighborhoods():
    url = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/511/query?where=1%3D1&outFields=*&f=json"
    response = requests.get(url)
    data = response.json()
    features = data["features"]

    neighborhoods = []
    for f in features:
        attributes = f["attributes"]
        geometry = f.get("geometry", {})
        rings = geometry.get("rings", [])

        if not rings:
            continue

        center = calculate_center(rings)

        neighborhoods.append(
            {
                "neighborhoodName": attributes.get("shem_shchuna"),
                "Shape_Area": attributes.get("Shape_Area"),
                "x_center": center[0],
                "y_center": center[1],
            }
        )

    df = pd.DataFrame(neighborhoods).sort_values(by="neighborhoodName")
    df.to_csv("data/neighborhoods.csv", index=False, encoding="utf-8-sig")
    return df
