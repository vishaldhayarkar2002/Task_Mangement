import frappe
from frappe.model.document import Document
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd  # Required for GeoDataFrame

class Area(Document):
    def before_save(self):
        """Frappe hook to calculate area before saving the document."""
        self.calculate_area()

    def calculate_area(self):
        """Calculate land area dynamically using GIS libraries from child table data."""

        # Fetching child table data
        coordinates = self.get("location_data")

        # Ensure at least three points are provided
        if len(coordinates) < 3:
            frappe.throw("At least three latitude and longitude values are required.")

        # Extract latitudes and longitudes from child table
        latitudes = [float(coord.latitude) for coord in coordinates]
        longitudes = [float(coord.longitude) for coord in coordinates]

        frappe.msgprint(f"Latitudes: {latitudes}, Longitudes: {longitudes}")

        # Step 4: Convert lat/lng pairs into coordinate tuples
        coords = list(zip(longitudes, latitudes))

        # Step 5: Close the polygon by repeating the first point at the end
        coords.append(coords[0])

        # Step 6: Create a polygon using Shapely
        polygon = Polygon(coords)

        # Debug: Print the polygon
        frappe.msgprint(f"Polygon Coordinates: {polygon.wkt}")

        # Step 7: Convert to a GeoDataFrame and assign a geographic coordinate system (WGS84)
        gdf = gpd.GeoDataFrame(pd.DataFrame(index=[0]), geometry=[polygon], crs="EPSG:4326")

        # Step 8: Convert to UTM Zone 44N (EPSG:32644) for accurate area calculation
        gdf = gdf.to_crs(epsg=32644)

        # Step 9: Compute the area in square meters
        area_sq_meters = gdf.area.iloc[0]

        # Step 10: Convert the area to acres (1 acre = 4046.86 square meters)
        area_acres = area_sq_meters / 4046.86

        # Step 11: Store the calculated area in the document
        self.cal_area = round(area_acres, 2)

        # Debug: Print the calculated area
        frappe.msgprint(f"Calculated Area: {self.cal_area} acres")

        # Step 12: Raise an error if the area is unrealistic
        if self.cal_area <= 0 or self.cal_area > 10000:
            frappe.throw(f"Error: Calculated area {self.cal_area} acres seems incorrect.")
