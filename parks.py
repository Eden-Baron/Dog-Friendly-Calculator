import requests
import pandas as pd
from shapely.geometry import Polygon
from shapely.wkt import dumps as wkt_dumps


def create_parks():
    url = "https://gisn.tel-aviv.gov.il/GisOpenData/service.asmx/GetLayer?layerCode=551&layerWhere=&xmin=&ymin=&xmax=&ymax=&projection="
    response = requests.get(url)
    data = response.json()
    features = data["features"]

    parks = []

    for f in features:
        attributes = f["attributes"]
        geometry = f.get("geometry", {})
        rings = geometry.get("rings")
        
        if not rings:
            continue

        polygon = Polygon(rings[0])

        polygon = polygon.simplify(3)

        geom_wkt = wkt_dumps(polygon)

        # סינון לפי גודל פארק
        if attributes.get("ms_area", 0) > 10000:
            parks.append(
                {
                    "park_name": attributes.get("shem_gan"),
                    "park_size": attributes.get("ms_area"),
                    "geometry": geom_wkt,
                }
            )

    df = pd.DataFrame(parks)

    # מיזוג פארקים בעלי אותו שם
    df = (
        df.groupby("park_name")
        .agg(
            {
                "park_size": "sum",
                "geometry": "first",
            }
        )
        .reset_index()
    )

    df.to_csv("data/parks.csv", encoding="utf-8-sig", index=False)

