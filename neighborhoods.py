import pandas as pd
import requests
from shapely.geometry import Polygon
from shapely.wkt import dumps as wkt_dumps


def create_neighborhoods():
    url = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/511/query?where=1%3D1&outFields=*&f=json"
    data =  requests.get(url).json()
    features = data["features"]

    neighborhoods = []
    for f in features:
        attributes = f["attributes"]
        geometry = f.get("geometry", {})
        rings = geometry.get("rings", [])

        polygon = Polygon(rings[0]) 
        polygon = polygon.simplify(3) 

        neighborhoods.append(
            {
                "neighborhoodName": attributes.get("shem_shchuna"),
                "neighborhoodSize": attributes.get("Shape_Area"),
                "geometry": wkt_dumps(polygon) 
            }
        )

    df = pd.DataFrame(neighborhoods).sort_values(by="neighborhoodName")
    df.to_csv("data/neighborhoods.csv", index=False, encoding="utf-8-sig")
    return df

