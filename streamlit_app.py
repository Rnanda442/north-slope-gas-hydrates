from dashboard import app as dashboard_app
from dashboard import mapbox_map as north_slope_map


def render_regional_map() -> None:
    north_slope_map.render_regional_atlas_mapbox(dashboard_app)


dashboard_app.render_regional_atlas = render_regional_map
main = dashboard_app.main


if __name__ == "__main__":
    main()
