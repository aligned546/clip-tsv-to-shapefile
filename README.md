# Clip and Filter TSV Data Using a Shapefile Boundary

This script reads in a tab-separated data file (`.tsv`) containing point-based latitude and longitude values and filters it based on whether those points fall within a specified geographic region defined by a shapefile (`.shp`, EPSG:4326). The filtered data is exported to a CSV file containing selected columns.

---

# Input Files

Ensure all of the following files are located in the **same folder as the script**:

- `Data.tsv` — A tab-delimited text file containing latitude/longitude and other attributes.
- `ROI.shp` — A shapefile that defines the spatial region of interest (must be in **EPSG:4326**). Ensure all associated shapefile components (`.shx`, `.dbf`, etc.) are present.

---

# 📤 Output

- `clipped.csv` — A CSV file containing rows from the input TSV whose coordinates fall within the ROI shapefile, limited to selected columns.

---

# Requirements

pandas
geopandas
shapely
