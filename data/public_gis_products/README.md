# Public GIS Products

This folder contains small, public-safe derived GIS layers used by the website
and slide exports. Raw source packages stay in OSL/source-library storage or
temporary build folders unless they are explicitly approved for GitHub.

## North Slope Borough Boundary

File:
`north_slope_borough_boundary_tiger2025.geojson`

Source:
U.S. Census Bureau TIGER/Line 2025 county shapefile,
`https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/tl_2025_us_county.zip`.

Build script:
`01_pipeline/build_public_north_slope_borough_boundary.py`.

Use:
The unified North Slope website/slide map uses this layer as a bold geographic
edge for the North Slope Borough. It is administrative/geographic context only;
it is not hydrate occurrence, saturation, producibility, stability, or model
evidence.
