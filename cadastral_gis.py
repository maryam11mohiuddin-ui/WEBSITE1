"""
Cadastral GIS Engine for Bhoomi-AI.
Manages spatial polygon boundaries, GPS centroids, neighbor parcel linkages,
and GeoJSON serialization for Leaflet & MapLibre GIS Visualizer.
"""

class CadastralGISEngine:
    def __init__(self, db_instance):
        self.db = db_instance

    def get_all_parcels(self):
        """Returns the full FeatureCollection of all cadastral parcels."""
        return self.db.get_cadastral_geojson()

    def get_parcel_by_id(self, plot_id):
        geojson = self.db.get_cadastral_geojson()
        for f in geojson.get("features", []):
            if f.get("id") == plot_id or f.get("properties", {}).get("recordId") == plot_id:
                return f
        return None

    def search_parcels_by_village(self, village_name):
        geojson = self.db.get_cadastral_geojson()
        matched = []
        for f in geojson.get("features", []):
            if village_name.lower() in f.get("properties", {}).get("village", "").lower():
                matched.append(f)
        return {
            "type": "FeatureCollection",
            "features": matched
        }

    def add_or_update_parcel(self, record):
        """
        Creates or updates a Cadastral polygon when a new record is ingested.
        """
        khasra = str(record.get("khasraNo", "0")).replace("/", "-")
        state_code = record.get("stateCode", "IN")
        plot_id = f"CAD-{state_code}-{khasra}"
        coords = record.get("coordinates", {"lat": 20.5937, "lng": 78.9629})
        
        lat = coords.get("lat", 20.5937)
        lng = coords.get("lng", 78.9629)
        d = 0.0018  # approximate polygon boundary offset

        feature = {
            "type": "Feature",
            "id": plot_id,
            "properties": {
                "recordId": record.get("id"),
                "khasraNo": record.get("khasraNo"),
                "owner": record.get("landownerName"),
                "village": record.get("village"),
                "district": record.get("district"),
                "state": record.get("state"),
                "areaAcres": record.get("totalArea", {}).get("value", 1.0),
                "classification": record.get("landClassification"),
                "status": record.get("status", "Validated"),
                "centroid": [lat, lng],
                "color": "#10b981" if record.get("status") == "Validated" else "#f59e0b",
                "neighbors": {"North": "Adjacent Plot", "South": "Road", "East": "Drain", "West": "Plot"}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [lng - d, lat - d],
                    [lng + d, lat - d],
                    [lng + d + 0.0003, lat + d],
                    [lng - d + 0.0002, lat + d],
                    [lng - d, lat - d]
                ]]
            }
        }

        # Check if already exists, else append
        existing = False
        features = self.db.cadastral.get("features", [])
        for i, f in enumerate(features):
            if f.get("id") == plot_id or f.get("properties", {}).get("recordId") == record.get("id"):
                features[i] = feature
                existing = True
                break
        if not existing:
            features.append(feature)

        return feature
