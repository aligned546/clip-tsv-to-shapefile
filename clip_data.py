import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# Set working directory to the script's location
folder = os.path.dirname(os.path.abspath(__file__))

# File paths -- modify these as needed
tsv_path = os.path.join(folder, "Data.tsv")
shp_path = os.path.join(folder, "ROI.shp")
output_path = os.path.join(folder, "clipped.csv")

# Load shapefile and ensure correct CRS
roi = gpd.read_file(shp_path).to_crs(epsg=4326)

# Load TSV data
df = pd.read_csv(tsv_path, sep='\t', dtype=str)

# Strip column names to avoid hidden spaces
df.columns = df.columns.str.strip()

# Print columns to verify names
print("📋 Columns found in the TSV file:")
print(df.columns.tolist())

# Convert latitude and longitude to numeric
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Clip to ROI
gdf_clipped = gdf[gdf.geometry.within(roi.union_all())]

# Desired columns to keep -- you can modify this list as needed
columns_to_keep = [
    'Project', 'ParentProject', 'StationName', 'StationCode', 'SampleDate',
    'LocationCode', 'MDL', 'RL', 'SampleTypeCode', 'MatrixName',
    'Analyte', 'Unit', 'Result', 'latitude', 'longitude',
    'StationLUCode', 'StationLUName'
]

# Verify which columns exist
existing_columns = [col for col in columns_to_keep if col in gdf_clipped.columns]
missing_columns = set(columns_to_keep) - set(existing_columns)

# Warn if any columns are missing
if missing_columns:
    print(f"⚠️ Warning: These columns were not found and will be skipped: {missing_columns}")
    print(f"Available columns: {gdf_clipped.columns.tolist()}")

# Export to CSV
gdf_clipped[existing_columns].to_csv(output_path, index=False)
print(f"✅ Filtered data written to: {output_path}")
