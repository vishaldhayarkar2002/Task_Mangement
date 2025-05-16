import frappe
from frappe.model.document import Document
import math
from decimal import Decimal


class Area1(Document):
    def before_save(self):
        self.calculate_area()

    @frappe.whitelist()
    def calculate_area(self):
        
        coordinates = self.get("location_data")

        
        if len(coordinates) < 3:
            frappe.throw("At least three latitude and longitude values are required.")

        latitudes = [Decimal(coord.latitude) for coord in coordinates]
        longitudes = [Decimal(coord.longitude) for coord in coordinates]

        # Compute Reference Latitude (Average)
        lat_ref = sum(latitudes) / len(latitudes)
        lat_ref_rad = lat_ref * Decimal(math.pi) / Decimal(180)  # Convert to radians

        # Convert Latitude and Longitude to Cartesian Coordinates (Meters)
        x = [(lon - longitudes[0]) * Decimal(111320) * Decimal(math.cos(lat_ref_rad)) for lon in longitudes]
        y = [(lat - latitudes[0]) * Decimal(111320) for lat in latitudes]

        # Compute Area using Shoelace Formula
        sum1, sum2 = Decimal(0), Decimal(0)
        for i in range(len(x)):
            next_i = (i + 1) % len(x)
            sum1 += x[i] * y[next_i]
            sum2 += y[i] * x[next_i]

        area_m2 = abs(sum1 - sum2) / Decimal(2)  
        area_acres = area_m2 / Decimal(4046.86)  

       
        self.cal_area = area_acres

        frappe.msgprint(f"Calculated Area: {area_acres} acres (High Precision)")
